import streamlit as st

st.title("Visualize archive extraction")


ZIP_TEXT = "[wiki/ZIP](https://en.wikipedia.org/wiki/ZIP_(file_format))"
GZIP_TEXT = "[wiki/Gzip](https://en.wikipedia.org/wiki/Gzip)"


st.markdown(
    f"""
| Archive | Number of files  | Read type  |  Visualization | Documents link |
| :---    | ---              |---         |  ---           | --- |
| **zip**  | many | random access | [try it](/zip) | {ZIP_TEXT} |
| **gzip** | 1    | stream        | [try it](/gzip) | {GZIP_TEXT} |
"""
)
