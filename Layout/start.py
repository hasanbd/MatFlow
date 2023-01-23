import streamlit as st
import streamlit.components.v1 as components
from mp import MP

ml = MP()


def load_view():
    img1, img2, img3 = st.columns((4,25,1))
    with img2:
        st.image(
            'https://i.ibb.co/SmxY6J9/banner.png')

    tit1, tit2 = st.columns((1,20))
    with tit2:
        st.markdown(
            '''
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
            <div class="" style="margin-left: 100px; margin-right: 100px">
                <div class='d-flex justify-content-center'>
                    <h2 style='font-size: 35px;font-weight: 100%; color:purple; text-transform: uppercase; text-align: center';>
                    A Machine Learning Based Data Analysis and Exploration System For Material Design</h2>
                </div>
        ''', unsafe_allow_html=True
        )
    st.markdown("""
             <div>
             <hr style="height:20px;border:none; background-color:#fbffe3;" /> 
             <div
               class="des-title" style='text-align: justify; font-weight: bold; background-color: #fbffe3; color: #0aa0c2; 
               font-family: Tahoma, Verdana, sans-serif; font-size: 20px;'>
               MatFlow is a web-based dataflow framework for visual data exploration. It employs a 
               subset dataflow that allows the user to interactively select, manipulate, brush and 
               link data subsets across multiple visualizations. VisFlow is simple and intuitive to 
               use and can help fast launch data analyses in a web browser. See the video below for 
               a short overview of the system. Follow the tutorial to start your visualization and data
               exploration.
             </div>    
             <br>
             <h3 class="title" style='text-align: center; text-decoration: overline underline; background-color:#fbffe3; 
             font-family: "Lucida Console", "Courier New", monospace; font-weight: bold; color:purple'>
                How to do it?</h3>
             </div>   
             <br>
                """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    local_css("style.css")

    with col3:
        started = st.button("Started")
        if (started):
            st.write("I am going to start the apps")
    with col5:
        gitHub = st.button("Git Hub")
        if (gitHub):
            st.write("I am going to start github link")
    with col7:
        demo = st.button("Demo")
        if (demo):
             st.video('https://youtu.be/hxPbnFc7iU8')
    vid1, vid2,vid3 = st.columns(3)
    with vid2:
        st.video('https://youtu.be/hxPbnFc7iU8')

    st.markdown(
        '''
        </div>
        <h4 style='font-size: 25px; text-align:center; font-weight: 700;margin: 0 0 20px 0;color: #599bb3; background-color: purple'>References</h4>
        <p>
            <span style='font-size: 20px;font-weight:Bold; color: #012970;'>Austin Biaggne, Lawrence Spear, German Barcenas, Maia Ketteridge, Young C.Kim, Joseph S.Melinger, Willia B.Knowlton, Bernard Yurke, and Lan Li - </span>
            <span style='font-size: 15px; font-weight:Bold; color: #012970; font-style: italic;'>Data-Driven and Multiscale Modeling of DNA-Templated Dye</span>   
        </p>
        <p>
            <span style='font-size: 20px;font-weight:Bold; color: #012970;'>Hasan M Jamil, Lan Li -</span>
            <span style='font-size: 15px; font-weight:Bold; color: #012970; font-style: italic;'>A Knowledgebased Novel Materials Design System using Machine Learning</span>
        </p>
        </div>
        ''', unsafe_allow_html=True
       )
