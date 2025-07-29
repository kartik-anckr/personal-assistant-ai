"""
Weather Agent Execution Tool
"""

from langchain_core.tools import tool

def create_weather_agent_tool(weather_agent):
    """Create the weather agent execution tool"""
    
    @tool
    def execute_weather_agent(query: str, context: str = "") -> str:
        """Execute the weather agent for weather questions.
        
        Args:
            query: The weather question  
            context: Previous results to use
            
        Returns:
            Weather result
        """
        print(f"🌤️ [V2 TOOL] Executing weather agent: {query}")
        
        # Add context if available
        if context:
            full_query = f"Previous context: {context}\nWeather question: {query}"
        else:
            full_query = query
        
        # Execute the agent directly
        result = weather_agent.invoke({"messages": [{"role": "user", "content": full_query}]})
        response = result["messages"][-1].content
        
        print(f"🌤️ [V2 TOOL] Weather result: {response}")
        return response
    
    return execute_weather_agent 