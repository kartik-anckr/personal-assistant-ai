"""
Arithmetic Agent - Specialized for mathematical operations
Handles addition, subtraction, and other arithmetic operations
"""

import os
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

# Import math tools
from ..utils.tools import addition_tool, subtraction_tool

class ArithmeticState(TypedDict):
    messages: Annotated[list, add_messages]

def create_arithmetic_agent():
    """Create a specialized arithmetic agent"""
    
    print("🧮 Creating Arithmetic Agent...")
    
    # Set up Google Gemini 2.0 Flash
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        raise Exception("No Gemini API key found!")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_api_key,
        temperature=0.3  # Lower temperature for precise math
    )
    
    # Math-specific tools
    math_tools = [addition_tool, subtraction_tool]
    llm_with_tools = llm.bind_tools(math_tools)
    
    # Arithmetic-specific system prompt
    ARITHMETIC_PROMPT = """You are a specialized arithmetic agent. Your expertise is mathematical operations.

🔢 YOUR ROLE:
- You ONLY handle arithmetic and mathematical questions
- Use addition_tool for addition operations
- Use subtraction_tool for subtraction operations
- For other math (multiplication, division), calculate directly with high precision
- Always provide clear, accurate mathematical results

🎯 EXAMPLES:
- "Add 15 and 25" → Use addition_tool
- "Subtract 10 from 50" → Use subtraction_tool  
- "What is 6 × 8?" → Calculate directly: 6 × 8 = 48
- "Divide 100 by 4" → Calculate directly: 100 ÷ 4 = 25

Be precise, clear, and focused on mathematical accuracy."""

    # Create state graph
    graph_builder = StateGraph(ArithmeticState)
    
    def arithmetic_chatbot(state: ArithmeticState):
        messages = state["messages"].copy()
        
        # Add arithmetic system prompt
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=ARITHMETIC_PROMPT)
            messages = [system_msg] + messages
            
        return {"messages": [llm_with_tools.invoke(messages)]}
    
    # Add nodes
    graph_builder.add_node("arithmetic_chatbot", arithmetic_chatbot)
    
    tool_node = ToolNode(tools=math_tools)
    graph_builder.add_node("arithmetic_tools", tool_node)
    
    # Add edges
    graph_builder.add_edge(START, "arithmetic_chatbot")
    graph_builder.add_conditional_edges(
        "arithmetic_chatbot",
        tools_condition,
        {"tools": "arithmetic_tools", "__end__": END}
    )
    graph_builder.add_edge("arithmetic_tools", "arithmetic_chatbot")
    
    # Compile
    graph = graph_builder.compile()
    
    print("✅ Arithmetic Agent ready!")
    return graph

async def chat_with_arithmetic_agent(agent, user_input: str):
    """Chat with the arithmetic agent"""
    print(f"🧮 [ARITHMETIC AGENT] Processing: {user_input}")
    
    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    response = result["messages"][-1].content
    
    print(f"🧮 [ARITHMETIC AGENT] Result: {response}")
    return response 