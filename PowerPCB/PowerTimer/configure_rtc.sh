#!/bin/bash

# Ensure the script is run with superuser privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Ensure Internet Connectivity
if ! ping -c 1 8.8.8.8 >/dev/null 2>&1; then
    echo "No internet connection. Please ensure your network is connected and try again."
    exit 1
fi

# Synchronize with NTP
echo "Synchronizing system time with NTP..."
timedatectl set-ntp true
sleep 5

# Update & Upgrade System
echo "Updating and upgrading system packages..."
apt-get update && apt-get upgrade -y

# Add dtoverlay for DS3231 to /boot/config.txt if it's not already there
if ! grep -q "dtoverlay=i2c-rtc,ds3231,wakeup-source" /boot/config.txt; then
    echo "dtoverlay=i2c-rtc,ds3231,wakeup-source" >> /boot/config.txt
    echo "Added DS3231 overlay to /boot/config.txt."
else
    echo "DS3231 overlay already present in /boot/config.txt."
fi

# Remove fake-hwclock
echo "Removing fake-hwclock..."
apt-get -y remove fake-hwclock
update-rc.d -f fake-hwclock remove
systemctl disable fake-hwclock

# Adjust hwclock-set if necessary
SCRIPT_HWCLOCK_SET=/lib/udev/hwclock-set
sed -i -e "s,^\(if \[ \-e /run/systemd/system \] ; then\),if false; then\n#\1," $SCRIPT_HWCLOCK_SET

# Recommend a reboot
echo "All steps completed. Please reboot your Raspberry Pi for changes to take effect."


