import streamlit as st

st.title("Visualize archive extraction")


zip_text = "[wiki/ZIP](https://en.wikipedia.org/wiki/ZIP_(file_format))"
gzip_text = "[wiki/Gzip](https://en.wikipedia.org/wiki/Gzip)"


st.markdown(
    f"""
| Archive | Number of files  | Read type  |  Visualization | Documents link |
| :---    | ---              |---         |  ---           | --- |
| **zip**  | many | random access | [try it](/zip) | {zip_text} |
| **gzip** | 1    | stream        | [try it](/gzip) | {gzip_text} |
"""
)
