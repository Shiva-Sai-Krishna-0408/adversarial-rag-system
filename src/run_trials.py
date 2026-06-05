from src.pipeline import answer_query

def run_trials(query, retriever, generator, n):
    trials = []
    for i in range (n):
        response,retrieved = answer_query(query,retriever,generator)
        trials.append({"response": response, "retrieved": retrieved})
    return trials