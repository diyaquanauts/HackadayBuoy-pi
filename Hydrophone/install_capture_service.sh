#!/bin/bash

# Set the target locations
SERVICE_NAME="hydrophone-capture.service"
TARGET_DIR=$(pwd)
SERVICE_DIR="/etc/systemd/system"

# Ensure the capture.sh script is executable
chmod +x $TARGET_DIR/capture.sh

# Create the systemd service file
sudo bash -c "cat > $SERVICE_DIR/$SERVICE_NAME" << EOL
[Unit]
Description=Audio Capture Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$TARGET_DIR
ExecStart=/usr/bin/nice -n -10 /usr/bin/ionice -c2 -n0 $TARGET_DIR/capture.sh
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
