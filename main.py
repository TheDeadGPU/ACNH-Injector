from sysbot_acnh import ACNHInjector

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

def is_valid_ipv4(ip_str):
  # Split the string by dots
  parts = ip_str.split(".")

  # An IPv4 address must have exactly 4 octets
  if len(parts) != 4:
    return False

  for part in parts:
    # Check if the part is a number (only digits) and not empty
    if not part.isdigit():
      return False

    # Prevent leading zeros (e.g., "192.168.01.1" is technically invalid standard form)
    if len(part) > 1 and part[0] == "0":
      return False

    # Convert to integer and check if it's between 0 and 255
    num = int(part)
    if not (0 <= num <= 255):
      return False

  return True


def get_ip_address():
  while True:
    user_input = input("Please enter your Nintendo Switch IPv4 address: ").strip()

    if is_valid_ipv4(user_input):
      return user_input
    else:
      print(
          "Invalid IP address format. Ensure it's in the format X.X.X.X (0-255"
          " per section).\n"
      )

def get_player_index():
  while True:
    user_input = input("Please enter a player index from 1 to 8: ").strip()

    try:
      # Convert input string to an integer
      number = int(user_input)

      # Check if the number is within the allowed range
      if 1 <= number <= 8:
        return number
      else:
        print(
            "Out of range! The player index must be between 1 and 8. Please try"
            " again.\n"
        )

    except ValueError:
      # Catches cases where the user types letters or symbols instead of digits
      print("Invalid input. Please enter a valid whole number.\n")


def show_items():
    print("\nItems in the standard batch:")
    for slot, item in enumerate(item_hex_codes, start=1):
        print(f"  {slot:2}. {item:#06x}")
    print()


def get_menu_choice():
    while True:
        print("1. Inject the standard 40-item batch")
        print("2. Preview the item batch")
        print("3. Wipe a player's inventory")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice in {"0", "1", "2", "3"}:
            return choice
        print("Invalid option. Enter 1, 2, 3, or 0.\n")


def confirm_injection():
    while True:
        answer = input("Inject these items now? [y/N]: ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"", "n", "no"}:
            return False
        print("Please enter y or n.\n")


def confirm_wipe():
    answer = input(
        "This clears all 40 inventory slots. Type WIPE to confirm: "
    ).strip()
    return answer == "WIPE"


def ascii_header():
    header = r"""
   db    .d88b 8b  8 8   8    888 8b  8  8888 8888 .d88b 88888 .d88b. 888b. 
  dPYb   8P    8Ybm8 8www8     8  8Ybm8    8  8www 8P      8   8P  Y8 8  .8 
 dPwwYb  8b    8  "8 8   8     8  8  "8 w  8  8    8b      8   8b  d8 8wwK' 
dP    Yb `Y88P 8   8 8   8    888 8   8 `Yw"  8888 `Y88P   8   `Y88P' 8  Yb 
                                                                            
  """
    print(header)

if __name__ == "__main__":
    ascii_header()
    while True:
        choice = get_menu_choice()
        if choice == "0":
            print("Goodbye.")
            break
        if choice == "2":
            show_items()
            continue

        ip = get_ip_address()
        player_index = get_player_index()
        if choice == "1":
            show_items()
            print(f"Ready to inject {len(item_hex_codes)} items into player {player_index} at {ip}.")
            if not confirm_injection():
                print("Injection cancelled.\n")
                continue

            with ACNHInjector(ip, 6000, 5.0) as injector:
                injector.inject_items(player_index, item_hex_codes)
            print("Injection complete.\n")
        elif choice == "3":
            print(f"Ready to wipe player {player_index}'s inventory at {ip}.")
            if not confirm_wipe():
                print("Wipe cancelled.\n")
                continue

            with ACNHInjector(ip, 6000, 5.0) as injector:
                injector.wipe_player_inventory(player_index)
            print("Inventory wiped.\n")
