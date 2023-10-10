#!/bin/bash

# Define the path and name of the service file
SERVICE_PATH="/etc/systemd/system/"
SERVICE_NAME="power_scanner.service"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


# Check for root permissions
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo or as root."
    exit 1
fi

# Create the service file content
cat > ${SERVICE_PATH}${SERVICE_NAME} <<EOL
[Unit]
Description=Power Monitor Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 $DIR/read.py
Restart=always
User=$(whoami)
WorkingDirectory=$DIR

[Install]
WantedBy=multi-user.target
EOL

# Reload the systemd manager configuration
systemctl daemon-reload

# Enable and start the service
systemctl enable ${SERVICE_NAME}
systemctl start ${SERVICE_NAME}

# Show the status
systemctl status ${SERVICE_NAME}

