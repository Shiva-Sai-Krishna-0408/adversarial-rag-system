import numpy as np
import faiss 
import os
import pickle

def build_index(chunks, client, embedding_model='text-embedding-3-small'):

    texts = [c[1] for c in chunks]
    embd = client.embeddings.create(model=embedding_model,input=texts)
    vectors = []
    for item in embd.data:
        vectors.append(item.embedding)

    vectors = np.array(vectors, dtype='float32')
    index = faiss.IndexFlatL2(1536)
    index.add(vectors)

    return index,chunks

def load_index(all_chunks, client, index_dir="index"):
    path_1 = f"{index_dir}/faiss.index"
    path_2 = f"{index_dir}/chunks.pkl"

    if os.path.exists(path_1) and os.path.exists(path_2):
        # LOAD ONLY
        # 1. read FAISS index from path_1 → into a variable
        index = faiss.read_index(path_1)
        # 2. open path_2 in binary read mode, pickle.load → into a variable
        with open(path_2,"rb") as f:
            chunks = pickle.load(f)
        # 3. return both
        return index, chunks

    else:
        # BUILD AND SAVE
        # 1. make sure index_dir exists (os.makedirs)
        os.makedirs(index_dir,exist_ok=True)
        # 2. call build_index(...) to get index and chunks
        index, chunks = build_index(all_chunks,client)
        # 3. write FAISS index to path_1
        faiss.write_index(index,path_1)
        # 4. open path_2 in binary write mode, pickle.dump
        with open(path_2,"wb") as f:
           pickle.dump(chunks,f)
        # 5. return both
        return index, chunks