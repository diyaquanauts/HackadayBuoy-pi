#!/bin/bash

# Set the target locations
SERVICE_NAME="secure_server.service"
TARGET_DIR=$(pwd)
SERVICE_DIR="/etc/systemd/system"

# Ensure the secure_server.py script is executable
chmod +x $TARGET_DIR/secure_server.py

# Create the systemd service file
sudo bash -c "cat > $SERVICE_DIR/$SERVICE_NAME" << EOL
[Unit]
Description=Secure Server Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$TARGET_DIR
ExecStart=/usr/bin/python3 $TARGET_DIR/secure_server.py
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

