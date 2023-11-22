const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const duration = 600;

// Mount point and device for the external hard drive
const mountPoint = "/mnt/sandisk";
const driveDevice = "/dev/sda2";
const baseDir = '/mnt/sandisk/cameraCaptures';

// Check if the SSD is mounted
if (!fs.existsSync(driveDevice) || !execSync('mount').toString().includes(mountPoint)) {
    console.error("External SSD is not mounted. Attempting to mount...");

    // Attempt to mount the SSD
    try {
        execSync(`sudo mount ${driveDevice} ${mountPoint}`);
    } catch (error) {
        console.error(`Failed to mount SSD: ${error.message}`);
        process.exit(1);
    }
}

// Ensure base directory exists
if (!fs.existsSync(baseDir)) {
    fs.mkdirSync(baseDir, { recursive: true });
}

// Prefix for the filenames
const prefix = "rec_";

// Device ID for the USB video device
const deviceId = "/dev/video0";

// Check if the USB video device is available
if (!fs.existsSync(deviceId)) {
    console.error("USB video device not found");
    process.exit(1);
}
console.log('Capture init OK');

function recordVideo(){
    const currentDate = new Date();
    const folderName = path.join(baseDir, currentDate.toISOString().split('T')[0]);
    const filename = `${prefix}${currentDate.toISOString().replace(/[-:T]/g, '_').split('.')[0]}.mp4`;

    if (!fs.existsSync(folderName)) {
        fs.mkdirSync(folderName, { recursive: true });
    }
    console.log(`Recording to: ${path.join(folderName, filename)}`);
    // Record video and take snapshot
    try {
        execSync(`yes | ffmpeg -f v4l2 -input_format mjpeg -i ${deviceId} -frames:v 1 -update 1 ${path.join(folderName, 'snapshot.jpg')}`);
        execSync(`ffmpeg -f v4l2 -input_format mjpeg -r 25 -s 1920x1080 -i ${deviceId} -t ${duration} -c:v libx264 -preset ultrafast -crf 23 ${path.join(folderName, filename)}`);
        console.log(`Recording saved: ${filename}`);
    } catch (error) {
        console.error(`Error during recording: ${error}`);
    }
}

recordVideo();

setInterval(() => {
    recordVideo();
}, duration * 1000);

