#------imports------

import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
import json

from src.extractor import extract_text_pypdf
from src.cleaner import clean_text
from src.chunker import chunk_text
from src.indexer import load_index
from src.retriever import Retriever
from src.generator import Generator
from src.pipeline import answer_query
from src.evaluator import run_eval
from attacks.tests import tests_ML

# --- setup: load env, build OpenAI client ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client_anthropic = Anthropic()

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
index, all_chunks = load_index(all_chunks, client)

# --- build Retriever and Generator ---
retriever = Retriever(all_chunks, index, client, 'text-embedding-3-small')
system_prompt = 'You are a helpful legal document assistant. Answer only based on context provided. Do not use your own knowledge.'
generator = Generator(client, model='gpt-4o', system_prompt=system_prompt)

#----evaluation----
baseline_results = {}
for test in tests_ML:
    query = test["query"]
    criterion = test["criterion"]
    result = run_eval(query,criterion,retriever=retriever,generator=generator,client=client_anthropic)
    baseline_results[test['id']] = result

for test_id,result in baseline_results.items():
    print(test_id,result['asr'])

with open("attacks/baseline_results_ml.json", "w") as f:
    json.dump(baseline_results,f,indent=2)
    