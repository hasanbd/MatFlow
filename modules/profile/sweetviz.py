import os
import streamlit as st
import pandas as pd
import codecs
from pandas_profiling import ProfileReport
import streamlit.components.v1 as components
from streamlit_pandas_profiling import st_profile_report
import sweetviz as sv


def sweetviz(report_html, width=1000, height=500):
    st.markdown("<h5 style='text-align: center; color: black;'>🔅Sweetviz Report🔅</h5>",
                unsafe_allow_html=True)
    if 'iris.csv' not in os.listdir('data'):
        st.markdown("Please upload data through `Upload Data` page!")
    else:
        data = pd.read_csv('data/iris.csv')
        st.dataframe(data.head())
    report_file = codecs.open(report_html, 'r')
    page = report_file.read()
    components.html(page, width=width, height=height, scrolling=True)

    report = sv.analyze(data)
    report.show_html()
    #st_display_sweetviz("SWEETVIZ_REPORT.html")

