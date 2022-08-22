import drawSvg as draw
import pandas as pd


class Drawer:
    def __init__(self, state, size) -> None:
        self._size = size
        self._screen_width = 1024
        self._state = state

    def __call__(self, df):

        d = draw.Drawing(self._size, 1, displayInline=False)
        r = draw.Rectangle(0, 0, self._size, 1, fill="red")
        r.appendTitle("Our first rectangle")  # Add a tooltip
        d.append(r)

        for start, end in self._get_section(df):
            r = draw.Rectangle(start, 0, end, 1, fill="green")
            d.append(r)
        scale = int(self._screen_width / self._size)
        d = d.setPixelScale(scale)

        self._state.bar_container.write(d)  # Display as SVG

    def _get_section(self, df: pd.DataFrame):
        in_read = False
        read_start = None

        for raw in df.iterrows():
            _, (byte_index, byte_status, val) = raw

            if in_read:
                if byte_status == "r":
                    continue
                else:
                    yield read_start, byte_index - 1
                    in_read = False
            else:
                if byte_status == "r":
                    read_start = byte_index
                    in_read = True
