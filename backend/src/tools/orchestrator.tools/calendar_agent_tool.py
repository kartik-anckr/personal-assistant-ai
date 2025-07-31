"""
Calendar Agent Execution Tool for Orchestrator
"""

from langchain_core.tools import tool

def create_calendar_agent_tool(calendar_agent):
    """Create the calendar agent execution tool"""

    @tool
    def execute_calendar_agent(query: str, context: str = "", user_id: str = "") -> str:
        """Execute the calendar agent for event creation requests.

        Args:
            query: The calendar/scheduling request
            context: Previous conversation context
            user_id: ID of the user making the request

        Returns:
            Calendar operation result
        """
        print(f"📅 [ORCHESTRATOR TOOL] Executing calendar agent: {query}")
        print(f"📅 [ORCHESTRATOR TOOL] User ID received: {user_id}")

        # Validate user_id
        if not user_id or user_id == "unknown":
            return "❌ Calendar feature requires user authentication. Please ensure you're logged in."

        # Add context if available
        if context:
            full_query = f"Previous context: {context}\nCalendar request: {query}"
        else:
            full_query = query

        # Execute the calendar agent with user context
        result = calendar_agent.invoke({
            "messages": [{"role": "user", "content": full_query}],
            "user_id": user_id
        })
        response = result["messages"][-1].content

        print(f"📅 [ORCHESTRATOR TOOL] Calendar result: {response}")
        return response

    return execute_calendar_agent 