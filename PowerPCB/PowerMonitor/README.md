
# Power Monitoring System

This project is a comprehensive power monitoring system for Raspberry Pi, leveraging the INA219 sensors. It consists of the following components:

1.  `systemd` service installer: A bash script named `install_monitor_service.sh` that sets up the monitoring script as a background service on your Linux system.
2.  `voltageMonitor.py`: A driver script to read values from the INA219 sensors using the `pi-ina219` library.
3.  `battery_monitor.py`: The main script that captures various power-related metrics and posts them to a local server (see the NEDB directory within this folder)

The `battery_monitor.py` script will capture and post data every 5 seconds to the specified local server. You'll see metrics like battery voltage, current, power consumption, shunt voltage, and CPU temperature.

The `voltageMonitor.py` acts as a driver for reading data from the INA219 sensor(s) and is invoked internally by the main script.

## Installation & Usage

Before installing the monitoring service, ensure the NEDB database is up and running (see the NEDB folder) otherwise there will be no end point to POST the data to.

`sudo bash install_monitor_service.sh`

Once executed, the service should be active and continuously monitor the power data in the background.
