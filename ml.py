import numpy as np
import streamlit as st
from PIL import Image

from forms import dl, intelli, du, dv, evaluation, ExData, DFrame, FEngineering, pProfile, home
from Layout  import layout, contact
from mp import MP




# create page title
st.set_page_config(
    layout="wide",
    page_title="MatFlow: Materials Design System",
    page_icon="👨‍💻",
)




ml = MP()
# display = Image.open('banner.png')
# display = np.array(display)
# st.image(display)


# Navbar
# layout.navbar()
ml.ly()

# Remove Streamlit footer note and repository notes
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add all my application pages here
# home.load_view()
# contact.form()
