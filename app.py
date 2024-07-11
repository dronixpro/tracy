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
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .stTitle {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        color: #2c3e50;
    }
    .stButton > button {
        width: 100%;
        height: auto;
        min-height: 60px;
        white-space: normal !important;
        word-wrap: break-word;
        padding: 0.75rem 1rem;
        background-color: #3498db;
        color: white;
        font-size: 1rem;
        font-weight: 500;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #2980b9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stButton > button:active {
        background-color: #2574a9;
    }
    .search-container {
        margin-bottom: 2rem;
    }
    .results-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    }
    .category-image {
        max-width: 100%;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    .category-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .category-title {
        font-size: 1.25rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.title('Unhoused Patron Assistance')

# Search functionality
with st.container():
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    text_search = st.text_input("Search Training Material", placeholder="Enter your search query")
    if text_search:
        results = tracyllm_main(text_search)
        st.markdown("<div class='results-container'>", unsafe_allow_html=True)
        st.markdown(results, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Category buttons
with st.container():
    cols = st.columns(5)
    for i, col_name in enumerate(data.columns):
        with cols[i % 5]:
            st.markdown("<div class='category-container'>", unsafe_allow_html=True)
            if col_name in img:
                st.image(img[col_name], use_column_width=True, output_format="PNG", class_="category-image")
            if st.button(col_name, key=f"col_{i}", use_container_width=True):
                st.session_state['selected_column'] = col_name
            st.markdown("</div>", unsafe_allow_html=True)

# Display selected category data
if 'selected_column' in st.session_state and st.session_state['selected_column'] != 'none':
    st.markdown(f"<h2 class='category-title'>{st.session_state['selected_column']} Resources</h2>", unsafe_allow_html=True)
    for item in data[st.session_state['selected_column']].dropna().tolist():
        formatted_item = format_link(str(item))
        st.markdown(formatted_item, unsafe_allow_html=True)
    if st.button("Clear Selection"):
        st.session_state['selected_column'] = 'none'
        







