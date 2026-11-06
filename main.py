"""Interactive and CLI entrypoint for ACNH inventory injection."""

from __future__ import annotations

import argparse
from typing import Iterable

from sysbot_acnh import ACNHInjector, SLOT_COUNT

STANDARD_ITEM_BATCH = {
   "Exercise Bike": 0x011F,
   "Treadmill": 0x0122,
   "Barbecue": 0x014A,
   "Birdbath": 0x014B,
   "Birdhouse": 0x014D,
   "Lawn Mower": 0x0152,
   "Tiki Torch": 0x0157,
   "Acoustic Guitar": 0x017F,
   "Beach Chair": 0x0298,
   "Ukulele": 0x029D,
   "Statue of Liberty": 0x02B5,
   "Moai Statue": 0x02BA,
   "Fireplace": 0x02E6,
   "Jukebox": 0x0317,
   "Phonograph": 0x031A,
   "Safe": 0x0347,
   "Billiard Table": 0x035F,
   "Cat Tower": 0x0380,
   "Cuckoo Clock": 0x0393,
   "Dartboard": 0x03A9,
   "Fruit Basket": 0x03CF,
   "Harp": 0x03DB,
   "Microwave": 0x0413,
   "Pinball Machine": 0x043F,
   "Scarecrow": 0x0460,
   "Telescope": 0x04A2,
   "Typewriter": 0x04BB,
   "Campfire": 0x0595,
   "Rocket": 0x05A1,
   "Flying Saucer": 0x05A7,
   "Hammock": 0x0654,
   "Laptop": 0x073A,
   "Grand Piano": 0x0753,
   "Lighthouse": 0x091F,
   "Refrigerator": 0x0A99,
   "Katana": 0x0D4F,
   "Golden Toilet": 0x0D90,
   "Stonehenge": 0x1B83,
   "Pyramid": 0x21A0,
   "Sphinx": 0x21FE,
}


def is_valid_ipv4(ip_str: str) -> bool:
   parts = ip_str.split(".")
   if len(parts) != 4:
       return False

   for part in parts:
       if not part or not part.isdigit():
           return False
       if len(part) > 1 and part[0] == "0":
           return False
       value = int(part)
       if not 0 <= value <= 255:
           return False
   return True


def get_ip_address() -> str:
   while True:
       value = input("Please enter your Nintendo Switch IPv4 address: ").strip()
       if is_valid_ipv4(value):
           return value
       print("Invalid IP address format. Ensure it's in the format X.X.X.X (0-255 per section).\n")


def get_player_index() -> int:
   while True:
       value = input("Please enter a player index from 1 to 8: ").strip()
       try:
           player = int(value)
       except ValueError:
           print("Invalid input. Please enter a valid whole number.\n")
           continue

       if 1 <= player <= 8:
           return player
       print("Out of range! The player index must be between 1 and 8. Please try again.\n")


def show_items(items: dict[str, int] = STANDARD_ITEM_BATCH) -> None:
   print("\nItems in the standard batch:")
   for index, (name, value) in enumerate(items.items()):
       print(f"  {index:2}. {name}: {value:#06x}")
   print()


def get_menu_choice() -> str:
   while True:
       print("1. Inject the standard 40-item batch")
       print("2. Preview the item batch")
       print("3. Wipe a player's inventory")
       print("0. Exit")
       choice = input("Choose an option: ").strip()
       if choice in {"0", "1", "2", "3"}:
           return choice
       print("Invalid option. Enter 1, 2, 3, or 0.\n")


def confirm_injection() -> bool:
   while True:
       answer = input("Inject these items now? [y/N]: ").strip().lower()
       if answer in {"y", "yes"}:
           return True
       if answer in {"", "n", "no"}:
           return False
       print("Please enter y or n.\n")


def confirm_wipe() -> bool:
    answer = input("This clears all 40 inventory slots. Type WIPE to confirm: ").strip()
    return answer == "WIPE"


