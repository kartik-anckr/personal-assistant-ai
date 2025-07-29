"""
Simple FastAPI Server for LangGraph with Google Gemini 1.5 Flash
Like Express.js but in Python!
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

# Import our V2 orchestrator agent
from .agents.orchestrator_v2 import create_simple_orchestrator_v2

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app (like creating an Express app)
app = FastAPI(
    title="LangGraph with Google Gemini",
    description="A simple API to learn LangChain and LangGraph using Google Gemini 1.5 Flash",
    version="1.0.0"
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js default
        "http://localhost:3001", 
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8080",
        # Add any other localhost ports you might use
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create our V2 orchestrator system when the server starts
v2_orchestrator = None

@app.on_event("startup")
async def startup():
    """This runs when the server starts"""
    global v2_orchestrator
    print("🚀 Starting the server with V2 Orchestrator System...")
    
    # Check if we have Gemini API key
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if gemini_key:
        try:
            v2_orchestrator = await create_simple_orchestrator_v2()
            print("✅ V2 Orchestrator System created successfully!")
        except Exception as e:
            print(f"❌ Failed to create V2 Orchestrator System: {e}")
    else:
        print("⚠️  No Gemini API key found. Please set GEMINI_API_KEY in .env file")

# Simple models for our API (like TypeScript interfaces)
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    success: bool

# Routes (like Express routes)
@app.get("/")
async def home():
    """Home page - just a welcome message"""
    return {
        "message": "Welcome to LangGraph V2 Orchestrator API with Google Gemini 1.5 Flash! 🎭🤖⚡",
        "system_type": "V2 Workflow Orchestrator",
        "agents": {
            "arithmetic": "Handles math calculations (addition, subtraction, etc.)",
            "weather": "Provides weather information for cities",
            "orchestrator": "Intelligent tool-based agent execution with workflow state"
        },
        "ai_model": "Google Gemini 1.5 Flash",
        "features": "Tool-based execution, context passing, workflow state tracking!",
        "docs": "Go to /docs to see all endpoints",
        "examples": {
            "math": "Add 15 and 25",
            "weather": "What's the weather in Tokyo?", 
            "chat": "Hello, how are you?"
        }
    }

@app.get("/health")
async def health_check():
    """Check if everything is working"""
    has_system = v2_orchestrator is not None
    return {
        "status": "healthy" if has_system else "no_ai_configured",
        "ai_ready": has_system,
        "system_type": "V2 Workflow Orchestrator" if has_system else "None",
        "agents": ["Arithmetic Agent", "Weather Agent", "V2 Orchestrator"] if has_system else [],
        "ai_model": "Google Gemini 1.5 Flash" if has_system else "None",
        "message": "V2 Orchestrator System is ready!" if has_system else "Please set GEMINI_API_KEY in .env file"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat with our V2 Orchestrator System
    Send: {"message": "Hello!"} or {"message": "Add 5 and 10"} or {"message": "Weather in London?"}
    Get: {"response": "Hi there!", "success": true}
    
    The V2 Orchestrator uses tool-based execution with workflow state tracking!
    """
    if not v2_orchestrator:
        return ChatResponse(
            response="Sorry, V2 Orchestrator System not configured. Please set GEMINI_API_KEY in .env file.",
            success=False
        )
    
    try:
        # Use our V2 orchestrator system to get a response
        ai_response = await v2_orchestrator.chat(message.message)
        
        return ChatResponse(
            response=ai_response,
            success=True
        )
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return ChatResponse(
            response=f"Sorry, there was an error with V2 Orchestrator System: {str(e)}",
            success=False
        )

# Run the server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    
    print(f"🌟 Starting V2 Orchestrator server with Google Gemini 1.5 Flash on http://localhost:{port}")
    print(f"🎭 V2 Orchestrator System: Tool-based execution with workflow state!")
    print(f"⚡ Using Gemini 1.5 Flash with advanced orchestration!")
    print(f"📚 API docs will be at http://localhost:{port}/docs")
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=debug  # Auto-reload on changes (like nodemon)
    ) 