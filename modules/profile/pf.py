import os
import streamlit as st
import pandas as pd
import codecs
from pandas_profiling import ProfileReport
import streamlit.components.v1 as components
from streamlit_pandas_profiling import st_profile_report
import sweetviz as sv
# from modules.classes import data


def pandasProfile(data):
    st.markdown("<h5 style='text-align: center; color: black;'>🔅Automated EDA with Pandas Profiling🔅</h5>",
                unsafe_allow_html=True)
    st.dataframe(data.head())
    profile = ProfileReport(data)
    st_profile_report(profile)
