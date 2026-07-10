CUBLAS_WORKSPACE_CONFIG=:4096:8
noise=${1:-0}
printf "running with noise %s\n" $noise
./.venv/bin/inspect  eval ./evals/mmlu-sandbag.py  --model noised/microsoft/Phi-3-mini-128k-instruct --max-connections 6   -M noise_std=$noise -M seed=0 -M do_sample=false
