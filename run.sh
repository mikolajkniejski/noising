acp
ssh ubuntu@$SSH_IP -p $SSH_PORT -i ~/.ssh/id_ed25519 'cd ~/noising && git pull && ./phi4-mini.sh'
