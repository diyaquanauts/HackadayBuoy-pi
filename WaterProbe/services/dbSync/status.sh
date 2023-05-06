#!/bin/bash

SERVICE_NAME="nedb.socket.service"

status=$(systemctl status "$SERVICE_NAME")

echo $status
