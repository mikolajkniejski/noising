CUBLAS_WORKSPACE_CONFIG=:4096:8
./.venv/bin/inspect  eval ./evals/mmlu.py  --model hf/microsoft/Phi-4-mini-instruct --max-connections 2 --tags TEST -M do_sample=false
