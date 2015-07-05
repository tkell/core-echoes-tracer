echo "beginning rsync"
rsync -r --exclude 'deploy.sh' --exclude '.git' --rsh="ssh -i /home/thor/.ssh/amazon-personal.pem" \
/home/thor/Code/core-echoes-tracer/* ubuntu@52.10.186.129:/home/ubuntu/core-echoes-tracer
echo "rsync complete!"
