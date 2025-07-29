"""
Slack Agent Execution Tool
"""

from langchain_core.tools import tool

def create_slack_agent_tool(slack_agent):
    """Create the slack agent execution tool"""
    
    @tool
    def execute_slack_agent(query: str, context: str = "") -> str:
        """Execute the Slack agent for sending messages to Slack channels.
        
        Args:
            query: The Slack messaging request
            context: Previous results to use
            
        Returns:
            Slack result
        """
        print(f"📱 [V2 TOOL] Executing Slack agent: {query}")
        
        # Add context if available
        if context:
            full_query = f"Previous context: {context}\nSlack request: {query}"
        else:
            full_query = query
        
        # Execute the agent directly
        result = slack_agent.invoke({"messages": [{"role": "user", "content": full_query}]})
        response = result["messages"][-1].content
        
        print(f"📱 [V2 TOOL] Slack result: {response}")
        return response
    
    return execute_slack_agent 