#!/bin/bash

# Prompt the user for service name
read -p "Enter service name: " SERVICE_NAME

# Create a new folder for the service
SERVICE_FOLDER="$SERVICE_NAME"
mkdir "$SERVICE_FOLDER"
cd "$SERVICE_FOLDER"

# Prompt the user for service description
read -p "Enter service description: " SERVICE_DESCRIPTION

# Prompt the user for executable path or command
read -p "Enter the path or command for the executable: " EXECUTABLE

# Generate the load.sh script
cat > load.sh <<EOF
#!/bin/bash

# Get current working directory
DIR="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Fill out the systemd service file
cat > /etc/systemd/system/${SERVICE_NAME}.service <<SERVICE_EOF
[Unit]
Description=${SERVICE_DESCRIPTION} *USER*
After=network.target

[Service]
User=\$(whoami)
WorkingDirectory=\$DIR
ExecStart=${EXECUTABLE}
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Reload systemd daemon and start the service
systemctl daemon-reload
systemctl enable ${SERVICE_NAME}.service
systemctl start ${SERVICE_NAME}.service
EOF

# Generate the status.sh script
cat > status.sh <<EOF
#!/bin/bash

SERVICE_NAME="${SERVICE_NAME}.service"

status=\$(systemctl status "\$SERVICE_NAME")

echo "\$status"
EOF

# Make the scripts executable
chmod +x load.sh
chmod +x status.sh

