# memory_system.py — ConferaX SOTA Learning Loop
import os
import json
from datetime import datetime

MEMORY_FILE = "output/system_learnings.json"

def save_run_learnings(event_category: str, sr_text: str, da_text: str):
    """Extracts critiques and saves them to a persistent JSON memory bank."""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    
    memory = []
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memory = json.load(f)
        except json.JSONDecodeError:
            memory = []
            
    # Create the new learning node (cap length to avoid context window bloat)
    learning_node = {
        "timestamp": datetime.now().isoformat(),
        "category": event_category,
        "self_reflection_flags": sr_text[:1500] if sr_text else "None",
        "da_critical_fixes": da_text[:1500] if da_text else "None"
    }
    
    memory.append(learning_node)
    
    # Keep only the 5 most recent learnings
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory[-5:], f, indent=4)

def retrieve_past_learnings(event_category: str) -> str:
    """Injects past mistakes into the Orchestrator so the system adapts."""
    if not os.path.exists(MEMORY_FILE):
        return "No prior system learnings found. This is the first run."
        
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)
    except json.JSONDecodeError:
        return "Error reading past learnings."
        
    context = ""
    # Filter for learnings relevant to this category, or just use the latest if few exist
    relevant_memory = [m for m in memory if m.get("category") == event_category]
    if not relevant_memory:
        relevant_memory = memory[-2:] # Default to last 2 runs if no category match
        
    for node in relevant_memory:
        context += f"--- PAST DA FIXES ---\n{node['da_critical_fixes']}\n\n"
        context += f"--- PAST SELF-REFLECTION FLAGS ---\n{node['self_reflection_flags']}\n\n"
            
    return context.strip()