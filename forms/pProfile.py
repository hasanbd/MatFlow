import os
import streamlit as st
from modules import utils
from modules.profile import pf, sweetviz


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
        st.warning(e)
        st.stop()

    menus = ["Pandas Profiling"]
    tabs = [tab for tab in st.tabs(menus)]

    with tabs[0]:
        pf.pandasProfile(data)

    #with tabs[1]:
    #    sweetviz.sweetvizReport("SWEETVIZ_REPORT.html")

