import streamlit as st

st.title("Visualize archive extraction")


st.markdown(
    """
| Archive  | Number of files  | Read type     |  Visualization  | Documentation link    |
| :---     | ---              |---            |  ---            | ---                   |
| **zip**  | many             | random access | [try it](/zip)  | [wiki/ZIP][zip_doc]   |
| **gzip** | 1                | stream        | [try it](/gzip) | [wiki/Gzip][gzip_doc] |


[zip_doc]: https://en.wikipedia.org/wiki/ZIP_(file_format)
[gzip_doc]: https://en.wikipedia.org/wiki/Gzip

""",
)
