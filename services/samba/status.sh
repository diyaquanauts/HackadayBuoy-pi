#!/bin/bash

SERVICE_NAME="smbd"

status=$(systemctl status "$SERVICE_NAME")

echo $status
