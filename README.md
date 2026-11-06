# ACNH-Injector

A lightweight Python utility for injecting custom item IDs into Animal Crossing: New Horizons inventory slots using a Nintendo Switch running `sys-botbase`.

## Overview

`ACNH-Injector` is a small, targeted memory-editing tool designed to connect to a Switch over TCP and write item values directly into the game's inventory memory. It is intended for advanced users working in a controlled, local environment and is tightly coupled to the ACNH game memory layout.

This repository includes:

- a minimal socket client for communicating with `sys-botbase`
- ACNH-specific inventory memory offsets and slot calculations (ACNH 3.0.3)
- a CLI workflow for injecting or wiping inventory contents

## What it does

The script can:

- validate that the connected game is Animal Crossing: New Horizons
- calculate addresses for player inventory slots
- inject a list of item hex IDs into inventory slots
- wipe a player's 40-slot inventory
- fill an entire player's inventory with a single item

## Requirements

Before using this project, you need:

- A Nintendo Switch running `sys-botbase`
- A Nintendo Switch connected to the same network as the host machine
- Animal Crossing: New Horizons running on the Switch
- Python 3 installed on the machine running the script

## Project structure

- `sysbot.py` — low-level wrapper for communicating with the Switch via `sys-botbase`
- `sysbot_acnh.py` — ACNH inventory offset logic and injector class
- `main.py` — interactive command-line interface and item batch definitions

## Usage

Run the CLI:

```bash
python main.py
```

The program will prompt for:

- The target Nintendo Switch IPv4 address
- The player index (1-8)
- Whether to inject the predefined item batch, preview the batch, or wipe inventory

## Example behavior

The default batch includes 40 predefined household and furniture item IDs. The script writes these values into the chosen player's inventory slots in sequence.

## Important notes

This project is highly version-specific (ACNH 3.0.3) and depends on exact ACNH memory layout assumptions. In particular:

- Memory addresses are hardcoded
- The tool assumes an ACNH version compatible with the offsets in the code
- A title ID check is used as a safety gate before writes are performed

Because it modifies live game memory, use it with care. Incorrect offsets or unintended writes can result in corrupted game state and broken inventory. Broken Inventory Slots are not fixable and any item dropped into a broken slot will disappear.

## Safety / legal considerations

This project modifies game memory and may affect save data or gameplay state. Use it responsibly and only in environments you own or control. This is not a general-purpose application and is intended for advanced technical experimentation.

## License

This project is distributed under the terms of the repository's license. See the `LICENSE` file for details.
