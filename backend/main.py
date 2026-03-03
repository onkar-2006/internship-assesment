from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from agent import talent_scout_app
import uuid
import os

app = FastAPI(title="TalentScout Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    message: str
    thread_id: str

@app.get("/")
def health_check():
    return {"status": "online", "message": "TalentScout API is running"}
@app.post("/chat")
async def chat_endpoint(chat_input: ChatInput):
    config = {"configurable": {"thread_id": chat_input.thread_id}}
   
    inputs = {
        "messages": [HumanMessage(content=chat_input.message)],
        "candidate_data": CandidateProfile(
            full_name="",
            email="",
            phone="",
            experience="",
            position="",
            tech_stack=[]
        ),
        "phase": "screening" 
    }
    
    result = talent_scout_app.invoke(inputs, config=config)
    
    latest_message = result["messages"][-1].content
    current_phase = result.get("phase", "screening")
    extracted_data = result.get("candidate_data", {})
    
    return {
        "response": latest_message,
        "phase": current_phase,
        "data": extracted_data
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)