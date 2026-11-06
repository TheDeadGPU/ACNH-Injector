"""Minimal sys-botbase client with a namespaced API: bot.Ram.peek(...), bot.Controls.click(...)."""
import socket


class SysBot:
    def __init__(self, ip: str, port: int = 6000, timeout: float = 5.0):
        self._sock = socket.create_connection((ip, port), timeout=timeout)
        self._buf = b""
        # Sub-APIs: each gets a reference back to this connection.
        self.Ram = Ram(self)
        self.Controls = Controls(self)
        self.Utility = Utility(self)

    # ---- low-level transport (shared by every sub-API) ----
    def _send(self, command: str) -> None:
        self._sock.sendall((command + "\r\n").encode("ascii"))

    def _query(self, command: str) -> str:
        """Send a command and read one newline-terminated reply."""
        self._send(command)
        while b"\n" not in self._buf:
            chunk = self._sock.recv(4096)
            if not chunk:
                raise ConnectionError("Switch closed the connection")
            self._buf += chunk
        line, _, self._buf = self._buf.partition(b"\n")
        return line.decode("ascii").strip()

    def close(self) -> None:
        self._sock.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


class _Section:
    def __init__(self, bot: SysBot):
        self._bot = bot


class Ram(_Section):
    # ---- reads (return bytes) ----
    def peek(self, heap_offset: int, size: int) -> bytes:
        return bytes.fromhex(self._bot._query(f"peek {heap_offset:#x} {size}"))

    def peek_absolute(self, address: int, size: int) -> bytes:
        return bytes.fromhex(self._bot._query(f"peekAbsolute {address:#x} {size}"))

    def peek_main(self, nso_offset: int, size: int) -> bytes:
        return bytes.fromhex(self._bot._query(f"peekMain {nso_offset:#x} {size}"))

    def pointer_peek(self, size: int, *offsets: int) -> bytes:
        chain = " ".join(f"{o:#x}" for o in offsets)
        return bytes.fromhex(self._bot._query(f"pointerPeek {size} {chain}"))

    # ---- writes (take bytes; the Switch sends no reply) ----
    def poke(self, heap_offset: int, data: bytes) -> None:
        self._bot._send(f"poke {heap_offset:#x} 0x{data.hex()}")

    def poke_absolute(self, address: int, data: bytes) -> None:
        self._bot._send(f"pokeAbsolute {address:#x} 0x{data.hex()}")

    def poke_main(self, nso_offset: int, data: bytes) -> None:
        self._bot._send(f"pokeMain {nso_offset:#x} 0x{data.hex()}")

    def pointer_poke(self, data: bytes, *offsets: int) -> None:
        chain = " ".join(f"{o:#x}" for o in offsets)
        self._bot._send(f"pointerPoke 0x{data.hex()} {chain}")

    # ---- freezing ----
    def freeze(self, address: int, data: bytes) -> None:
        self._bot._send(f"freeze {address:#x} 0x{data.hex()}")

    def unfreeze(self, address: int) -> None:
        self._bot._send(f"unFreeze {address:#x}")

    def freeze_clear(self) -> None:
        self._bot._send("freezeClear")


class Controls(_Section):
    def click(self, button: str) -> None:
        self._bot._send(f"click {button}")

    def press(self, button: str) -> None:
        self._bot._send(f"press {button}")

    def release(self, button: str) -> None:
        self._bot._send(f"release {button}")

    def set_stick(self, side: str, x: int, y: int) -> None:
        self._bot._send(f"setStick {side.upper()} {x:#x} {y:#x}")


class Utility(_Section):
    def heap_base(self) -> int:
        return int(self._bot._query("getHeapBase"), 16)

    def main_nso_base(self) -> int:
        return int(self._bot._query("getMainNsoBase"), 16)

    def title_id(self) -> str:
        return self._bot._query("getTitleID")