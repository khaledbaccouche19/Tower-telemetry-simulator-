from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

# Pydantic models for request/response
class ChatMessageRequest(BaseModel):
    tower_id: int
    message: str

class ChatMessageResponse(BaseModel):
    tower_id: int
    user_message: str
    ai_response: str
    timestamp: str

# Initialize FastAPI app
app = FastAPI(title="Tower AI Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Tower AI Service is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/chat", response_model=ChatMessageResponse)
def chat_with_ai(request: ChatMessageRequest):
    """Simple chat endpoint for testing"""
    try:
        # Simple response based on the message
        if "hello" in request.message.lower() or "hi" in request.message.lower():
            response = f"Hello! I'm the AI assistant for Tower {request.tower_id}. How can I help you today?"
        elif "status" in request.message.lower():
            response = f"Tower {request.tower_id} is currently online and operating normally. All systems are functioning within expected parameters."
        elif "temperature" in request.message.lower():
            response = f"Tower {request.tower_id} temperature is currently at 32°C, which is within normal operating range."
        elif "battery" in request.message.lower():
            response = f"Tower {request.tower_id} battery level is at 85%, which is good. No immediate charging required."
        else:
            response = f"I understand you're asking about Tower {request.tower_id}. I can help you with status updates, performance metrics, maintenance schedules, and troubleshooting. What specific information would you like to know?"
        
        return ChatMessageResponse(
            tower_id=request.tower_id,
            user_message=request.message,
            ai_response=response,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return ChatMessageResponse(
            tower_id=request.tower_id,
            user_message=request.message,
            ai_response=f"Sorry, I encountered an error: {str(e)}",
            timestamp=datetime.now().isoformat()
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

