import asyncio
import time
from atlas_i2c import atlas_i2c

DO_SENSOR_ADDRESS = 97  # Replace with your DO sensor's I2C address
PH_SENSOR_ADDRESS = 99  # Replace with your pH sensor's I2C address

async def read_sensor(sensor_address):
    dev = atlas_i2c.AtlasI2C()
    dev.set_i2c_address(sensor_address)
    dev.write("R")
    await asyncio.sleep(1.5)  # Give the sensor some time to process the reading

    result = dev.read("R")
    if result.status_code == 1:
        return float(result.data)
    else:
        raise Exception(f"Error reading sensor at address {sensor_address}: {result}")

async def read_do():
    return await read_sensor(DO_SENSOR_ADDRESS)

async def read_ph():
    return await read_sensor(PH_SENSOR_ADDRESS)

async def main():
    do_reading = await read_do()
    ph_reading = await read_ph()

    print(f"DO: {do_reading} mg/L")
    print(f"pH: {ph_reading}")

if __name__ == "__main__":
    asyncio.run(main())
