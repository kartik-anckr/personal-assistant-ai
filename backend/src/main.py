"""
Enhanced FastAPI Server for Simplified Two-Agent LangGraph System with Authentication
Focus on Slack and Weather agents with LLM-driven tool selection and user authentication
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Import our enhanced three-agent orchestrator
import sys
import os
_backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _backend_path)
from src.agents.orchestrator_v3 import EnhancedThreeAgentOrchestrator

# Import authentication components
from src.routes.auth_routes import router as auth_router, get_current_user, get_current_user_with_token
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

# Include session management routes
from src.routes.session_routes import router as session_router
app.include_router(session_router)

# Simple models for our API (like TypeScript interfaces)
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None  # Add session support

class ChatResponse(BaseModel):
    response: str
    success: bool
    user_id: str = None
    session_id: Optional[str] = None  # Return session_id to frontend

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
    user_and_token: tuple[UserResponse, str] = Depends(get_current_user_with_token)
):
    """
    Enhanced chat endpoint with session support (maintains backward compatibility)

    Examples:
    - With session: {"message": "Hello", "session_id": "uuid-here"}
    - New session: {"message": "Hello", "session_id": null}
    - Legacy (backward compatible): {"message": "Hello"}
    """
    if not enhanced_orchestrator:
        raise HTTPException(
            status_code=503,
            detail="AI system not available"
        )

    try:
        # Extract user and JWT token
        current_user, jwt_token = user_and_token
        
        # Import session management components
        from src.database.session_operations import session_manager
        from src.database.message_operations import message_manager
        from src.services.memory_service import memory_service
        
        session_id = message.session_id

        # If no session_id provided, create a new session for backward compatibility
        if not session_id:
            logger.info(f"No session_id provided, creating new session for user {current_user.id}")
            new_session = await session_manager.create_session(
                user_id=current_user.id,
                title=f"Chat {message.message[:30]}...",
                jwt_token=jwt_token
            )
            if new_session:
                session_id = new_session["id"]
                logger.info(f"Created new session {session_id} for user {current_user.id}")
            else:
                logger.warning("Session creation failed, falling back to original behavior")
                # Fallback to original behavior if session creation fails
                ai_response = await enhanced_orchestrator.chat(message.message, current_user.id)
                return ChatResponse(
                    response=ai_response,
                    success=True,
                    user_id=current_user.id
                )

        # Verify session belongs to user
        logger.info(f"Verifying session {session_id} belongs to user {current_user.id}")
        session = await session_manager.get_session(session_id, current_user.id, jwt_token)
        if not session:
            # If session not found, try a small delay and retry once (for new sessions)
            import asyncio
            await asyncio.sleep(0.1)
            session = await session_manager.get_session(session_id, current_user.id, jwt_token)
            
        if not session:
            logger.error(f"Session {session_id} not found for user {current_user.id}")
            # Let's also check if the session exists but belongs to a different user (debugging)
            all_sessions = await session_manager.get_user_sessions(current_user.id, active_only=False)
            logger.info(f"User {current_user.id} has {len(all_sessions)} total sessions")
            raise HTTPException(status_code=404, detail="Session not found")

        # Load recent messages for context
        recent_messages = await memory_service.load_session_context(
            session_id, current_user.id, max_messages=20
        )

        # Add current user message to context
        all_messages = recent_messages + [{"role": "user", "content": message.message}]

        # Create enhanced state with session context
        initial_state = {
            "messages": all_messages,
            "agent_results": {},
            "context": "",
            "user_id": current_user.id,
            "session_id": session_id
        }

        # Get memory configuration for this session
        config = memory_service.get_thread_config(session_id)

        # Update orchestrator to use memory checkpointer
        if not hasattr(enhanced_orchestrator, 'workflow_graph_with_memory'):
            try:
                # Create workflow with memory checkpointer
                from langgraph.graph import StateGraph
                from src.states import SimpleWorkflowState
                from src.nodes import create_simplified_orchestrator_node
                from src.edges import create_simplified_workflow_edges
                from langgraph.prebuilt import ToolNode
                
                graph_builder = StateGraph(SimpleWorkflowState)
                orchestrator_node = create_simplified_orchestrator_node(enhanced_orchestrator.llm_with_tools, enhanced_orchestrator.llm)
                graph_builder.add_node("orchestrator", orchestrator_node)
                
                # Enhanced tool node with user context
                def enhanced_tool_node(state):
                    messages = state["messages"]
                    user_id = state.get("user_id", "")
                    
                    # Find and modify tool calls to include user_id
                    modified_messages = []
                    for msg in messages:
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                if 'args' in tool_call and isinstance(tool_call['args'], dict):
                                    tool_call['args']['user_id'] = user_id
                        modified_messages.append(msg)
                    
                    enhanced_state = state.copy()
                    enhanced_state["messages"] = modified_messages
                    
                    tool_node = ToolNode(tools=enhanced_orchestrator.tools)
                    result = tool_node.invoke(enhanced_state)
                    result["user_id"] = user_id
                    return result
                
                graph_builder.add_node("manager", enhanced_tool_node)
                
                # Add edges using existing edge logic
                workflow_edges = create_simplified_workflow_edges()
                workflow_edges(graph_builder)
                
                # Compile with memory checkpointer (if available)
                checkpointer = memory_service.get_checkpointer()
                enhanced_orchestrator.workflow_graph_with_memory = graph_builder.compile(checkpointer=checkpointer)
                
            except Exception as e:
                logger.error(f"Failed to create memory-enhanced workflow: {e}")
                # Fallback to original workflow without memory
                enhanced_orchestrator.workflow_graph_with_memory = enhanced_orchestrator.workflow_graph

        # Use orchestrator with memory
        result = enhanced_orchestrator.workflow_graph_with_memory.invoke(initial_state, config)

        # Extract response
        final_message = result["messages"][-1]
        ai_response = final_message.content if hasattr(final_message, 'content') else str(final_message)

        # Save messages to database
        await message_manager.add_message(session_id, current_user.id, "user", message.message, jwt_token=jwt_token)
        await message_manager.add_message(session_id, current_user.id, "assistant", ai_response, jwt_token=jwt_token)

        return ChatResponse(
            response=ai_response,
            success=True,
            user_id=current_user.id,
            session_id=session_id
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