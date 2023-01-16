import os
from shutil import rmtree
import streamlit as st
from PIL import Image
def main():
    try:
        rmtree('output')
        os.mkdir('./output')
        os.system('jupyter nbconvert --to html --output-dir=output --execute .\code\DataExtraction-*.ipynb')
        os.system('jupyter nbconvert --to html --output-dir=output --execute .\code\BuildDataset-Experimental.ipynb')
        os.system('jupyter nbconvert --to html --output-dir=output --execute .\code\BuildDataset-Training.ipynb')
        os.system('jupyter nbconvert --to html --output-dir=output --execute .\code\BuildDataset-Unknown.ipynb')
        os.system('jupyter nbconvert --to html --output-dir=output --execute .\code\ChartsForPaper-*.ipynb')
        image = Image.open('D:\hafiz sir project\ML-Apps\ML-Apps\output\chart-overall-data.png')
        st.image(image)
        image = Image.open('D:\hafiz sir project\ML-Apps\ML-Apps\output\chart-overall-RandomForestClassifier.png')
        st.image(image)
        image = Image.open('D:\hafiz sir project\ML-Apps\ML-Apps\output\chart-overall-RandomForestRegressor.png')
        st.image(image)
        image = Image.open('D:\hafiz sir project\ML-Apps\ML-Apps\output\chart-prediction-experimental.png')
        st.image(image)
        image = Image.open('D:\hafiz sir project\ML-Apps\ML-Apps\output\chart-prediction-unknown.png')
        st.image(image)
        st.success('Trained Successfully!')
    except:
        st.error('Can\'t train properly :(')
        pass
