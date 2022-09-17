from gzip import GzipFile
from typing import BinaryIO
from zipfile import ZipFile

from visualizer.call_tracer import CommandRegister, wrap_to_tracer


def extract_zip_file(zipped: BinaryIO, file_to_extract: list[str]) -> CommandRegister:
    zipped.seek(0)
    archive, commands = wrap_to_tracer(zipped)
    commands.add_section("Open archive and read headers")

    with ZipFile(archive, "r") as zip_object:
        for name in file_to_extract:
            commands.add_section(f"Read {name} header")
            with zip_object.open(name) as myfile:
                commands.add_section(f"Read {name} content")
                result = myfile.read()
            commands.add_section(f"{name} content: {(result.decode())}")
    return commands


def extract_gzip_file(archive: BinaryIO) -> CommandRegister:
    archive.seek(0)
    archive, commands = wrap_to_tracer(archive)
    commands.add_section("Open and read archive")
    with GzipFile(fileobj=archive) as stream:
        result = stream.read()
        commands.add_section(f"Content: {(result.decode())}")
    return commands
