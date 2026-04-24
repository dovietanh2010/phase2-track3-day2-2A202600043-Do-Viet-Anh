from typing import TypedDict, List, Dict, Any, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from memory_backends import ShortTermMemory, LongTermProfile, EpisodicMemory, SemanticMemory
import config

# Define State
class MemoryState(TypedDict):
    messages: List[BaseMessage]
    user_input: str
    user_profile: Dict[str, Any]
    episodes: List[Dict[str, Any]]
    semantic_hits: List[str]
    response: str
    memory_budget: int

# Initialize Memory Backends
st_memory = ShortTermMemory()
lt_profile = LongTermProfile(config.USER_PROFILE_PATH)
ep_memory = EpisodicMemory(config.EPISODES_PATH)
sem_memory = SemanticMemory(config.CHROMA_DB_DIR)

llm = ChatOpenAI(model=config.MODEL_NAME)

def retrieve_memory_node(state: MemoryState):
    """Retrieve context from all memory backends."""
    user_input = state["user_input"]
    
    # 1. Long-term Profile
    profile = lt_profile.get_profile()
    
    # 2. Episodic Memory
    episodes = ep_memory.get_episodes()
    
    # 3. Semantic Memory (RAG)
    semantic_hits = sem_memory.search(user_input)
    
    return {
        "user_profile": profile,
        "episodes": episodes,
        "semantic_hits": semantic_hits
    }

def agent_node(state: MemoryState):
    """Generate response with memory-augmented prompt."""
    profile_str = ", ".join([f"{k}: {v}" for k, v in state["user_profile"].items()])
    episodes_str = "\n".join([f"- {e['summary']} -> {e['outcome']}" for e in state["episodes"]])
    semantic_str = "\n".join([f"- {hit}" for hit in state["semantic_hits"]])
    
    system_prompt = f"""You are a multi-memory assistant. Use the following context to help the user.
    
USER PROFILE:
{profile_str if profile_str else "No profile data yet."}

PAST EPISODES:
{episodes_str if episodes_str else "No past relevant episodes."}

FACTUAL CONTEXT:
{semantic_str if semantic_str else "No relevant facts found."}

IMPORTANT:
- If the user provides a fact about themselves, acknowledge it.
- If the user corrects a previous fact (e.g., changing an allergy), use the new information.
"""
    
    messages = [SystemMessage(content=system_prompt)]
    # Add short-term history (last 5 messages)
    history = st_memory.get_messages()
    for m in history:
        if m["role"] == "user":
            messages.append(HumanMessage(content=m["content"]))
        else:
            messages.append(AIMessage(content=m["content"]))
            
    messages.append(HumanMessage(content=state["user_input"]))
    
    response = llm.invoke(messages)
    
    # Update Short-term memory
    st_memory.add_message("user", state["user_input"])
    st_memory.add_message("assistant", response.content)
    
    return {"response": response.content}

def update_memory_node(state: MemoryState):
    """Analyze interaction to update long-term memory and episodic memory."""
    user_input = state["user_input"]
    response = state["response"]
    
    # Simple extraction logic (In real app, use a dedicated LLM call)
    # Better extraction logic
    extract_prompt = f"""Extract user facts from this message: "{user_input}"
    Use these standardized keys:
    - "name": user name
    - "project": what they are working on
    - "health": allergies or medical restrictions (e.g., caffeine)
    - "preference": how they want answers (e.g., code snippets, concise)
    
    If it's a correction, return the new value.
    Return format: KEY: VALUE (one per line).
    If no fact found, return 'NONE'.
    """
    extraction_res = llm.invoke(extract_prompt).content
    
    if "NONE" not in extraction_res and ":" in extraction_res:
        for line in extraction_res.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                lt_profile.update_fact(key.strip().lower(), val.strip())
                
    # 2. Episodic logging (Only for termination or significant events)
    if "xong việc" in user_input.lower() or "hoàn thành" in user_input.lower():
        print(f"Recording episode: {user_input[:50]}")
        ep_memory.add_episode(
            summary=f"User asked about: {user_input[:50]}",
            outcome=response[:100]
        )
        print("Episode recorded successfully.")
        
    return state

# Build Graph
workflow = StateGraph(MemoryState)

workflow.add_node("retrieve", retrieve_memory_node)
workflow.add_node("agent", agent_node)
workflow.add_node("update", update_memory_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "agent")
workflow.add_edge("agent", "update")
workflow.add_edge("update", END)

# Compile
app = workflow.compile()

def run_agent(user_input: str):
    initial_state = {
        "user_input": user_input,
        "messages": [],
        "user_profile": {},
        "episodes": [],
        "semantic_hits": [],
        "response": "",
        "memory_budget": 2000
    }
    final_state = app.invoke(initial_state)
    return final_state["response"]
