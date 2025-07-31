"""
Enhanced Three-Agent Orchestrator - Slack, Weather, and Calendar
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

# Import all three agents
from .weather_agent import create_weather_agent
from .slack_agent import create_slack_agent
from .calendar_agent import create_calendar_agent

# Import modular components
from ..states import SimpleWorkflowState
from ..nodes import create_simplified_orchestrator_node
from ..edges import create_simplified_workflow_edges

# Import tools
import sys
_tools_dir = os.path.join(os.path.dirname(__file__), '..', 'tools', 'orchestrator.tools')
sys.path.insert(0, _tools_dir)
try:
    from weather_agent_tool import create_weather_agent_tool
    from slack_agent_tool import create_slack_agent_tool
    from calendar_agent_tool import create_calendar_agent_tool
finally:
    sys.path.remove(_tools_dir)

class EnhancedThreeAgentOrchestrator:
    """Enhanced orchestrator managing Slack, Weather, and Calendar agents"""

    def __init__(self):
        print("🎭 Creating Enhanced Three-Agent Orchestrator...")

        # Create all three agents
        print("🔧 Setting up Slack, Weather, and Calendar agents...")
        self.slack_agent = create_slack_agent()
        self.weather_agent = create_weather_agent()
        self.calendar_agent = create_calendar_agent()

        # Create LLM
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise Exception("No Gemini API key found!")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=gemini_api_key,
            temperature=0.2
        )

        # Create three-agent tools
        self.tools = self._create_three_agent_orchestrator_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # Create enhanced workflow graph with custom tool node
        self.workflow_graph = self._create_enhanced_workflow()

        print("✅ Enhanced Three-Agent Orchestrator ready!")
        print("🎯 Available agents: Slack, Weather, Calendar")

    def _create_three_agent_orchestrator_tools(self):
        """Create orchestrator tools for three-agent architecture"""

        slack_tool = create_slack_agent_tool(self.slack_agent)
        weather_tool = create_weather_agent_tool(self.weather_agent)
        calendar_tool = create_calendar_agent_tool(self.calendar_agent)

        # Update tool names and descriptions
        slack_tool.name = "invoke_slack_agent"
        slack_tool.description = "Handle Slack messaging requests"

        weather_tool.name = "invoke_weather_agent"
        weather_tool.description = "Handle weather-related requests"

        calendar_tool.name = "invoke_calendar_agent"
        calendar_tool.description = "Handle calendar event creation and scheduling requests"

        return [slack_tool, weather_tool, calendar_tool]

    def _create_enhanced_workflow(self):
        """Create enhanced workflow for three agents"""

        graph_builder = StateGraph(SimpleWorkflowState)

        # Add nodes
        orchestrator_node = create_simplified_orchestrator_node(self.llm_with_tools, self.llm)
        graph_builder.add_node("orchestrator", orchestrator_node)
        
        # Create custom tool node that injects user_id into tool calls
        def enhanced_tool_node(state):
            """Tool node that passes user_id to tools"""
            messages = state["messages"]
            user_id = state.get("user_id", "")
            
            print(f"🔧 [ENHANCED TOOL NODE] User ID: {user_id}")
            
            # Find and modify tool calls to include user_id
            modified_messages = []
            for msg in messages:
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    # Modify tool calls to include user_id
                    for tool_call in msg.tool_calls:
                        if 'args' in tool_call and isinstance(tool_call['args'], dict):
                            tool_call['args']['user_id'] = user_id
                            print(f"🔧 [ENHANCED TOOL NODE] Injected user_id into {tool_call.get('name', 'unknown tool')}")
                modified_messages.append(msg)
            
            # Update state with modified messages
            enhanced_state = state.copy()
            enhanced_state["messages"] = modified_messages
            
            # Execute tools with user context
            tool_node = ToolNode(tools=self.tools)
            result = tool_node.invoke(enhanced_state)
            
            # Preserve user_id in result
            result["user_id"] = user_id
            return result
        
        graph_builder.add_node("manager", enhanced_tool_node)

        # Add edges
        graph_builder = create_simplified_workflow_edges(graph_builder)

        return graph_builder.compile()

    async def chat(self, user_input: str, user_id: str = None) -> str:
        """Enhanced chat interface with user context"""
        print(f"\n🎭 [ENHANCED ORCHESTRATOR] Processing: {user_input}")

        # Enhanced initial state with user context
        initial_state = {
            "messages": [{"role": "user", "content": user_input}],
            "agent_results": {},
            "context": "",
            "user_id": user_id  # Pass user ID for calendar operations
        }

        try:
            # Execute enhanced workflow
            result = self.workflow_graph.invoke(initial_state)

            # Extract response
            final_message = result["messages"][-1]
            response = final_message.content if hasattr(final_message, 'content') else str(final_message)

            print(f"🎭 [ENHANCED ORCHESTRATOR] Response: {response}")
            return response

        except Exception as e:
            error_msg = f"Enhanced Orchestrator failed: {str(e)}"
            print(f"❌ {error_msg}")
            return f"Sorry, I encountered an error: {error_msg}" 