"""
Orchestrator V2 - Simplified Workflow Orchestrator (Beginner-Friendly)
Demonstrates tool-based agent execution with workflow state, but simplified
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from .arithmetic_agent import create_arithmetic_agent
from .weather_agent import create_weather_agent
from .slack_agent import create_slack_agent
from .google_meet_agent import create_google_meet_agent

# Import states, tools, nodes and edges from separate modules
from ..states import SimpleWorkflowState
from ..tools import create_orchestrator_tools
from ..nodes import create_orchestrator_node, create_context_update_node
from ..edges import create_workflow_edges

class SimpleOrchestratorV2:
    """Simplified V2 Orchestrator - Easy to understand but keeps V2 concepts"""
    
    def __init__(self):
        print("🎭 Creating Simple Orchestrator V2...")
        
        # Hardcoded agents - much simpler!
        print("🔧 Setting up agents directly...")
        self.arithmetic_agent = create_arithmetic_agent()
        self.weather_agent = create_weather_agent()
        self.slack_agent = create_slack_agent()
        self.google_meet_agent = create_google_meet_agent()
        
        # Create LLM
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise Exception("No Gemini API key found!")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  # Using 1.5 flash to avoid quota issues
            google_api_key=gemini_api_key,
            temperature=0.2
        )
        
        # Create tools that actually execute agents (V2 concept)
        self.tools = create_orchestrator_tools(self.arithmetic_agent, self.weather_agent, self.slack_agent, self.google_meet_agent)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Create workflow graph
        self.workflow_graph = self._create_workflow()
        
        print("✅ Simple Orchestrator V2 ready!")
    

    
    def _create_workflow(self):
        """Create the workflow graph - simpler than complex V2"""
        
        graph_builder = StateGraph(SimpleWorkflowState)
        
        # Create nodes from separate modules
        orchestrator_node = create_orchestrator_node(self.llm_with_tools)
        context_update_node = create_context_update_node()
        
        # Add nodes
        graph_builder.add_node("orchestrator_with_tools", orchestrator_node)
        graph_builder.add_node("tool_execution", ToolNode(tools=self.tools))
        graph_builder.add_node("update_context", context_update_node)
        
        # Add edges from separate module
        graph_builder = create_workflow_edges(graph_builder)
        
        return graph_builder.compile()
    
    async def chat(self, user_input: str) -> str:
        """Simple chat interface for V2 orchestrator"""
        print(f"\n🎭 [V2 ORCHESTRATOR] Starting: {user_input}")
        
        # Initialize simple workflow state
        initial_state = {
            "messages": [{"role": "user", "content": user_input}],
            "agent_results": {},
            "context": ""
        }
        
        try:
            # Execute the V2 workflow
            result = self.workflow_graph.invoke(initial_state)
            
            # Extract response
            final_message = result["messages"][-1]
            response = final_message.content if hasattr(final_message, 'content') else str(final_message)
            
            # Show what agents were executed
            agent_results = result.get("agent_results", {})
            if agent_results:
                print(f"🎭 [V2 ORCHESTRATOR] Agent results: {agent_results}")
            
            return response
            
        except Exception as e:
            error_msg = f"V2 Orchestrator failed: {str(e)}"
            print(f"❌ {error_msg}")
            return f"Sorry, I encountered an error: {error_msg}"

# Factory function
async def create_simple_orchestrator_v2():
    """Create the simplified V2 orchestrator"""
    return SimpleOrchestratorV2() 