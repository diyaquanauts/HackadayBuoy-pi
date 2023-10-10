#!/bin/bash

# Set the directory to save recordings
dir="./recordings"

# Set the duration of each recording
duration=1800   # seconds

# Set the desired prefix for the filenames
prefix="rec_"

# Set the device ID for the USB recording device
device_id="hw:1,0"

# Check if the USB recording device is available
#if ! arecord -l | grep $device_id > /dev/null; then
#    echo "USB recording device not found"
#    exit 1
#fi

# Infinite loop to continuously record audio
while true
do
    # Get the current date and time
    current_date=$(date +%Y-%m-%d)
    current_time=$(date +%H-%M-%S)

    # Generate a new folder name based on the current date
    folder_name=$dir/$current_date

    # Create the folder if it doesn't exist
    mkdir -p $folder_name

    # Generate a unique filename based on the current time with the specified prefix
    filename=$prefix$current_time.wav

    # Save the name of the recording to a hidden file
    echo $filename > .recording

    # Send an SMS with the new recording filename
    gammu sendsms TEXT "+19252551045" -text "New recording started: $folder_name/$filename. The hydrophone is now recording."

    # Use arecord to record audio
    arecord -d $duration -f cd -c 2 -D $device_id --buffer-size=262144 $folder_name/$filename

    # Clear the contents of the hidden file
    echo "" > .recording
done