def ascii_header() -> None:
    header = r"""
   db    .d88b 8b  8 8   8    888 8b  8  8888 8888 .d88b 88888 .d88b. 888b.
  dPYb   8P    8Ybm8 8www8     8  8Ybm8    8  8www 8P      8   8P  Y8 8  .8
 dPwwYb  8b    8  "8 8   8     8  8  "8 w  8  8    8b      8   8b  d8 8wwK'
 dP    Yb `Y88P 8   8 8   8    888 8   8 `Yw"  8888 `Y88P   8   `Y88P' 8  Yb

Welcome to the ACNH Injector! This tool allows you to inject a standard batch of 40 items into a player's inventory on your Nintendo Switch running ACNH 3.0.3. Please ensure your Switch is connected to the same network as this computer and that you have the necessary permissions to perform these actions.
    """
    print(header)


def parse_item_code(raw_value: str) -> int:
    return int(raw_value, 0)


def run_interactive_cli() -> None:
    ascii_header()
    while True:
        choice = get_menu_choice()
        if choice == "0":
            print("Goodbye.")
            return
        if choice == "2":
            show_items()
            continue

        ip_address = get_ip_address()
        player_index = get_player_index()

        if choice == "1":
            show_items()
            print(f"Ready to inject {len(STANDARD_ITEM_BATCH)} items into player {player_index} at {ip_address}.")
            if not confirm_injection():
                print("Injection cancelled.\n")
                continue

            with ACNHInjector(ip_address, 6000, 5.0) as injector:
                injector.inject_items(player_index, STANDARD_ITEM_BATCH.values())
            print("Injection complete.\n")
        elif choice == "3":
            print(f"Ready to wipe player {player_index}'s inventory at {ip_address}.")
            if not confirm_wipe():
                print("Wipe cancelled.\n")
                continue

            with ACNHInjector(ip_address, 6000, 5.0) as injector:
                injector.wipe_player_inventory(player_index)
            print("Inventory wiped.\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inject items into an Animal Crossing: New Horizons inventory via sys-botbase.")
    parser.add_argument("--ip", help="Nintendo Switch IPv4 address")
    parser.add_argument("--player", type=int, help="Player index from 1 to 8")
    parser.add_argument("--port", type=int, default=6000, help="Switch sys-botbase port")
    parser.add_argument("--timeout", type=float, default=5.0, help="TCP timeout in seconds")
    parser.add_argument("--preview", action="store_true", help="Print the default item batch without injecting")
    parser.add_argument("--wipe", action="store_true", help="Wipe a player's inventory")
    parser.add_argument("--fill", help="Fill the player's inventory with a single item in hexadecimal form, e.g. 0x011F")
    parser.add_argument("--inject", nargs="*", help="Custom item IDs in hexadecimal form to inject into the target player")
    return parser


def run_cli() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.preview:
        show_items()
        return

    if not any((args.ip, args.player, args.wipe, args.fill, args.inject)):
        run_interactive_cli()
        return

    if not args.ip:
        parser.error("--ip is required unless running the interactive menu")
    if not is_valid_ipv4(args.ip):
        parser.error("invalid --ip value; expected IPv4 in the form X.X.X.X")
    if args.player is None:
        parser.error("--player is required when using injection or wipe commands")
    if not 1 <= args.player <= 8:
        parser.error("--player must be between 1 and 8")

    if args.wipe:
        with ACNHInjector(args.ip, args.port, args.timeout) as injector:
            injector.wipe_player_inventory(args.player)
        return

    if args.fill is not None:
        item_code = parse_item_code(args.fill)
        with ACNHInjector(args.ip, args.port, args.timeout) as injector:
            injector.fill_inventory_with_item(args.player, item_code)
        return

    values = [parse_item_code(value) for value in (args.inject or STANDARD_ITEM_BATCH.values())]
    with ACNHInjector(args.ip, args.port, args.timeout) as injector:
        injector.inject_items(args.player, values)


if __name__ == "__main__":
    run_cli()
