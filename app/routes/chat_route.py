from fastapi import FastAPI,APIRouter,HTTPException,Depends
from app.services.llm_services import ChatService
from app.models.chat_request import ChatRequest,ChatResponse
from google import genai
from dotenv import load_dotenv

load_dotenv()

def chat_service():
    client=genai.Client()
    return ChatService(client,model_name="gemini-3-flash-preview")

chatbot_router=APIRouter(prefix="/chat",tags=["Chatbot"])

@chatbot_router.post("/chats/")
async def chat_with_bot(prompt:ChatRequest,chat_service:ChatService=Depends(chat_service)):
    try:
        response= await chat_service.chat(prompt.user_prompt)
    except Exception:
        raise HTTPException(status_code=404,detail="Chatbot not available")
    except Exception:
        raise HTTPException(status_code=500,detail="Internal Server Error ")
    return ChatResponse(bot_response=response)
    
    