"""
Multi-Agent LangGraph System - V2 Orchestrator with Specialized Agents
Routes user input to appropriate specialized agents using V2 tool-based orchestration
"""

import os
from .agents.orchestrator_v2 import create_simple_orchestrator_v2

async def create_agent():
    """Create the V2 orchestrator system"""
    print("🚀 Creating V2 Orchestrator System...")
    return await create_simple_orchestrator_v2()

async def chat_with_agent(v2_orchestrator, user_input: str):
    """Chat with the V2 orchestrator system"""
    print(f"\n💭 User: {user_input}")
    
    # Use V2 orchestrator system
    response = await v2_orchestrator.chat(user_input)
    
    print(f"🎉 Final Response: {response}")
    return response

async def test_agent():
    """Test the V2 orchestrator system"""
    try:
        print("🚀 Creating V2 orchestrator system...")
        v2_orchestrator = await create_agent()
        
        print("\n" + "="*60)
        print("🧪 Testing V2 Orchestrator - Arithmetic Agent (Addition)")
        print("="*60)
        await chat_with_agent(v2_orchestrator, "Can you add 15 and 25 for me?")
        
        print("\n" + "="*60)
        print("🧪 Testing V2 Orchestrator - Arithmetic Agent (Subtraction)")  
        print("="*60)
        await chat_with_agent(v2_orchestrator, "What is 100 minus 30?")
        
        print("\n" + "="*60)
        print("🧪 Testing V2 Orchestrator - Weather Agent")
        print("="*60)
        await chat_with_agent(v2_orchestrator, "What's the weather like in London?")
        
        print("\n" + "="*60)
        print("🧪 Testing V2 Orchestrator - Weather Agent (Different City)")
        print("="*60)
        await chat_with_agent(v2_orchestrator, "How's the weather in Tokyo today?")
        
        print("\n" + "="*60)
        print("🧪 Testing V2 Orchestrator - Direct Response")
        print("="*60)
        await chat_with_agent(v2_orchestrator, "Hello! How are you today?")
        
        print("\n" + "="*60)
        print("🧪 Testing V2 Orchestrator - Complex Math (Multiplication)")
        print("="*60)
        await chat_with_agent(v2_orchestrator, "What is 6 times 8?")
        
        print("\n✅ All V2 orchestrator tests completed!")
        
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