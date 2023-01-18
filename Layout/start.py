import streamlit as st
import streamlit.components.v1 as components

def load_view():
    st.markdown(
    '''
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
        <div class="" style="margin-left: 100px; margin-right: 100px">
            <div class='d-flex justify-content-center'>
                <img src='../Logo.png' />
                <h3 style='font-size: 28px;font-weight: 700;color:#4154f1; text-transform: uppercase'>Web-Based Dataflow Framework for Visual Data Exploration</h1>
            </div>
            <div class='d-flex justify-content-center'>
                <button class='btn btn-secondary mx-1 btn-lg px-5'>two</button>
                <button class='btn btn-secondary mx-1 btn-lg px-5'>one</button>
                <button class='btn btn-secondary mx-1 btn-lg px-5'>three</button>
            </div>
            <h2 style='color: #444444;margin: 15px 0 0 0;font-size: 20px; text-align: center;'>
                VisFlow is a web-based dataflow framework for visual data exploration. It employs a subset dataflow that allows the user to interactively select, manipulate, brush and link data subsets across multiple visualizations. VisFlow is simple and intuitive to use and can help fast launch data analyses in a web browser. See the video below for a short overview of the system. Follow the tutorial to start your visualization and data exploration.
            </h2>
        </div>
    ''', unsafe_allow_html=True
    )
