#!/bin/bash

CONFIG_FILE="/boot/config.txt"

# Check if GPIO 17 boot configuration exists
if ! grep -q "^gpio=17=op,dh" $CONFIG_FILE; then
    echo "Adding GPIO 17 boot configuration..."
    echo "gpio=17=op,dh" | sudo tee -a $CONFIG_FILE
else
    echo "GPIO 17 boot configuration already exists."
fi

# Check if GPIO 17 poweroff configuration exists
if ! grep -q "^gpio-poweroff=gpiopin=17,active_low" $CONFIG_FILE; then
    echo "Adding GPIO 17 poweroff configuration..."
    echo "gpio-poweroff=gpiopin=17,active_low" | sudo tee -a $CONFIG_FILE
else
    echo "GPIO 17 poweroff configuration already exists."
fi

echo "Configuration complete. Reboot to apply changes."

