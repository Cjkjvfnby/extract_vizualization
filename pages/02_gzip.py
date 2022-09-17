from typing import Any, BinaryIO, Callable

from visualizer.base_extractor import ExtractBase
from visualizer.call_tracer import CommandRegister
from visualizer.create_archive import make_gzip
from visualizer.extract_archive import extract_gzip_file


class ExtractGzip(ExtractBase):
    def make_archive(self, filenames: list[str]) -> tuple[BinaryIO, int]:
        return make_gzip()

    def get_file_names(self) -> list[str]:
        """
        Return list of files to pack into archive.
        """
        return ["file.txt"]

    def extract_archive(self, files: list[str]) -> CommandRegister:
        """
        Extract archive and return list of commands.
        """
        return extract_gzip_file(self._archive)

    def get_title(self) -> str:
        return """
            # Case: Extract a file from GZip archive

            This format contains a single file and could be read as a stream.
            """

    def make_extraction_form(
        self,
        container: Any,
        file_names: list[str],
        callback: Callable[[list[str]], None],
    ) -> None:
        form = container.form("Extraction")
        submitted = form.form_submit_button("Extract")
        if submitted:
            callback([])


ExtractGzip().draw()
