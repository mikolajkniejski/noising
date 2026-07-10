from inspect_ai import log

l = log.list_eval_logs("./logs")

ac = []
no = []
seds = []
for i in l:
    llll  = log.read_eval_log(i)
    if "run14" in llll.tags and llll.status == "success":
        noise = llll.eval.model_args.get('noise_std', 100)
        seed = llll.eval.model_args.get('seed', 100)
        seds.append(seed)
        # breakpoint()
        if llll.results:
            _ac = llll.results.scores[0].metrics['accuracy'].value
            ac.append(_ac)
        no.append(noise)





# import polars as pl
# df = pl.DataFrame({
#     'accuracy':[0.21, 0.26, 0.26, 0.27, 0.34, 0.29, 0.32, 0.23, 0.19, 0.15, 0.26, 0.26, 0.32, 0.32, 0.3, 0.34, 0.35, 0.25, 0.32, 0.4, 0.54, 0.52, 0.32, 0.32],
#     'noise_std': [0.006, 0.006, 0.005, 0.004, 0.003, 0.001, 0, 0.005, 0.006, 0.004, 0.003, 0.006, 0.001, 0, 0.005, 0.004, 0.003, 0.001, 0, 0.005, 0.004, 0.003, 0.001, 0],
#     'seed': [4, 3, 4, 4, 4, 4, 4, 3, 2, 3, 3, 1, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
# })
