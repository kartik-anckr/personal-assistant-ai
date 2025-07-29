"""
Math Agent Execution Tool
"""

from langchain_core.tools import tool

def create_math_agent_tool(arithmetic_agent):
    """Create the math agent execution tool"""
    
    @tool
    def execute_math_agent(query: str, context: str = "") -> str:
        """Execute the arithmetic agent for math questions.
        
        Args:
            query: The math question
            context: Previous results to use
            
        Returns:
            Math result
        """
        print(f"🧮 [V2 TOOL] Executing arithmetic agent: {query}")
        
        # Add context if available
        if context:
            full_query = f"Previous context: {context}\nMath question: {query}"
        else:
            full_query = query
        
        # Execute the agent directly
        result = arithmetic_agent.invoke({"messages": [{"role": "user", "content": full_query}]})
        response = result["messages"][-1].content
        
        print(f"🧮 [V2 TOOL] Math result: {response}")
        return response
    
    return execute_math_agent 