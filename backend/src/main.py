"""
Enhanced FastAPI Server for Simplified Two-Agent LangGraph System with Authentication
Focus on Slack and Weather agents with LLM-driven tool selection and user authentication
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

# Import our enhanced three-agent orchestrator
import sys
import os
_backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _backend_path)
from src.agents.orchestrator_v3 import EnhancedThreeAgentOrchestrator

# Import authentication components
from src.routes.auth_routes import router as auth_router, get_current_user
from src.models.auth_models import UserResponse

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app (like creating an Express app)
app = FastAPI(
    title="LangGraph Multi-Agent System with Authentication",
    description="AI-powered multi-agent system with user authentication, Slack, Weather, and Calendar capabilities",
    version="3.0.0"
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

# Create our enhanced orchestrator system when the server starts
enhanced_orchestrator = None

@app.on_event("startup")
async def startup():
    """This runs when the server starts"""
    global enhanced_orchestrator
    print("🚀 Starting server with Enhanced Three-Agent Orchestrator...")
    
    # Check if we have Gemini API key
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if gemini_key:
        try:
            enhanced_orchestrator = EnhancedThreeAgentOrchestrator()
            print("✅ Enhanced Three-Agent Orchestrator created successfully!")
        except Exception as e:
            print(f"❌ Failed to create Enhanced Orchestrator: {e}")
    else:
        print("⚠️  No Gemini API key found. Please set GEMINI_API_KEY in .env file")

# Include authentication and calendar routes
app.include_router(auth_router)
from src.routes.calendar_routes import router as calendar_router
app.include_router(calendar_router)

# Simple models for our API (like TypeScript interfaces)
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    success: bool
    user_id: str = None

# Routes (like Express routes)
@app.get("/")
async def home():
    """Enhanced home page with authentication info"""
    return {
        "message": "LangGraph Multi-Agent System with Authentication",
        "version": "3.0.0",
        "features": [
            "User authentication (signup/signin)",
            "Multi-agent orchestration",
            "Slack messaging",
            "Weather information",
            "Google Calendar integration"
        ],
        "auth_endpoints": {
            "signup": "/auth/signup",
            "signin": "/auth/signin",
            "profile": "/auth/me"
        },
        "agents": {
            "slack": "Comprehensive Slack operations (send, read, channels, info)",
            "weather": "Complete weather services (current, forecast, climate, compare)",
            "calendar": "Google Calendar event creation and scheduling"
        },
        "ai_model": "Google Gemini 2.0 Flash",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Check if everything is working"""
    has_system = enhanced_orchestrator is not None
    
    # Check Supabase configuration
    import os
    supabase_configured = bool(
        os.getenv("SUPABASE_URL") and 
        os.getenv("SUPABASE_ANON_KEY") and 
        os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    )
    
    return {
        "status": "healthy" if has_system else "no_ai_configured",
        "ai_ready": has_system,
        "auth_ready": supabase_configured,
        "system_type": "Enhanced Three-Agent Orchestrator" if has_system else "None",
        "agents": ["Enhanced Slack Agent", "Enhanced Weather Agent", "Google Calendar Agent"] if has_system else [],
        "ai_model": "Google Gemini 2.0 Flash" if has_system else "None",
        "message": "Enhanced Three-Agent System is ready!" if has_system else "Please set GEMINI_API_KEY in .env file",
        "auth_message": "Supabase authentication ready!" if supabase_configured else "Please configure Supabase environment variables in .env file"
    }

@app.get("/auth/status")
async def auth_status():
    """Check authentication system status"""
    import os
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_anon = os.getenv("SUPABASE_ANON_KEY")
    supabase_service = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    
    return {
        "supabase_configured": bool(supabase_url and supabase_anon and supabase_service),
        "jwt_configured": bool(jwt_secret),
        "setup_required": {
            "supabase_url": not bool(supabase_url),
            "supabase_anon_key": not bool(supabase_anon),
            "supabase_service_role_key": not bool(supabase_service),
            "jwt_secret_key": not bool(jwt_secret)
        },
        "instructions": {
            "1": "Create a Supabase project at https://supabase.com",
            "2": "Run the SQL schema from backend/database_schema.sql",
            "3": "Create backend/.env file with your Supabase credentials",
            "4": "Add SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, JWT_SECRET_KEY"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def authenticated_chat(
    message: ChatMessage,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Chat endpoint that requires authentication
    
    Examples:
    - Slack: {"message": "Send 'Meeting at 3PM' to team channel"}
    - Weather: {"message": "What's the weather forecast for Tokyo?"}
    
    The system uses LLM intelligence to automatically select the right agent and tools!
    """
    if not enhanced_orchestrator:
        raise HTTPException(
            status_code=503,
            detail="AI system not available"
        )
    
    try:
        # Use our enhanced orchestrator system to get a response with user context
        ai_response = await enhanced_orchestrator.chat(message.message, current_user.id)
        
        return ChatResponse(
            response=ai_response,
            success=True,
            user_id=current_user.id
        )
    
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )

# Run the server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    
    print(f"🌟 Starting Enhanced Three-Agent server with Google Gemini 2.0 Flash on http://localhost:{port}")
    print(f"🎭 Three-Agent System: Slack + Weather + Calendar with LLM-driven selection!")
    print(f"⚡ Using Gemini 2.0 Flash with intelligent agent routing!")
    print(f"📚 API docs will be at http://localhost:{port}/docs")
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=debug  # Auto-reload on changes (like nodemon)
    ) 