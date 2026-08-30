# Wi‑Fi Beacon Bomb

A lightweight Python tool that continuously broadcasts fake 802.11 beacon frames to simulate multiple access points. It is built for wireless testing, lab environments, and educational exploration using Scapy.

> Warning: This project is intended only for authorized, lawful testing in environments where you have explicit permission to assess wireless behavior.

## What this project does

The script creates randomized SSIDs and locally administered MAC addresses, then injects beacon frames onto a selected wireless interface. This can be useful in controlled network research, Wi‑Fi lab setups, and defensive testing scenarios.

## Features

- broadcasts up to (depends on system performance) fake APs in a loop
- generates a unique SSID for each beacon frame
- creates randomized BSSID-like MAC addresses
- uses raw packet injection with Scapy
- supports quick deployment from a Linux-based wireless adapter

## Repository structure

```text
wifi-bomb/
├── core/
│   └── core.py
├── src/
│   └── payload.txt
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── .gitignore
```

## Requirements

- Python 3
- Scapy
- a wireless interface capable of monitor mode
- Linux-based environment for packet injection

Install dependencies:

```bash
python3 -m pip install scapy
```

## Setup

Before running the tool, make sure the interface is available and in monitor mode.

Example:

```bash
sudo airmon-ng start wlan0
```

Then confirm the monitor interface name, such as `wlan0mon`.

## Usage

Run the script directly:

```bash
python3 core/core.py
```

The script uses this configuration by default:

```python
IFACE = "wlan0mon"
```

To adjust behavior, edit the values in [core/core.py](core/core.py).

### Stop the script

Press `Ctrl + C` in the terminal to stop the broadcast loop.

## How it works

The script:

1. selects a wireless interface
2. creates fake SSIDs like `FAKE_AP_0`, `FAKE_AP_1`, and so on
3. generates random MAC addresses
4. builds 802.11 beacon packets with Scapy
5. injects them continuously using `sendp()`

This approach is intentionally simple and readable for educational use.

## Ducky payload

The repository also includes a payload file in [src/payload.txt](src/payload.txt) that automates the setup and starts the Python script in the background.

## Safety and ethics

Use this project only in environments you own, manage, or are explicitly authorized to test. Do not target third-party networks, production infrastructure, or public Wi‑Fi environments without permission.

The code is provided for learning, defensive testing, and authorized research only.

## Contributing

Contributions are welcome if they improve documentation, compatibility, safety, or maintainability. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

This project is distributed under the terms of the repository license. See [LICENSE](LICENSE) for details.

## Disclaimer

The author assumes no responsibility for misuse of this software. This project is not intended to facilitate unauthorized interference with wireless networks.
