import numpy as np
import streamlit as st
from PIL import Image

#from forms import dl, intelli, du, dv, evaluation, ExData, DFrame, FEngineering, pProfile
from forms import dl, DFrame, FEngineering, ExData, pProfile, machine_learning, ModelBuild, home,epsilon
from mp import MP

# create page title
st.set_page_config(
    layout="wide",
    page_title="MatFlow: Materials Design System",
    page_icon="👨‍💻",
)
st.markdown("""
<h3 class="title" style='text-align: center; background-color: lightblue; font-family: "Lucida Console", "Courier New", monospace;'>
        Knowledgebased Materials Design System Using Machine Learning</h3>
""", unsafe_allow_html=True)
# instance of our system
ml = MP()
display = Image.open('banner.png')
display = np.array(display)
st.image(display)

hide_streamlit_style = """ 
 <style>
     #MainMenu {visibility:hidden}
     footer{visibility:hidden}
    </style>
"""
st.markdown('''
<style>
.css-163ttbj {
    position: relative;
    top: 2px;
    background-color: rgb(240, 242, 246);
    z-index: 999991;
    min-width: 264px;
    max-width: 269px;
    orm: none;
    transition: transform 300ms ease 0s, min-width 300ms ease 0s, max-width 300ms ease 0s;
}
</style>
''',unsafe_allow_html=True)
# Remove Streamlit footer note and repository notes
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#
# # Add all my application pages here
ml.connect("Start", home.load_view)
ml.connect("🗃️Upload Dataset", dl.main)
ml.connect("⚙️Training", ModelBuild.main)
ml.connect("💡 Best Fit", machine_learning.main)
#ml.connect("✅ Change Metadata", du.main)
ml.connect("🖥 Statistical Data", DFrame.main)
ml.connect("📉 Exploratory Data Analysis", ExData.main)
ml.connect("⚙️ Feature Engineering", FEngineering.main)
#ml.connect("📊 Data Analysis", dv.main)
#ml.connect("📉 Optimization and Evaluation", evaluation.main)

ml.connect("👩🏻‍💻Pandas Auto Profiling", pProfile.main)
# The main app
ml.start()
