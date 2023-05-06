import asyncio
from gpsd.client import GPSDClient

async def read_gps_data():
    # Connect to the gpsd daemon
    client = GPSDClient()

    # Open the serial port for reading
    serial_port = await asyncio.open_serial_connection('/dev/serial0', baudrate=9600)

    # Create a stream reader for reading data from the serial port
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await serial_port[0].set_protocol(protocol)

    # Read data from the serial port
    while True:
        # Read one line of data from the serial port
        line = await reader.readline()

        # Decode the line into a string
        line_str = line.decode().strip()

        # Check if the line starts with a GPS sentence
        if line_str.startswith('$GPGGA'):
            # Parse the GPS sentence
            gps_data = client(gps_data=line_str)
            lat = gps_data.position()[0]
            lng = gps_data.position()[1]
            fix = gps_data.fix().mode
            utc_time = gps_data.time()[0]
            utc_date = gps_data.date()[0]
            hdop = gps_data.hdop()
            altitude = gps_data.altitude()

            # Print the parsed GPS data
            print(f"Latitude: {lat:.6f}")
            print(f"Longitude: {lng:.6f}")
            print(f"Fix: {fix}")
            print(f"UTC Time: {utc_time}")
            print(f"UTC Date: {utc_date}")
            print(f"HDOP: {hdop:.2f}")
            print(f"Altitude: {altitude:.2f} meters")

    # Close the serial port
    serial_port[0].close()

