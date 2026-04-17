# main.py — ConferaX v3.0
import os
from dotenv import load_dotenv
load_dotenv()

from crew import run_conferax, print_serpapi_summary
from html_generator import generate_html_report

from agent_graph_export import export_agent_graph
from data_extractor import extract_chart_data_to_json

def collect_inputs() -> dict:
    print("\n" + "="*62)
    print("  ✨ ConferaX v3.0 — Autonomous Conference Intelligence")
    print("  14 Agents | Prediction Engine | Outreach | Devil's Advocate")
    print("  Self-Reflection | Decision Layer | 10-Search Tavily")
    print("="*62)
    print("\nAnswer 14 questions to launch your conference intelligence engine.")
    print("Press Enter to use the [default] value.\n")

    def ask(question: str, default: str = "") -> str:
        prompt = f"  ➤ {question}"
        if default:
            prompt += f"\n    [{default}]"
        prompt += "\n    > "
        answer = input(prompt).strip()
        return answer if answer else default

    inputs = {
        "event_category":             ask("Event Category (e.g. AI, Web3, ClimateTech, Healthcare)", "AI & Technology"),
        "geography_region":           ask("Geography / Target Region (e.g. India, Delhi, Singapore)", "Delhi, India"),
        "target_audience_size":       ask("Target Audience Size (e.g. 500, 1000, 5000)", "1000"),
        "event_date_range":           ask("Event Date or Date Range (e.g. May 2026, Q3 2026)", "May 4, 2026"),
        "expected_duration":          ask("Expected Duration (Half-day / 1 day / 2 days / 3 days)", "1 day"),
        "event_format":               ask("Event Format (Summit / Conference / Expo / Workshop / Hybrid)", "Summit"),
        "budget_range":               ask("Budget Range (e.g. ₹50L, ₹1Cr, $100K)", "₹1 Crore INR"),
        "expected_audience_persona":  ask("Expected Audience Persona (e.g. founders, developers, investors)", "Founders, developers, investors"),
        "venue_preference_constraints": ask("Venue Preferences (e.g. indoor, premium, city-center)", "Indoor, premium, city-center"),
        "sponsor_priority":           ask("Sponsor Priority (e.g. tech companies, VCs, startups)", "Tech companies and VCs"),
        "speaker_priority":           ask("Speaker Priority (e.g. global keynotes, practitioners, celebrities)", "Global AI thought leaders and practitioners"),
        "ticketing_intent":           ask("Ticketing Intent (Free / Paid / Tiered / Invite-only)", "Tiered pricing"),
        "organizer_objective":        ask("Organizer Objective (revenue / brand building / community / leads)", "Brand building and community growth"),
        "hard_constraints":           ask("Hard Constraints (language, capacity, accessibility)", "English primary, wheelchair accessible, max 2000 capacity"),
    }

    print("\n" + "─"*62)
    print("  ✅ Inputs collected. Launching ConferaX v3.0 engine...")
    print("─"*62 + "\n")
    return inputs

def save_outputs(results: dict, inputs: dict):
    os.makedirs("output", exist_ok=True)
    
    file_map = {
        "strategy_profile":        "01_strategy_profile.txt",
        "research_output":         "02_research_output.txt",
        "sponsor_output":          "03a_sponsor_output.txt",
        "exhibitor_output":        "03b_exhibitor_output.txt",
        "speaker_output":          "04_speaker_output.txt",
        "venue_output":            "05_venue_output.txt",
        "pricing_output":          "06_pricing_output.txt",
        "gtm_output":              "07_gtm_output.txt",
        "ops_output":              "08_ops_output.txt",
        "devils_advocate_output":  "09_devils_advocate.txt",
        "self_reflection_output":  "10_self_reflection.txt",
        "outreach_output":         "11_outreach_emails.txt",
        "decision_output":         "12_decisions.txt",
        "final_report":            "13_final_report.txt",
    }

    for key, filename in file_map.items():
        content = results.get(key, "")
        with open(f"output/{filename}", "w", encoding="utf-8") as f:
            f.write(content)
    extracted_json_data = extract_chart_data_to_json(results, inputs)
    # Extract required data from results for the new v5.0 html_generator signature
    prediction_data = results.get("prediction_data", None)
    report_content = results.get("final_report", "")

    # Call generate_html_report expecting a single HTML string return
    raw_html = generate_html_report(
        report_content=report_content,
        inputs=inputs,
        results=results,
        prediction_data=prediction_data,
        extracted_chart_data=extracted_json_data
    )

    # Write the returned HTML string to a file
    with open("output/conferax_report.html", "w", encoding="utf-8") as f:
        f.write(raw_html)
    # NEW: Generate standalone agent pipeline graph
    graph_path = export_agent_graph("output")

    print("\n📁 All outputs saved to /output/")
    print("   ├── 01_strategy_profile.txt")
    print("   ├── 02_research_output.txt")
    print("   ├── 03a_sponsor_output.txt")
    print("   ├── 03b_exhibitor_output.txt")
    print("   ├── 04_speaker_output.txt")
    print("   ├── 05_venue_output.txt")
    print("   ├── 06_pricing_output.txt")
    print("   ├── 07_gtm_output.txt")
    print("   ├── 08_ops_output.txt")
    print("   ├── 09_devils_advocate.txt")
    print("   ├── 10_self_reflection.txt")
    print("   ├── 11_outreach_emails.txt      ←  9 email drafts")
    print("   ├── 12_decisions.txt")
    print("   ├── 13_final_report.txt")
    print("   └── conferax_report.html        ← Open in browser!")
    if graph_path:
        print("   ├── agent_pipeline.png          ←  Standalone Agent Graph")
    else:
        print("   ├── [Skipped] agent_pipeline.png (requires: pip install matplotlib networkx)")
        
    print("   └── conferax_report.html        ← Open in browser!")
def main():
    if not os.getenv("NVIDIA_API_KEY"):
        print("❌ ERROR: NVIDIA_API_KEY not set in environment or .env file")
        return

    if not os.getenv("TAVILY_API_KEY"):
        print("⚠️  WARNING: TAVILY_API_KEY not set — Phase 0 web research will be skipped")

    inputs  = collect_inputs()
    results = run_conferax(inputs)
    print_serpapi_summary(results)
    save_outputs(results, inputs)
    
    
    print("\n🏆 ConferaX v3.0 complete! Open output/conferax_report.html in your browser.\n")


if __name__ == "__main__":
    main()