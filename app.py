import streamlit as st
import pandas as pd
import os
import base64
from functools import lru_cache
from tracyllm import main as tracyllm_main

st.set_page_config(layout="centered")

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

st.title('I have an unhoused patron or I need help with...')

st.markdown('''<style>
button { height: 1em; }
[data-testid="column"] {
    width: calc(20% - 1rem) !important;
    flex: 1 1 calc(20% - 1rem) !important;
    min-width: calc(20% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)

def display_search_results(results):
    st.html(results)
    st.write('---')
    st.markdown(results, unsafe_allow_html=True)
    st.write('---')

with st.container():
    text_search = st.text_input(label="Search Training Material", label_visibility='collapsed', placeholder="Search")

    if text_search:
        results = tracyllm_main(text_search)
        display_search_results(results)

with st.container():
    columns_per_segment = 3
    cols = st.columns(3)

    for i, col in enumerate(cols):
        with col:
            for j in range(columns_per_segment):
                index = i * columns_per_segment + j
                if index < len(data.columns):
                    col_name = data.columns[index]
                    if col_name in img:
                        st.image(img[col_name], use_column_width='auto')
                    if st.button(col_name, key=f"col{i}_{j}", use_container_width=True):
                        st.session_state['selected_column'] = col_name

with st.container():
    if 'selected_column' in st.session_state:
        st.write(f"### {st.session_state['selected_column']} Data")
        for item in data[st.session_state['selected_column']].dropna().tolist():
            formatted_item = format_link(str(item))
            st.markdown(formatted_item, unsafe_allow_html=True)
        st.session_state['selected_column'] = 'none'
        







