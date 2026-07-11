#!/usr/bin/env bash
tags=big_fat_3
mkdir -p sweeps

for model in noised/microsoft/Phi-3-mini-128k-instruct \
            noised/microsoft/Phi-4-mini-instruct \
            noised/meta-llama/Llama-3.1-8B-Instruct; do
    name=$(basename "$model")
    parallel -j1 --joblog "sweeps/$tags-$name.joblog" --resume-failed \
        --timeout 300% --results "sweeps/$tags-$name" --line-buffer --dry-run \
        ./.venv/bin/python ro.py \
            --task {1} --model "$model" --noise-std {2} --seed {3} --tags "$tags" \
        ::: ./evals/mmlu-not-sandbag.py ./evals/mmlu-sandbag.py ./evals/mmlu-not-sandbag-alt.py \
        ::: 0 0.003 0.004 0.005 0.006 0.007 \
        ::: 1 2 3 4 5
done
