#!/bin/bash

FILE="/etc/dhcpcd.conf"
WLAN="interface wlan0\nmetric 200"
USB="interface usb0\nmetric 300"

# Function to add configuration if not already present
add_config() {
    if ! grep -q "$1" "$FILE"; then
        echo -e "$1" | sudo tee -a "$FILE"
    fi
}

# Add configurations
add_config "$WLAN"
add_config "$USB"

echo "Network interface priorities will not update until you reboot."

