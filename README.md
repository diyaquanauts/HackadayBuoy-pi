# HackadayBuoy-pi

This Project is broken up into 3 sections for different buoy types. For the most part processes are pretty isolated, however some services still overlap (its a work in progress).

At a high level, the buoy runs [tailscale](https://tailscale.com/) so that you can connect it when it running on its cellular modem connection. It also runs [cockpit](https://cockpit-project.org/) to allow easy management of the deployment and custom linux services.

For parsing GPS NMEA data, it is running [GPSd](https://gpsd.io/) to allow easy subscription to GPS data.

Currently, it also uses python's [http-server](https://docs.python.org/3/library/http.server.html) to allow simple review of the filesystem and captured data on your mobile device while in the field.

## Installation

This is all still very much a work in progress. However, for every service the buoy has to run, I am also creating a bash install script that generates the relevant systemd service file information.

For example, withing the `/hydrophone` folder there is a script titled `install_capture_service.sh` which loads and reloads the `capture.sh` as a linux service.

I am working to remove old, unused files from the project as well unwanted cross-dependencies between buoy types as quickly as possible.

Working Pi images also to follow.

#### ReefCamOpenCV

This folder contains the relevant code for setting up the raspberry pi for long-term video capture.

#### WaterProbe

This folder contains the relevant code for setting up the raspberry pi for long-term water quality capture.
The directory `asyncSensors`  uses pythons asyncio to allow concurrent sensor reading on the I2C bus.

Currently tested & working sensors include:

 - Atlas Scientific Dissolved Oxygen Probe
 - Atlas Scientific pH Probe
 - Blue Robotics Depth Sensor
 - Blue Robotics Temperature Sensor
 - TSL2591 Light Sensor

Numerical data is stored in a server process which binds the captured data with a local NEDB database.

#### hydrophone

This folder contains the relevant code for setting up the raspberry pi for long-term water audio capture.

