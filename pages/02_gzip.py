from typing import Any, Callable

from visualizer.base_extractor import ExtractBase
from visualizer.call_tracer import CommandRegister
from visualizer.create_archive import make_gzip
from visualizer.extract_archive import extract_gzip_file


class ExtractGzip(ExtractBase):
    def get_create_archive_func_and_args(self) -> tuple[Callable, tuple]:
        return make_gzip, ()

    def extract_archive(self, _: list[str]) -> CommandRegister:
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
        callback: Callable[[list[str]], None],
    ) -> None:
        form = container.form("Extraction")
        submitted = form.form_submit_button("Extract")
        if submitted:
            callback([])


ExtractGzip().draw()
