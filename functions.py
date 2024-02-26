import streamlit as st

# sidebar_color
def side_bar_color(color):
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background-color : {color};
        }}
        </style>
        """,
        unsafe_allow_html=True,
        )
    
# sidebar_img
def side_bar_img(img):
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background: url("{img}") center;
            background-size:cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
        )

# background_color
def background_color(color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color : {color};
        }}
        </style>
        """,
        unsafe_allow_html=True,
        )
    
# background_img
def background_img(path):
    st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("{path}") center;
        background-size:cover;
    }}
    </style>
    """,
    unsafe_allow_html=True,
    )

# text
def text(text,font_name,color,size):
    st.markdown(
    f"""
    <style>
    .my-text{{
        color:{color};
        font-family:{font_name};
    }}
    </style>
    """,
    unsafe_allow_html=True,
    )
    st.markdown(f'<{size} class="my-text">{text}</{size}>',unsafe_allow_html=True)

# title
def title(title,font_name,color,size):
    st.markdown(
    f"""
    <style>
    .my-title{{
        color:{color};
        font-family:{font_name};
    }}
    </style>
    """,
    unsafe_allow_html=True,
    )
    st.markdown(f'<{size} class="my-title">{title}</{size}>',unsafe_allow_html=True)


