import streamlit as st


def file_creation_form(state, callback):
    with state.form_container.form("zip_file"):
        slider_val = st.slider("Number of files", min_value=1, max_value=9, value=1)

        submitted = st.form_submit_button("Submit")
        if submitted:
            callback(state, slider_val)
