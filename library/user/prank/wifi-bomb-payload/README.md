# Wi‑Fi Beacon Bomb

A lightweight Python payload that broadcasts fake 802.11 beacon frames to simulate multiple access points. This README is synchronized with the code in `src/` and `core/` (Bash setup script and Python core script).

> Warning: Use only in controlled environments where you have explicit permission to perform wireless testing.

## What is included

- `core/core.py` — Python 3 script that generates and injects beacon frames using Scapy.
- `src/payload.sh` — Bash setup script that prepares the environment, enables monitor mode, and launches the Python script in the background.

## Requirements

- Python 3
- Scapy (`python3 -m pip install scapy`)
- A wireless adapter that supports monitor mode and packet injection
- Linux-based environment for running packet injection tools (e.g., airmon-ng, iwconfig)
- WiFi Pineapple Pager (optional; can run on any Linux system with proper wireless adapter)

## Quick start

### Direct execution

Run the payload (in the src directory)

and tadaaa !!!

It will:
- Install Python dependencies (pip, Scapy)
- Auto-detect wireless interface if needed
- Enable monitor mode using airmon-ng or iwconfig
- Launch the core beacon bomb script in the background
- Log all output to `/tmp/wifi_bomb.log`

**LED Indicators (WiFi Pineapple Pager):**
- 🟣 Magenta Solid — Configuring environment and dependencies
- 🟠 Amber Blink — Monitor mode activated
- 🟢 Green Solid — Beacon bomb core script launched
- 🔴 Red Blink — Error during setup

## Configuration

### Environment variables

- `WIFI_BOMB_IFACE` — Monitor mode interface name (default: `wlan0mon`)
- `WIFI_BOMB_TOTAL` — Number of fake APs per cycle (default: `1000`)
- `WIFI_BOMB_INTERVAL` — Seconds between packets (default: `0.005`)
- `WIFI_IFACE` — Primary wireless interface for setup script (default: `wlan0`)
- `WIFI_MON_IFACE` — Explicit monitor mode interface override (optional)
- `WIFI_LOG_FILE` — Log file path (default: `/tmp/wifi_bomb.log`)

### Command-line arguments (core.py)

- `--iface` — Monitor mode interface to use
- `--total` — Number of fake APs per cycle
- `--interval` — Seconds between packets
- `--simulate` — Run in non-transmitting simulation mode
- `--verbose` — Print per-packet info to stdout

### Example configurations

```bash
# Transmit 2000 fake APs with 10ms interval on wlan0mon
env WIFI_BOMB_IFACE=wlan0mon WIFI_BOMB_TOTAL=2000 WIFI_BOMB_INTERVAL=0.01 python3 core/core.py

# Simulate without transmitting, with verbose output
python3 core/core.py --simulate --verbose

# Use custom interface
python3 core/core.py --iface ath0 --total 500
```

## How it works (implementation notes)

- The script builds 802.11 beacon frames with Scapy (RadioTap/Dot11/Dot11Beacon/Dot11Elt).
- It generates locally administered MAC addresses (first byte = 0x02) and cycles through the SSID list in `core/core.py`.
- Packets are sent via Scapy's `sendp(pkt, iface=iface, count=1)` in a tight loop.
- The payload script (`payload.sh`) handles:
  - Wireless interface auto-detection
  - Package installation and dependency management
  - Monitor mode activation via airmon-ng or iwconfig
  - Background process management with nohup
  - Comprehensive logging and error handling
- A KeyboardInterrupt (Ctrl+C) stops the loop and exits cleanly.

## SSID List

The script cycles through a list of funny/prank SSID names:

```
Searching...
Loading_WiFi_99%
Get_Your_Own_WiFi
Connecting_to_FBI_van...
Virus_Infected_AP
Router_Not_Found
Password_is_12345678
Click_Here_For_Free_RAM
Tell_My_WiFi_Love_Her
No_Free_WiFi_Here
Win_XP_Error_404
Searching_for_signal...
cheeky-breeky-iv-WANkey
what_are_you_looking
english_or_spanish
english_or_english
kim_jong_WAN
FBI_network
buy_you_own_rounter_you_thief
gameover_zeus_network
```

## Safety and ethics

Use this only on equipment and networks you own or are authorized to test. Broadcasting many fake APs can:
- Disrupt nearby Wi‑Fi clients and infrastructure
- Cause performance degradation on wireless networks
- Interfere with legitimate Wi‑Fi operations
- May violate local telecommunications regulations

**The author is not responsible for misuse.**

## Troubleshooting

### No packets being transmitted
- Verify monitor mode is active: `iwconfig | grep Monitor`
- Check adapter supports packet injection: `aireplay-ng -9 your_interface`
- Try simulation mode first: `python3 core/core.py --simulate --verbose`

## License

See the repository LICENSE file.
