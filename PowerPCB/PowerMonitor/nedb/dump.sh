#!/bin/bash

# Endpoint URL
URL="http://localhost:6666/fetch"

# POST request to fetch all data
# Here, we're sending an empty JSON object {} as the body, which means we're not applying any filters on the fetch.
curl -s -X POST -H "Content-Type: application/json" -d '{}' $URL | jq 

# Note: The | jq at the end will format the JSON output for readability. 
# If you don't have `jq` installed, you can remove that or install `jq` using:
# sudo apt install jq (for Debian/Ubuntu-based systems)

