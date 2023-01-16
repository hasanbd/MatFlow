"""
Purpose:connect manager for page to page link
"""
import streamlit as st
from Layout  import layout

class MP:

    # @st.cache()
    def __init__(self) -> None:
        self.forms = []

    def connect(self, title, func) -> None:
        self.forms.append(
            {
                "title": title,
                "function": func
            }
        )

    def start(self):
        # st.write('What you want to do?')
        # pass

        # st.sidebar.image('Logo.png')
        page = st.sidebar.selectbox(
            '💎 System Navigation here⤵️::💎',
            self.forms,
            format_func=lambda form: form['title']
        )
        page['function']()
    def ly(self):
        layout.navbar()

