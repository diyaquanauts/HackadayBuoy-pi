import smbus
import asyncio
from tsl2591 import Tsl2591
from tsl2591 import (FULLSPECTRUM, INFRARED, VISIBLE)
from ms5837 import MS5837
from atlas_i2c import atlas_i2c
from tsys01 import TSYS01
import time
import requests
import uuid
import json
import random
import datetime
import gpsd

DO_SENSOR_ADDRESS = 97  # Replace with your DO sensor's I2C address
PH_SENSOR_ADDRESS = 99  # Replace with your pH sensor's I2C address
lastLat = 0
lastLng = 0
lastTime = ""


async def readSensor(sensorAddress):
    dev = atlas_i2c.AtlasI2C()
    dev.set_i2c_address(sensorAddress)
    dev.write("R")
    await asyncio.sleep(1.5)  # Give the sensor some time to process the reading

    result = dev.read("R")
    if result.status_code == 1:
        return float(result.data)
    else:
        raise Exception(f"Error reading sensor at address {sensorAddress}: {result}")

async def initTemp():
    sensor = TSYS01(bus=1)
    await sensor.init()
    return sensor

async def initLux():
    sensor = Tsl2591()
    await sensor.setup()
    return sensor

async def initDepth():
    # Create an instance of the MS5837 class
    sensor = MS5837()

    # Initialize the sensor
    initialized = await sensor.init()
    if not initialized:
        print("Failed to initialize the sensor")
        return
    return sensor

async def insertDataToDatabase(postData):
    # Send a POST request to the '/store' endpoint with some test data
    url = 'http://localhost:6666/store'
    headers = {'Content-Type': 'application/json'}
    
    print(json.dumps(postData, indent=4))
    response = requests.post(url, json=postData, headers=headers)
    if response.status_code == 200:
        print('Data uploaded successfully')
    else:
        print(f'Error uploading data: {response.content}')
    

async def main():
    lightSensor = await initLux()
    depthSensor = await initDepth()
    tempSensor = await initTemp()
    sessionStartTime = time.monotonic()
    sessionId = str(uuid.uuid4())
    recordIndex = 0

    while True:
        start_time = time.time()


        validSats = 0
        packet = gpsd.get_current()
        print(vars(packet))
        if packet.mode >= 2:
            lastUtc = packet.time
            lastLat = packet.lat
            lastLng = packet.lon
            validSats = packet.sats_valid
    
    
        print("Starting tasks...")
        results = await asyncio.gather(
            readSensor(DO_SENSOR_ADDRESS),
            readSensor(PH_SENSOR_ADDRESS),
            lightSensor.get_luminosity(FULLSPECTRUM),
            depthSensor.read(),
            tempSensor.read()
        )

        print("Sensor reading results:")
        print(f"DO: {results[0]} mg/L")
        print(f"pH: {results[1]}")
        print(f"Full spectrum luminosity: {results[2]}")
        print(f"Pressure: {depthSensor.pressure()}")
        print(f"Temperature: {tempSensor.temperature()} °C")

        day = random.randint(3, 9)

        postData = {
            'sessionId': sessionId,
            'recordIndex': f"{recordIndex:06d}",
            'uploaded': False,      
            'gps':{
                'time': lastUtc,
                'lat': lastLat,
                'lon': lastLng,
                'sats': int(validSats),
                'fix': int(packet.mode),
            },
            'pressure': round(depthSensor.pressure(), 2),
            'temperature': round(tempSensor.temperature(), 2),
            'light': round(results[2], 2),
            'do': round(results[0], 2),
            'ph': round(results[1], 2),
            'runtime': time.monotonic()-sessionStartTime,
            'message': 'This is a test.'
        }            
    
        await insertDataToDatabase(postData)
        recordIndex += 1
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        sleep_time = max(2 - elapsed_time, 0)
        print(sleep_time)
        
        await asyncio.sleep(sleep_time)


if __name__ == "__main__":
    gpsd.connect()

    # Wait for a GPS fix
    while True:      
        print("Waiting for GPS fix...")
        packet = gpsd.get_current()
        print(vars(packet))
        if packet.mode >= 2:
            break
        time.sleep(1)

    # Get the UTC time from the GPS data
    lastUtc = packet.time
    lastLat = packet.lat
    lastLng = packet.lon

    asyncio.run(main())
    


    
