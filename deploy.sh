echo "beginning rsync"
rsync -r --exclude 'deploy.sh' --exclude '.git' --rsh="ssh -i /home/thor/.amazon/amazon-personal-ec2.pem" \
/home/thor/Code/core-echoes-tracer/* ubuntu@54.191.252.196:/home/ubuntu/core-echoes-tracer
echo "rsync complete!"
