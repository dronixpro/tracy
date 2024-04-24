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

img = {}

for col_name in data.columns:
    image_path = "assets/" + col_name + ".jpg"
    img[col_name] = image_path

# Streamlit UI components
st.header('I have an unhoused patron or I need help with...')

# # Display column headers as icons/links
# col_links = st.columns(len(data.columns))
# for i, col_name in enumerate(data.columns):
#     with col_links[i]:
#         if st.button(col_name,use_container_width=True):
#             st.session_state['selected_column'] = col_name

st.write('''<style>

[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)

# with st.container():

#     # Assuming 'data' is your DataFrame and it has exactly 9 columns
#     columns_per_segment = 9 // 3  # Calculate columns per Streamlit column
    
#     # Create three Streamlit columns
#     col1, col2, col3 = st.columns(3)
    
#     # Display the first segment of columns in the first Streamlit column
#     with col1:
#         for i in range(columns_per_segment):
#             col_name = data.columns[i]
#             if st.button(st.image(img[col_name]), key=f"col1_{i}", use_container_width=True):
#                 st.session_state['selected_column'] = col_name
    
#     # Display the second segment of columns in the second Streamlit column
#     with col2:
#         for i in range(columns_per_segment, 2 * columns_per_segment):
#             col_name = data.columns[i]
#             if st.button(col_name, key=f"col2_{i}", use_container_width=True):
#                 st.session_state['selected_column'] = col_name
    
#     # Display the third segment of columns in the third Streamlit column
#     with col3:
#         for i in range(2 * columns_per_segment, 3 * columns_per_segment):
#             col_name = data.columns[i]
#             if st.button(col_name, key=f"col3_{i}", use_container_width=True):
#                 st.session_state['selected_column'] = col_name


with st.container():
    # Assuming 'data' is your DataFrame and it has exactly 9 columns
    columns_per_segment = 9 // 3  # Calculate columns per Streamlit column

    # Create three Streamlit columns
    col1, col2, col3 = st.columns(3)

    # Display the first segment of columns in the first Streamlit column
    with col1:
        for i in range(columns_per_segment):
            col_name = data.columns[i]
            st.image(img[col_name])
            if st.button(col_name, key=f"col1_{i}", use_container_width=True):
                st.session_state['selected_column'] = col_name

    # Display the second segment of columns in the second Streamlit column
    with col2:
        for i in range(columns_per_segment, 2 * columns_per_segment):
            col_name = data.columns[i]
            st.image(img[col_name])
            if st.button(col_name, key=f"col2_{i}", use_container_width=True):
                st.session_state['selected_column'] = col_name

    # Display the third segment of columns in the third Streamlit column
    with col3:
        for i in range(2 * columns_per_segment, 3 * columns_per_segment):
            col_name = data.columns[i]
            st.image(img[col_name])
            if st.button(col_name, key=f"col3_{i}", use_container_width=True):
                st.session_state['selected_column'] = col_name


with st.container():
    # Display rows of the selected column
    if 'selected_column' in st.session_state:
        st.write(f"### {st.session_state['selected_column']} Data")
        for item in data[st.session_state['selected_column']].dropna().tolist():
            formatted_item = format_link(str(item))
            st.markdown(formatted_item, unsafe_allow_html=True)

