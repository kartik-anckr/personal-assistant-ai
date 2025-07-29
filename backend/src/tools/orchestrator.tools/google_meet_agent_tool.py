"""
Google Meet Agent Execution Tool
"""

from langchain_core.tools import tool

def create_google_meet_agent_tool(google_meet_agent):
    """Create the Google Meet agent execution tool"""
    
    @tool
    def execute_google_meet_agent(query: str, context: str = "") -> str:
        """Execute the Google Meet agent for scheduling meetings and calendar operations.
        
        Args:
            query: The Google Meet scheduling request
            context: Previous results to use
            
        Returns:
            Google Meet scheduling result
        """
        print(f"📅 [V2 TOOL] Executing Google Meet agent: {query}")
        
        # Add context if available
        if context:
            full_query = f"Previous context: {context}\nGoogle Meet request: {query}"
        else:
            full_query = query
        
        # Execute the agent directly
        result = google_meet_agent.invoke({"messages": [{"role": "user", "content": full_query}]})
        response = result["messages"][-1].content
        
        print(f"📅 [V2 TOOL] Google Meet result: {response}")
        return response
    
    return execute_google_meet_agent 