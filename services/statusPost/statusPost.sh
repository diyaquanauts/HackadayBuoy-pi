#!/bin/bash

while true; do
  cd ..
  # Loop through all subdirectories of the current directory
  for dir in */; do
    # Check if there's a file called "post.js" in the directory
    if [ -f "${dir}/post.js" ]; then
      # Run the "post.js" script using "node"
      cd "$dir"
      node post.js
      cd ..
    fi
  done

  # Sleep for 30 minutes
  sleep 1800
done

