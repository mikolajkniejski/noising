mkdir -p ./noising/logs && rsync -avz -e "ssh -p 32378 -i ~/.ssh/id_ed25519" ubuntu@216.81.200.237:~/noising/noising/logs/ ./noising/logs/
