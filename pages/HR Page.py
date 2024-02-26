import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages, Page, show_pages
from functions import title

hide_pages(['Interview','Result'])
title("HR Input","serif","black","h2")

# st.title("HR Input")

with st.form("login"):
    question=st.text_input("**Enter Interview Question**")
    ideal_ans=st.text_area("**Enter Ideal Answer**")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if question and ideal_ans:
            st.session_state['question']=question
            st.session_state['ideal_ans']=ideal_ans
            switch_page('Login')
        else:
            # st.write("Please update the Question or Ideal Answer.")
            with st.container(border=True,):
                st.error("Please fill the Question or Ideal Answer.")
