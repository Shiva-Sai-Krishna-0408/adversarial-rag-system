import numpy as np

class Retriever:
    def __init__(self,chunks,index,client,embedding_model, reranker):
        self.chunks = chunks
        self.index = index
        self.client = client
        self.embedding_model = embedding_model
        self._embed_cache = {}
        self.source_labels = {'apple_tos': 'Apple ToS', 'github_tos':'GitHub ToS', 'openai_tos': 'OpenAI ToS'}
        self.reranker = reranker
        
    def _embed(self,query):
        if query not in self._embed_cache:
            response = self.client.embeddings.create(input=query,model=self.embedding_model)
            self._embed_cache[query] = np.array(response.data[0].embedding,dtype='float32').reshape(1,-1)
        return self._embed_cache[query]

    def retrieve(self,query,K=15,k=3):
        query_np = self._embed(query)
        distances, indices = self.index.search(query_np,K)
        retrieved_chunks = [self.chunks[int(i)] for i in indices[0]]
        unranked = [(query, f"[{ self.source_labels.get(chunk[0], 'Unknown Source') }] {chunk[1]}") for chunk in retrieved_chunks]
        scores = self.reranker.predict(unranked)
        ranked = sorted(zip(scores, retrieved_chunks), key= lambda x:x[0], reverse=True)
        top_k = ranked[:k]
        chunk_text = "\n\n".join([
        f"[{ self.source_labels.get(chunk[0], 'Unknown Source') }] {chunk[1]}" for score, chunk in top_k])
        top_chunks = [chunk for score,chunk in top_k]
        return chunk_text, top_chunks