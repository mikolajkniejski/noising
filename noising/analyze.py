from inspect_ai import log
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use("kitcat")

TAG = 'big_fat_run2'
l = log.list_eval_logs("./logs", filter=lambda x: TAG in x.tags and x.status == "success")

ac = []
no = []
seds = []
tasks = []
models = []
cmpl_a = []
for i in l:
    llll  = log.read_eval_log(i)
    per_a = llll.samples
    cmpletions = [i.output.completion for  i in per_a]
    # print(cmpletions)
    if per_a:
        cmpl_a.append(len([i for  i in cmpletions if i == 'ANSWER: A' or i == 'A']))
    else:
        cmpl_a.append(0)
    # breakpoint()
    noise = llll.eval.model_args.get('noise_std', 100)
    seed = llll.eval.model_args.get('seed', 100)
    seds.append(seed)
    tasks.append(llll.eval.task_file)
    models.append(llll.eval.model)
    if llll.results:
        _ac = llll.results.scores[0].metrics['accuracy'].value
        ac.append(_ac)
    no.append(noise)




import polars as pl
df = pl.DataFrame({
    'accuracy': ac,
    'noise_std': no,
    'seed': seds,
    'tasks': tasks,
    'models': models,
    'per_a': cmpl_a
})

print(df.group_by("noise_std", "models", "tasks").agg(pl.col("accuracy").min().alias("min"), pl.col("accuracy").max().alias("max")).sort("noise_std"))

# df.pivot('noise_std', index=['tasks', 'models'],values=['accuracy'], aggregate_function='min')
# df.pivot('noise_std', index=['tasks', 'models'],values=['accuracy'], aggregate_function='max')

# df.pivot('noise_std', index=['tasks', 'models'],values=['per_a'], aggregate_function='min')
# df.pivot('noise_std', index=['tasks', 'models'],values=['per_a'], aggregate_function='max')


breakpoint()
groups = df.select(["models", "tasks"]).unique().to_dicts()

# commit_hash = 'a'

# for g in groups:
#     model, task = g["models"], g["tasks"]
#     sub = df.filter((pl.col("models") == model) & (pl.col("tasks") == task))

#     fig, ax = plt.subplots(figsize=(8, 5))
#     for seed in sorted(sub["seed"].unique().to_list()):
#         seed_df = sub.filter(pl.col("seed") == seed).sort("noise_std")
#         ax.plot(
#             seed_df["noise_std"], seed_df["accuracy"],
#             marker="o", label=f"seed={seed}",
#         )

#     ax.set_xlabel("noise_std")
#     ax.set_ylabel("accuracy")
#     ax.set_ylim(0, 1)
#     ax.set_title(f"{model}\n{task}")
#     ax.legend(title="seed", bbox_to_anchor=(1.02, 1), loc="upper left")
#     ax.grid(alpha=0.3)

#     fig.text(
#         0.99, 0.01, f"inspect_ai: {commit_hash}",
#         ha="right", va="bottom", fontsize=7, color="gray",
#     )
#     fig.tight_layout()
#     plt.show()
