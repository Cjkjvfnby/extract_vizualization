from typing import BinaryIO
from zipfile import ZipFile

from visualizer.call_tracer import CallTracer, CommandRegister


def extract_file(zipped: BinaryIO, file_to_extract: list[str]) -> CommandRegister:
    commands = CommandRegister()
    zipped.seek(0)
    archive = CallTracer(zipped, commands)
    commands.add_section("Open archive and read headers")

    with ZipFile(archive, "r") as zip_object:
        for name in file_to_extract:
            commands.add_section(f"Read {name} header")
            with zip_object.open(name) as myfile:
                commands.add_section(f"Read {name} content")
                result = myfile.read()
            commands.add_section(f"{name} content: {(result.decode())}")
    return commands
