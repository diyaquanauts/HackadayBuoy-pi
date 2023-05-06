sudo tee /etc/systemd/system/tmate.service > /dev/null <<EOF
[Unit]
Description=tmate
After=network.target

[Service]
Type=simple
User=$USER
ExecStart=/usr/bin/tmate -S /tmp/tmate.sock -F
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

# Enable and start the tmate service
sudo systemctl enable tmate.service
sudo systemctl start tmate.service
