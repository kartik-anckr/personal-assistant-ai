"""
Context Update Node - Updates context with agent results
"""

def create_context_update_node():
    """Create the context update node"""
    
    def update_context(state):
        """Update context with agent results - simple V2 feature"""
        messages = state["messages"]
        agent_results = state.get("agent_results", {})
        
        # Simple context building from the last message
        if messages:
            last_content = getattr(messages[-1], 'content', '')
            new_context = f"Latest result: {last_content}"
            
            return {
                "context": new_context,
                "agent_results": {**agent_results, f"step_{len(agent_results)}": last_content}
            }
        
        return {"context": state.get("context", "")}
    
    return update_context 