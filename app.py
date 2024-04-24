import streamlit as st
import pandas as pd
import os

st. set_page_config(layout="wide")
# Load the Excel file
@st.cache_data
def load_data():
    filepath = os.path.join(os.getcwd(), 'APP Layout.xlsx')
    return pd.read_excel(filepath)

def format_link(cell_content):
    # Check if the cell content follows the 'link,title' format
    if ';' in cell_content:
        parts = cell_content.split(';')
        if len(parts) == 2:
            link, title = parts
            # Check if it's a valid URL
            if link.startswith("http://") or link.startswith("https://"):
                return f"[{title}]({link})"
    return cell_content  
data = load_data()

# Streamlit UI components
st.header('I have an unhoused patron or I need help with...')

# Display column headers as icons/links
col_links = st.columns(len(data.columns))
for i, col_name in enumerate(data.columns):
    with col_links[i]:
        if st.button(col_name,use_container_width=True):
            st.session_state['selected_column'] = col_name

# Display rows of the selected column
if 'selected_column' in st.session_state:
    st.write(f"### {st.session_state['selected_column']} Data")
    for item in data[st.session_state['selected_column']].dropna().tolist():
        formatted_item = format_link(str(item))
        st.markdown(formatted_item, unsafe_allow_html=True)

