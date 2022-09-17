import streamlit as st

st.title("Visualize archive extraction")


zip_text = "[zip](https://en.wikipedia.org/wiki/ZIP_(file_format))"
gzip_text = "[gzip](https://en.wikipedia.org/wiki/Gzip)"


st.markdown(
    f"""
| Archive | Number of files  | Read type  |  Visualization
| :---    | ---              |---         |  ---
| **{zip_text}**  | many | random access | [extract zip](/zip)
| **{gzip_text}** | 1    | stream        | [extract gzip](/gzip)
"""
)
