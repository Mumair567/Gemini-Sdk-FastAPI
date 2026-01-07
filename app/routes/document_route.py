from fastapi import FastAPI, APIRouter, HTTPException,File,UploadFile,Depends
from app.services.llm_services import ChatService
from google import genai
from app.models.chat_request import ChatRequest,ChatResponse
import asyncio
from app.InlineDB.db import save_data
from dotenv import load_dotenv
load_dotenv()

def get_chat_service():
    client=genai.Client()
    return ChatService(client,"gemini-3-flash-preview")

doc_id=0

document_router=APIRouter(prefix="/documents",tags=["Document Router"])

@document_router.post("/upload_docs/")

async def docs_upload(file:UploadFile=File(...)):
    
    global doc_id
    try:
        content=await file.read()
        text=content.decode("utf-8")
        doc_id+=1
    except Exception:
        raise HTTPException (status_code=400,detail="Upload only text document")
    new_doc={
        "id":doc_id,
        "filename":file.filename,
        "content":text
    }
    save_data.append(new_doc)
    return{
        "id":new_doc["id"],
        "filename":new_doc["filename"],
        "content":new_doc["content"]
    }


# document by id 

@document_router.get("/docu_id/{doc_id}")
def document_byid(docid:int):
    found =None
    for id in save_data:
        if id["id"]==docid:
            found=id
            break 
    if found is None:
        return HTTPException(status_code=404,detail="Document not exist id mismatch")
    return found

# get all documents
@document_router.get("/all_docs/")
async def All_docs():
    return  save_data

# chat with document by it's id 

@document_router.post("/chat_with_docid/")
async def chat_docid(doc_id:int,User_prompt:ChatRequest,chatservice:ChatService=Depends(get_chat_service)):
    doc=None
    try:
        for idd in save_data:
            if idd["id"]==doc_id:
                doc=idd
    except Exception:
        raise HTTPException(status_code=404,detail="document not found")
    doc_content=doc["content"]
    prompt=f" {doc_content} and user request is {User_prompt.user_prompt}"
    model_reply=await chatservice.chat(prompt)
    return ChatResponse(bot_response=model_reply)