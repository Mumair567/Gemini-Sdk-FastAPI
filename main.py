from fastapi import FastAPI
from app.routes.document_route import document_router

app=FastAPI()
app.include_router(document_router)