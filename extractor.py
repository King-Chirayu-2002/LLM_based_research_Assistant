import fitz  # PyMuPDF
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "pdfstorage"

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def upload_pdf_to_blob(pdf_path, blob_name):
    """Upload PDF to Azure Blob Storage."""
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
    with open(pdf_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    return f"Uploaded {blob_name} successfully!"

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

