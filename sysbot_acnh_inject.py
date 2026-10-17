from sysbot_acnh import ACNHInjector

import argparse
import socket
import struct
import sys

SWITCH_IP = "192.168.12.115"
PORT = 6000
TIMEOUT = 5.0

item_hex_codes = [
    0x011F,  # slot 1: exercise bike
    0x0122,  # slot 2: treadmill
    0x014A,  # slot 3: barbecue
    0x014B,  # slot 4: birdbath
    0x014D,  # slot 5: birdhouse
    0x0152,  # slot 6: lawn mower
    0x0157,  # slot 7: tiki torch
    0x017F,  # slot 8: acoustic guitar
    0x0298,  # slot 9: beach chair
    0x029D,  # slot 10: ukulele
    0x02B5,  # slot 11: Statue of Liberty
    0x02BA,  # slot 12: moai statue
    0x02E6,  # slot 13: fireplace
    0x0317,  # slot 14: jukebox
    0x031A,  # slot 15: phonograph
    0x0347,  # slot 16: safe
    0x035F,  # slot 17: billiard table
    0x0380,  # slot 18: cat tower
    0x0393,  # slot 19: cuckoo clock
    0x03A9,  # slot 20: dartboard
    0x03CF,  # slot 21: fruit basket
    0x03DB,  # slot 22: harp
    0x0413,  # slot 23: microwave
    0x043F,  # slot 24: pinball machine
    0x0460,  # slot 25: scarecrow
    0x04A2,  # slot 26: telescope
    0x04BB,  # slot 27: typewriter
    0x0595,  # slot 28: campfire
    0x05A1,  # slot 29: rocket
    0x05A7,  # slot 30: flying saucer
    0x0654,  # slot 31: hammock
    0x073A,  # slot 32: laptop
    0x0753,  # slot 33: grand piano
    0x091F,  # slot 34: lighthouse
    0x0A99,  # slot 35: refrigerator
    0x0D4F,  # slot 36: katana
    0x0D90,  # slot 37: golden toilet
    0x1B83,  # slot 38: Stonehenge
    0x21A0,  # slot 39: pyramid
    0x21FE,  # slot 40: sphinx
]

with ACNHInjector(SWITCH_IP, PORT, TIMEOUT) as injector:
    injector.wipe_player_inventory(1)
    #injector.inject_items(1, item_hex_codes)
    #injector.inject_items(1,item_hex_codes)
    #injector.fill_inventory_with_item(1, 0x3604)
