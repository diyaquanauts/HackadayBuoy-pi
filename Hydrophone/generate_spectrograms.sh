#!/bin/bash

# Set the recordings directory path
dir="./recordings"

while true; do
    echo "Starting loop..."

    # Loop through all the date folders in the recordings directory
    for date_folder in "$dir"/*; do
        if [ -d "$date_folder" ]; then

            # Loop through all the WAV files in the current date folder
            for filename in "$date_folder"/*.wav; do
                if [ -e "$filename" ]; then
                    echo "Converting file: $filename"
                    if fuser -s "$filename"; then
                        echo "File is still being written to: $filename"
                    else
                        # Generate the PNG file name based on the original WAV file name
                        png_filename="${filename%.*}.png" # replace the file extension with .png

                        # Check if the PNG file already exists, and skip the conversion if it does
                        if [ -e "$png_filename" ]; then
                            echo "Skipping conversion, PNG file already exists: $png_filename"
                        else
                            # Generate the spectrogram for the WAV file
			    # sox -V3 "$filename" -n remix 1 spectrogram -x 1920 -y 1080 -z 120 -X 64 -o "$png_filename"
			    sox -V3 "$filename" -n remix 1 spectrogram -o "$png_filename"
                            # ffmpeg -i "$filename" -lavfi "showspectrumpic=s=1280x720" "$png_filename"
                        fi
                    fi
                fi
            done

        fi
    done

    echo "Finished loop."

    # Sleep for 10 minutes before running the loop again
    echo "Sleeping for 1 minute..."
    sleep 30
done

