from dataclasses import dataclass


@dataclass(frozen=True)
class Blob:
    data: bytes

    def serialize(self) -> bytes:
        header = f"blob {len(self.data)}\0".encode("ascii")
        return header + self.data