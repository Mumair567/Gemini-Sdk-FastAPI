from pydantic import BaseModel,Field

class ChatRequest(BaseModel):
    user_prompt:str

class ChatResponse(BaseModel):
    bot_response:str