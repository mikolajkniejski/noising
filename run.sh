acp
result=$(ssh ubuntu@216.81.200.237 -p 32378 -i ~/.ssh/id_ed25519 'cd ~/noising && pwd')
printf "$result"
