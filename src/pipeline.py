from src.retriever import Retriever
from src.generator import Generator

def answer_query(query,retriever,generator):

    context, retrieved = retriever.retrieve(query)
    answer = generator.generate(context,query)
    return answer