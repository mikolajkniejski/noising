"""Pre-generate noise LoRA adapters (CPU only). Lives in ~/noising/noising/.

Whole grid:
    parallel ./.venv/bin/python make_adapters.py --model {1} --noise-std {2} --seed {3} \
      ::: microsoft/Phi-3-mini-128k-instruct microsoft/Phi-4-mini-instruct meta-llama/Llama-3.1-8B-Instruct \
      ::: 0.003 0.004 0.005 0.006 0.007 ::: 1 2 3 4 5
"""

import argparse

from inspect_ai.model._providers.noised_vllm import build_noise_adapter

p = argparse.ArgumentParser()
p.add_argument("--model", required=True)
p.add_argument("--noise-std", type=float, required=True)
p.add_argument("--seed", type=int, required=True)
p.add_argument("--rank", type=int, default=32)
args = p.parse_args()
print(build_noise_adapter(args.model, args.noise_std, args.seed, args.rank))
