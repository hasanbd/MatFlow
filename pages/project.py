import streamlit as st
from forms import dl

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

dl.main()

