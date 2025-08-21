#!/bin/bash

DIR="silfloresapp"
ENV_FILE="dotenv_files/.env"
NGROK_PID=

# Function to clean up and exit
function finish_script() {
    echo ""
    echo "Finishing server..."
    if [ ! -z "$NGROK_PID" ]; then
        kill $NGROK_PID
    fi
    echo "Bringing down Docker services..."
    docker-compose down
    exit 0
}

# Trap SIGINT (Ctrl+C) to run the cleanup function
trap finish_script SIGINT

# Function to start ngrok and docker
function start_all() {
    echo "Starting ngrok tunnel for django (port 8000)..."
    # Start ngrok in the background
    ngrok http 8000 > /dev/null &
    NGROK_PID=$!

    # Wait a moment for ngrok to initialize and its API to become active
    sleep 5

    # Fetch the public URL from the local ngrok API
    NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[] | select(.proto == "https") | .public_url')

    if [ -z "$NGROK_URL" ] || [ "$NGROK_URL" == "null" ]; then
        echo "Error: Failed to retrieve ngrok URL."
        echo "Please ensure ngrok is installed and authenticated."
        finish_script
    fi

    echo "Ngrok URL: $NGROK_URL"

    # Update or add the NGROK_URL in the .env file
    if grep -q "^NGROK_URL=" "$ENV_FILE"; then
        sed -i "s|^NGROK_URL=.*|NGROK_URL=$NGROK_URL|" "$ENV_FILE"
    else
        echo "NGROK_URL=$NGROK_URL" >> "$ENV_FILE"
    fi

    echo "Starting Docker services..."
    docker-compose up
}

# Initial start of services
start_all

echo "Watching for file changes in '$DIR'..."
echo "(Excluding .js and .css files)"

# Use inotifywait to monitor for file changes and restart the service.
# The '-m' option makes it monitor indefinitely.
# The '--exclude' option uses a regex to ignore .js and .css files.
inotifywait -r -m -e modify,create,delete --exclude "\.(js|css)$" "$DIR" |
while read path action file; do
    echo "Change detected: $path$file ($action). Restarting Docker services..."
    docker-compose down
    sleep 12
    docker-compose up
done
