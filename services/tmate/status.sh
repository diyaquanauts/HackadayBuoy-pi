#!/bin/bash

SERVICE_NAME="tmate"

status=$(systemctl status "$SERVICE_NAME")

echo $status
