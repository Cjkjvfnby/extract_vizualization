from __future__ import annotations

import base64
import io
from typing import TYPE_CHECKING

from visualizer.make_swg import SwgMaker

if TYPE_CHECKING:
    from collections.abc import Iterator

    from visualizer.call_tracer import Call, CommandRegister


class _TableBuilder:
    def __init__(self, size: int):
        self._size = size
        self._result = []
        self._plotter = SwgMaker(size)
        self._columns = "Operation", "Process", "Description"

    def add_call(self, call: Call) -> None:
        if call.name == "seek":
            self._handle_seek(call)
        elif call.name == "read":
            self._handle_read(call)

    def _to_img(self, swg: str) -> str:
        data_base64 = base64.b64encode(swg.encode())  # encode to base64 (bytes)
        data_base64 = data_base64.decode()  # convert bytes to string
        return f'<img src="data:image/svg+xml;base64,{data_base64}">'

    def add_text(self, text: str) -> None:
        self._result.append([text])

    def _add_read(
        self,
        call_args: tuple,
        start_offset: int,
        end_offset: int,
        text: str,
    ) -> None:
        args = ", ".join(map(str, call_args))
        self._result.append(
            [
                f"read({args})",
                self._to_img(self._plotter.make_read(start_offset, end_offset)),
                text,
            ],
        )

    def _add_seek(
        self,
        call_args: tuple,
        start_offset: int,
        end_offset: int,
        text: str,
    ) -> None:
        if len(call_args) == 1:
            args = str(call_args[0])
        else:
            offset, whence = call_args

            whence_names = ["io.SEEK_SET", "io.SEEK_CUR", "io.SEEK_END"]

            args = f"{offset}, {whence_names[whence]}"

        self._result.append(
            [
                f"seek({args})",
                self._to_img(self._plotter.make_seek(start_offset, end_offset)),
                text,
            ],
        )

    def _handle_seek(self, call: Call) -> None:
        offset, *whence = call.args
        default_whence = 0
        whence = whence[0] if whence else default_whence
        if whence == io.SEEK_END:
            self._add_seek(
                call.args,
                -1,
                call.end_offset,
                f"Seek from the end of the file with {offset=} and stop at the position {call.result}",
            )
        elif whence == io.SEEK_SET:
            self._add_seek(
                call.args,
                call.start_offset,
                call.end_offset,
                f"Seek from the start of the file with {offset=} and stop at the position {call.result}",
            )

    def _handle_read(self, call: Call) -> None:
        if len(call.args) == 1:
            read_bytes = call.args[0]
            self._add_read(
                call.args,
                call.start_offset,
                call.end_offset,
                f"Read {read_bytes} bytes, actual bytes read {len(call.result)}",
            )
        elif len(call.args) == 0:
            self._add_read(
                call.args,
                call.start_offset,
                call.end_offset,
                f"Read from the current position till the end, actual bytes read {len(call.result)}",
            )

    def _build_header(self) -> Iterator[str]:
        yield '<table border="1">'
        yield "<thead>"
        yield "<tr>"
        yield from [f'<th style="text-align: center; ">{c}</th>' for c in self._columns]
        yield "</tr>"
        yield "</thead>"

    def _build_row(self, row: tuple[str] | tuple[str, str, str]) -> Iterator[str]:
        yield "<tr>"
        if len(row) == 1:
            yield f'<td style="text-align: center;" colspan=3><strong>{row[0]}</strong></td>'
        else:
            for col in row:
                yield f"<td>{col}</td>"
        yield "</tr>"

    def build(self) -> Iterator[str]:
        yield from self._build_header()
        yield "<tbody>"
        for row in self._result:
            yield from self._build_row(row)
        yield "</tbody>"
        yield "</table>"


def create_table(size: int, registry: CommandRegister) -> str:
    builder = _TableBuilder(size)

    for section in registry:
        title, *items = section
        builder.add_text(title)
        for call in items:
            builder.add_call(call)
    return "\n".join(builder.build())
