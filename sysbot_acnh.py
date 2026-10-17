from sysbot import SysBot

import argparse
import socket
import struct
import sys

ACNH_TITLE_ID = "01006F8002326000"
BASE_INVENTORY_OFFSET = 0xB27BB758  # player 1 inventory slots 1-20, ACNH 3.0.0 (heap-relative)
BASE_INVENTORY2_OFFSET = 0xB27BB6A0  # player 1 inventory slots 21-40, ACNH 3.0.0 (heap-relative)
PLAYER_SPACING = 0x131F70
SLOT_STRIDE = 0x8                   # one item = 8 bytes
SLOT_COUNT = 40
BLOCK_SIZE = 20

class ACNHInjector:
    def __init__(self, switch_ip: str, port: int = 6000, timeout: float = 5.0):
        self.switch_ip = switch_ip
        self.port = port
        self.timeout = timeout
        self.bot = SysBot(switch_ip, port, timeout)

    def close(self) -> None:
            self.bot.close()
        
    def __enter__(self):
            return self
    
    def __exit__(self, *exc):
        self.close()



    def slot_address(self, player: int, slot: int) -> int:
        if player < 1:
            raise ValueError("player must be >= 1")
        if not 0 <= slot < SLOT_COUNT:
            raise ValueError(f"slot must be 0-{SLOT_COUNT - 1}")
        block, index = divmod(slot, BLOCK_SIZE)
        base = BASE_INVENTORY_OFFSET if block == 0 else BASE_INVENTORY2_OFFSET
        return base + PLAYER_SPACING * (player - 1) + SLOT_STRIDE * index


    def inject_items(self, player: int, item_hex_codes) -> None:
        """Inject a list of item hex codes into a player's inventory slots."""
        with self.bot as bot:
            title = bot.Utility.title_id()
            if ACNH_TITLE_ID.lower() not in title.lower():
                sys.exit(f"[-] ACNH not detected (title ID: {title!r})")

            if len(item_hex_codes) > SLOT_COUNT:
                sys.exit(f"[-] Too many items to inject (max {SLOT_COUNT})")

            for counter, item in enumerate(item_hex_codes):
                print(f"[+] Injecting item {item:#06x} into player {player} slot {counter}")
                bot.Ram.poke(self.slot_address(player, counter), struct.pack("<I", item))

    def wipe_player_inventory(self, player: int) -> None:
         with self.bot as bot:
            title = bot.Utility.title_id()
            if ACNH_TITLE_ID.lower() not in title.lower():
                sys.exit(f"[-] ACNH not detected (title ID: {title!r})")

            for i in range(0, SLOT_COUNT):
                bot.Ram.poke(self.slot_address(player,i), struct.pack("<I", 0xFFFE))
            print(f"[-] Wiped player{player}'s inventory slots.")

    def fill_inventory_with_item(self, player: int, item_hex_code: int) -> None:
        """Fill a player's inventory with a specific item hex code."""
        with self.bot as bot:
            title = bot.Utility.title_id()
            if ACNH_TITLE_ID.lower() not in title.lower():
                sys.exit(f"[-] ACNH not detected (title ID: {title!r})")

            for i in range(0, SLOT_COUNT):
                bot.Ram.poke(self.slot_address(player,i), struct.pack("<I", item_hex_code))
            print(f"[+] Filled player{player}'s inventory slots with item {item_hex_code:#06x}.")
              


    