import streamlit as st
def select():
    st.write('What you want to do?')
    col1,col2=st.columns(2)
    with col1:
        st.button('Project')
    with col2:
        st.button('File')