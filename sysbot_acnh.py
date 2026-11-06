"""Animal Crossing: New Horizons inventory injection helpers."""

from __future__ import annotations

import struct
from typing import Iterable, Sequence

from sysbot import SysBot

ACNH_TITLE_ID = "01006F8002326000"
BASE_INVENTORY_OFFSETS = (0xB27BB758, 0xB27BB6A0)
PLAYER_SPACING = 0x131F70
SLOT_STRIDE = 0x8
SLOT_COUNT = 40
BLOCK_SIZE = 20
EMPTY_ITEM = 0xFFFE


class ACNHInventoryError(RuntimeError):
    """Raised when an inventory operation cannot be safely performed."""


class GameNotDetectedError(ACNHInventoryError):
    """Raised when the connected title is not Animal Crossing."""


class ACNHInjector:
    """Write ACNH inventory values through sys-botbase."""

    def __init__(self, switch_ip: str, port: int = 6000, timeout: float = 5.0):
        self.switch_ip = switch_ip
        self.port = port
        self.timeout = timeout
        self.bot = SysBot(switch_ip, port, timeout)

    def close(self) -> None:
        self.bot.close()

    def __enter__(self) -> "ACNHInjector":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    @staticmethod
    def _validate_player(player: int) -> None:
        if not 1 <= player <= 8:
            raise ValueError("player must be between 1 and 8")

    @staticmethod
    def _validate_slot(slot: int) -> None:
        if not 0 <= slot < SLOT_COUNT:
            raise ValueError(f"slot must be between 0 and {SLOT_COUNT - 1}")

    @staticmethod
    def _require_acnh(bot: SysBot) -> None:
        title_id = bot.Utility.title_id()
        if ACNH_TITLE_ID.lower() not in title_id.lower():
            raise GameNotDetectedError(f"ACNH not detected (title ID: {title_id!r})")

    def slot_address(self, player: int, slot: int) -> int:
        self._validate_player(player)
        self._validate_slot(slot)

        block, index = divmod(slot, BLOCK_SIZE)
        base = BASE_INVENTORY_OFFSETS[block]
        return base + PLAYER_SPACING * (player - 1) + SLOT_STRIDE * index

    def _write_inventory_values(self, player: int, values: Sequence[int], *, action: str) -> None:
        if not values:
            return

        if len(values) > SLOT_COUNT:
            raise ValueError(f"too many inventory entries to write (max {SLOT_COUNT})")

        with self.bot as bot:
            self._require_acnh(bot)

            codes = [int(value) & 0xFFFFFFFF for value in values]
            addresses = [self.slot_address(player, index) for index in range(len(codes))]
            start = min(addresses)
            end = max(addr + SLOT_STRIDE for addr in addresses)
            current = bytearray(bot.Ram.peek(start, end - start))

            for offset, value in enumerate(codes):
                item_bytes = struct.pack("<I", value)
                address = addresses[offset]
                index = address - start
                print(f"[+] {action} item {value:#06x} into player {player} slot {offset}")
                current[index:index + len(item_bytes)] = item_bytes

            bot.Ram.poke(start, bytes(current))

    def inject_items(self, player: int, item_hex_codes: Iterable[int]) -> None:
        """Inject a list of item hex codes into a player's inventory slots."""
        items = list(item_hex_codes)
        self._write_inventory_values(player, items, action="Injecting")

    def wipe_player_inventory(self, player: int) -> None:
        """Write EMPTY_ITEM into every slot in a player's inventory."""
        self._write_inventory_values(player, [EMPTY_ITEM] * SLOT_COUNT, action="Wiping")
        print(f"[-] Wiped player {player}'s inventory slots.")

    def fill_inventory_with_item(self, player: int, item_hex_code: int) -> None:
        """Fill a player's inventory with a single item hex code."""
        self._write_inventory_values(player, [int(item_hex_code)] * SLOT_COUNT, action="Filling")
        print(f"[+] Filled player {player}'s inventory slots with item {int(item_hex_code):#06x}.")


    