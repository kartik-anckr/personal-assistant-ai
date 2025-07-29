# Project Graph Structure - Actual Implementation

## 🎯 Complete Multi-Agent System Architecture

Your project implements a **hierarchical graph structure** with multiple interconnected graphs:

### **📊 System Overview**

```
┌─────────────────── MULTI-AGENT SYSTEM ───────────────────┐
│                                                           │
│  🎭 ORCHESTRATOR GRAPH                                    │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ START → orchestrator_with_tools → [tool_execution] │ │
│  │           │                             │           │ │
│  │           └──── update_context ←────────┘           │ │
│  │                     │                               │ │
│  │                     ▼                               │ │
│  │                   END                               │ │
│  └─────────────────────────────────────────────────────┘ │
│                                │                          │
│                                ▼                          │
│  ┌─────────────── SPECIALIZED AGENTS ────────────────┐   │
│  │                                                   │   │
│  │  🧮 ARITHMETIC GRAPH      🌤️ WEATHER GRAPH       │   │
│  │  ┌─────────────────┐      ┌─────────────────┐     │   │
│  │  │ START           │      │ START           │     │   │
│  │  │   ▼             │      │   ▼             │     │   │
│  │  │ arithmetic_     │      │ weather_        │     │   │
│  │  │ chatbot ←──┐    │      │ chatbot ←──┐    │     │   │
│  │  │   │        │    │      │   │        │    │     │   │
│  │  │   ▼        │    │      │   ▼        │    │     │   │
│  │  │ arithmetic_│    │      │ weather_   │    │     │   │
│  │  │ tools ─────┘    │      │ tools ─────┘    │     │   │
│  │  │   │             │      │   │             │     │   │
│  │  │   ▼             │      │   ▼             │     │   │
│  │  │ END             │      │ END             │     │   │
│  │  └─────────────────┘      └─────────────────┘     │   │
│  └───────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────┘
```

## 🎭 Orchestrator Graph Structure (Simplified V2)

**File:** `src/agents/orchestrator_v2.py`

### **Graph Definition:**

```python
graph_builder = StateGraph(SimpleWorkflowState)

# Nodes
graph_builder.add_node("orchestrator_with_tools", orchestrator_with_tools)
graph_builder.add_node("tool_execution", ToolNode(tools=self.tools))
graph_builder.add_node("update_context", update_context)

# Edges
graph_builder.add_edge(START, "orchestrator_with_tools")
graph_builder.add_conditional_edges(
    "orchestrator_with_tools",
    tools_condition,
    {"tools": "tool_execution", "__end__": "update_context"}
)
graph_builder.add_edge("tool_execution", "update_context")
graph_builder.add_edge("update_context", END)
```

### **ASCII Graph Structure:**

```
🚀 START
   │
   ▼
┌─────────────────────────────────┐
│ orchestrator_with_tools         │
│                                 │
│ • LLM analyzes user input       │
│ • Decides which tool to call    │
│ • Can respond directly          │
└─────────┬───────────────────────┘
          │
          ▼ (tools_condition)
      ┌───────┐
      │ TOOL  │ ◀── Does LLM call tools?
      │ CALL? │
      └───┬───┘
          │
    ┌─────▼─────┐
YES │           │ NO
    ▼           ▼
┌─────────┐ ┌─────────────────────┐
│ tool_   │ │ update_context      │
│ execu-  │ │                     │
│ tion    │ │ • Store results     │
│         │ │ • Update state      │
│ • Run   │ │ • Pass context      │
│ LLM's   │ │                     │
│ chosen  │ │                     │
│ tool    │ │                     │
└────┬────┘ └─────────────────────┘
     │                   ▲
     │                   │
     └───────────────────┘
                         │
                         ▼
                    🏁 END
```

## 🧮 Arithmetic Agent Graph Structure

**File:** `src/agents/arithmetic_agent.py`

### **Graph Definition:**

```python
graph_builder = StateGraph(ArithmeticState)

# Nodes
graph_builder.add_node("arithmetic_chatbot", arithmetic_chatbot)
graph_builder.add_node("arithmetic_tools", ToolNode(tools=math_tools))

# Edges
graph_builder.add_edge(START, "arithmetic_chatbot")
graph_builder.add_conditional_edges(
    "arithmetic_chatbot",
    tools_condition,
    {"tools": "arithmetic_tools", "__end__": END}
)
graph_builder.add_edge("arithmetic_tools", "arithmetic_chatbot")
```

### **ASCII Graph Structure:**

```
🚀 START
   │
   ▼
┌─────────────────────────────────┐
│ arithmetic_chatbot              │
│                                 │
│ • Math-focused LLM              │
│ • Decides when to use tools     │
│ • Can calculate directly        │
└─────────┬───────────────────────┘
          │
          ▼ (tools_condition)
      ┌───────┐
      │ MATH  │ ◀── Use math tools?
      │ TOOL? │
      └───┬───┘
          │
    ┌─────▼─────┐
YES │           │ NO
    ▼           ▼
┌─────────┐   🏁 END
│ arith-  │
│ metic_  │
│ tools   │
│         │
│ • add   │
│ • sub   │
└────┬────┘
     │
     │ (loops back)
     ▼
┌─────────────────────────────────┐
│ arithmetic_chatbot              │ (continues conversation)
└─────────────────────────────────┘
```

