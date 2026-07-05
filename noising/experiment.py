from dataclasses import asdict, dataclass, field

import json
import socket
import subprocess
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator, List


WANDB_PROJECT = "unit"
SCRIPT_DIR = Path(__file__).resolve().parent
RUNS_DIR = SCRIPT_DIR / "runs"


@dataclass
class Args:
    name: str = "sweep"
    notes: str = ""
    tags: List[str] = field(default_factory=list)
    skip_wandb: bool = False
    skip_commit: bool = True

    # Example
    seed: List[int] = field(default_factory=list)
    lr: List[int] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


def _git(args, check=False) -> str:
    out = subprocess.run(
        ["git"] + args, cwd=SCRIPT_DIR, capture_output=True, text=True, check=check
    )
    return out.stdout.strip()


class Sweep():
    def _commit(self) -> str:
        _git(["add", "-A"])
        _git(["commit", "-m", f"experiment {self.args.name} {self.timestamp_iso}"])
        return _git(["rev-parse", "HEAD"], check=True)

    def __init__(self, args: Args) -> None:
        self.args = args
        self.timestamp_iso = datetime.now().astimezone().isoformat(timespec="seconds")
        self.timestamp = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
        self.sweep_id = f"{self.timestamp}-{args.name}"
        self.script_dir = SCRIPT_DIR
        self.host = socket.gethostname()
        if not args.skip_commit:
            self.git_sha = self._commit()
        self.git_sha = ""

    def _run_trail(self, trail_dict):
        print(trail_dict)

    def run_trail(self, trail_dict):
        if self.args.skip_wandb:
            print("skipping")
            self._run_trail(trail_dict)
        else:
            import wandb
            self.wandb_run = wandb.init(
                project=WANDB_PROJECT,
                entity="fgrttt-none",
                group=self.sweep_id,
                name=self.args.name,
                tags=self.args.tags,
                notes=self.args.notes,
                reinit=True,
                dir=str(self.script_dir),
                config={
                    "sweep_id": self.sweep_id,
                    "git_sha": self.git_sha,
                    "host": self.host,
                    "args": self.args.to_dict(),
                },
            )
            try:
                self._run_trail(trail_dict)
                self.wandb_run.finish(exit_code=0)
            except Exception:
                self.wandb_run.finish(exit_code=1)
                raise

    def trails(self):
        for lr in self.args.lr:
            for seed in args.seed:
                yield (lr, seed), {"lr": lr, "seed": seed}

    def run(self):
        for args, trail_dict in self.trails():
            self.run_trail(trail_dict)

    def log(self, args):
        self.wandb_run.log(args)

if __name__ == "__main__":
    args = Args(
        name="sweep",
        notes="",
        seed=[1, 2],
        lr=[4, 5],
        tags=[],
    )

    Sweep(args).run()
