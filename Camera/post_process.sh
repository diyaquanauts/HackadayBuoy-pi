#!/bin/bash

# Set the recordings directory path
dir="./recordings"

# Custom Python script command
python_script="python3 detect_objects.py"

while true; do
    echo "Starting loop..."

    # Loop through all the date folders in the recordings directory
    for date_folder in "$dir"/*; do
        if [ -d "$date_folder" ]; then

            # Loop through all the MP4 files in the current date folder
            for filename in "$date_folder"/*.mp4; do
                if [ -e "$filename" ]; then
                    echo "Processing file: $filename"
                    if fuser -s "$filename"; then
                        echo "File is still being written to: $filename"
                    else
                        # Generate the output filename based on the original MP4 file name
                        output_filename="${filename%.*}_processed.mp4" # add "_processed" to the file name

                        # Check if the output file already exists, and skip processing if it does
                        if [ -e "$output_filename" ]; then
                            echo "Skipping processing, output file already exists: $output_filename"
                        else
                            # Run the custom Python script with the MP4 filename as an argument
                            echo "Running custom Python script..."
                            output="$($python_script "$filename" "$output_filename")"
                            echo "Custom Python script output: $output"
                        fi
                    fi
                fi
            done

        fi
    done

    echo "Finished loop."

    # Sleep for 10 minutes before running the loop again
    echo "Sleeping for 1 minute..."
    sleep 60
done

