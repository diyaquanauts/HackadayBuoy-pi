#!/bin/bash

# Get current working directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Fill out the systemd service file
cat > /etc/systemd/system/restDbSync.service <<EOF
[Unit]
Description=RestDB sync for local NEDB
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$DIR
ExecStart=/usr/bin/node $DIR/dbSync.js
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon and start the service
systemctl daemon-reload
systemctl enable restDbSync.service
systemctl start restDbSync.service
