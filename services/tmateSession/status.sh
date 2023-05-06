#!/bin/bash

SERVICE_NAME="tmateSessionFinder.service"

status=$(systemctl status "$SERVICE_NAME")

echo $status
