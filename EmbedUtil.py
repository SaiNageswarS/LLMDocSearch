import os

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')

from dotenv import load_dotenv
load_dotenv()

import pinecone
pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment=os.environ.get("PINECONE_ENVIRONMENT"))

PINECONE_INDEX = "kotlang-vectordb"
PINECONE_COLLECTION = "medical-ert-guideline"
# pinecone.create_index(name=PINECONE_INDEX, dimension=768, metric="cosine")
index = pinecone.Index(PINECONE_INDEX)