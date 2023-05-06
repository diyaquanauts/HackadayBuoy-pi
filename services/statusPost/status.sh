#!/bin/bash

SERVICE_NAME="systemStatus.service"

status=$(systemctl status "$SERVICE_NAME")

echo $status
