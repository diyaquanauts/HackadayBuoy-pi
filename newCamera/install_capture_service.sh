#!/bin/bash

# Set the target locations
SERVICE_NAME="camera-capture.service"
TARGET_DIR=$(pwd)
SERVICE_DIR="/etc/systemd/system"

# Create the systemd service file
sudo bash -c "cat > $SERVICE_DIR/$SERVICE_NAME" << EOL
[Unit]
Description=Video Capture Service (Node JS)
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$TARGET_DIR
ExecStart=sudo /usr/bin/node $TARGET_DIR/capture.js
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOL

# Reload the systemd daemon
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "The $SERVICE_NAME has been installed and started."
