import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from io import BytesIO
from zipfile import ZipFile

from zip_cloud.call_tracer import Call, CommandRegister
from zip_cloud.extractor import extract_file
from zip_cloud.file_creation_form import file_creation_form
from zip_cloud.file_progress import FileProgress
from zip_cloud.progress_drawer import Drawer
from zip_cloud.state import State

state = State()


def call_to_human(call: Call):
    if call.name == "seek":
        offset, *whence = call.args
        default_whence = 0
        whence = whence[0] if whence else default_whence

        if whence == 2:
            return f"Start seek from the end of the file with {offset=}, stop at position {call.result}"
        elif whence == 0:
            return f"Start seek from the start of the file with {offset=}, stop at position {call.result}"
    elif call.name == "tell":
        return f"Check current position in the file, its {call.result}"
    elif call.name == "read":
        if len(call.args) == 1:
            offset = call.args[0]
            return f"Read {offset} bytes, actual bytes read {len(call.result)}"
        elif len(call.args) == 0:
            return f"Read file from current position till the end, actual bytes read {len(call.result)}"
    elif call.name == "seekable":
        return ""

    return str(call)


def visualize_command_execurion(container, registry: CommandRegister):
    makrdown = []
    for section in registry:
        title, *items = section
        makrdown.append(f"- {title}")
        for item in items:
            human_readable = call_to_human(item)
            if human_readable:
                makrdown.append(f"  - {call_to_human(item)}")
    container.markdown("\n".join(makrdown))


def get_buttons(state, file_names):
    def button_callback():
        registry = extract_file(state)
        visualize_command_execurion(state.bar_container, registry)

    for name in file_names:
        state.actions_container.button(f"Extract {name}", on_click=button_callback)


def make_zip_file(state, slider_val):
    zipped = BytesIO()
    file_names = []
    with ZipFile(zipped, "w") as file_obj:
        for i in range(1, slider_val + 1):
            file_name = f"file_{i}.txt"
            file_content = str(i) * i
            state.bar_container.write(
                f"adding file file_{file_name}.txt with {file_content}"
            )
            file_obj.writestr(file_name, file_content)
            file_names.append(file_name)

    size = zipped.tell()
    fp = FileProgress(10, drawer=Drawer(state, size))
    fp.draw()
    state.file_progress = fp
    state.archive = zipped
    get_buttons(state, file_names)


file_creation_form(state, make_zip_file)
