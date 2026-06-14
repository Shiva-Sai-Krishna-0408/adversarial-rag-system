import time
import openai
from src.pipeline import answer_query

def call_with_retry(func,*args,max_retries=5,**kwargs):
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except (openai.RateLimitError, openai.APIError, openai.APITimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
            
def run_trials(query, retriever, generator, n):
    trials = []
    for i in range (n):
        response,retrieved = call_with_retry(answer_query,query,retriever,generator)
        trials.append({"response": response, "retrieved": retrieved})
        time.sleep(0.5)
    return trials