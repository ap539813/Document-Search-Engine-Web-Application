from ctypes import alignment
import altair as alt
import streamlit as st

## Basic setup and app layout
st.set_page_config(layout="wide")

alt.renderers.set_embed_options(scaleFactor=2)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            div.stButton > button:first-child { 
                color: #4F8BF9;
                height: 3em;
                width: 100%; 
                }
            
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
# page_bg_img = '''
# <style>
# body {
# background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
# background-size: cover;
# }
# </style>
# '''

# st.markdown(page_bg_img, unsafe_allow_html=True)

st.image("Document search engine.png")

col1, col2, col3 = st.columns([1,3,1])
# col2.radio(
#         "Mode of Operation",
#         ("Search", "Configure"),
#     )

col2.markdown('<div style="text-align: center;"> <h2> Select mode of operation </h2></div>', unsafe_allow_html=True)
# col2.markdown('<div style="text-align: center;">Hello World!</div>', unsafe_allow_html=True)


col2.button('Search')
col2.button('Configure')

# col1.