import streamlit as st
import pandas as pd
import os
import base64


st.set_page_config(layout="centered")

if 'selected_column' in st.session_state:
    del st.session_state['selected_column']
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
img_data = {}
icon = {}

for col_name in data.columns:
    image_path = "assets/" + col_name + ".jpg"
    img[col_name] = image_path
    with open(img[col_name], "rb") as f:
        idata = f.read()
        encoded = base64.b64encode(idata)
    img_data[col_name] = "data:image/png;base64," + encoded.decode("utf-8")


# Streamlit UI components
st.title('I have an unhoused patron or I need help with...')


st.markdown('''<style>
[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)


with st.container(): 
    text_search = st.text_input(label="Search Training Material", label_visibility='collapsed', placeholder="Search")
    
    if text_search:
        # Initialize a combined mask with False values for all rows
        combined_mask = pd.Series([False] * len(data))
    
        # Loop through all columns in the DataFrame
        for column in data.columns:
            # Update the combined mask to include rows where the text_search is found in any part of the current column
            # Ensure the column data is string type to use str.contains
            combined_mask |= data[column].astype(str).str.contains(text_search, na=False, case=False, regex=True)
    
        # Filter the DataFrame using the combined mask
        data_search = data[combined_mask]
    
        # Define the number of cards per row
        N_cards_per_row = 10
        
    
        # Check if there is filtered data to display
        if not data_search.empty:
            # Reset the index to properly use iterrows
            for n_row, row in data_search.reset_index().iterrows():
                i = n_row % N_cards_per_row  # Determine the column to place the card based on the row number
                if i == 0:
                    st.write("---")  # Separator for visual clarity
                    cols = st.columns(N_cards_per_row, gap="small")  # Define the columns for cards
    
                # Display the card in the appropriate column
                with cols[i]:
                    # Display selected data fields as markdown in cards, ensuring all data is treated as string
                    st.markdown(f"**Counseling & Community: {str(row['Counseling & Community']).strip()}**")
                    st.markdown(f"*Food: {str(row['Food']).strip()}*")
                    st.markdown(f"**Staff Resources & Training: {str(row['Staff Resources & Training']).strip()}**")
                    st.markdown(f"**Jobs & Interviews: {str(row['Jobs & Interviews']).strip()}**")
                    st.markdown(f"**Crisis: {str(row['Crisis']).strip()}**")
                    st.markdown(f"**Public Transit: {str(row['Public Transit']).strip()}**")
                    st.markdown(f"**Shelter: {str(row['Shelter']).strip()}**")
                    st.markdown(f"**Substance Misuse: {str(row['Substance Misuse']).strip()}**")
                    st.markdown(f"**Healthcare: {str(row['Healthcare']).strip()}**")

with st.container():
    # Assuming 'data' is your DataFrame and it has exactly 9 columns
    columns_per_segment = 9 // 3  # Calculate columns per Streamlit column

    # Create three Streamlit columns
    col1, col2, col3 = st.columns(3)

    # Display the first segment of columns in the first Streamlit column
    with col1:
        for i in range(columns_per_segment):
            col_name = data.columns[i]
            st.image(img[col_name],use_column_width='auto')
            if st.button(col_name, key=f"col1_{i}", use_container_width=True):
                st.session_state['selected_column'] = col_name

    # Display the second segment of columns in the second Streamlit column
    with col2:
        for i in range(columns_per_segment, 2 * columns_per_segment):
            col_name = data.columns[i]
            st.image(img[col_name],use_column_width='auto')
            if st.button(col_name, key=f"col2_{i}", use_container_width=True):
                st.session_state['selected_column'] = col_name


    # Display the third segment of columns in the third Streamlit column
    with col3:
        for i in range(2 * columns_per_segment, 3 * columns_per_segment):
            col_name = data.columns[i]
            st.image(img[col_name],use_column_width='auto')
            if st.button(col_name, key=f"col3_{i}", use_container_width=True):
                st.session_state['selected_column'] = col_name



# columns_per_segment = len(data.columns) // 3  


# all_columns = st.columns(5)


# middle_columns = all_columns[1:4]

# for index, col in enumerate(middle_columns):
#     # Calculate the range of column indices for each Streamlit column
#     start_index = index * columns_per_segment
#     end_index = start_index + columns_per_segment

#     # Ensure we don't go out of bounds if data.columns has fewer than total needed items
#     end_index = min(end_index, len(data.columns))

#     with col:
#         for i in range(start_index, end_index):
#             col_name = data.columns[i]
#             # Each column displays an image and a button corresponding to a data column
#             st.image(img[col_name], use_column_width='always')
#             if st.button(col_name, key=f"middle_{index}_{i}", use_container_width=True):
#                 st.session_state['selected_column'] = col_name


              
with st.container():
    # Display rows of the selected column
    if 'selected_column' in st.session_state:
        st.write(f"### {st.session_state['selected_column']} Data")
        for item in data[st.session_state['selected_column']].dropna().tolist():
            formatted_item = format_link(str(item))
            st.markdown(formatted_item, unsafe_allow_html=True)
            st.session_state['selected_column'] = 'none'
            
        







