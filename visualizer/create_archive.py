import io
from zipfile import ZipFile


def make_zip(file_names: list[str]) -> tuple[io.BytesIO, int]:
    file = io.BytesIO()

    with ZipFile(file, "w") as zip_obj:
        for filename in file_names:
            zip_obj.writestr(filename, "test")

    return file, file.tell()