## 🌤️ Weather Agent Graph Structure

**File:** `src/agents/weather_agent.py`

### **Graph Definition:**

```python
graph_builder = StateGraph(WeatherState)

# Nodes
graph_builder.add_node("weather_chatbot", weather_chatbot)
graph_builder.add_node("weather_tools", ToolNode(tools=weather_tools))

# Edges
graph_builder.add_edge(START, "weather_chatbot")
graph_builder.add_conditional_edges(
    "weather_chatbot",
    tools_condition,
    {"tools": "weather_tools", "__end__": END}
)
graph_builder.add_edge("weather_tools", "weather_chatbot")
```

### **ASCII Graph Structure:**

```
🚀 START
   │
   ▼
┌─────────────────────────────────┐
│ weather_chatbot                 │
│                                 │
│ • Weather-focused LLM           │
│ • Decides when to use tools     │
│ • Can respond directly          │
└─────────┬───────────────────────┘
          │
          ▼ (tools_condition)
      ┌───────┐
      │WEATHER│ ◀── Use weather tools?
      │ TOOL? │
      └───┬───┘
          │
    ┌─────▼─────┐
YES │           │ NO
    ▼           ▼
┌─────────┐   🏁 END
│ weather_│
│ tools   │
│         │
│ • get_  │
│ weather │
│ _info   │
└────┬────┘
     │
     │ (loops back)
     ▼
┌─────────────────────────────────┐
│ weather_chatbot                 │ (continues conversation)
└─────────────────────────────────┘
```

## 🔄 Complete Execution Flow

### **User Input Processing:**

```
👤 USER INPUT: "Add 15 and 25"
│
▼
┌─────────────── ORCHESTRATOR GRAPH ───────────────┐
│                                                   │
│ START → orchestrator_with_tools                   │
│              │                                    │
│              ▼ (LLM decides: use execute_math_agent)
│         tool_execution                            │
│              │                                    │
│              ▼ (calls execute_math_agent tool)    │
│         ┌─────────────────────────────────────┐   │
│         │ TOOL EXECUTES ARITHMETIC AGENT:    │   │
│         │                                     │   │
│         │  ┌─── ARITHMETIC GRAPH ────┐       │   │
│         │  │                         │       │   │
│         │  │ START → arithmetic_     │       │   │
│         │  │         chatbot         │       │   │
│         │  │           │             │       │   │
│         │  │           ▼             │       │   │
│         │  │         arithmetic_     │       │   │
│         │  │         tools           │       │   │
│         │  │           │             │       │   │
│         │  │           ▼             │       │   │
│         │  │         END             │       │   │
│         │  │                         │       │   │
│         │  └─── RETURNS "Sum is 40" ─┘       │   │
│         └─────────────────────────────────────┘   │
│              │                                    │
│              ▼                                    │
│         update_context                            │
│              │                                    │
│              ▼                                    │
│         END                                       │
└───────────────────────────────────────────────────┘
│
▼
👤 USER RECEIVES: "The sum of 15 and 25 is 40"
```

## 📊 State Management Across Graphs

### **Orchestrator State:**

```python
class SimpleWorkflowState(TypedDict):
    messages: Annotated[list, add_messages]
    agent_results: Dict[str, str]
    context: str
```

### **Agent States:**

```python
class ArithmeticState(TypedDict):
    messages: Annotated[list, add_messages]

class WeatherState(TypedDict):
    messages: Annotated[list, add_messages]
```

## 🔗 Graph Connections

### **How Graphs Connect:**

1. **Orchestrator** receives user input
2. **Tools** in orchestrator execute **specialized agents**
3. Each **specialized agent** has its own internal graph
4. **Results** flow back through the orchestrator graph
5. **Context** is maintained at orchestrator level

### **Tool Integration:**

```
📍 ORCHESTRATOR TOOLS:
├── execute_math_agent(query, context) → Invokes Arithmetic Graph
└── execute_weather_agent(query, context) → Invokes Weather Graph

📍 ARITHMETIC TOOLS:
├── addition_tool(a, b) → Returns sum
└── subtraction_tool(a, b) → Returns difference

📍 WEATHER TOOLS:
└── get_weather_info(location) → Returns weather data
```

## 🎯 Key Graph Features

### **Orchestrator Graph:**

• **Conditional routing** based on LLM tool calls
• **Context preservation** across multiple agent calls  
• **State tracking** for complex workflows

### **Agent Graphs:**

• **Tool-based execution** with automatic LLM routing
• **Loop-back architecture** for continued conversation
• **Specialized prompts** for domain expertise

### **System Benefits:**

• **Hierarchical design** - Clear separation of concerns
• **Reusable agents** - Each agent graph can be used independently  
• **Scalable architecture** - Easy to add new agents and tools
• **State management** - Context flows properly between graphs
