from pandas import DataFrame


class FileProgress:
    def __init__(self, size, drawer):
        self._drawer = drawer
        self._data = DataFrame(
            data={
                "byte_index": list(range(size)),
                "byte_status": ["u"] * size,
                "val": [1] * size,
            }
        )

    def draw(self):
        self._drawer(self._data)

    def mark_read(self, start, end):
        self._data.loc[start : end + 1, ["byte_status"]] = ["r"]

    def mark_unread(self, start, end):
        self._data.loc[start : end + 1, ["byte_status"]] = ["r"]
