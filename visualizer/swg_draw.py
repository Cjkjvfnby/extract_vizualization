from enum import Enum, auto
from typing import NamedTuple

import drawSvg


class DrawType(Enum):
    SECTION = auto()
    POINTER = auto()
    TEXT_ONLY = auto()


class Command(NamedTuple):
    start: int
    end: int
    draw: DrawType
    text: str


class Plotter:
    def __init__(self, file_bytes: int, size: int):
        self._file_bytes = file_bytes
        self._size = size
        self._height = 10

    def make_read(self, start: int, end: int) -> str:
        border = 1
        bg_width = self._file_bytes + 2 * border
        bg_height = self._height + 2 * border
        widht = self._file_bytes
        height = self._height

        d = drawSvg.Drawing(bg_width, bg_height, displayInline=False)

        background = drawSvg.Rectangle(0, 0, bg_width, bg_height, fill="gray")
        file_block = drawSvg.Rectangle(border, border, widht, height, fill="white")
        read_block = drawSvg.Rectangle(
            start + border, border, end - start, height, fill="green"
        )

        d.extend([background, file_block, read_block])

        scale = int(self._file_bytes / self._size)
        d = d.setPixelScale(scale)
        return d.asSvg()

    def make_seek(self, start: int, end: int) -> str:
        border = 1
        bg_width = self._file_bytes + 2 * border
        bg_height = self._height + 2 * border
        widht = self._file_bytes
        height = self._height

        d = drawSvg.Drawing(bg_width, bg_height, displayInline=False)

        background = drawSvg.Rectangle(0, 0, bg_width, bg_height, fill="gray")
        file_block = drawSvg.Rectangle(border, border, widht, height, fill="white")
        start_seek = drawSvg.Rectangle(start + border, border, 1, height, fill="green")
        end_seek = drawSvg.Rectangle(end + border, border, 1, height, fill="green")
        d.extend([background, file_block, start, start_seek, end_seek])

        scale = int(self._file_bytes / self._size)
        d = d.setPixelScale(scale)
        return d.asSvg()
