import chromadb
from chromadb.utils import embedding_functions
import pandas as pd

# Initialize ChromaDB client
client = chromadb.Client()

# Create a collection
collection = client.create_collection("resource_database")

# Load data (assuming it's been processed into a pandas DataFrame)
df = pd.read_excel("APP_Layout.xlsx")

# Prepare data for ingestion
documents = df.apply(lambda row: " ".join(row.dropna().astype(str)), axis=1).tolist()
metadatas = df.to_dict(orient="records")
ids = [str(i) for i in range(len(df))]

# Ingest data into ChromaDB
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

def search_database(query):
    n_results = 3
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    formatted_results = []
    for i in range(len(results['ids'][0])):
        formatted_results.append({
            'id': results['ids'][0][i],
            'document': results['documents'][0][i],
            'metadata': results['metadatas'][0][i],
            'distance': results['distances'][0][i]
        })
    
    return formatted_results
