acp
result=$(ssh ubuntu@216.81.200.237 -p 32378 -i ~/.ssh/id_ed25519 'cd ~/noising/noising && git pull && ./phi4-mini.sh')
printf "$result"
