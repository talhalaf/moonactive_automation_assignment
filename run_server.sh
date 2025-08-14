#!/usr/bin/env sh
set -e

# Default host/port can be overridden with ENV
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

# If running behind docker and env file exists, load it
if [ -f .env ]; then
  echo "Loading environment from .env"
  set -o allexport
  # shellcheck disable=SC1091
  . ./.env
  set +o allexport
fi

# Start FastAPI via uvicorn
# The ASGI app is `app` inside `server.py`
exec uvicorn server:app --host "$HOST" --port "$PORT"
