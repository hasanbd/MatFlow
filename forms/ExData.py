import os
import pandas as pd
import streamlit as st
from modules import utils
from modules.graph import barplot, pieplot, countplot, histogram, boxplot, violinplot, scatterplot, regplot, lineplot
#from modules.profile import pf, sweetviz

def main():
    try:
        dataset = st.session_state["dataset"]
        default_idx = st.session_state["default_dataset_idx"]
        data_opt = utils.dataset_opt(dataset.list_name(), default_idx)
        data = dataset.get_data(data_opt)
    except KeyError:
        st.markdown("<h5 style='text-align: left; color: black;'>❗✅ Select a Dataset❓</h5>",
                    unsafe_allow_html=True)
        st.stop()
    except Exception as e:
        st.write(e)
        st.stop()
    menus = ["Bar Plot", "Pie Plot", "Scatter Plot", "Line Plot"]
    tabs = [tab for tab in st.tabs(menus)]

    with tabs[0]:
            barplot.barplot(data)

    with tabs[1]:
            pieplot.pieplot(data)

    with tabs[2]:
            scatterplot.scatterplot(data)

    with tabs[3]:
            lineplot.lineplot(data)

