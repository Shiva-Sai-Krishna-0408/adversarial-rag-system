class Generator:
    def __init__(self,client,model,system_prompt):
        self.client = client
        self.model = model
        self.system_prompt = system_prompt
        
    def generate(self,chunk_text,query,temp=0.7,max_t=500):
        response = self.client.chat.completions.create(
            model = self.model,
            messages=[
                    {'role':'system','content':self.system_prompt},
                    {'role':'user','content':f"<context>\n{chunk_text}\n</context>\n\n<query>\n{query}\n</query>"}
                ],
                temperature = temp,
                max_tokens = max_t
            )
    
        return response.choices[0].message.content