import asyncio

class ChatService:
    def __init__(self,client,model_name:str,max_history:int=5):

        self.client=client
        self.model=model_name
        self.max_history=max_history
        self.history=[]
    def _build_prompt(self,user_input):
        self.history=self.history[-self.max_history:]
        conversation="\n".join(self.history)
        system_prompt="""
You are helpful assistant your job is to answer to user question
- Do not hallucinate
- Do not answer any irrelevant questions
- Always answer in clear and concise and professional tone

"""

        prompt= f"""{system_prompt}\n conversation so far {conversation}user input: {user_input}"""
        return prompt
    
    async def chat(self,user_input:str)->str:
        if not user_input.strip():
            raise ValueError("prompt cannot be empty")
        
        final_prompt= self._build_prompt(user_input)

        try:
            response= await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model,
                contents=final_prompt
            )
            bot_reply=response.text.strip()
        except Exception:
            raise RuntimeError("chatbot not responding check your api credits")
        
        self.history.append(f"user_input:{user_input}")
        self.history.append(f"bot_reply:{bot_reply}")
        return bot_reply
    
