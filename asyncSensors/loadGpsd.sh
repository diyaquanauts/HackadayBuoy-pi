#!/bin/bash

# Write gpsd.conf file
echo "START_DAEMON=\"true\"" > /etc/default/gpsd
echo "GPSD_OPTIONS=\"/dev/serial0 -F /var/run/gpsd.sock\"" >> /etc/default/gpsd

echo "DEVICE=\"/dev/serial0\"" > /etc/default/gpsd
echo "GPSD_OPTIONS=\"\"" >> /etc/default/gpsd

echo "DEVICES=\"/dev/serial0\"" > /etc/default/gpsd
echo "USBAUTO=\"false\"" >> /etc/default/gpsd

echo "GPSD_SOCKET=\"/var/run/gpsd.sock\"" > /etc/default/gpsd
echo "GPSD_PIDFILE=\"/var/run/gpsd.pid\"" >> /etc/default/gpsd

# Restart gpsd service
sudo systemctl restart gpsd.service
