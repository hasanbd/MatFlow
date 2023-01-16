import numpy as np
import streamlit as st
from PIL import Image

from forms import dl, intelli, du, dv, evaluation, ExData, DFrame, FEngineering, pProfile, home
import hydralit_components as hc
from Layout import layout, contact
from mp import MP




#make it look nice from the start
st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

# specify the primary menu definition
menu_data = [
    {'icon': "far fa-copy", 'label':"Contact"},
    {'id':'Copy','icon':"🐙",'label':"About"},
    
    
]

over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme = over_theme
    # {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
,
    home_name='Home',
    login_name='Logout',
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

if(menu_id == "Home"):
    home.load_view()
if(menu_id == "Contact"):
    contact.form()