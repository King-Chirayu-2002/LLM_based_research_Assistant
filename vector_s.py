import faiss
import numpy as np
import os
from dotenv import load_dotenv
import openai


load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("OPENAI_API_KEY")

openai.api_type = "azure"
openai.api_base = "AZURE_OPENAI_ENDPOINT"
openai.api_version = "2024-12-01-preview"  # Check for the latest version
openai.api_key = "OPENAI_API_KEY"

client = openai.AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-12-01-preview",  # Use the latest version if available
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def get_embedding(text, model="text-embedding-3-large"):
    """Generate embeddings using Azure OpenAI."""
    response = client.embeddings.create(input=[text], model=model)
    return np.array(response.data[0].embedding)

class VectorStore:
    def __init__(self, dimension=3072):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.text_data = []

    def add_text(self, text):
        """Add text to FAISS index."""
        embedding = get_embedding(text)
        self.index.add(np.array([embedding]).astype("float32"))
        self.text_data.append(text)

    def search(self, query, top_k=3):
        """Search for relevant text."""
        query_embedding = get_embedding(query)
        distances, indices = self.index.search(np.array([query_embedding]).astype("float32"), top_k)
        return [self.text_data[i] for i in indices[0] if i < len(self.text_data)]

