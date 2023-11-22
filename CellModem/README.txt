In the context of your use case, where you want your Raspberry Pi to gracefully handle swapping between Wi-Fi (wlan0) and a USB cellular modem (usb0), these scripts dynamically adjust network priorities based on the connection status of each interface:

    usb0 Script:
        When the USB modem (usb0) is connected, the script lowers its metric, making it the preferred route for internet traffic. This means if the USB modem is connected, the Pi will use it for internet connectivity.
        When usb0 is disconnected, it removes this route, meaning the Pi will no longer prioritize the USB modem for internet traffic.

    wlan0 Script:
        Similarly, when the Wi-Fi connection (wlan0) becomes available (comes in range), the script sets a lower metric (but higher than usb0), making it the secondary choice for internet traffic.
        When wlan0 goes out of range, it removes this route, so the Pi won't use Wi-Fi for internet traffic.

These scripts allow for automatic switching between the cellular modem and Wi-Fi based on availability, without manually adjusting network settings or restarting the Pi

To install these scripts for ifplugd on your Raspberry Pi, follow these steps:

    Create the Scripts:
        Open a text editor to create each script. For example, use nano:

        bash

sudo nano /etc/ifplugd/action.d/usb0-action

Write the script for usb0. Save and exit (Ctrl+X, then Y, then Enter).
Repeat for wlan0:

bash

    sudo nano /etc/ifplugd/action.d/wlan0-action

Make the Scripts Executable:

bash

sudo chmod +x /etc/ifplugd/action.d/usb0-action
sudo chmod +x /etc/ifplugd/action.d/wlan0-action

Restart ifplugd (or the entire Raspberry Pi) to ensure the scripts are loaded and recognized:

bash

    sudo systemctl restart ifplugd

These steps will set up the scripts to be executed automatically by ifplugd when usb0 or wlan0 changes state (connected/disconnected)..
