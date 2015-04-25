echo "beginning rsync"
rsync -r --exclude 'deploy.sh' --exclude '.git' /home/thor/Code/core-echoes-tracer/* tidepool@tide-pool.ca:/home/tidepool/core-echoes-trace
echo "rsync complete!"
