import streamlit as st
from modules.classes import data
from modules.dataset import read, display, split, download


def main():
    try:
        dataset = st.session_state["dataset"]
        default_idx = st.session_state["default_dataset_idx"]

    except:
        st.session_state["dataset"] = data.Dataset()
        dataset = st.session_state["dataset"]

        st.session_state["default_dataset_idx"] = 0
        default_idx = st.session_state["default_dataset_idx"]

    #menus = ["Dataset List", "Read Dataset", "Split Dataset", "Download Dataset"]
    menus = ["📤Dataset", "🧮Split Dataset"]
    tabs = st.tabs(menus)
    try:
        with tabs[0]:
            read.read_dataset(dataset)
    except:
        pass
    # with tabs[1]:
    #     split.split_dataset(dataset)

    #with tabs[3]:
    #    download.download(dataset)
