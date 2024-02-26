import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import fuzzywuzzy as fw 
from st_pages import hide_pages, Page, show_pages
from functions import background_img,side_bar_color,title,text,background_color

st.set_page_config(page_title="Interview AI")

# show_pages(
#     [
        
#         Page(path="pages\HR Page.py", name="HR Inputs", icon="🏠"),
#     ]
# )

if 'question' not in st.session_state:
    st.session_state['question']='''What is Machine Learning?'''

if 'ideal_ans' not in st.session_state:
    st.session_state['ideal_ans']='''Machine learning, a specialized domain within artificial intelligence, 
revolves around crafting algorithms and models that empower computers to discern
patterns and formulate decisions autonomously, without the need for explicit
programming instructions. '''


hide_pages(['Interview','Result'])

# background_img("https://e0.pxfuel.com/wallpapers/88/120/desktop-wallpaper-autodesk-website-background.jpg")
background_color("white")
side_bar_color("white")
st.markdown("<style>.my-title{font-family:'serif';}</style>",unsafe_allow_html=True,)
st.markdown(f'<h1 class="my-title">Login Page</h1>',unsafe_allow_html=True)
# title("Login Page","Serif","black","h1")

with st.form("login"):
    text("Eligibility Check","serif","black","h5")
    experience = st.slider("**Experience**",0,5,1)  
    education = st.radio("**Education**",['**Intermediate**',"**Graduate**","**Master's**"])
    submitted = st.form_submit_button("**Submit**")


# Every form must have a submit button.

    if submitted:
        if (experience>2) and (education=="**Graduate**" or education=="**Master's**"):
            switch_page("Interview") 
        else:
            with st.container(border=True,):
                st.warning("Sorry, you don't meet the eligibility criteria. Please try next time.", icon="⚠️")

                
