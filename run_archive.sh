#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
HOST="${HOST:-127.0.0.1}"
REQUESTED_PORT="${PORT:-8090}"

port_available() {
  python3 - "$HOST" "$1" <<'PY'
import socket
import sys

host, port = sys.argv[1], int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((host, port))
    except OSError:
        sys.exit(1)
PY
}

find_available_port() {
  local port="$REQUESTED_PORT"
  local attempts=0

  while ! port_available "$port"; do
    if [[ "$attempts" -eq 0 ]]; then
      echo "Port $port is in use, trying the next available port..." >&2
    fi
    port=$((port + 1))
    attempts=$((attempts + 1))
    if [[ "$attempts" -gt 50 ]]; then
      echo "Error: could not find a free port near $REQUESTED_PORT." >&2
      exit 1
    fi
  done

  echo "$port"
}

PORT="$(find_available_port)"
URL="http://${HOST}:${PORT}/"

cd "$ROOT"

echo "Priscilla Petty — archived pages viewer"
echo "Directory: $ROOT"
echo "URL:       $URL"
echo ""
echo "Use the sidebar to switch between retired pages."
echo "Press Ctrl+C to stop."
echo ""

if [[ "$(uname -s)" == "Darwin" ]] && [[ "${OPEN_BROWSER:-1}" == "1" ]]; then
  (sleep 0.5 && open "$URL") &
fi

exec python3 "$ROOT/scripts/archive_server.py" --host "$HOST" --port "$PORT"
