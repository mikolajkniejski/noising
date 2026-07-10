CUBLAS_WORKSPACE_CONFIG=:4096:8
noise=${1:-0}
tags=${2:-'placeholder'}
seed=${3:-0}
printf "running with noise %s and tags %s\n" $noise $tags
./.venv/bin/inspect  eval ./evals/mmlu-sandbag.py  --model noised/microsoft/Phi-3-mini-128k-instruct --max-connections 2 -M noise_std=$noise -M seed=$seed -M do_sample=false --tags $tags
