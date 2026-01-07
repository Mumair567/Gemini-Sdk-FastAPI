from fastapi import FastAPI
from app.routes.document_route import document_router
from app.routes.chat_route import chatbot_router

app=FastAPI()

app.include_router(document_router)
app.include_router(chatbot_router)

@app.get("/")

def read_root():
    return {"message":"Welcome to my project"}
