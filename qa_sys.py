import os
from dotenv import load_dotenv
import openai


load_dotenv()

NAI_ENDPOINT = os.getenv("GPT_ENDPOINT")
NAI_KEY = os.getenv("GPT_KEY")

openai.api_type = "azure"
openai.api_base = "NAI_ENDPOINT"
openai.api_version = "2024-12-01-preview"  # Check for the latest version
openai.api_key = "NAI_KEY"

client = openai.AzureOpenAI(
    api_key=NAI_KEY,
    api_version="2024-12-01-preview",  # Use the latest version if available
    azure_endpoint=NAI_ENDPOINT
)


def ask_gpt(question, context):
    """Use Azure OpenAI GPT-4 to generate answers."""
    prompt = f"Based on the following context, answer the question:\n\nContext:\n{context}\n\nQuestion: {question}"

    response = client.chat.completions.create(
        model="YOUR_DEPLOYMENT_NAME",  # Use the correct deployment name
        messages=[{"role": "user", "content": prompt}],  # Correct format for chat models
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
