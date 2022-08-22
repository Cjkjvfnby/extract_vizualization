from zipfile import ZipFile

from zip_cloud.call_tracer import CallTracer, CommandRegister
from zip_cloud.state import State


def extract_file(state: State):
    commands = CommandRegister()
    archive = CallTracer(state.archive, commands)
    commands.add_section("Open archive and read headers")

    with ZipFile(archive, "r") as zip_object:
        names = zip_object.namelist()
        for name in names:
            commands.add_section(f"Find file to read file {name}")
            with zip_object.open(name) as myfile:
                commands.add_section(f"Read file {name}")
                result = myfile.read()
            commands.add_section(f"File contents: {(result.decode())}")
    return commands
