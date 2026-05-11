import numpy as np

class Retriever:
    def __init__(self,chunks,index,client,embedding_model):
        self.chunks = chunks
        self.index = index
        self.client = client
        self.embedding_model = embedding_model
        
    def retrieve(self,query,k=3):
        response = self.client.embeddings.create(input=query,model=self.embedding_model)
        query_vector = response.data[0].embedding
        query_np = np.array(query_vector,dtype='float32').reshape(1,-1)
        distances, indices = self.index.search(query_np,k)
        retrieved_chunks = [self.chunks[int(i)] for i in indices[0]]
        chunk_text = "\n\n".join([chunk[1] for chunk in retrieved_chunks])
        return chunk_text, retrieved_chunks