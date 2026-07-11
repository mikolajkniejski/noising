"""ro.py — run one (task, model, noise, seed) eval config and print a JSON result line."""

import argparse
import json
import sys

from inspect_ai import eval as inspect_eval

p = argparse.ArgumentParser()
p.add_argument("--task", required=True)
p.add_argument("--model", required=True, help="full inspect model, e.g. noised-vllm/microsoft/Phi-3-mini-128k-instruct")
p.add_argument("--noise-std", type=float, required=True)
p.add_argument("--seed", type=int, required=True)
p.add_argument("--tags", required=True)
p.add_argument("--max-tokens", type=int, default=64)
p.add_argument("--noise-rank", type=int, default=32)
args = p.parse_args()

logs = inspect_eval(
    args.task,
    model=args.model,
    model_args=dict(
        noise_std=args.noise_std,
        seed=args.seed,
        noise_rank=args.noise_rank,
        max_loras=8,
    ),
    temperature=0.0,          # greedy — vLLM-style; do NOT pass do_sample here
    max_tokens=args.max_tokens,
    max_connections=3,
    tags=[args.tags],
    display="plain",
)

log = logs[0]
result = {"task": args.task, "model": args.model, "noise_std": args.noise_std,
          "seed": args.seed, "status": log.status, "accuracy": None}

if log.status == "success":
    result["accuracy"] = next(
        (s.metrics["accuracy"].value for s in log.results.scores if "accuracy" in s.metrics),
        None,
    )

print(json.dumps(result))
# Nonzero exit on failure so parallel's joblog records it and --resume-failed retries.
sys.exit(0 if log.status == "success" and result["accuracy"] is not None else 1)
