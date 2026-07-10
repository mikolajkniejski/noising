tags=run8

trap 'echo; echo "Interrupted — stopping sweep."; exit 130' INT

SECONDS=0
./phi3-mini-mmlu-sandbag.sh 0 test 0
limit=$(( SECONDS * 5 ))
echo "Baseline ${SECONDS}s -> timeout ${limit}s"

timed () {
    timeout --kill-after=30 "$limit" ./phi3-mini-mmlu-sandbag.sh "$@"
    local rc=$?
    if [ "$rc" -eq 124 ]; then
        echo "TIMEOUT after ${limit}s: $*" >&2
    fi
    return 0   # keep the sweep going even if one run dies
}

for seed in 1 2 3 4; do
    for std in 0 0.001 0.003 0.004 0.005 0.006; do
        timed "$std" "$tags" "$seed"
    done
done
