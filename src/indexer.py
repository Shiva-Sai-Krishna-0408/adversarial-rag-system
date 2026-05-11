import numpy as np
import faiss 

def build_index(chunks, client, embedding_model='text-embedding-3-small'):

    texts = [c[1] for c in chunks]
    embd = client.embeddings.create(model=embedding_model,input=texts)
    vectors = []
    for item in embd.data:
        vectors.append(item.embedding)

    vectors = np.array(vectors, dtype='float32')
    index = faiss.IndexFlatL2(1536)
    index.add(vectors)

    return index