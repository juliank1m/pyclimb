#!/bin/sh
set -e

# Default to port 8000 if PORT is not set
PORT="${PORT:-8000}"

echo "Starting gunicorn on port $PORT"
exec gunicorn pyclimb.wsgi:application --bind "0.0.0.0:$PORT"
