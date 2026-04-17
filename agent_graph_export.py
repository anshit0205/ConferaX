# graph_generator.py — ConferaX v6.0 (New File)
# Handles generating the agent collaboration pipeline as a standalone PNG.
# Note: Requires matplotlib and networkx -> `pip install matplotlib networkx`

import os
import matplotlib.pyplot as plt
import networkx as nx

def generate_pipeline_png(output_path="output/agent_pipeline.png"):
    """Generates the agent pipeline graph as a standalone PNG."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    G = nx.DiGraph()
    
    nodes = [
        ("Tavily Search", {"color": "#06B6D4", "layer": 0}),
        ("Engine Pass 1", {"color": "#F97316", "layer": 0}),
        ("Orchestrator", {"color": "#3B82F6", "layer": 1}),
        ("Research Analyst", {"color": "#06B6D4", "layer": 2}),
        ("Sponsor Intel", {"color": "#8B5CF6", "layer": 2}),
        ("Exhibitor Intel", {"color": "#10B981", "layer": 2}),
        ("Speaker & Agenda", {"color": "#EC4899", "layer": 2}),
        ("Venue Intel", {"color": "#F59E0B", "layer": 2}),
        ("GTM & Audience", {"color": "#14B8A6", "layer": 2}),
        ("Engine Pass 2", {"color": "#F97316", "layer": 3}),
        ("Pricing Agent", {"color": "#FBBF24", "layer": 4}),
        ("Ops & Risk", {"color": "#6366F1", "layer": 4}),
        ("Devil's Advocate", {"color": "#EF4444", "layer": 5}),
        ("Self-Reflection", {"color": "#F97316", "layer": 6}),
        ("Decision Layer", {"color": "#84CC16", "layer": 7}),
        ("Outreach Agent", {"color": "#34D399", "layer": 8}),
        ("Synthesizer CSO", {"color": "#0EA5E9", "layer": 9}),
    ]
    
    edges = [
        ("Tavily Search", "Orchestrator"), ("Tavily Search", "Research Analyst"), 
        ("Tavily Search", "Sponsor Intel"), ("Tavily Search", "Exhibitor Intel"), 
        ("Tavily Search", "Speaker & Agenda"), ("Tavily Search", "Venue Intel"), 
        ("Tavily Search", "GTM & Audience"), ("Engine Pass 1", "Orchestrator"), 
        ("Engine Pass 1", "Pricing Agent"), ("Orchestrator", "Sponsor Intel"), 
        ("Orchestrator", "Exhibitor Intel"), ("Orchestrator", "Speaker & Agenda"), 
        ("Orchestrator", "Venue Intel"), ("Orchestrator", "GTM & Audience"), 
        ("Research Analyst", "Pricing Agent"), ("Sponsor Intel", "Engine Pass 2"), 
        ("Exhibitor Intel", "Engine Pass 2"), ("Engine Pass 2", "Pricing Agent"), 
        ("Engine Pass 2", "Decision Layer"), ("Pricing Agent", "Ops & Risk"), 
        ("Speaker & Agenda", "Ops & Risk"), ("Venue Intel", "Ops & Risk"), 
        ("Sponsor Intel", "Devil's Advocate"), ("Exhibitor Intel", "Devil's Advocate"), 
        ("Speaker & Agenda", "Devil's Advocate"), ("Venue Intel", "Devil's Advocate"), 
        ("Pricing Agent", "Devil's Advocate"), ("GTM & Audience", "Devil's Advocate"), 
        ("Ops & Risk", "Devil's Advocate"), ("Devil's Advocate", "Self-Reflection"), 
        ("Self-Reflection", "Decision Layer"), ("Devil's Advocate", "Decision Layer"), 
        ("Sponsor Intel", "Outreach Agent"), ("Speaker & Agenda", "Outreach Agent"), 
        ("Decision Layer", "Outreach Agent"), ("Outreach Agent", "Synthesizer CSO"), 
        ("Decision Layer", "Synthesizer CSO"), ("Pricing Agent", "Synthesizer CSO"), 
        ("Ops & Risk", "Synthesizer CSO"), ("GTM & Audience", "Synthesizer CSO"),
    ]
    
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    fig, ax = plt.subplots(figsize=(16, 9), facecolor="#101525")
    
    pos = nx.multipartite_layout(G, subset_key="layer", align="horizontal")
    
    colors = [data["color"] for _, data in G.nodes(data=True)]
    
    # Draw graph elements
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=2500, alpha=0.9, ax=ax, edgecolors="white", linewidths=1.5)
    nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color="white", arrowsize=15, ax=ax, node_size=2500, connectionstyle="arc3,rad=0.1")
    
    labels = {node: node.replace(" ", "\n") for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color="white", font_weight="bold", ax=ax)
    
    ax.set_title("ConferaX Agent Collaboration Pipeline", color="white", fontsize=18, fontweight="bold", pad=20)
    ax.set_facecolor("#101525")
    ax.axis("off")
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="#101525")
    plt.close()