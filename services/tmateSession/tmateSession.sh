#!/bin/bash

# Get the device name
device_name=$(hostname)

while true; do

  # Get the session IDs
  read -r session_id < <(sudo tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}')

  # Construct the query object
  query="{\"deviceName\":\"$device_name\",\"serviceName\":\"tmateSessionID\"}"

  # Check if there's an existing record with the same device name and service name
  response=$(curl -k -H "Content-Type: application/json" \
    -H "x-apikey: apikey" \
    -X GET -d "$query" "deployments endpoint")

  # Check if the response contains any records
  if [[ "$response" == *"\"_id\""* ]]; then
    # Update the existing record with the new session ID
    record_id=$(echo "$response" | jq -r .[0]._id)
    update_data="{\"extra\":\"$session_id\"}"
    curl -k -H "Content-Type: application/json" \
      -H "x-apikey: apikey" \
      -X PUT -d "$update_data" "deployments endpoint/$record_id"
  else
    # Create a new record with the session ID
    data="{\"deviceName\":\"$device_name\",\"serviceName\":\"tmateSessionID\",\"extra\":\"$session_id\"}"
    curl -k -H "Content-Type: application/json" \
      -H "x-apikey: apikey" \
      -X POST -d "$data" "deployments endpoint"
  fi

  sleep 300 # Wait for 5 minutes
done

