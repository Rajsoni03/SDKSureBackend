"""Checksum helpers."""


def crc16(data: bytes) -> int:
    return sum(data) % 0xFFFF

