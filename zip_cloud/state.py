import streamlit as st


class State:
    def __init__(self):
        self.form_container = st.container()
        self.bar_container = st.container()
        self.actions_container = st.container()
        self.archive = None
        self.file_progress = None
