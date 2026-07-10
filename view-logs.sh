mkdir -p ./noising/logs && rsync -avz -e "ssh -p $SSH_PORT -i ~/.ssh/id_ed25519" ubuntu@$SSH_IP:~/noising/noising/logs/ ./noising/logs/
inspect view --log-dir ./noising/logs
