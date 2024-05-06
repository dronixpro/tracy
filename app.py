import streamlit as st
import pandas as pd
import os
import base64
from nltk.corpus import wordnet as wn
import nltk
from fuzzywuzzy import fuzz


st.set_page_config(layout="centered")


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
        

button {
    height: 1em;
}


[data-testid="column"] {
    width: calc(20% - 1rem) !important;
    flex: 1 1 calc(20% - 1rem) !important;
    min-width: calc(20% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)

custom_synonyms = {
    'jobs': ['employment', 'work', 'career'],
    'food': ['nutrition', 'meals', 'groceries'],
    'shelter': ['housing', 'accommodation', 'lodging'],
    'bus':['transportation','transit','mta'],
    'transit':['bus']
}

# Ensure nltk resources are downloaded
nltk.download('wordnet')
nltk.download('omw-1.4')

# Define additional synonyms for specific terms
custom_synonyms = {
    'jobs': ['employment', 'work', 'career'],
    'food': ['nutrition', 'meals', 'groceries'],
    'shelter': ['housing', 'accommodation', 'lodging']
}

# Function to find synonyms using WordNet and custom synonyms
def find_synonyms(word, n=3):
    synonyms = set()
    
    # Add custom synonyms
    if word in custom_synonyms:
        synonyms.update(custom_synonyms[word])
    
    # Add WordNet synonyms
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    
    return list(synonyms)[:n]

# Function to apply fuzzy matching and return best matches
def find_best_matches(df, search_terms, threshold=80):
    results = []
    
    for term in search_terms:
        for column in df.columns:
            for idx, value in df[column].dropna().items():
                similarity_score = fuzz.partial_ratio(term.lower(), str(value).lower())
                if similarity_score >= threshold:
                    results.append((similarity_score, idx, column, str(value).strip()))
    
    # Sort results by similarity score in descending order
    results = sorted(results, key=lambda x: x[0], reverse=True)
    return results

# Function to highlight the matching terms
def highlight_matches(text, search_terms):
    for term in search_terms:
        text = text.replace(term, f"<mark>{term}</mark>")
    return text

# Function to display the best matching individual pieces of information
def display_search_results(results, search_terms, N_cards_per_row=1):
    if results:
        for n_row, (score, idx, column, value) in enumerate(results):
            i = n_row % N_cards_per_row
            if i == 0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="small")
            
            with cols[i]:
                highlighted_value = highlight_matches(value, search_terms)
                st.markdown(f"**{column}:** {highlighted_value}", unsafe_allow_html=True)
                st.write('---')


with st.container():
    text_search = st.text_input(label="Search Training Material", label_visibility='collapsed', placeholder="Search")

    if text_search:
        # Find synonyms and include the original search term
        synonyms = find_synonyms(text_search, n=3)
        synonyms.append(text_search)

        # Find the best matches
        best_matches = find_best_matches(data, synonyms)

        # Display search results using the custom function
        display_search_results(best_matches, synonyms)


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
            
        







