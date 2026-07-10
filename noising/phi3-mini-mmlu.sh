CUBLAS_WORKSPACE_CONFIG=:4096:8
./.venv/bin/inspect  eval ./evals/mmlu.py  --model hf/microsoft/Phi-3-mini-128k-instruct --max-connections 2 --tags TEST -M do_sample=false
