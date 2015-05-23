echo "beginning rsync"
rsync -r --exclude 'deploy.sh' --exclude '.git' --rsh="ssh -i /home/thor/.amazon/amazon-personal-ec2.pem" \
/home/thor/Code/core-echoes-tracer/* ubuntu@52.24.2.243:/home/ubuntu/core-echoes-tracer
echo "rsync complete!"
