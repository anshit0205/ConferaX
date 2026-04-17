# crew.py — ConferaX v3.0 Full Pipeline
# 11 Phases | 14 Agents | Prediction Engine | Outreach Agent
# Pass1 before agents | Pass2 after sponsor+exhibitor | Unified numbers throughout


from memory_system import retrieve_past_learnings, save_run_learnings
from dotenv import load_dotenv
load_dotenv()

import time
from crewai import Crew, Process

from agents import (
    orchestrator_agent, sponsor_agent, exhibitor_agent,
    speaker_agent, venue_agent, pricing_agent,
    gtm_agent, ops_agent, synthesizer_agent,
    outreach_agent
)
from agents_advanced import (
    research_agent, devils_advocate_agent,
    self_reflection_agent, decision_layer_agent
)
from tasks import (
    task_orchestrator, task_sponsor, task_exhibitor,
    task_speaker, task_venue, task_pricing,
    task_gtm, task_ops, task_outreach, task_synthesize
)
from tasks_advanced import (
    task_research, task_devils_advocate,
    task_self_reflection, task_decision_layer
)
from tavily_research import run_phase0_research
from prediction_engine import pass1, pass2
from thinking_indicators import (
    ThinkingIndicator, print_phase_header, print_agent_start,
    print_agent_result, print_conferax_banner, print_completion_summary
)

def print_serpapi_summary(results_dict: dict):
    """
    Scans all agent outputs for [SERPAPI] labels and prints a summary.
    Helps debug whether SerpAPI searches are actually happening.
    """
    import re
    total_serpapi_refs = 0
    print("\n  🔍 SerpAPI Usage Summary:")
    for key, output in results_dict.items():
        if not output or not isinstance(output, str):
            continue
        refs = len(re.findall(r'\[SERPAPI', output, re.IGNORECASE))
        if refs > 0:
            print(f"     {key}: {refs} SerpAPI reference(s)")
            total_serpapi_refs += refs
    print(f"     Total: {total_serpapi_refs} SerpAPI-verified data points\n")

def run_agent_with_indicator(crew_obj: Crew, agent_name: str,
                              phase: str, color: str = "cyan") -> str:
    indicator = ThinkingIndicator(agent_name, phase, color)
    indicator.start()
    try:
        result = crew_obj.kickoff()
        indicator.stop(success=True)
        return str(result)
    except Exception as e:
        indicator.stop(success=False)
        print(f"\n  ⚠️  {agent_name} error: {str(e)[:120]}")
        return f"[Agent output unavailable: {str(e)[:200]}]"


