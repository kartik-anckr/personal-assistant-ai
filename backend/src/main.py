"""
Simple FastAPI Server for Simplified Two-Agent LangGraph System
Focus on Slack and Weather agents with LLM-driven tool selection
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

# Import our simplified two-agent orchestrator
import sys
import os
_backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _backend_path)
from src.agents.orchestrator_v2 import SimplifiedTwoAgentOrchestrator

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app (like creating an Express app)
app = FastAPI(
    title="Simplified Two-Agent LangGraph System",
    description="Intelligent LLM-driven agent selection focusing on Slack and Weather capabilities",
    version="2.0.0"
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

# Create our simplified orchestrator system when the server starts
simplified_orchestrator = None

@app.on_event("startup")
async def startup():
    """This runs when the server starts"""
    global simplified_orchestrator
    print("🚀 Starting server with Simplified Two-Agent Orchestrator...")
    
    # Check if we have Gemini API key
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if gemini_key:
        try:
            simplified_orchestrator = SimplifiedTwoAgentOrchestrator()
            print("✅ Simplified Two-Agent Orchestrator created successfully!")
        except Exception as e:
            print(f"❌ Failed to create Simplified Orchestrator: {e}")
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
        "message": "Welcome to Simplified Two-Agent LangGraph System! 🎭📱🌤️",
        "system_type": "Simplified Two-Agent Orchestrator",
        "agents": {
            "slack": "Comprehensive Slack operations (send, read, channels, info)",
            "weather": "Complete weather services (current, forecast, climate, compare)"
        },
        "ai_model": "Google Gemini 2.0 Flash",
        "features": "LLM-driven agent selection, multiple tools per agent, intelligent routing",
        "docs": "Go to /docs to see all endpoints",
        "examples": {
            "slack_send": "Send 'Meeting at 3PM' to team channel",
            "slack_read": "What are the latest messages in team channel?",
            "slack_info": "List all available Slack channels",
            "weather_current": "What's the weather in Tokyo?",
            "weather_forecast": "Give me a 5-day forecast for London",
            "weather_compare": "Compare weather between New York and Paris"
        }
    }

@app.get("/health")
async def health_check():
    """Check if everything is working"""
    has_system = simplified_orchestrator is not None
    return {
        "status": "healthy" if has_system else "no_ai_configured",
        "ai_ready": has_system,
        "system_type": "Simplified Two-Agent Orchestrator" if has_system else "None",
        "agents": ["Enhanced Slack Agent", "Enhanced Weather Agent"] if has_system else [],
        "ai_model": "Google Gemini 2.0 Flash" if has_system else "None",
        "message": "Simplified Two-Agent System is ready!" if has_system else "Please set GEMINI_API_KEY in .env file"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat with our Simplified Two-Agent System
    
    Examples:
    - Slack: {"message": "Send 'Meeting at 3PM' to team channel"}
    - Weather: {"message": "What's the weather forecast for Tokyo?"}
    
    The system uses LLM intelligence to automatically select the right agent and tools!
    """
    if not simplified_orchestrator:
        return ChatResponse(
            response="Sorry, Simplified Two-Agent System not configured. Please set GEMINI_API_KEY in .env file.",
            success=False
        )
    
    try:
        # Use our simplified orchestrator system to get a response
        ai_response = await simplified_orchestrator.chat(message.message)
        
        return ChatResponse(
            response=ai_response,
            success=True
        )
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return ChatResponse(
            response=f"Sorry, there was an error with the Simplified Two-Agent System: {str(e)}",
            success=False
        )

# Run the server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    
    print(f"🌟 Starting Simplified Two-Agent server with Google Gemini 2.0 Flash on http://localhost:{port}")
    print(f"🎭 Two-Agent System: Slack + Weather with LLM-driven selection!")
    print(f"⚡ Using Gemini 2.0 Flash with intelligent agent routing!")
    print(f"📚 API docs will be at http://localhost:{port}/docs")
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=debug  # Auto-reload on changes (like nodemon)
    ) 