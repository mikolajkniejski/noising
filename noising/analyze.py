from inspect_ai import log

l = log.list_eval_logs("./logs")

ac = []
no = []
seds = []
for i in l:
    llll  = log.read_eval_log(i, header_only=True)
    if "run14" in llll.tags and llll.status == "success":
        noise = llll.eval.model_args.get('noise_std', 100)
        seed = llll.eval.model_args.get('seed', 100)
        seds.append(seed)
        # breakpoint()
        if llll.results:
            _ac = llll.results.scores[0].metrics['accuracy'].value
            ac.append(_ac)
        no.append(noise)





import polars as pl
df = pl.DataFrame({
    'accuracy': ac,
    'noise_std': no,
    'seed': seds
})

print(df.group_by(pl.col("noise_std")).agg(pl.col("accuracy").min().alias("min"), pl.col("accuracy").max().alias("max")).sort("noise_std"))
