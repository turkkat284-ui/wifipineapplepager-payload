# Wi‑Fi Beacon Bomb

A lightweight Python payload that broadcasts fake 802.11 beacon frames to simulate multiple access points. This README is synchronized with the code in `src/` and `core/` (payload script and Ducky payload), and documents only the files shipped in this payload directory.

> Warning: Use only in controlled environments where you have explicit permission to perform wireless testing.

## What is included

- core/core.py — Python 3 script that generates and injects beacon frames using Scapy.
- src/payload.txt — DuckyScript-style payload that prepares the environment, enables monitor mode, and launches the Python script in the background.

## Requirements

- Python 3
- Scapy (`python3 -m pip install scapy`)
- A wireless adapter that supports monitor mode and packet injection
- Linux-based environment for running packet injection tools (e.g., airmon-ng)

## Quick start

1. Put your wireless interface into monitor mode (the included Ducky payload attempts to do this automatically via airmon-ng):

   ```bash
   sudo airmon-ng start wlan0
   ```

2. Run the Python script directly:

   ```bash
   python3 core/core.py
   ```

   By default the script uses the `WIFI_BOMB_IFACE` environment variable or `wlan0mon` if not set.

3. To run without transmitting packets (simulation mode):

   ```bash
   python3 core/core.py --simulate --verbose
   ```

4. The DuckyScript payload (`src/payload.txt`) will attempt to install pip/scapy, enable monitor mode, and start the script in the background:

   - It sets `WIFI_BOMB_IFACE` to the monitor interface and launches: `env WIFI_BOMB_IFACE=wlan0mon python3 core/core.py`

## Configuration

- Interface: change the default monitor interface by setting the `WIFI_BOMB_IFACE` environment variable or passing `--iface` to `core.py`.
- Total fake APs per cycle: `--total` (default from code: 1000 or from env `WIFI_BOMB_TOTAL`).
- Packet interval: `--interval` seconds between packets (default 0.005 or from env `WIFI_BOMB_INTERVAL`).
- Simulate: `--simulate` to run in non-transmitting mode for testing.
- Verbose: `--verbose` for per-packet logging to stdout.

## How it works (implementation notes)

- The script builds 802.11 beacon frames with Scapy (RadioTap/Dot11/Dot11Beacon/Dot11Elt).
- It generates locally administered MAC addresses and cycles through a small SSID list included in `core/core.py`.
- Packets are sent via `sendp(pkt, iface=iface, count=1)` in a tight loop.
- A KeyboardInterrupt (Ctrl+C) stops the loop and exits cleanly.

## Safety and ethics

Use this only on equipment and networks you own or are authorized to test. Broadcasting many fake APs can disrupt nearby Wi‑Fi clients and infrastructure.

## License

See the repository LICENSE file.
