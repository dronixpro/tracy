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
        padding: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .stTitle {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    .search-container {
        margin-bottom: 1rem;
    }
    .results-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .category-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    .category-item {
        background-color: #ffffff;
        padding: 0.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .category-image {
        width: 100%;
        max-width: 100px;
        height: auto;
        border-radius: 8px;
        margin-bottom: 0.25rem;
    }
    .category-button {
        width: 100%;
        padding: 0.25rem;
        background-color: #3498db;
        color: white;
        font-size: 0.8rem;
        font-weight: 500;
        border: none;
        border-radius: 4px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .category-button:hover {
        background-color: #2980b9;
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

# Category buttons in 3x3 grid
st.markdown("<div class='category-grid'>", unsafe_allow_html=True)
for i, col_name in enumerate(data.columns[:9]):  # Limit to 9 categories
    st.markdown(f"""
    <div class='category-item'>
        <img src='{img.get(col_name, '')}' class='category-image'>
        <button class='category-button' onclick="Streamlit.setComponentValue('selected_column', '{col_name}')">{col_name}</button>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Handle button clicks
if st.session_state.get('selected_column'):
    selected_column = st.session_state['selected_column']
    st.markdown(f"<h2 class='category-title'>{selected_column} Resources</h2>", unsafe_allow_html=True)
    for item in data[selected_column].dropna().tolist():
        formatted_item = format_link(str(item))
        st.markdown(formatted_item, unsafe_allow_html=True)
    if st.button("Clear Selection"):
        st.session_state['selected_column'] = None

# JavaScript to handle button clicks
st.markdown("""
<script>
    function handleCategoryClick(columnName) {
        Streamlit.setComponentValue('selected_column', columnName);
    }
</script>
""", unsafe_allow_html=True)
