#!/bin/bash

# Get current working directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Fill out the systemd service file
cat > /etc/systemd/system/nedb.socket.service <<EOF
[Unit]
Description=NEDB socket for DREAM data
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$DIR
ExecStart=/usr/bin/node $DIR/nedb.js
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon and start the service
systemctl daemon-reload
systemctl enable nedb.socket.service
systemctl start nedb.socket.service
