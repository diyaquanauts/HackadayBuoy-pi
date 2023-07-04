#!/bin/bash

# Set the directory to save recordings and snapshots
dir="./recordings"

# Set the duration of each recording
duration=60   # seconds

# Set the mount point and device for the external hard drive
mount_point="/mnt/sandisk"
drive_device="/dev/sda2"

if [ ! -d $mount_point ]; then
    echo "Creating mount point"
    sudo mkdir -p $mount_point
fi

# If the hard drive is available and not already mounted, mount it
if [ -b $drive_device ] && ! mount | grep $mount_point > /dev/null; then
    echo "Mounting external hard drive"
    sudo mount $drive_device $mount_point
    dir=$mount_point
fi

# Set the desired prefix for the filenames
prefix="rec_"

# Set the device ID for the USB video device
device_id="/dev/video0"

# Check if the USB video device is available
if [ ! -e $device_id ]; then
    echo "USB video device not found"
    exit 1
fi

# Infinite loop to continuously record video
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
    filename=$prefix$current_time.mp4

    # Save the name of the recording to a hidden file
    echo $filename > .recording

    # Send an SMS with the new recording filename
    # gammu sendsms TEXT "+19252551045" -text "New recording started: $folder_name/$filename. The video stream is now being recorded."

    yes | ffmpeg -f v4l2 -input_format mjpeg -i $device_id -frames:v 1 snapshot.jpg
    ffmpeg -f v4l2 -input_format mjpeg -r 25 -s 1920x1080 -i $device_id -t $duration -c:v copy $folder_name/$filename
    #ffmpeg -f v4l2 -input_format mjpeg -r 24 -s 1920x1080 -i $device_id -t $duration -c:v copy $folder_name/$filename
    #timeout $duration ffmpeg -y -f v4l2 -input_format mjpeg -r 24 -s 1920x1080 -i $device_id -c:v copy "$folder_name/$filename" -vf "fps=1/2" -update 1 snapshot.jpg
    #ffmpeg -y -f v4l2 -input_format mjpeg -r 24 -s 1920x1080 -i $device_id -t $duration -c:v $folder_name/$filename -vf "fps=1/2" -update 1 snapshot.jpg
    #timeout $duration ffmpeg -y -f v4l2 -input_format mjpeg -r 24 -s 1920x1080 -i $device_id -c:v copy $folder_name/$filename -vf "fps=1/2" -update 1 snapshot.jpg

    # Clear the contents of the hidden file
    echo "" > .recording
done

