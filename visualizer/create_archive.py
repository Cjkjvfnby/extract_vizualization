import gzip
import io
from typing import BinaryIO
from zipfile import ZipFile


def make_zip(file_names: list[str]) -> tuple[BinaryIO, int]:
    file = io.BytesIO()

    with ZipFile(file, "w") as zip_obj:
        for filename in file_names:
            zip_obj.writestr(filename, "test")

    return file, file.tell()


def make_gzip() -> tuple[BinaryIO, int]:
    file = io.BytesIO()
    content = b"test"
    with gzip.open(file, mode="wb") as f:
        f.write(content)

    return file, file.tell()
