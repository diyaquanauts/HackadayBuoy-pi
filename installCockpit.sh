sudo apt-get install cockpit
curl -sSL https://repo.45drives.com/setup | sudo bash
sudo apt-get update
sudo apt install cockpit-file-sharing
wget https://github.com/45Drives/cockpit-navigator/releases/download/v0.5.10/cockpit-navigator_0.5.10-1focal_all.deb
sudo apt install ./cockpit-navigator_0.5.10-1focal_all.deb
rm cockpit-navigator_0.5.10-1focal_all.deb
