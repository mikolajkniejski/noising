import argparse, json
from inspect_ai import eval

p = argparse.ArgumentParser()
p.add_argument("--task", required=True)
p.add_argument("--model", required=True)
p.add_argument("--noise-std", type=float, required=True)
p.add_argument("--seed", type=int, required=True)
p.add_argument("--tags", required=True)
args = p.parse_args()

logs = eval(
    args.task,
    model=args.model,
    model_args=dict(noise_std=args.noise_std, seed=args.seed, do_sample=False),
    max_tokens=64,
    max_connections=2,
    tags=[args.tags],
)

log = logs[0]
acc = next(s.metrics["accuracy"].value for s in log.results.scores if "accuracy" in s.metrics)
print(json.dumps({"task": args.task, "model": args.model, "noise_std": args.noise_std,
                  "seed": args.seed, "accuracy": acc, "status": log.status}))
