#!/bin/bash

# Get the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Create the service file
cat << EOF > /etc/systemd/system/tmateSessionFinder.service
[Unit]
Description=Tmate Session ID Updater

[Service]
Type=simple
Restart=always
RestartSec=5
ExecStart=/usr/bin/node $DIR/session.js

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable tmateSessionFinder.service
sudo systemctl start tmateSessionFinder.service
