import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.markdown('''
<style>
.css-163ttbj {
    position: relative;
    top: 2px;
    background-color: rgb(240, 242, 246);
    z-index: 999991;
    min-width: 264px;
    max-width: 269px;
    orm: none;
    display:none;
    transition: transform 300ms ease 0s, min-width 300ms ease 0s, max-width 300ms ease 0s;
}
</style>
''',unsafe_allow_html=True)
st.session_state.file=st.file_uploader('hello')
st.write('What you want to do?')
col1,col2=st.columns(2)
with col1:
    project = st.button('project')
    if project:
        switch_page('project')
with col2:
    file = st.button('File')
    if file:
        switch_page('project')
