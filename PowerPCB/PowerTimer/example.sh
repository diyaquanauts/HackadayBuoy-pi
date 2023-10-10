#!/bin/bash

# Clear the alarm interrupt pin
echo "Clearing alarm interrupt..."
if ! echo "0" | sudo tee /sys/class/rtc/rtc0/wakealarm; then
    echo "Failed to clear alarm interrupt. Exiting."
    exit 1
fi

# Set the alarm for 2 minutes from now
echo "Setting alarm for 2 minutes from now..."
if ! date '+%s' -d '+10 minutes' | sudo tee /sys/class/rtc/rtc0/wakealarm; then
    echo "Failed to set alarm. Exiting."
    exit 1
fi

# Shutdown the system
echo "Shutting down in 10 seconds. Make sure switch is set to auto or the system cannot wake itself up!"
sleep 10
shutdown -h now
