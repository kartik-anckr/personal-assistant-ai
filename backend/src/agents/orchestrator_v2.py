"""
Simplified Two-Agent Orchestrator - Uses modular components
Focus on Slack and Weather agents with LLM-driven agent selection and streamlined architecture
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

# Import only the two agents we need
from .weather_agent import create_weather_agent
from .slack_agent import create_slack_agent

# Import modular components
from ..states import SimpleWorkflowState
from ..tools import create_simplified_orchestrator_tools
from ..nodes import create_simplified_orchestrator_node
from ..edges import create_simplified_workflow_edges

class SimplifiedTwoAgentOrchestrator:
    """Simplified orchestrator focusing on Slack and Weather agents using modular components"""
    
    def __init__(self):
        print("🎭 Creating Simplified Two-Agent Orchestrator...")
        
        # Only create the two core agents
        print("🔧 Setting up Slack and Weather agents...")
        self.slack_agent = create_slack_agent()
        self.weather_agent = create_weather_agent()
        
        # Create LLM
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise Exception("No Gemini API key found!")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Use latest model
            google_api_key=gemini_api_key,
            temperature=0.2
        )
        
        # Create simplified tools - only 2 agent invocation tools
        self.tools = create_simplified_orchestrator_tools(self.slack_agent, self.weather_agent)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Create simplified workflow graph using modular components
        self.workflow_graph = self._create_simplified_workflow()
        
        print("✅ Simplified Two-Agent Orchestrator ready!")
        print("🎯 Available agents: Slack, Weather")
    
    def _create_simplified_workflow(self):
        """Create simplified workflow using modular components"""
        
        graph_builder = StateGraph(SimpleWorkflowState)
        
        # Add nodes using modular components
        orchestrator_node = create_simplified_orchestrator_node(self.llm_with_tools)
        graph_builder.add_node("orchestrator", orchestrator_node)
        graph_builder.add_node("manager", ToolNode(tools=self.tools))
        
        # Add edges using modular components
        graph_builder = create_simplified_workflow_edges(graph_builder)
        
        return graph_builder.compile()
    
    async def chat(self, user_input: str) -> str:
        """Simplified chat interface"""
        print(f"\n🎭 [SIMPLIFIED ORCHESTRATOR] Processing: {user_input}")
        
        # Simple initial state
        initial_state = {
            "messages": [{"role": "user", "content": user_input}],
            "agent_results": {},
            "context": ""
        }
        
        try:
            # Execute simplified workflow
            result = self.workflow_graph.invoke(initial_state)
            
            # Extract response
            final_message = result["messages"][-1]
            response = final_message.content if hasattr(final_message, 'content') else str(final_message)
            
            print(f"🎭 [SIMPLIFIED ORCHESTRATOR] Response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Simplified Orchestrator failed: {str(e)}"
            print(f"❌ {error_msg}")
            return f"Sorry, I encountered an error: {error_msg}" 