def run_conferax(inputs: dict) -> dict:
    """
    ConferaX v3.0 — Full 11-Phase Pipeline

    Phase 0:    Tavily Batch Search (10 parallel searches)
    Phase 0.5:  Prediction Engine Pass 1 (computed before any agent)
    Phase 1:    Orchestrator — Strategy Profile (with pass1 context)
    Phase 2:    Research Agent — Analyzes all 10 Tavily searches
    Phase 3a:   Sponsor Agent — Evidence-first (structured revenue output)
    Phase 3b:   Exhibitor Agent — Cvent/EventLocations (structured revenue output)
    Phase 3c:   Speaker Agent — Scholar/Semantic Scholar/arXiv
    Phase 3d:   Venue Agent — Cvent/EventLocations
    Phase 3e:   GTM Agent — Disboard + Cvent communities
    Phase 3.5:  Prediction Engine Pass 2 (reconciles sponsor+exhibitor estimates)
    Phase 4:    Pricing Agent — Validates and enriches prediction engine output
    Phase 5:    Operations & Risk — 7 workstreams
    Phase 6:    Devil's Advocate — Challenges all agents + prediction engine
    Phase 7:    Self-Reflection — Pipeline meta-analysis
    Phase 8:    Decision Layer — 10 final committed decisions (with pass2 context)
    Phase 9:    Outreach Agent — 9 personalized email drafts
    Phase 10:   Final Synthesis — Full report (with pass2 context, no conflicting numbers)
    """

    print_conferax_banner()
    pipeline_start = time.time()
    phases_done    = 0

    # ═══════════════════════════════════════════════════════
    # PHASE 0 — TAVILY BATCH SEARCH
    # ═══════════════════════════════════════════════════════
    print_phase_header(0, "Phase 0: Tavily Batch Web Search",
                       "10 targeted searches — Disboard + Cvent + Scholar/arXiv + Exhibitor")

    web_context = run_phase0_research(inputs)
    phases_done += 1

    # ═══════════════════════════════════════════════════════
    # PHASE 0.5 — PREDICTION ENGINE PASS 1
    # ═══════════════════════════════════════════════════════
    print_phase_header(0, "Phase 0.5: Prediction Engine Pass 1",
                       "Computing baseline from user inputs — grounding agents in quantitative reality")

    print("  🔢 Running prediction engine pass 1...")
    p1_data      = pass1(inputs)
    pass1_summary = p1_data["agent_summary"]
    print(f"  ✅ Pass 1 complete — "
          f"Pricing mode: {p1_data['pricing_mode']} | "
          f"Optimal price: ₹{p1_data['optimal_price']:,} | "
          f"Budget: ₹{int(p1_data['budget']):,}")
    phases_done += 1
    # ═══════════════════════════════════════════════════════
    # NEW: RETRIEVE PAST LEARNINGS
    # ═══════════════════════════════════════════════════════
    print("  🧠 Retrieving past system learnings...")
    past_learnings = retrieve_past_learnings(inputs.get("event_category", ""))
    # ═══════════════════════════════════════════════════════
    # PHASE 1 — ORCHESTRATOR
    # ═══════════════════════════════════════════════════════
    print_phase_header(1, "Central Orchestrator",
                       "Building strategy profile with prediction engine baseline & past learnings")
    print_agent_start("Central Orchestrator Agent",
                      "Interpret inputs + web data + prediction engine + memory → strategy profile")

    orch      = orchestrator_agent()
    orch_task = task_orchestrator(
        orch, inputs,
        web_context=web_context.get("orchestrator", ""),
        pass1_summary=pass1_summary,
        past_learnings=past_learnings
    )
    p1 = Crew(agents=[orch], tasks=[orch_task], process=Process.sequential, verbose=False)
    strategy_profile = run_agent_with_indicator(p1, "Central Orchestrator", "PHASE 1", "blue")
    print_agent_result("Central Orchestrator", strategy_profile)
    phases_done += 1
    time.sleep(8)

    # ═══════════════════════════════════════════════════════
    # PHASE 2 — RESEARCH AGENT
    # ═══════════════════════════════════════════════════════
    print_phase_header(2, "Research Intelligence Analysis",
                       "Analyzing all 10 Tavily searches")
    print_agent_start("Research Intelligence Agent",
                      "Extract intelligence, validate strategy profile")

    res      = research_agent()
    res_task = task_research(res, inputs, strategy_profile,
                             web_context=web_context.get("research", ""))
    p2 = Crew(agents=[res], tasks=[res_task], process=Process.sequential, verbose=False)
    research_output = run_agent_with_indicator(p2, "Research Intelligence Agent", "PHASE 2", "cyan")
    print_agent_result("Research Intelligence Agent", research_output)
    phases_done += 1
    time.sleep(10)

    # ═══════════════════════════════════════════════════════
    # PHASE 3 — SPECIALIST AGENTS
    # ═══════════════════════════════════════════════════════
    print_phase_header(3, "Specialist Intelligence Agents",
                       "Sponsor → Exhibitor → Speaker → Venue → GTM")

    # ── 3a: Sponsor ──────────────────────────────────────
    print_agent_start("Sponsor Intelligence Agent",
                      "Evidence-first dossiers — structured revenue output for prediction engine")
    sp      = sponsor_agent()
    sp_task = task_sponsor(sp, inputs, strategy_profile,
                           web_context=web_context.get("sponsor", ""))
    p3a = Crew(agents=[sp], tasks=[sp_task], process=Process.sequential, verbose=False)
    sponsor_output = run_agent_with_indicator(p3a, "Sponsor Intelligence Agent", "PHASE 3a", "yellow")
    print_agent_result("Sponsor Intelligence Agent", sponsor_output)
    time.sleep(10)

    # ── 3b: Exhibitor ────────────────────────────────────
    print_agent_start("Exhibitor Intelligence Agent",
                      "Cvent/EventLocations — structured revenue output for prediction engine")
    ex      = exhibitor_agent()
    ex_task = task_exhibitor(ex, inputs, strategy_profile,
                             web_context=web_context.get("exhibitor", ""))
    p3b = Crew(agents=[ex], tasks=[ex_task], process=Process.sequential, verbose=False)
    exhibitor_output = run_agent_with_indicator(p3b, "Exhibitor Intelligence Agent", "PHASE 3b", "green")
    print_agent_result("Exhibitor Intelligence Agent", exhibitor_output)
    time.sleep(10)

    # ── 3c: Speaker ──────────────────────────────────────
    print_agent_start("Speaker & Agenda Agent",
                      "Scholar / Semantic Scholar / arXiv / Sessionize vetting")
    spk      = speaker_agent()
    spk_task = task_speaker(spk, inputs, strategy_profile,
                            web_context=web_context.get("speaker", ""))
    p3c = Crew(agents=[spk], tasks=[spk_task], process=Process.sequential, verbose=False)
    speaker_output = run_agent_with_indicator(p3c, "Speaker & Agenda Agent", "PHASE 3c", "magenta")
    print_agent_result("Speaker & Agenda Agent", speaker_output)
    time.sleep(10)

    # ── 3d: Venue ────────────────────────────────────────
    print_agent_start("Venue Intelligence Agent",
                      "5 venues from Cvent/EventLocations — verify exhibitor floor space")
    v      = venue_agent()
    v_task = task_venue(v, inputs, strategy_profile,
                        web_context=web_context.get("venue", ""))
    p3d = Crew(agents=[v], tasks=[v_task], process=Process.sequential, verbose=False)
    venue_output = run_agent_with_indicator(p3d, "Venue Intelligence Agent", "PHASE 3d", "blue")
    print_agent_result("Venue Intelligence Agent", venue_output)
    time.sleep(10)

    # ── 3e: GTM ──────────────────────────────────────────
    print_agent_start("GTM & Audience Discovery Agent",
                      "Disboard Discord + Cvent + named channels")
    g      = gtm_agent()
    g_task = task_gtm(g, inputs, strategy_profile,
                      web_context=web_context.get("gtm", ""))
    p3e = Crew(agents=[g], tasks=[g_task], process=Process.sequential, verbose=False)
    gtm_output = run_agent_with_indicator(p3e, "GTM & Audience Discovery Agent", "PHASE 3e", "cyan")
    print_agent_result("GTM & Audience Discovery Agent", gtm_output)
    phases_done += 1
    time.sleep(10)

    # ═══════════════════════════════════════════════════════
    # PHASE 3.5 — PREDICTION ENGINE PASS 2
    # ═══════════════════════════════════════════════════════
    print_phase_header(3, "Phase 3.5: Prediction Engine Pass 2",
                       "Reconciling sponsor + exhibitor agent estimates with quantitative model")

    print("  🔢 Running prediction engine pass 2...")
    p2_data       = pass2(p1_data, sponsor_output, exhibitor_output)
    pass2_summary = p2_data["agent_summary"]
    print(f"  ✅ Pass 2 complete — "
          f"Final sponsor: ₹{p2_data['final_sponsor_rev']:,} | "
          f"Final exhibitor: ₹{p2_data['final_exhibitor_rev']:,} | "
          f"Total revenue P50: ₹{p2_data['monte_carlo']['p50']:,}")
    phases_done += 1

    # ═══════════════════════════════════════════════════════
    # PHASE 4 — PRICING & FOOTFALL
    # ═══════════════════════════════════════════════════════
    print_phase_header(4, "Pricing & Footfall Analysis",
                       "Validating and enriching prediction engine output with market intelligence")
    print_agent_start("Pricing & Footfall Agent",
                      "Validate computed prices vs market data — add qualitative reasoning")

    p_agent = pricing_agent()
    p_task  = task_pricing(
        p_agent, inputs, strategy_profile,
        speaker_output=speaker_output,
        sponsor_output=sponsor_output,
        venue_output=venue_output,
        exhibitor_output=exhibitor_output,
        web_context=web_context.get("pricing", ""),
        pass1_summary=pass1_summary,   # ← computed baseline
        pass2_summary=pass2_summary,   # ← reconciled numbers
    )
    p4 = Crew(agents=[p_agent], tasks=[p_task], process=Process.sequential, verbose=False)
    pricing_output = run_agent_with_indicator(p4, "Pricing & Footfall Agent", "PHASE 4", "yellow")
    print_agent_result("Pricing & Footfall Agent", pricing_output)
    phases_done += 1
    time.sleep(10)

    # ═══════════════════════════════════════════════════════
    # PHASE 5 — OPERATIONS & RISK
    # ═══════════════════════════════════════════════════════
    print_phase_header(5, "Operations & Risk Planning",
                       "7 workstreams including Exhibitor + Razorpay + Accessibility")
    print_agent_start("Event Ops & Risk Agent",
                      "Build execution plan with exhibitor floor ops + payment gateway")

    o      = ops_agent()
    o_task = task_ops(
        o, inputs, strategy_profile,
        venue_output=venue_output,
        speaker_output=speaker_output,
        sponsor_output=sponsor_output,
        exhibitor_output=exhibitor_output,
    )
    p5 = Crew(agents=[o], tasks=[o_task], process=Process.sequential, verbose=False)
    ops_output = run_agent_with_indicator(p5, "Event Ops & Risk Agent", "PHASE 5", "magenta")
    print_agent_result("Event Ops & Risk Agent", ops_output)
    phases_done += 1
    time.sleep(10)

    # ═══════════════════════════════════════════════════════
    # PHASE 6 — DEVIL'S ADVOCATE (v4.0)
    # ═══════════════════════════════════════════════════════
    print_phase_header(6, "Devil's Advocate — Quantitative Critical Challenger",
                       "Challenges engine numbers, uses benchmark comparisons, derives weakness score")
    print_agent_start("Devil's Advocate Agent",
                      "3 challenge types: logical + quantitative + benchmark. Event-adaptive.")

    da      = devils_advocate_agent()
    da_task = task_devils_advocate(
        da, inputs,
        strategy_profile=strategy_profile,
        sponsor_output=sponsor_output,
        exhibitor_output=exhibitor_output,
        speaker_output=speaker_output,
        venue_output=venue_output,
        pricing_output=pricing_output,
        gtm_output=gtm_output,
        ops_output=ops_output,
        research_output=research_output,
        pass2_summary=pass2_summary,   # ← NEW: DA now challenges the engine directly
    )
    p6 = Crew(agents=[da], tasks=[da_task], process=Process.sequential, verbose=False)
    devils_advocate_output = run_agent_with_indicator(p6, "Devil's Advocate", "PHASE 6", "red")
    print_agent_result("Devil's Advocate", devils_advocate_output)
    phases_done += 1
    time.sleep(10)
    
    # ═══════════════════════════════════════════════════════
    # PHASE 7 — SELF-REFLECTION (v4.0)
    # ═══════════════════════════════════════════════════════
    print_phase_header(7, "Self-Reflection — Structured Audit + Priority List",
                       "Scorecard table, data quality audit, DA fix eval, SR priority list for DL")
    print_agent_start("Self-Reflection Agent",
                      "Produces structured priority list that orders Decision Layer's decisions")

    all_outputs = {
        "strategy_profile":  strategy_profile,
        "research_output":   research_output,
        "sponsor_output":    sponsor_output,
        "exhibitor_output":  exhibitor_output,
        "speaker_output":    speaker_output,
        "venue_output":      venue_output,
        "pricing_output":    pricing_output,
        "gtm_output":        gtm_output,
        "ops_output":        ops_output,
    }

    sr      = self_reflection_agent()
    sr_task = task_self_reflection(sr, inputs, all_outputs, devils_advocate_output, pass2_summary=pass2_summary)
    p7 = Crew(agents=[sr], tasks=[sr_task], process=Process.sequential, verbose=False)
    self_reflection_output = run_agent_with_indicator(p7, "Self-Reflection Agent", "PHASE 7", "cyan")
    print_agent_result("Self-Reflection Agent", self_reflection_output)
    phases_done += 1
    time.sleep(10)

    # ═══════════════════════════════════════════════════════
    # PHASE 8 — DECISION LAYER (v4.0)
    # ═══════════════════════════════════════════════════════
    print_phase_header(8, "Decision Layer — 10 Committed, Specific Decisions",
                       "Uses SR priority list ordering + Pass2 numbers + DA challenges")
    print_agent_start("Decision Layer Agent",
                      "Confidence scores derived with formula. Budget arithmetic shown. Go/No-Go linked to engine.")

    all_outputs["devils_advocate_output"] = devils_advocate_output
    all_outputs["self_reflection_output"] = self_reflection_output

    # NOTE: Outreach output not yet available at this phase.
    # Decision Layer references email drafts by number (Draft 1, Draft 2, etc.)
    # The actual drafts are produced in Phase 9 based on DL decisions.
    # We pass a placeholder that tells DL what drafts will be available.
    outreach_placeholder = (
        "Outreach Agent will produce 9 email drafts after your decisions are committed:\n"
        "Draft 1: Title Sponsor pitch (Tier 1 top candidate)\n"
        "Draft 2: Gold Sponsor pitch (Tier 1 second candidate)\n"
        "Draft 3: Silver Sponsor pitch (Tier 2 top candidate)\n"
        "Draft 4: Keynote speaker invite (top choice)\n"
        "Draft 5: Panel/Workshop speaker invite\n"
        "Draft 6: Fireside chat speaker invite\n"
        "Draft 7: Exhibitor booth invite (Cluster A — Startup)\n"
        "Draft 8: Exhibitor booth invite (Cluster C — Tools)\n"
        "Draft 9: Exhibitor booth invite (Cluster B — Enterprise)\n"
        "Reference these by number in your 7-day action plan."
    )

    dl      = decision_layer_agent()
    dl_task = task_decision_layer(
        dl, inputs, all_outputs,
        devils_advocate_output,
        self_reflection_output,
        pass2_summary=pass2_summary,
        outreach_output=outreach_placeholder,  # placeholder — real drafts come in Phase 9
    )
    p8 = Crew(agents=[dl], tasks=[dl_task], process=Process.sequential, verbose=False)
    decision_output = run_agent_with_indicator(p8, "Decision Layer Agent", "PHASE 8", "green")
    print_agent_result("Decision Layer Agent", decision_output)
    phases_done += 1
    time.sleep(10)

    # ═══════════════════════════════════════════════════════
    # PHASE 9 — OUTREACH AGENT (v4.0 — now runs AFTER Decision Layer)
    # ═══════════════════════════════════════════════════════
    print_phase_header(9, "Outreach Drafting — 9 Personalized Emails",
                       "Uses Decision Layer's committed decisions to personalize outreach")
    print_agent_start("Outreach Agent",
                      "Emails now reflect DL's priority order and committed targets")

    out_agent = outreach_agent()
    out_task  = task_outreach(
        out_agent, inputs,
        sponsor_output=sponsor_output,
        speaker_output=speaker_output,
        exhibitor_output=exhibitor_output,
        pass2_summary=pass2_summary,
        decision_output=decision_output,  # ← NEW: outreach now aligned to DL decisions
    )
    p9 = Crew(agents=[out_agent], tasks=[out_task], process=Process.sequential, verbose=False)
    outreach_output = run_agent_with_indicator(p9, "Outreach Agent", "PHASE 9", "yellow")
    print_agent_result("Outreach Agent", outreach_output)
    phases_done += 1
    time.sleep(10)

    # ═══════════════════════════════════════════════════════
    # PHASE 10 — FINAL SYNTHESIS
    # ═══════════════════════════════════════════════════════
    print_phase_header(10, "Final Report Synthesis",
                        "Synthesizing all 14 agent outputs → full report, zero conflicting numbers")
    print_agent_start("Chief Strategy Officer (Synthesizer)",
                      "Reconcile all outputs + prediction engine → ConferaX report")

    enhanced_ops = (
        f"{ops_output}\\n\\n"
        f"=== DEVIL'S ADVOCATE CHALLENGES  ===\\n{devils_advocate_output}\\n\\n"
        f"=== SELF-REFLECTION AUDIT  ===\\n{self_reflection_output}\\n\\n"
        f"=== FINAL DECISIONS (10 committed decisions) ===\\n{decision_output}"
    )

    synth      = synthesizer_agent()
    synth_task = task_synthesize(
        synth, inputs,
        strategy_profile=strategy_profile,
        sponsor_output=sponsor_output,
        exhibitor_output=exhibitor_output,
        speaker_output=speaker_output,
        venue_output=venue_output,
        pricing_output=pricing_output,
        gtm_output=gtm_output,
        ops_output=enhanced_ops,
        outreach_output=outreach_output,
        pass2_summary=pass2_summary,   # ← authoritative numbers for report
    )
    p10 = Crew(agents=[synth], tasks=[synth_task], process=Process.sequential, verbose=False)
    final_report = run_agent_with_indicator(p10, "Chief Strategy Officer", "FINAL", "green")
    print_agent_result("Chief Strategy Officer", final_report)
    # ═══════════════════════════════════════════════════════
    # NEW: SAVE NEW LEARNINGS FOR NEXT RUN
    # ═══════════════════════════════════════════════════════
    print("  💾 Saving system learnings to memory bank...")
    save_run_learnings(
        event_category=inputs.get("event_category", "Unknown"),
        sr_text=self_reflection_output,
        da_text=devils_advocate_output
    )
    total_time = time.time() - pipeline_start
    print_completion_summary(phases_done, total_time, "output/conferax_report.html")
    #print_serpapi_summary(result)
    return {
        "strategy_profile":        strategy_profile,
        "research_output":         research_output,
        "sponsor_output":          sponsor_output,
        "exhibitor_output":        exhibitor_output,
        "speaker_output":          speaker_output,
        "venue_output":            venue_output,
        "pricing_output":          pricing_output,
        "gtm_output":              gtm_output,
        "ops_output":              ops_output,
        "devils_advocate_output":  devils_advocate_output,
        "self_reflection_output":  self_reflection_output,
        "decision_output":         decision_output,
        "outreach_output":         outreach_output,
        "final_report":            final_report,
        # Prediction engine data for HTML charts
        "prediction_data":         p2_data,    
    }
