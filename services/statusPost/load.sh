#!/bin/bash

# Get current working directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Fill out the systemd service file
cat > /etc/systemd/system/systemStatus.service <<EOF
[Unit]
Description=Post systemctl status to restdb
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$DIR
ExecStart=$DIR/statusPost.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon and start the service
systemctl daemon-reload
systemctl enable systemStatus.service
systemctl start systemStatus.service
