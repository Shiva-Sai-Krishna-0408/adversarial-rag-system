import time
from src.pipeline import answer_query

def run_trials(query, retriever, generator, n):
    trials = []
    for i in range (n):
        response,retrieved = answer_query(query,retriever,generator)
        trials.append({"response": response, "retrieved": retrieved})
        time.sleep(4)
    return trials