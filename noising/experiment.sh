#!/usr/bin/env bash
# Noise sweep: one vLLM server per base model (sequential), noise configs as
# hot-swapped LoRA adapters, grid via GNU parallel with joblog resume.
#
#   ./r.sh TAG --dry-run    # print commands, run nothing
#   ./r.sh TAG              # run (resumable: rerun the same command after any death)

tags=test
mkdir -p sweeps
export VLLM_BASE_URL=http://localhost:8000/v1 VLLM_API_KEY=inspectai

MODELS=(
    microsoft/Phi-3-mini-128k-instruct
    microsoft/Phi-4-mini-instruct
    meta-llama/Llama-3.1-8B-Instruct
)
EVALS=(./evals/mmlu-not-sandbag.py ./evals/mmlu-sandbag.py ./evals/mmlu-not-sandbag-alt.py)
NOISES=(0 0.003 0.004 0.005 0.006 0.007)
SEEDS=(1 2 3 4 5)
TOTAL=$(( ${#EVALS[@]} * ${#NOISES[@]} * ${#SEEDS[@]} ))

for model in "${MODELS[@]}"; do
    name=$(basename "$model")
    joblog="sweeps/$tags/$name.joblog"

    # Skip fully-completed model blocks without paying a server start.
    if [ "$(awk 'NR>1 && $7==0' "$joblog" 2>/dev/null | wc -l)" -eq "$TOTAL" ]; then
        echo "$name: complete, skipping"
        continue
    fi

    VLLM_ALLOW_RUNTIME_LORA_UPDATING=True vllm serve "$model" \
        --api-key inspectai --enable-lora --max-lora-rank 32 --max-loras 8 \
        --port 8000 > "sweeps/$tags-$name.server.log" 2>&1 &
    server_pid=$!
    trap 'kill $server_pid 2>/dev/null' EXIT

    echo "$name: waiting for server (pid $server_pid)..."
    until curl -sf localhost:8000/health >/dev/null; do
        kill -0 "$server_pid" 2>/dev/null || { echo "$name: server died — see $tags-$name.server.log" >&2; exit 1; }
        sleep 5
    done

    parallel -j4 --joblog "$joblog" --resume-failed --timeout 300% \
        --halt soon,fail=10 --results "sweeps/$tags-$name" --line-buffer "$@" \
        ./.venv/bin/python ro.py \
            --task {1} --model "noised-vllm/$model" --noise-std {2} --seed {3} --tags "$tags" \
        ::: "${EVALS[@]}" ::: "${NOISES[@]}" ::: "${SEEDS[@]}"

    kill "$server_pid"; wait "$server_pid" 2>/dev/null
done

echo "harvest: find sweeps -name stdout -exec cat {} + | jq -s ."
