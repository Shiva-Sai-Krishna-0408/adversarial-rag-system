#------imports------

import os
from dotenv import load_dotenv
from openai import OpenAI

from src.extractor import extract_text_pypdf
from src.cleaner import clean_text
from src.chunker import chunk_text
from src.indexer import build_index
from src.retriever import Retriever
from src.generator import Generator

# --- setup: load env, build OpenAI client ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- ingestion: extract, clean, chunk all PDFs into all_chunks ---
path = r'C:\Users\Shiva\projects\adversarial-rag-system\data'
files = ['apple_tos.pdf', 'github_tos.pdf', 'openai_tos.pdf']
all_chunks = []

for filename in files:
    file_path = os.path.join(path, filename)
    name = (filename.split('.')[0])
    extracted_text = extract_text_pypdf(file_path)
    cleaned_text = clean_text(extracted_text)
    chunks = chunk_text(cleaned_text,500,50,name)
    all_chunks.extend(chunks)

# --- build the FAISS index from all_chunks ---
index = build_index(all_chunks, client)

# --- build Retriever and Generator ---
retriever = Retriever(all_chunks, index, client, 'text-embedding-3-small')
system_prompt = 'You are a helpful legal document assistant. Answer only based on context provided. Do not use your own knowledge.'
generator = Generator(client, model='gpt-4o', system_prompt=system_prompt)

# --- run a query ---
query = "What are the terms for using Apple iCloud?"
context, retrieved = retriever.retrieve(query)
answer = generator.generate(context,query)
print(answer)