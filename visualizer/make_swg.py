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


class SwgMaker:
    def __init__(self, file_bytes: int):
        self._file_bytes = file_bytes
        self._height = 10
        self._border = 1

    def _make_swg(self) -> drawSvg.Drawing:
        border = self._border
        bg_width = self._file_bytes + 2 * border
        bg_height = self._height + 2 * border
        widht = self._file_bytes

        d = drawSvg.Drawing(bg_width, bg_height, displayInline=False)
        background = drawSvg.Rectangle(0, 0, bg_width, bg_height, fill="gray")
        file_block = drawSvg.Rectangle(
            border, border, widht, self._height, fill="white"
        )
        d.extend([background, file_block])
        return d

    def to_swg(self, d: drawSvg.Drawing) -> str:
        return d.asSvg()

    def make_read(self, start: int, end: int) -> str:
        border = self._border
        d = self._make_swg()
        read_block = drawSvg.Rectangle(
            start + border, border, end - start, self._height, fill="green"
        )
        d.append(read_block)
        return self.to_swg(d)

    def make_seek(self, start: int, end: int) -> str:
        border = self._border
        d = self._make_swg()
        start_seek = drawSvg.Rectangle(
            start + border, border, 1, self._height, fill="green"
        )
        end_seek = drawSvg.Rectangle(
            end + border, border, 1, self._height, fill="green"
        )
        d.extend([start, start_seek, end_seek])
        return self.to_swg(d)
