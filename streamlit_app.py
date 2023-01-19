import numpy as np
import streamlit as st
from PIL import Image

#from forms import dl, intelli, du, dv, evaluation, ExData, DFrame, FEngineering, pProfile
from forms import dl, DFrame, FEngineering, ExData, pProfile, machine_learning, ModelBuild, home,epsilon,dv
import hydralit_components as hc
from Layout import contact, help, about, footer, start
from mp import MP

ml = MP()


#make it look nice from the start
st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

# specify the primary menu definition
menu_data = [
    {'id': 'Home', 'icon': 'fa-home', 'label': "Home"},
    {'id':'Contact','icon': "far fa-copy", 'label':"Contact"},
    {'id':'About','icon':"🐙",'label':"About"},
    
    
]

over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme = {'bgcolor': 'green','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
,
    home_name=None,
    login_name=None,
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

if(menu_id == "Home"):
    start.load_view()
    ml.start()
    footer.load_view()
if(menu_id == "About"):
    about.load_view()
    footer.load_view()
if(menu_id == "Contact"):
    contact.form()
    footer.load_view()
if(menu_id == "Help"):
    help.load_view()
