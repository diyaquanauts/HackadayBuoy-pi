#!/bin/bash

# Update the repositories
sudo apt-get update

# List of packages to install
packages=(
    screen
    vim
    v4l-utils
    ffmpeg
    python3-pip
    alsa-utils
    jq
    sox
    #cockpit  # Uncomment if you want to install cockpit
)

# Install each package using apt-get
for pkg in "${packages[@]}"; do
    echo "Installing $pkg..."
    sudo apt-get install -y $pkg
    if [ $? -ne 0 ]; then
        echo "Failed to install $pkg. Exiting."
        exit 1
    fi
    echo "$pkg installed successfully."
done

echo "All packages installed successfully."
