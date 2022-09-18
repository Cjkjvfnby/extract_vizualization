from typing import Any, Callable, Sequence

from visualizer.base_extractor import ExtractBase
from visualizer.call_tracer import CommandRegister
from visualizer.create_archive import make_zip
from visualizer.extract_archive import extract_zip_file


class ExtractZip(ExtractBase):
    def __init__(self):
        super().__init__()

    def get_create_archive_func_and_args(self) -> tuple[Callable, tuple]:
        return make_zip, (self.get_file_names(),)

    def get_file_names(self) -> Sequence[str]:
        """
        Return list of files to pack into archive.
        """
        return "file1.txt", "file2.txt", "file3.txt"

    def extract_archive(self, files: list[str]) -> CommandRegister:
        return extract_zip_file(self._archive, files)

    def get_title(self) -> str:
        return """
            # Case: Extract specific or all files from the Zip archive

            With a couple of reads you could extract only data you need.

            This require a random access to the archive file, which is supported by
            many web storages.

            The archive has 3 files with dummy text.
            Choose files to see what operation are done on archive to read the data.
            """

    def make_extraction_form(
        self,
        container: Any,
        callback: Callable[[list[str]], None],
    ) -> None:
        file_names = self.get_file_names()
        form = container.form("extraction select")
        form.write("Select files to extract")
        checkboxes = []
        for name in file_names:
            checkboxes.append(form.checkbox(name))
        submitted = form.form_submit_button("Extract")
        if submitted:
            files = [file_names[i] for i, val in enumerate(checkboxes) if val]
            callback(files)


ExtractZip().draw()
