import streamlit as st
import pandas as pd
import os
import base64
from functools import lru_cache
from tracyllm import main as tracyllm_main

# Page configuration
st.set_page_config(layout="wide", page_title="Unhoused Patron Assistance", page_icon="🏠")

# Load the Excel file
@st.cache_data
def load_data():
    filepath = os.path.join(os.getcwd(), 'APP Layout.xlsx')
    return pd.read_excel(filepath)

@lru_cache(maxsize=100)
def format_link(cell_content):
    if ';' in cell_content:
        parts = cell_content.split(';')
        if len(parts) == 2:
            link, title = parts
            if link.startswith("http://") or link.startswith("https://"):
                return f"[{title}]({link})"
    return cell_content

@st.cache_data
def load_images():
    img = {}
    img_data = {}
    for col_name in data.columns:
        image_path = os.path.join("assets", f"{col_name}.jpg")
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                img_data[col_name] = base64.b64encode(f.read()).decode("utf-8")
            img[col_name] = f"data:image/jpeg;base64,{img_data[col_name]}"
    return img

data = load_data()
img = load_images()

# Custom CSS
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        height: auto;
        white-space: normal !important;
        word-wrap: break-word;
        padding: 0.5rem;
        font-size: 0.8rem;
    }
    .category-image {
        width: 100%;
        max-width: 100px;
        height: auto;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.title('Unhoused Patron Assistance')

# Search functionality
with st.container():
    text_search = st.text_input("Search Training Material", placeholder="Enter your search query")
    if text_search:
        results = tracyllm_main(text_search)
        st.markdown(results, unsafe_allow_html=True)

# Category buttons in 3x3 grid
st.write("### Categories")
cols = st.columns(3)
for i, col_name in enumerate(data.columns[:9]):  # Limit to 9 categories
    with cols[i % 3]:
        st.image(img.get(col_name, ''), width=100)
        if st.button(col_name, key=f"col_{i}", use_container_width=True):
            st.session_state['selected_column'] = col_name

# Display selected category data
if 'selected_column' in st.session_state and st.session_state['selected_column'] is not None:
    st.write(f"### {st.session_state['selected_column']} Resources")
    for item in data[st.session_state['selected_column']].dropna().tolist():
        formatted_item = format_link(str(item))
        st.markdown(formatted_item, unsafe_allow_html=True)
    if st.button("Clear Selection"):
        st.session_state['selected_column'] = None
