import argparse, json, sys
from inspect_ai import eval as inspect_eval   # don't shadow the builtin

p = argparse.ArgumentParser()
p.add_argument("--task", required=True)
p.add_argument("--model", required=True)
p.add_argument("--noise-std", type=float, required=True)
p.add_argument("--seed", type=int, required=True)
p.add_argument("--tags", required=True)
p.add_argument("--max-tokens", type=int, default=256)
args = p.parse_args()

logs = inspect_eval(
    args.task,
    model=args.model,
    model_args=dict(noise_std=args.noise_std, seed=args.seed, do_sample=False),
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
sys.exit(0 if log.status == "success" and result["accuracy"] is not None else 1)
