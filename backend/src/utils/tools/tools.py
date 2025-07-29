"""
Tools for the LangGraph Agent
Contains all tool functions that the agent can use
"""

from langchain_core.tools import tool

@tool
def addition_tool(a: float, b: float) -> float:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    result = a + b
    print(f"🔧 Tool used: {a} + {b} = {result}")
    return result

@tool
def subtraction_tool(a: float, b: float) -> float:
    """Subtract second number from first number.
    
    Args:
        a: First number (minuend)
        b: Second number (subtrahend) 
        
    Returns:
        The difference (a - b)
    """
    result = a - b
    print(f"🔧 Tool used: {a} - {b} = {result}")
    return result

# List of all available tools
ALL_TOOLS = [
    addition_tool,
    subtraction_tool
] 