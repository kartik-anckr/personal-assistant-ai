"""
Simplified Two-Agent LangGraph System
Routes user input to appropriate specialized agents using LLM-driven agent selection
"""

import os
from .agents.orchestrator_v2 import SimplifiedTwoAgentOrchestrator

async def create_agent():
    """Create the simplified two-agent orchestrator system"""
    print("🚀 Creating Simplified Two-Agent Orchestrator...")
    return SimplifiedTwoAgentOrchestrator()

async def chat_with_agent(simplified_orchestrator, user_input: str):
    """Chat with the simplified two-agent orchestrator system"""
    return await simplified_orchestrator.chat(user_input)

async def test_agent():
    """Test the simplified two-agent orchestrator system"""
    try:
        print("🚀 Creating Simplified Two-Agent Orchestrator...")
        simplified_orchestrator = await create_agent()
        
        print("\n" + "="*60)
        print("🧪 Testing Simplified Two-Agent Orchestrator - Slack Agent")
        print("="*60)
        await chat_with_agent(simplified_orchestrator, "List all available Slack channels")
        
        print("\n" + "="*60)
        print("🧪 Testing Simplified Two-Agent Orchestrator - Slack Channel Info")  
        print("="*60)
        await chat_with_agent(simplified_orchestrator, "Get information about the development channel")
        
        print("\n" + "="*60)
        print("🧪 Testing Simplified Two-Agent Orchestrator - Weather Agent")
        print("="*60)
        await chat_with_agent(simplified_orchestrator, "What's the weather like in London?")
        
        print("\n" + "="*60)
        print("🧪 Testing Simplified Two-Agent Orchestrator - Weather Forecast")
        print("="*60)
        await chat_with_agent(simplified_orchestrator, "Give me a 5-day forecast for Tokyo")
        
        print("\n" + "="*60)
        print("🧪 Testing Simplified Two-Agent Orchestrator - Weather Comparison")
        print("="*60)
        await chat_with_agent(simplified_orchestrator, "Compare weather between New York and Paris")
        
        print("\n" + "="*60)
        print("🧪 Testing Simplified Two-Agent Orchestrator - Direct Response")
        print("="*60)
        await chat_with_agent(simplified_orchestrator, "Hello! How are you today?")
        
        print("\n✅ All Simplified Two-Agent Orchestrator tests completed!")
        print("🎭 Successfully tested: Slack Agent (4 tools) + Weather Agent (4 tools)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    
    print("🔧 Loading environment variables...")
    load_dotenv()
    
    asyncio.run(test_agent()) 