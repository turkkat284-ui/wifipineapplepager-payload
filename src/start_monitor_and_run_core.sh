#!/usr/bin/env bash
set -e

INTERFACE="${1:-wlan0}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$(realpath "$SCRIPT_DIR/../core")"
CORE_PY="$CORE_DIR/core.py"

if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root. Use sudo." >&2
  exit 1
fi

# Try to enable monitor mode using airmon-ng if available, otherwise fall back to iw
if command -v airmon-ng >/dev/null 2>&1; then
  echo "Using airmon-ng to enable monitor mode on $INTERFACE"
  # airmon-ng may kill interfering processes; allow it to continue even if it fails
  airmon-ng check kill || true
  airmon-ng start "$INTERFACE"
  # After airmon-ng, the monitor interface is usually <iface>mon. Try to detect it.
  MON_IF=$(iw dev | awk '/Interface/ {print $2}' | grep -E "^${INTERFACE}|mon" | head -n1 || true)
else
  echo "Using iw to enable monitor mode on $INTERFACE"
  ip link set "$INTERFACE" down || true
  if iw dev "$INTERFACE" set type monitor 2>/dev/null; then
    ip link set "$INTERFACE" up
    MON_IF="$INTERFACE"
  else
    echo "Failed to set monitor mode with iw. You may need to use airmon-ng or install wireless-tools." >&2
    ip link set "$INTERFACE" up || true
    exit 1
  fi
fi

if [ -z "$MON_IF" ]; then
  echo "Could not determine monitor interface." >&2
  iw dev || true
  exit 1
fi

echo "Monitor interface: $MON_IF"
# Export the interface name so core.py can read it from environment if desired
export MON_IF

if [ ! -f "$CORE_PY" ]; then
  echo "Core script not found at $CORE_PY" >&2
  exit 1
fi

echo "Starting core.py with monitor interface $MON_IF"
python3 "$CORE_PY" "$MON_IF"
