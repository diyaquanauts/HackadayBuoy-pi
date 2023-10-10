import os
import sys
import psutil
import requests
cwd = os.path.dirname(__file__)
capture_scripts_path = os.path.join(cwd, "..","captureScripts")
sys.path.append(capture_scripts_path)
import voltageMonitor
import time

voltage_monitor = voltageMonitor.useReadInputPower(0x40)


def get_cpu_temperature():
    # Execute the command to get the CPU temperature
    result = os.popen('vcgencmd measure_temp').readline()
    # Extract the temperature value from the result
    temp = float(result.replace("temp=", "").replace("'C\n", ""))
    return temp


def post_power_data():
    cpu_temp = get_cpu_temperature()
    battery_voltage = float(voltage_monitor.voltage())
    shunt_voltage = float(voltage_monitor.shunt_voltage())
    battery_current = float(voltage_monitor.current())
    power_consumption = float(voltage_monitor.power())

    # Store the data in a dictionary
    data_to_send = {
        "temperature": cpu_temp,
        "bVoltage": battery_voltage,
        "sVoltage": shunt_voltage,
        "current": battery_current,
        "power": power_consumption,
        "cpu": psutil.cpu_percent(interval=1)  # Assuming you've also added the psutil library as shown earlier
    }

    # Define the URL for the local server
    url = "http://localhost:6666/store"

    # Make the POST request
    response = requests.post(url, json=data_to_send)

    # Check the response
    if response.status_code == 200:
        print("Data successfully sent to the server!")
    else:
        print("Failed to send data to the server!")

    print("Battery voltage: ", battery_voltage, "V")
    print("Shunt voltage: ", shunt_voltage, "mV")
    print("Battery current: ", battery_current, " mA")
    print("Power consumption: ", power_consumption, " mW")
    print("CPU temperature: ", cpu_temp, "°C")

def main():
    while True:
        post_power_data()
        time.sleep(5)  # Sleep for 5 seconds before the next iteration

if __name__ == "__main__":
    main()