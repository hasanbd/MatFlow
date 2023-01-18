"""
Purpose:connect manager for page to page link
"""
import streamlit as st
import selectpage as sp

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
        col1,col2=st.columns([1.5,1])
        with col2:
           next= st.button('next page')
        if next:
            sp.select()
        # st.write('hello')
        # st.write('What you want to do?')
        pass
        #
        # # st.sidebar.image('Logo.png')
        # page = st.sidebar.selectbox(
        #     '💎 System Navigation here⤵️::💎',
        #     self.forms,
        #     format_func=lambda form: form['title']
        # )
        # page['function']()

