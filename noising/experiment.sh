tags=big_fat_run2
# ${1:?usage: r.sh TAGS}

trap 'echo; echo "Interrupted — stopping sweep."; exit 130' INT

timed () {
    timeout --foreground --kill-after=30 "$limit" \
        ./.venv/bin/inspect eval "$eval" --model "$model" --max-connections 3 --max-tokens 256 \
        -M noise_std="$noise" -M seed="$seed" -M do_sample=false --tags "$tags"
    local rc=$?
    if [ "$rc" -eq 124 ]; then
        echo "TIMEOUT after ${limit}s: $eval $model noise=$noise seed=$seed" >&2
    fi
    return 0
}

for eval in ./evals/mmlu-not-sandbag.py ./evals/mmlu-sandbag.py ./evals/mmlu-not-sandbag-alt.py; do
    for model in noised/microsoft/Phi-3-mini-128k-instruct \
                 noised/microsoft/Phi-4-mini-instruct \
                 noised/meta-llama/Llama-3.1-8B-Instruct; do
        SECONDS=0
        if ! ./.venv/bin/inspect eval "$eval" --model "$model" --max-connections 2 \
                -M noise_std=0 -M seed=1 -M do_sample=false --tags test; then
            echo "Baseline failed for $eval / $model — skipping." >&2
            continue
        fi
        limit=$(( SECONDS * 3 ))
        echo "Baseline ${SECONDS}s -> limit ${limit}s for $eval / $model"
        for seed in 1 2 3 4 5; do
            for noise in 0 0.003 0.004 0.005 0.006 0.007; do
                timed
            done
        done
    done
done
