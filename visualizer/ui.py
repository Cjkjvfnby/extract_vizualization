from typing import Any

import streamlit as st

from visualizer.create_archive import make_zip
from visualizer.extract_archive import extract_file
from visualizer.table_creator import create_table


class UI:
    def __init__(self):
        st.set_page_config(layout="wide")

        self._file_names = ["file1.txt", "file2.txt", "file3.txt"]
        self._archive, self._size = make_zip(self._file_names)

        self._screen_size = 1000

    def draw(self) -> None:
        left, right = st.columns(2)
        self._draw_extraction_form(right)
        left.markdown(
            """
        # Case: Extract only thing you need

        With a couple of reads you could extract all only data you need.
        This require a random access to files.
        Many web storages allow you to do it as well.

        We have archive with 3 files with dummy text.
        Choose files to see what operation are done on archive to read the data.
        """
        )

    def draw_extraction_process(self, files: list[str]) -> None:
        commands = extract_file(self._archive, files)
        st.container().markdown(
            create_table(self._size, commands), unsafe_allow_html=True
        )

    def _draw_extraction_form(self, container: Any) -> None:
        form = container.form("extraction select")
        form.write("Select files to extract")
        checkboxes = []
        for name in self._file_names:
            checkboxes.append(form.checkbox(name))
        submitted = form.form_submit_button("Extract")
        if submitted:
            files = [self._file_names[i] for i, val in enumerate(checkboxes) if val]
            self.draw_extraction_process(files)
