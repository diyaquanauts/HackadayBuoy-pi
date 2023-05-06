#!/bin/bash

# Set the target locations
SERVICE_NAME="tailscale.service"
TARGET_DIR="/usr/local/bin"
SERVICE_DIR="/etc/systemd/system"

# Download and install the Tailscale client
curl -fsSL https://pkgs.tailscale.com/stable/tailscale_1.14.0_amd64.tgz | sudo tar -C /usr/local/bin -xzf -

# Log in to Tailscale and authorize the Raspberry Pi
sudo tailscale up

# Create the systemd service file
sudo bash -c "cat > $SERVICE_DIR/$SERVICE_NAME" << EOL
[Unit]
Description=Tailscale Client
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/tailscale up
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Reload the systemd daemon
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "The $SERVICE_NAME has been installed and started."

