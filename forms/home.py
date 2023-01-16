
import streamlit as st
from . import dl

def load_view():
    st.markdown("""
        <h3 class="title" style='text-align: center; background-color: lightblue; font-family: "Lucida Console", "Courier New", monospace;'>
        Data Analysis for Prediction</h3>
        <br>

        <div 
        class="des-title" style='text-align: justify; background-color: #FFFACD; color: black; font-family: Tahoma, Verdana, sans-serif;'>
        This application analyses data to identify patterns in given set of instances in a data. While identifying patterns in each data instance of a data, the application is getting trained by 
        learning relation between set of features and the output value to be determined for each data instance. Training the 
        application to learn the relation between set of features and the output value for each data instance helps to predict
        output for unseen data instance. The unseen data instance whose output value needs to be predicted should have similar
        similar set of features as the earlier data instances used to train the application.

        </div>
        <br>
        <h4 class="title" style='text-align: center; background-color: lightblue; font-family: "Lucida Console", "Courier New", monospace;'>
        How to do it?</h4>
        <br><br>
        """, unsafe_allow_html=True)
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    local_css("style.css")

    col1, col2, col3= st.columns([1,1,1])
    upload_data = col1.button("💾Choose an Algorithm")
    if upload_data:
        dl.main()
    # bt=col2.button('☄️run epsilon')
    # if(bt):
    #
    #
    #
    #         # os.system('jupyter nbconvert --to html --output-dir=output --execute .\code\DataExtraction-*.ipynb')
    #         # os.system('jupyter nbconvert --to html --output-dir=output --execute .\code\BuildDataset-Experimental.ipynb')
    #         # os.system('jupyter nbconvert --to html --output-dir=output --execute .\code\BuildDataset-Training.ipynb')
    #         # os.system('jupyter nbconvert --to html --output-dir=output --execute .\code\BuildDataset-Unknown.ipynb')
    #         # os.system('jupyter nbconvert --to html --output-dir=output --execute .\code\ChartsForPaper-*.ipynb')
    #         st.success('Trained Successfully!')
    #     except:
    #         st.error('Can\'t train :(')
    #         pass
    train = col2.button("⚙️Training Data")
    result = col3.button("💡Result")
