# tasks.py — ConferaX v3.0
# SOTA prompts | Prediction Engine Integration | Outreach Task
# All tasks updated with prediction engine philosophy and context

from crewai import Task
from dotenv import load_dotenv
load_dotenv()

ZERO_TRUST_WORKFLOW = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 RESEARCH WORKFLOW & TOOL REQUIREMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Review the provided Phase 0 Tavily context.
2. If the Tavily context lacks specific, up-to-date numbers, budgets, or direct names required for this task, you MUST trigger your Search Tool to fill the gaps.
3. Do not guess, do not hallucinate, and do not use placeholders. If you don't know a fact, search for it.
"""
# ─────────────────────────────────────────────
# TASK 1 — ORCHESTRATOR
# ─────────────────────────────────────────────
def task_orchestrator(agent, inputs: dict,
                       web_context: str = "",
                       pass1_summary: str = "",
                       past_learnings: str = ""
                       ) -> Task:
    return Task(
        description=f"""
You are the CENTRAL ORCHESTRATOR of ConferaX — an autonomous conference intelligence engine.

Your job: deeply interpret ALL provided event inputs and produce a comprehensive
Internal Conference Strategy Profile that ALL downstream specialist agents will use —
including the Exhibitor Intelligence Agent and the Outreach Agent.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CRITICAL: PAST SYSTEM LEARNINGS (DO NOT REPEAT THESE MISTAKES)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The following are critical flaws, hallucinated data, or bad assumptions made by 
downstream agents in previous runs. 

{past_learnings}

YOUR DIRECTIVE: You MUST write explicit, targeted instructions in your 
"STRATEGIC DIRECTIVES FOR ALL AGENTS" section to prevent these specific mistakes 
from happening again. Preempt the failure.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREDICTION ENGINE CONTEXT — READ THIS FIRST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pass1_summary}

The prediction engine has computed the above quantitative baselines
from the user's inputs before you started reasoning.
These represent the mathematical reality of this event.

YOUR ROLE WITH THESE NUMBERS:
- Acknowledge them in your strategy profile
- Build qualitative strategic reasoning AROUND them
- Do not ignore or silently contradict them
- If you believe the computed ranges are wrong based on
  market knowledge, flag it explicitly with reasoning
- Your strategy directives to downstream agents must be
  consistent with these computed baselines

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL CHALLENGE HANDLING (address each explicitly):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. DATA FRAGMENTATION: Unify all scattered inputs into one coherent strategic view.
   Label every data point as [PROVIDED] or [INFERRED].

2. INCOMPLETE DATA: If any input is vague or missing, make a professional inference
   and flag it clearly. Never leave a gap unfilled.

3. CONFLICTING SIGNALS: If budget vs ambition conflict, flag the tension
   and propose a resolution path.

4. THREE-STREAM REVENUE MODEL: This event has THREE revenue streams —
   tickets + sponsors + exhibitors. The strategy profile must acknowledge all three
   and use the prediction engine's computed contribution ranges.

5. EXECUTION COMPLEXITY: Rate as Low / Medium / High / Critical with specific reasoning.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MANDATORY PROFILE DIMENSIONS (all required):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. AUDIENCE PROFILE
- Demographics, psychographics, pain points per persona
- What each persona cares about most
- Price sensitivity per persona (reference prediction engine elasticity values)
- Behavioral patterns (networking vs learning vs deal-making vs recruiting)

### 2. EVENT SCALE ASSESSMENT
- Scale classification (intimate / mid-scale / large / mega)
- Spatial requirements: plenary + breakout + EXHIBITOR FLOOR configuration
- Operational load estimate

### 3. THREE-STREAM REVENUE MODEL
- Ticket revenue potential — use prediction engine ranges as baseline
- Sponsor revenue potential range
- Exhibitor booth revenue potential range
- Combined total revenue estimate
- Which stream is most at risk and why

### 4. PRICE SENSITIVITY MATRIX
- Per-tier sensitivity analysis (informed by prediction engine persona profiles)
- Recommended tiering strategy with rationale
- Risk of overpricing vs underpricing for THIS specific audience

### 5. SPONSOR ATTRACTIVENESS SCORE (0-100)
- Why this event is attractive to sponsors
- What sponsors get (leads, brand, deal flow, community access)
- Estimated total sponsorship potential range

### 6. EXHIBITOR ATTRACTIVENESS ASSESSMENT
- What exhibitor categories are best suited to this event
- Why companies would pay for booth space here
- Recommended exhibitor clusters: Startup / Enterprise / Tools / Individual / Research Lab
- Estimated number of exhibitors and booth revenue range

### 7. VENUE TYPE FIT
- Ideal venue category
- Must-have technical requirements
- Exhibitor floor space minimum requirement
- City-specific considerations

### 8. CONTENT DEPTH FRAMEWORK
- Content mix percentages (visionary / technical / strategic / hands-on)
- Recommended session formats
- Content differentiation from competitor events

### 9. MARKET POSITIONING
- Where this event sits in the competitive landscape
- Unique positioning statement
- Key differentiators vs comparable events

### 10. ATTENDANCE POTENTIAL
- Realistic range: conservative / expected / optimistic
  (align with prediction engine attendance model)
- Key demand drivers
- Risk of under/over-attendance

### 11. EXECUTION COMPLEXITY RATING
- Overall: Low / Medium / High / Critical
- Top 3 hardest things to execute
- Recommended mitigation for each

### 12. STRATEGIC DIRECTIVES FOR ALL AGENTS
- Directive for Sponsor Agent (include that structured revenue estimates are needed)
- Directive for Exhibitor Agent (clusters to prioritize, structured revenue needed)
- Directive for Speaker Agent
- Directive for Venue Agent (note exhibitor floor space needed)
- Directive for Pricing Agent (validate prediction engine output, add market intelligence)
- Directive for GTM Agent
- Directive for Ops Agent (note exhibitor coordination workstream needed)
- Directive for Outreach Agent (which targets to prioritize for email drafts)
- Directive for Synthesizer Agent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USER INPUTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Event Category:          {inputs['event_category']}
Geography/Region:        {inputs['geography_region']}
Target Audience Size:    {inputs['target_audience_size']}
Event Date Range:        {inputs['event_date_range']}
Expected Duration:       {inputs['expected_duration']}
Event Format:            {inputs['event_format']}
Budget Range:            {inputs['budget_range']}
Audience Persona:        {inputs['expected_audience_persona']}
Venue Preferences:       {inputs['venue_preference_constraints']}
Sponsor Priority:        {inputs['sponsor_priority']}
Speaker Priority:        {inputs['speaker_priority']}
Ticketing Intent:        {inputs['ticketing_intent']}
Organizer Objective:     {inputs['organizer_objective']}
Hard Constraints:        {inputs['hard_constraints']}

{web_context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Structured text with clearly labeled sections.
Every claim marked [PROVIDED] or [INFERRED].
End with CONFIDENCE SUMMARY: overall score (0-100) and top 5 assumptions.
""",
        expected_output=(
            "Comprehensive Conference Strategy Profile covering all 12 dimensions. "
            "Includes specific preemptive directives based on past system learnings to prevent repeated mistakes. "
            "Three-stream revenue model consistent with prediction engine baselines. "
            "Exhibitor clusters defined. "
            "Strategic directives for all downstream agents including Outreach Agent. "
            "Every claim marked [PROVIDED] or [INFERRED]. "
            "Ends with confidence score and key assumptions."
        ),
        agent=agent,
    )


# ─────────────────────────────────────────────
# TASK 2 — SPONSOR INTELLIGENCE
# ─────────────────────────────────────────────
def task_sponsor(agent, inputs: dict, strategy_profile: str,
                 web_context: str = "",
                 pass1_summary: str = "") -> Task:
 
    # Derive budget band for prompt injection
    budget_str = inputs.get("budget_range", "₹50L").lower().replace(",","").replace(" ","")
    budget_band = "MID (₹25L–₹1Cr)"
    tier_guidance = "target mid-tier sponsors (₹5L–₹30L per deal)"
    startup_fee_range = "₹1L–₹8L"
    title_sponsor_range = "₹15L–₹40L"
    gold_range = "₹8L–₹20L"
    silver_range = "₹3L–₹10L"
    community_range = "₹50K–₹3L"
 
    if any(x in budget_str for x in ["crore","cr"]):
        val = float(''.join(c for c in budget_str if c.isdigit() or c=='.') or "1")
        if val >= 5:
            budget_band = "ENTERPRISE (>₹5Cr)"
            tier_guidance = "target Fortune 500 / Big 4 title sponsors (₹1Cr+ per deal)"
            startup_fee_range = "₹5L–₹25L"
            title_sponsor_range = "₹1Cr–₹3Cr"
            gold_range = "₹40L–₹1Cr"
            silver_range = "₹15L–₹40L"
            community_range = "₹3L–₹15L"
        elif val >= 1:
            budget_band = "LARGE (₹1Cr–₹5Cr)"
            tier_guidance = "target enterprise sponsors (₹20L–₹1.5Cr per deal)"
            startup_fee_range = "₹3L–₹15L"
            title_sponsor_range = "₹50L–₹1.5Cr"
            gold_range = "₹20L–₹50L"
            silver_range = "₹8L–₹25L"
            community_range = "₹2L–₹8L"
    elif any(x in budget_str for x in ["lakh","lac","25l","30l","40l","50l","60l","70l","80l","90l"]):
        pass  # keep MID defaults
    else:
        # assume small if nothing matched
        budget_band = "SMALL (<₹25L)"
        tier_guidance = "target community and startup sponsors (₹50K–₹5L per deal)"
        startup_fee_range = "₹50K–₹3L"
        title_sponsor_range = "₹5L–₹15L"
        gold_range = "₹2L–₹8L"
        silver_range = "₹75K–₹3L"
        community_range = "₹25K–₹1L"
 
    audience_size = inputs.get("target_audience_size", "500")
    geography     = inputs.get("geography_region", "India")
    category      = inputs.get("event_category", "Technology")
    persona       = inputs.get("expected_audience_persona", "founders, developers, investors")
    sponsor_prio  = inputs.get("sponsor_priority", "tech companies")
    objective     = inputs.get("organizer_objective", "brand building")
    date_range    = inputs.get("event_date_range", "2026")
 
    return Task(
        description=f"""
You are the SPONSOR INTELLIGENCE AGENT for ConferaX v4.0.
 
Your mission: Identify, evidence-verify, and rank the most realistic sponsors for this event
using a 7-phase methodology. Every recommendation must be backed by either Tavily web evidence
or a clearly flagged INFERRED label with reduced confidence.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  EVENT CONTEXT — READ AND ABSORB FULLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 
Category:          {category}
Geography:         {geography}
Audience Size:     {audience_size} people
Audience Persona:  {persona}
Event Date:        {date_range}
Budget Band:       {budget_band}
Sponsor Priority:  {sponsor_prio}
Organizer Goal:    {objective}
 
BUDGET-CALIBRATED TIER PRICING (use these ranges — do NOT exceed for this budget):
  Title Sponsor:    {title_sponsor_range}
  Gold Sponsor:     {gold_range}
  Silver Sponsor:   {silver_range}
  Community:        {community_range}
  Startup Cluster:  {startup_fee_range}
 
TIER STRATEGY: {tier_guidance}
 
PREDICTION ENGINE BASELINE:
{pass1_summary}
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PHASE 1 — EXTRACT FROM TAVILY WEB CONTEXT FIRST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Before proposing ANY sponsor from memory, read ALL the web context below.
Extract every company name that appears near these signals:
  - "sponsor", "presenting sponsor", "title partner", "gold sponsor"
  - Company name near event name in {geography} or adjacent regions
  - Company name near keywords: {category}, {sponsor_prio}
  - Recent marketing spend signals: funding announcements, product launches,
    new market entries, hiring surges, developer ecosystem programs
 
LIST ALL EXTRACTED COMPANY NAMES HERE before proceeding.
Format: Company | Source (Tavily/Cvent/Event Name) | Signal Type | Geography Match
 
This list IS your primary candidate pool. You may add candidates from memory
ONLY if they are well-known sponsors of comparable events AND labeled [INFERRED].
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PHASE 2 — GEOGRAPHY + HISTORICAL FREQUENCY FILTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
From your extracted candidate list, apply these priority filters:
 
PRIORITY 1 — SAME GEOGRAPHY, SAME CATEGORY (last 12 months):
  Companies that sponsored events in {geography} AND in {category} in the last 12 months.
  Historical Frequency Score: 1 event = +10pts | 2 events = +20pts | 3+ events = +35pts
  These sponsors have PROVEN willingness to spend in this exact market.
 
PRIORITY 2 — SAME GEOGRAPHY, ADJACENT CATEGORY (last 12 months):
  Companies that sponsored events in {geography} but in adjacent sectors.
  Historical Frequency Score: 1 event = +5pts | 2+ events = +15pts
 
PRIORITY 3 — SAME CATEGORY, ADJACENT GEOGRAPHY (last 12 months):
  Companies that sponsored {category} events but in other Indian cities or SEA.
  Historical Frequency Score: 1 event = +5pts | 2+ events = +10pts
  Outreach angle: "We're the {geography} version of [event they already sponsored]."
 
PRIORITY 4 — MARKETING SPEND SIGNAL (no direct sponsorship history):
  Companies with recent funding, product launches, or developer program announcements
  that make them motivated to sponsor NOW even without prior history.
  These are OPPORTUNISTIC — higher risk, higher upside.
 
Label every candidate with their Priority (1–4) before scoring.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PHASE 3 — EVIDENCE DOSSIER (mandatory for every sponsor)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For EACH candidate, answer all 5 points BEFORE scoring:
 
  (a) SPONSORSHIP HISTORY: Name the specific events they sponsored in last 12 months.
      Format: "[Event Name], [City], [Month Year], [Tier Level]"
      If sourced from Tavily: cite "Source: Tavily — [search query that returned this]"
      If inferred from memory: label [INFERRED — reduce confidence by 20pts]
 
  (b) ACTIVATION STYLE: How did they activate at those events?
      (Booth? Speaking slot? Workshop? Brand wall? Swag? Hackathon prize?)
      This tells you what budget to request and what activation to propose.
 
  (c) CURRENT MARKETING PRIORITY: What are they trying to achieve RIGHT NOW?
      (Product launch in India? Hiring 500 engineers? Developer ecosystem growth?
       Enterprise sales push? IPO brand building? Market entry in {geography}?)
      This is your outreach hook — match their priority to your event's audience.
 
  (d) AUDIENCE OVERLAP: What % of your event's audience matches their ICP?
      Be specific: "65% of our audience are developers — [Company]'s ICP is developers"
      NOT generic: "good audience fit"
 
  (e) BUDGET SIGNAL: What is their likely sponsorship budget range?
      Evidence: recent funding round size, employee count, marketing team size,
      comparable event sponsorship tier, regional marketing budget signals.
      Does this fit our {budget_band} tier pricing? YES / BORDERLINE / NO
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PHASE 4 — SCORING (only after dossier is complete)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score each candidate on 6 dimensions (0–100):
 
  Relevance (0–100):        Industry + audience persona match
  Feasibility (0–100):      Budget fit + decision speed + India presence
  Historical Frequency:     Auto-calculated from Priority filter above (+0 to +35)
  Impact (0–100):           Brand value + what they bring beyond money
  Cost Efficiency (0–100):  INR value per attendee marketing touchpoint
  Risk (0–100):             Likelihood of withdrawal, conflict, or slow close
 
  COMPOSITE = Relevance×0.28 + Feasibility×0.22 + Hist_Freq_Bonus + Impact×0.20 + CostEff×0.10 + (100-Risk)×0.10
  (Historical Frequency Bonus adds directly to composite: up to +35 points)
 
  Confidence Label:
    HIGH   = Tavily-sourced + Priority 1 or 2 + Budget fit confirmed
    MEDIUM = Inferred + Priority 3 + Budget borderline
    LOW    = Fully inferred + Priority 4 + Budget unconfirmed
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PHASE 5 — TIERED OUTPUT (all 5 tiers required)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 
For EACH sponsor in EACH tier, provide the complete block:
 
---
**[COMPANY NAME]** | [Tier Level] | Priority [1–4] | Composite: [score]/100
 
EVIDENCE DOSSIER:
  (a) Sponsorship History: [specific events, cities, dates, tiers]
      Source: [Tavily / Cvent / Event Name / INFERRED]
  (b) Activation Style: [what they did at those events]
  (c) Current Marketing Priority: [what they need right now]
  (d) Audience Overlap: [specific % and why — not generic]
  (e) Budget Signal: [why this tier price is realistic for them]
 
WHY THIS EVENT IS RIGHT FOR THEM NOW:
  [2-3 sentences connecting their current priority to THIS event's timing, audience, and geography]
 
SPONSORSHIP LEVEL: [Title / Gold / Silver / Community / Startup / In-Kind]
ESTIMATED VALUE:   [INR range — calibrated to {budget_band}]
LIKELIHOOD:        [High / Medium / Low] — [specific reason, not generic]
 
OUTREACH HOOK:
  [First-message angle — must reference their specific event from dossier point (a)
   AND connect to their marketing priority from point (c)
   AND propose ONE specific activation idea from point (b)]
 
ACTIVATION IDEAS:
  1. [Specific on-event activation matching their style]
  2. [Branded content or digital activation]
  3. [Post-event activation — report, leads, follow-up]
 
SCORES:
  Relevance: [X] | Feasibility: [X] | Hist. Freq. Bonus: [+X]
  Impact: [X] | Cost Efficiency: [X] | Risk: [X]
  COMPOSITE: [X]/100 | Confidence: [HIGH/MEDIUM/LOW]
 
TRADE-OFF: [What you give up by prioritizing them over another option]
---
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIER 1 — PRIMARY SPONSORS (2–4): Best fit, realistic budget, geo-proven
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
These are the sponsors you approach first, in the first week.
Every Tier 1 must be Priority 1 or 2 AND budget-confirmed.
If you cannot find 2 Priority 1/2 sponsors: explicitly say so and explain why.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIER 2 — FALLBACK SPONSORS (3–4): Good fit, approach in parallel
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
These are approached simultaneously with Tier 1 — not after.
They are fallbacks in terms of PREFERENCE, not in terms of timing.
Priority 2 or 3. May need geo-specific angle or longer close cycle.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIER 3 — STARTUP SPONSOR CLUSTER (3–5): MANDATORY, cannot be skipped
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Startups at funding stage: Seed → Series B.
Fee range for this event: {startup_fee_range}
Why startups are strategic here:
  - Faster decision cycle (founder can decide in 48 hours)
  - High activation energy (they WANT to prove themselves at the event)
  - Ecosystem credibility — the right startup sponsor signals community health
  - Often provide product access, API credits, or tools as supplementary value
 
For each startup: name, funding stage, product, why THIS audience = their ICP,
estimated fee, outreach angle (must be founder-direct, not marketing team).
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIER 4 — IN-KIND SPONSORS (2–3): Products / services / media
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
In-kind sponsors reduce cash costs rather than adding cash revenue.
Categories to target:
  - Venue or F&B partner (reduces catering cost)
  - Cloud or SaaS credits (reduces tech stack cost)
  - Media partner (amplifies reach — newspaper, podcast, newsletter)
  - Swag or print partner (reduces production cost)
For each: what they provide, estimated INR value of contribution, what we give in return.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIER 5 — ALTERNATIVE MONETIZATION (if pipeline collapses)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
If Tier 1 AND Tier 2 both fail entirely, what replaces that revenue?
Provide 3 specific alternatives with INR estimates:
  Option A: [e.g., paid masterclass / pre-event workshop]
  Option B: [e.g., premium delegate lounge / investor meet fee]
  Option C: [e.g., virtual attendance tier / event recording access]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PHASE 6 — FALLBACK SCENARIO PLANNING (mandatory, INR numbers)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Answer these 4 questions with EXACT INR numbers:
 
SCENARIO 1 — ALL TIER 1 DECLINE:
  What is total sponsor revenue from Tier 2 + Tier 3 + Tier 4 only?
  Is that enough to proceed? What must be cut from the event budget?
 
SCENARIO 2 — 50% TIER 2 CLOSE:
  What is realistic total sponsor revenue in this case?
  What % of the event's total budget does that cover?
 
SCENARIO 3 — ONLY STARTUP CLUSTER CLOSES:
  What is total revenue from Tier 3 alone?
  What does the event look like at that funding level?
 
SCENARIO 4 — MINIMUM VIABLE SPONSOR REVENUE:
  What is the MINIMUM total sponsor revenue that makes this event financially viable?
  Which specific sponsor combinations achieve that minimum?
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PHASE 7 — OUTREACH SEQUENCING CALENDAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For an event on {date_range}, produce a week-by-week outreach calendar:
 
  Week 1:  First contact to all Tier 1 + Tier 2 + Tier 3 simultaneously
  Week 2:  Follow-up to non-responders. Decision from fast-movers expected.
  Week 3:  Proposal decks sent to interested parties.
  Week 4:  LOI / agreement stage for Tier 1.
  Week 5:  Tier 3 startup outreach if Tier 1/2 pipeline is slow.
  Week 6:  In-kind sponsor approach.
  [Continue through to event date with specific milestones]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CONFERENCE STRATEGY PROFILE (context for all decisions)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{strategy_profile}
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 TAVILY WEB CONTEXT (extract ALL company names from here first)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{web_context}
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STRUCTURED REVENUE ESTIMATES (end of output, exact format)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 
These numbers feed the ConferaX Prediction Engine Pass 2.
They must be calibrated to:
  - Budget band: {budget_band}
  - Realistic close rates for Indian tech sponsorship (45–65% of outreached)
  - Comparable event sponsor packages from Tavily context
  - Only tiers that were confirmed as budget-realistic above
 
--- REVENUE ESTIMATES ---
Conservative: ₹[amount]
Expected:     ₹[amount]
Optimistic:   ₹[amount]
--- END REVENUE ESTIMATES ---
 
Conservative = Only Tier 3 (startup cluster) closes fully
Expected     = 2 Tier 1 + 2 Tier 2 + 3 Tier 3 + some in-kind
Optimistic   = All Tier 1 + most Tier 2 + full Tier 3 + all in-kind valued

{ZERO_TRUST_WORKFLOW}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL EXECUTION RULE (NO RAW TOOL CALLS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your Final Answer MUST be the fully written, completed Markdown report. 
- NEVER output raw tool-call tags (like `<tool_call>` or `<function>`) inside your Final Answer.
- If you need to use the SerpAPI tool, you must execute the tool properly in your thought process, wait for the observation, and ONLY write the Final Answer once you have the results.
- Do not output a "plan" to search. Actually perform the searches, read the data, and deliver the final synthesized analysis.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL QUALITY CHECK before submitting output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Did I extract all company names from Tavily context before proposing anyone?
☐ Is every Tier 1 sponsor confirmed as budget-realistic for {budget_band}?
☐ Did I include the startup cluster (Tier 3)?
☐ Did I complete all 4 fallback scenarios with INR numbers?
☐ Did I source every HIGH-confidence sponsor with a Tavily citation?
☐ Did I label every INFERRED sponsor clearly?
☐ Does the outreach hook reference a SPECIFIC past event, not a generic compliment?
☐ Are the revenue estimates calibrated (not optimistic, not deflated)?
☐ Is the STRUCTURED REVENUE ESTIMATES block present in exact format?
""",
        expected_output=(
            "Sponsor intelligence report with 5 tiers: "
            "Tier 1 Primary (2–4) + Tier 2 Fallback (3–4) + "
            "Tier 3 Startup Cluster (3–5) + Tier 4 In-Kind (2–3) + Tier 5 Alt Monetization. "
            "Phase 1 company extraction from Tavily web context listed explicitly. "
            "Every sponsor has full evidence dossier before scoring. "
            "All 6 scores + composite + confidence label per sponsor. "
            "Priority 1–4 geo/history filter applied to every candidate. "
            "4 fallback scenarios with exact INR numbers. "
            "Outreach sequencing calendar. "
            "STRUCTURED REVENUE ESTIMATES block in exact format at end."
        ),
        agent=agent,
    )


# ─────────────────────────────────────────────
# TASK 3 — EXHIBITOR INTELLIGENCE
# ─────────────────────────────────────────────
def task_exhibitor(agent, inputs: dict, strategy_profile: str,
                   web_context: str = "") -> Task:
    return Task(
        description=f"""
You are the EXHIBITOR INTELLIGENCE AGENT for ConferaX.

Your mission: Identify companies that exhibited at similar conferences and events
in the last 12 months, suggest relevant exhibitors for THIS event, and cluster them.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPORTANT — YOUR REVENUE ESTIMATES FEED THE PREDICTION ENGINE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
At the END of your output, you MUST include a structured revenue block
in the EXACT format below. This is parsed by the ConferaX Prediction Engine
to compute the final 3-stream P&L model and break-even analysis.

Your estimates must be grounded in real Cvent/EventLocations booth pricing data —
not optimistic guesses. The organizer's go/no-go decision depends on these numbers.

--- REVENUE ESTIMATES ---
Conservative: ₹[amount]
Expected:     ₹[amount]
Optimistic:   ₹[amount]
--- END REVENUE ESTIMATES ---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL DISTINCTION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Exhibitors ≠ Sponsors.
Sponsors pay for brand visibility and audience access.
Exhibitors pay for PHYSICAL FLOOR SPACE to demo and generate B2B leads.
Keep these categories separate. Do not mix them.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1 — RESEARCH PAST EXHIBITORS (from web context)
STEP 2 — SUGGEST POTENTIAL EXHIBITORS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For each exhibitor candidate:
- Company/Individual Name
- Past Exhibition Evidence
- Category Cluster (Step 3)
- Why they fit THIS event
- Booth Type: Standard (3×3m) / Premium (6×3m) / Demo Pod / Tabletop
- Estimated Booth Fee (INR)
- Lead Generation Potential
- Outreach Angle
- Relevance Score (0-100)
- Feasibility Score (0-100)
- Impact Score (0-100)
- Cost Efficiency Score (0-100)
- Risk Score (0-100)
- Confidence Label

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3 — CLUSTER BY CATEGORY (mandatory):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLUSTER A — STARTUPS: Seed to Series B. Standard/Tabletop booths.
CLUSTER B — ENTERPRISE: 500+ employees. Premium booths.
CLUSTER C — TOOLS & PLATFORMS: SaaS, APIs, dev platforms. Demo Pod.
CLUSTER D — INDIVIDUAL PRACTITIONERS: Consultants, coaches, authors. Tabletop.
CLUSTER E — RESEARCH LABS & ACADEMIA: Universities, think tanks. Standard.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4 — EXHIBITOR REVENUE MODEL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Recommended booths per cluster
- Booth fee per cluster (INR)
- Total exhibitor revenue: conservative / expected / optimistic
- % of total event revenue

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5 — EXPO FLOOR STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Floor layout logic (which clusters near which zones)
- Traffic flow optimization

{ZERO_TRUST_WORKFLOW}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL EXECUTION RULE (NO RAW TOOL CALLS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your Final Answer MUST be the fully written, completed Markdown report. 
- NEVER output raw tool-call tags (like `<tool_call>` or `<function>`) inside your Final Answer.
- If you need to use the SerpAPI tool, you must execute the tool properly in your thought process, wait for the observation, and ONLY write the Final Answer once you have the results.
- Do not output a "plan" to search. Actually perform the searches, read the data, and deliver the final synthesized analysis.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USER INPUTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Event Category:          {inputs['event_category']}
Geography:               {inputs['geography_region']}
Target Audience Size:    {inputs['target_audience_size']}
Audience Persona:        {inputs['expected_audience_persona']}
Budget Range:            {inputs['budget_range']}
Event Format:            {inputs['event_format']}
Venue Preferences:       {inputs['venue_preference_constraints']}

CONFERENCE STRATEGY PROFILE:
{strategy_profile}

{web_context}
""",
        expected_output=(
            "Exhibitor intelligence report with past exhibitor evidence, "
            "full candidate list with all 5 scores, "
            "5-cluster categorization, exhibitor revenue model, expo floor strategy. "
            "STRUCTURED REVENUE ESTIMATES block at the end in exact format."
        ),
        agent=agent,
    )


# ─────────────────────────────────────────────
# TASK 4 — SPEAKER & AGENDA
# ─────────────────────────────────────────────
def task_speaker(agent, inputs: dict, strategy_profile: str,
                 web_context: str = "") -> Task:
 
    from crewai import Task
 
    category     = inputs.get("event_category",            "AI & Technology")
    geography    = inputs.get("geography_region",          "Delhi, India")
    duration     = inputs.get("expected_duration",         "1 day")
    date         = inputs.get("event_date_range",          "May 2026")
    persona      = inputs.get("expected_audience_persona", "founders, developers, investors")
    budget       = inputs.get("budget_range",              "₹1 Crore")
    speaker_prio = inputs.get("speaker_priority",          "global thought leaders")
 
    return Task(
        description=f"""
You are the SPEAKER, ARTIST AND SUBJECT MATTER EXPERT DISCOVERY AGENT for ConferaX v4.0.
 
Your mission: Discover and vet the best speakers across all relevant archetypes
using archetype-specific sources and archetype-specific scoring.
Non-academic speakers are first-class citizens in this pipeline.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 EVENT CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Category:         {category}
Geography:        {geography}
Duration:         {duration}
Date:             {date}
Audience Persona: {persona}
Budget:           {budget}
Speaker Priority: {speaker_prio}
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 0 — ARCHETYPE DETECTION (do this before anything else)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Based on: Category [{category}] + Persona [{persona}] + Priority [{speaker_prio}]
 
State explicitly:
  Primary archetype(s) for this event: [Academic / Practitioner / Artist]
  Secondary archetype(s): [if applicable]
  Archetypes NOT applicable: [e.g., Artist if pure B2B tech summit]
 
This determines which scoring formula and which vetting sources apply.
Do NOT apply the Academic formula to Practitioners.
Do NOT apply the Artist formula to Academics.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 1 — EXTRACT FROM TAVILY WEB CONTEXT FIRST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Read ALL web context. Extract every person name found near:
  Academic signals:     "researcher, author, cited, h-index, arXiv, paper, professor"
  Practitioner signals: "speaker, keynote, panelist, CTO, founder, CEO, engineer,
                         product lead, Sessionize, Luma, Konfhub, HasGeek, NASSCOM,
                         GitHub, Substack, newsletter, podcast"
  Artist signals:       "performer, artist, musician, creator, YouTube, Instagram,
                         SoundCloud, live performance, TEDx, entertainment"
  Social signals:       "followers, subscribers, views, engagement"
 
LIST ALL EXTRACTED NAMES:
| Name | Source | Archetype Signal | Role/Company | Platform/Evidence | Geography |
Label additions from knowledge: [INFERRED]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 2 — VETTING SOURCES PER ARCHETYPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Apply ONLY the sources relevant to each candidate's archetype.
 
─── FOR ACADEMIC / RESEARCHER ───
Source 1 — Google Scholar:
  Find: h-index, total citations, recent paper titles in {category}
  Confidence: HIGH if found | MEDIUM if estimated | LOW if not found
 
Source 2 — Semantic Scholar:
  Find: domain authority ranking, most cited paper, co-author network
 
Source 3 — arXiv:
  Find: recent submissions (last 6 months), trending papers, topic match
 
Source 4 — Twitter/X (social reach):
  Query: "[name] twitter {category}"
  Find: follower count, engagement on research posts
 
Source 5 — Substack (optional, if they write):
  Find: newsletter name, subscriber count
 
Source 6 — LinkedIn public profile (via Tavily):
  Query: "[name] [institution] site:linkedin.com"
  Extract: role, institution, bio (public page only)
  Label: [PUBLIC PROFILE — via web search]
 
─── FOR PRACTITIONER / INDUSTRY EXPERT ───
Source 1 — Sessionize.com:
  Find: accepted talks count, event list, speaker profile
 
Source 2 — Luma / Konfhub / HasGeek / NASSCOM event pages:
  Find: past appearances, session titles, event names and dates
 
Source 3 — Conference website speaker archives:
  Find: TechSparks, Inc42 Summit, GITEX India, PyCon India, JSConf, etc.
 
Source 4 — LinkedIn public profile (via Tavily):
  Query: "[name] [company] [role] site:linkedin.com"
  Extract: current role, company, bio summary, connection count if visible
  Label: [PUBLIC PROFILE — via web search]
 
Source 5 — Twitter/X:
  Query: "[name] twitter {category} India"
  Find: follower count, recent posts about {category}
 
Source 6 — GitHub (for developer/tech events):
  Query: "[name] github {category} stars repositories"
  Find: notable repos, star count, contribution activity
  This is STRONG credibility signal for developer-focused events
 
Source 7 — YouTube:
  Query: "[name] youtube {category} talk workshop"
  Find: channel subscribers, video views, content type
 
Source 8 — Substack / Medium / Hashnode:
  Query: "[name] substack OR medium {category}"
  Find: publication name, subscriber count or follower count
 
Source 9 — Podcast (Spotify/Apple):
  Query: "[name] podcast Spotify Apple {category} India"
  Find: show name, episode count, listener signals
 
─── FOR ARTIST / PERFORMER ───
Source 1 — Instagram:
  Query: "[name] instagram artist performer {category}"
  Find: follower count, engagement rate, content type
  This is PRIMARY signal for artists — do not skip
 
Source 2 — YouTube:
  Query: "[name] youtube performance music {category}"
  Find: subscribers, video views, live performance content
 
Source 3 — Spotify / Apple Music / SoundCloud:
  Query: "[name] Spotify monthly listeners OR SoundCloud followers"
  Find: monthly listener count, follower count
 
Source 4 — Twitter/X:
  Find: follower count, engagement
 
Source 5 — Past event appearances:
  Query: "[name] performance conference corporate event India"
  Find: event names, dates, types of events performed at
 
Source 6 — Booking platform:
  Query: "[name] BookMyShow artist OR gigmit OR booking agency India"
  Find: booking presence, past bookings, rider info
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 3 — INFLUENCE SCORE (archetype-branching formula)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALWAYS state archetype FIRST, then apply that archetype's formula.
Never apply the wrong formula. Never penalize for N/A dimensions.
 
─── ACADEMIC FORMULA (max 100) ───
  Academic Authority (40%):
    h-index 20+ = 40 | 10–20 = 28 | 5–10 = 16 | <5 = 8 | Not found = 4
    arXiv submission last 6 months = +5 bonus (capped at 40)
  Social Reach (15%):
    Twitter 50K+ = 15 | 10K+ = 10 | 1K+ = 6 | <1K = 2
    Substack 5K+ subs = +3 bonus (capped at 15)
  Speaking History (20%):
    15+ verified talks = 20 | 8–15 = 14 | 3–8 = 8 | 1–3 = 4 | 0 = 0
  Topic Relevance (25%):
    Core topic + active researcher = 25 | Adjacent = 15 | Tangential = 5
  ACADEMIC INFLUENCE SCORE = sum (max 100)
 
─── PRACTITIONER FORMULA (max 100) ───
  Academic Authority: N/A — NOT SCORED, NOT PENALIZED
  Speaking History (35%):
    20+ verified talks = 35 | 10–20 = 25 | 5–10 = 15 | 1–5 = 8 | 0 = 0
  Social Reach (35%) — weighted sum across ALL platforms:
    Twitter/X:        100K+ = 20 | 50K+ = 15 | 10K+ = 10 | 1K+ = 5 | <1K = 1
    GitHub:           5K+ stars = +8 | 1K+ stars = +5 | active contributor = +3
    YouTube:          50K+ subs = +5 | 10K+ = +3 | present = +1
    Substack/Medium:  5K+ subs = +4 | 1K+ = +2 | present = +1
    Podcast:          show present = +3 | 10K+ listeners = +5
    (Social Reach total capped at 35)
  Topic Relevance (30%):
    Core topic + senior role (C-suite/founder/staff engineer) = 30
    Adjacent topic + senior role = 20
    Core topic + mid-level role = 18
    Tangential = 8
  PRACTITIONER INFLUENCE SCORE = sum (max 100)
 
─── ARTIST FORMULA (max 100) ───
  Academic Authority: N/A — NOT SCORED, NOT PENALIZED
  Performance History (30%):
    20+ paid performances = 30 | 10–20 = 22 | 5–10 = 14 | 1–5 = 7 | 0 = 0
  Social Reach (45%) — weighted sum across ALL platforms:
    Instagram:    500K+ = 30 | 100K+ = 22 | 50K+ = 16 | 10K+ = 10 | <10K = 4
    YouTube:      100K+ subs = +10 | 50K+ = +7 | 10K+ = +4 | present = +1
    Spotify/SC:   10K+ monthly = +5 | present = +2
    Twitter/X:    50K+ = +3 | present = +1
    (Social Reach capped at 45)
  Event Relevance (25%):
    Perfect fit (vibe + audience match) = 25
    Good fit = 16
    Acceptable fit = 8
  ARTIST INFLUENCE SCORE = sum (max 100)
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 4 — FULL CANDIDATE BLOCK (every speaker, every slot)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For every critical slot: TOP CHOICE + 2 ALTERNATIVES + 1 BACKUP.
Use this block template — skip sections that are N/A for the archetype:
 
---
**SLOT: [Name]** | [HH:MM–HH:MM] | [Keynote/Panel/Workshop/Performance]
 
TOP CHOICE: [Full Name]
  ARCHETYPE: [Academic / Practitioner / Artist]
 
  === ACADEMIC EVIDENCE (Academic archetype only) ===
  Google Scholar:
    h-index: [X] | Citations: [X] | Recent papers: [title, year]
    Source: [URL / "not found in Tavily context"]
  Semantic Scholar: [domain rank / key finding]
  arXiv: [recent paper title + date / "no recent submissions found"]
 
  === PRACTITIONER EVIDENCE (Practitioner archetype only) ===
  Speaking History:
    [Event Name, City, Month Year] — Source: [Sessionize/Luma/Konfhub/HasGeek/Conference site]
    [Event Name, City, Month Year] — Source: [same]
    Total verified talks: [X]
  LinkedIn (public web):
    Role: [extracted] | Company: [extracted] | Bio: [extracted if available]
    Label: [PUBLIC PROFILE — via web search]
    Source: Tavily query "[name] [company] site:linkedin.com"
  GitHub:
    Notable repos: [name, stars] | Contribution activity: [active/inactive]
    Source: Tavily query "[name] github {category}"
    (Skip if non-developer event)
  Podcast/Substack:
    [Show name, subscriber/listener count / "not found"]
 
  === ARTIST EVIDENCE (Artist archetype only) ===
  Instagram: [X] followers | Engagement: [high/med/low]
    Source: Tavily query "[name] instagram"
  YouTube: [X] subscribers | Notable videos: [title, views]
  Spotify/SoundCloud: [X] monthly listeners / followers
  Past performances: [Event Name, City, Year] | [Event Name, City, Year]
  Booking: [platform presence / corporate event history]
 
  === SOCIAL REACH (ALL archetypes) ===
  Twitter/X: [X] followers | Recent relevant post: [topic / "not found"]
    Source: Tavily query "[name] twitter {category}"
 
  === INFLUENCE SCORE ===
  Archetype formula applied: [Academic / Practitioner / Artist]
  Speaking/Performance History: [X/35 or X/30 or X/20]
  Social Reach:                 [X/35 or X/45 or X/15]
  Academic Authority:           [X/40 or N/A]
  Topic Relevance:              [X/30 or X/25]
  INFLUENCE SCORE:              [X]/100
  Evidence confidence:          [HIGH / MEDIUM / LOW]
    HIGH = 3+ sources confirmed via Tavily
    MEDIUM = 1–2 sources confirmed + rest inferred
    LOW = fully inferred — flagged
 
  Topical Fit:      [why perfect for this slot and this audience]
  Availability:     [High / Medium / Low] — [reason]
  Budget Fit:       [Within / Borderline / Over] — [estimated fee range in INR]
  Geography:        [Based in / travel from]
 
  OUTREACH HOOK:
    [Reference ONE specific verifiable item:]
    Academic:     "Your paper [title] on arXiv ([month year]) addresses exactly what
                  our [X] developer/researcher audience is working on right now..."
    Practitioner: "Your talk at [Event Name, City, Date] on [topic] is the kind of
                  applied depth our [persona] audience is hungry for..."
    Artist:       "Your performance at [Event/YouTube video] got [X] views/reactions —
                  that energy is exactly what we want to close our networking session..."
 
  CONFLICT CHECK: ✅ No conflict | ⚠️ [flag if double-booked or org concentration risk]
 
ALTERNATIVE 1: [Name] | Archetype: [X] | Influence: [X]/100 | Why: [1 sentence]
ALTERNATIVE 2: [Name] | Archetype: [X] | Influence: [X]/100 | Why: [1 sentence]
BACKUP:        [Name] | Archetype: [X] | Influence: [X]/100 | Availability: HIGH | Why safe: [1 sentence]
---
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 5 — AGENDA NARRATIVE ARC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Design agenda for {duration} as a narrative arc.
 
ARCHETYPE-ENERGY PLACEMENT RULES:
  Morning (high attention):   Academic keynotes, deep technical practitioner talks
  Late morning:               Practitioner panels, case studies, applied sessions
  Post-lunch (energy dip):    Interactive workshops, Q&A panels, NOT solo keynotes
  Afternoon:                  Workshops, breakouts, practitioner masterclasses
  Networking/Closing:         Artist/performer, lighter practitioner fireside chats
 
SLOT TIMING RULES:
  Keynote: 30–45 min | Panel: 45–60 min | Workshop: 60–90 min
  Artist: 20–30 min | Break: 15 min | Lunch: 60–75 min
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 6 — CONFLICT DETECTION (all 5 checks)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHECK 1 — Speaker double-booking: same speaker in 2 simultaneous slots?
CHECK 2 — Org concentration: 2 consecutive keynotes from same company?
CHECK 3 — Topic repetition: same topic within 2 hours?
CHECK 4 — Room transition: 15 min buffer between sessions in same room?
CHECK 5 — Energy management: high-energy format at post-lunch slot?
 
Result per check: ✅ PASS or ⚠️ CONFLICT FOUND — [detail + fix]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 7 — FINAL TABLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 
AGENDA-SPEAKER MAPPING TABLE (conflict-free):
| Time | Session | Topic | Archetype | Speaker | Influence | Backup | Conflict |
|------|---------|-------|-----------|---------|-----------|--------|----------|
 
SPEAKER BUDGET TABLE:
| Speaker | Archetype | Fee Range | Travel | Accommodation | Total |
|---------|-----------|-----------|--------|---------------|-------|
Total speaker budget: ₹[X] conservative / ₹[X] expected
% of total budget {budget}: [X]%
 
INFLUENCE LEADERBOARD (top 10 candidates ranked by influence score):
| Rank | Name | Archetype | Score | Top Evidence | Availability |
|------|------|-----------|-------|--------------|-------------|
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STRATEGY PROFILE AND WEB CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONFERENCE STRATEGY PROFILE:
{strategy_profile}
 
TAVILY WEB CONTEXT (extract ALL names from here first):
{web_context}

{ZERO_TRUST_WORKFLOW}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL EXECUTION RULE (NO RAW TOOL CALLS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your Final Answer MUST be the fully written, completed Markdown report. 
- NEVER output raw tool-call tags (like `<tool_call>` or `<function>`) inside your Final Answer.
- If you need to use the SerpAPI tool, you must execute the tool properly in your thought process, wait for the observation, and ONLY write the Final Answer once you have the results.
- Do not output a "plan" to search. Actually perform the searches, read the data, and deliver the final synthesized analysis. 

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL OUTPUT REQUIREMENT: THE SPEAKER DATA MATRIX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
At the very end of your report, you MUST output a strict Markdown table summarizing your top 4-6 speakers. 
This table is read by a downstream JSON parser, so you must follow these rules perfectly:
- All score columns MUST be raw integers from 0 to 100. Do not use ranges (e.g., "80-90"), do not use percentages (e.g., "80%"), and do not use text (e.g., "High"). 
- 'Pipeline Status' must be exactly one of: Confirmed, Pending, or Backup.
- 'Archetype' must be short (e.g., Practitioner, Academic, Executive).

Format your table EXACTLY like this:

### SPEAKER DATA MATRIX
| Name | Archetype | Pipeline Status | Influence Score | Topic Fit | Availability | Social Reach | Speaking History |
|---|---|---|---|---|---|---|---|
| Jane Doe | Executive | Confirmed | 88 | 92 | 45 | 75 | 80 |
| John Smith | Academic | Pending | 65 | 95 | 80 | 40 | 90 |
| [Continue for all recommended speakers...] |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL QUALITY CHECK:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Did I state which archetypes apply to THIS event before starting?
☐ Did I extract all names from Tavily context first?
☐ Did I apply the CORRECT formula per archetype (no cross-contamination)?
☐ Is Academic Authority marked N/A for Practitioners and Artists?
☐ Did I check GitHub for practitioner speakers at developer events?
☐ Did I check Instagram + Spotify for artist speakers?
☐ Did I check Substack/Medium/Podcast for practitioner speakers?
☐ Does every HIGH-confidence score have 3+ Tavily-sourced data points?
☐ Does every outreach hook reference ONE specific verifiable item?
☐ Are all 5 conflict checks run and shown?
☐ Are the 3 final tables complete (agenda mapping, budget, influence leaderboard)?
""",
        expected_output=(
            "Speaker report with archetype detection stated upfront. "
            "Tavily extraction listed before any candidates proposed. "
            "Archetype-specific vetting applied — Academic uses Scholar/arXiv, "
            "Practitioner uses Sessionize/LinkedIn/GitHub/Substack/Podcast, "
            "Artist uses Instagram/YouTube/Spotify. "
            "Archetype-branching influence score (no cross-penalization). "
            "All platforms covered per archetype with source labels. "
            "Every critical slot: Top + 2 Alternatives + 1 Backup. "
            "5 conflict checks run with pass/fail. "
            "3 final tables: agenda mapping, budget, influence leaderboard."
        ),
        agent=agent,
    )


# ─────────────────────────────────────────────
# TASK 5 — VENUE INTELLIGENCE
# ─────────────────────────────────────────────
def task_venue(agent, inputs: dict, strategy_profile: str,
               web_context: str = "") -> Task:
 
    geography   = inputs.get("geography_region",            "Delhi, India")
    size        = inputs.get("target_audience_size",         "1000")
    budget      = inputs.get("budget_range",                 "₹1 Crore")
    constraints = inputs.get("hard_constraints",             "wheelchair accessible")
    venue_pref  = inputs.get("venue_preference_constraints", "indoor, premium")
    format_     = inputs.get("event_format",                 "Summit")
    date        = inputs.get("event_date_range",             "May 2026")
 
    # Estimate venue budget allocation
    venue_budget_note = (
        f"Event budget: {budget}. "
        f"Typical venue allocation: 25–35% of total budget for venue hire + AV + basic F&B. "
        f"Use this to compute the hard budget ceiling for venue day rate."
    )
 
    return Task(
        description=f"""
You are the VENUE INTELLIGENCE AGENT for ConferaX v4.0.
 
Your mission: Recommend 5 venues using a budget-first, footfall-aware methodology
sourced from Cvent.com, EventLocations.com, and Tavily web data.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  EVENT CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Geography:         {geography}
Expected Audience: {size} people
Budget:            {budget}
{venue_budget_note}
Format:            {format_}
Date:              {date}
Venue Preference:  {venue_pref}
Hard Constraints:  {constraints}
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PHASE 1 — BUDGET HARD GATE (run before any other evaluation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1: Compute venue budget ceiling.
  Total budget: {budget}
  Venue allocation (25–35%): ₹[X] – ₹[Y]
  This is the MAXIMUM you will spend on venue hire per day.
 
Step 2: For every candidate venue, label immediately:
  WITHIN BUDGET:   Day rate ≤ lower allocation estimate
  BORDERLINE:      Day rate between lower and upper estimate
  OVER BUDGET:     Day rate > upper allocation estimate → ELIMINATED unless exceptional
 
Step 3: Only WITHIN BUDGET and BORDERLINE venues proceed to full evaluation.
If you cannot find 5 budget-compliant venues: say so explicitly,
explain what trade-offs allow borderline venues to proceed,
and recommend negotiation tactics (off-peak day rate, F&B minimum waiver, etc.).
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PHASE 2 — EXTRACT FROM TAVILY WEB CONTEXT FIRST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Before proposing any venue from memory, read ALL web context below.
Extract every venue name found near these signals:
  - Conference, summit, expo, tech event in {geography}
  - Venue name near capacity numbers or event attendance
  - Cvent.com listings for {geography}
  - EventLocations.com results for {geography}
  - Past event reviews or articles mentioning specific venues
 
LIST ALL EXTRACTED VENUES:
Format: Venue Name | Source | Capacity (if found) | Past Events (if found) | Budget Signal
 
Add from knowledge only if labeled [INFERRED — not from Tavily data].
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PHASE 3 — FULL VENUE EVALUATION BLOCK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For EACH of the 5 venues, complete this full block:
 
---
**[VENUE NAME]** | [City, Neighbourhood] | Budget Status: [WITHIN/BORDERLINE/OVER]
 
SOURCE:
  Primary:   [Cvent listing / EventLocations / Tavily web result / INFERRED]
  Confidence:[HIGH = Cvent verified | MEDIUM = comparable data | LOW = general knowledge]
 
SPECIFICATIONS:
  Main Hall Capacity:    Theater [X] | Banquet [X] | Cocktail [X]
  Breakout Rooms:        [number] rooms × [capacity each]
  Total Area:            [sq ft or sq m if known]
  Day Rate:              ₹[X] per day (Source: [Cvent / quote / estimate])
  Budget Status:         [WITHIN / BORDERLINE / OVER] — [reasoning]
 
PAST EVENT USAGE (from Tavily web context):
  Event 1: [Event Name] | [Date] | [Attendance] | [Category]
  Event 2: [Event Name] | [Date] | [Attendance] | [Category]
  Source: [Tavily result / conference website / news article / INFERRED]
  Confidence: [HIGH if Tavily-sourced | LOW if inferred]
 
FOOTFALL ANALYSIS:
  Entry/Exit Flow:
    Can {size} people enter in 20 min? [YES/NO/RISK] — [detail]
    Number of entry gates/doors: [X]
    Registration queue space: [adequate / tight / insufficient]
 
  Internal Flow:
    Hallway width between main hall and breakouts: [wide/narrow]
    Bottleneck risk points: [describe]
    Estimated flow time main hall → breakout: [X] min
 
  Exhibitor Floor Footfall:
    Floor position: [on main traffic path / side room / separate floor]
    Natural footfall drivers: [near F&B / near registration / near toilets / isolated]
    EXHIBITOR FOOTFALL SCORE: [1–10]
      10 = every attendee passes through twice
      1  = requires deliberate detour
    Recommendation: [acceptable if ≥6 / flag if <6]
 
EXHIBITOR FLOOR CAPACITY:
  Standard booths (3×3m): [X] booths
  Premium booths (6×3m):  [X] booths
  Demo pods:              [X] pods
  Recommended layout:     [brief description]
 
TECHNICAL INFRASTRUCTURE:
  AV:      [in-house / external required]
  Wi-Fi:   [capacity / dedicated lines available]
  Power:   [adequate / requires upgrade for exhibitors]
  Staging: [permanent / temporary required]
 
ACCESSIBILITY COMPLIANCE:
  ☐ Wheelchair ramps at all entry points
  ☐ Accessible toilets on each floor used
  ☐ Elevator access to all event floors
  ☐ Hearing loop / PA system
  ☐ Accessible parking
  ☐ Step-free path from parking to main hall
  Status: [FULLY COMPLIANT / PARTIALLY COMPLIANT (gaps listed) / NON-COMPLIANT]
 
NEIGHBOURHOOD CONTEXT:
  Nearest metro station: [name] — [X] min walk
  Airport distance:      [X] km / [X] min
  Hotels within 1km:     [number] — [price range]
  F&B within 500m:       [adequate / limited]
 
AVAILABILITY RISK:
  For {date}: [LOW / MEDIUM / HIGH / UNKNOWN]
  Reasoning: [peak season? competing events? typical lead time for this venue?]
  Action: [book site visit within X weeks / confirm availability immediately]
 
DIMENSION SCORES (0–100):
  Relevance:        [X] — [why]
  Feasibility:      [X] — [why]
  Impact:           [X] — [why]
  Cost Efficiency:  [X] — [why]
  Risk:             [X] — [why]
  COMPOSITE:        [weighted average]
 
TRADE-OFF vs BEST OPTION:
  What you gain: [1 sentence]
  What you give up: [1 sentence]
  Choose this when: [specific condition that makes this better than Best Option]
---
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  REQUIRED 5-VENUE STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEST OPTION:          Highest composite score, budget compliant, proven past usage
PREMIUM ALTERNATIVE:  Better specs but borderline budget — worth it if sponsors close
BALANCED OPTION:      Good footfall + good price, minor trade-offs
BUDGET OPTION:        Clearly within budget, acceptable specs, lower footfall score
FALLBACK:             Different geography or format — if all above unavailable
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HARD CONSTRAINTS VERIFICATION: {constraints}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For every hard constraint listed above:
  Constraint: [X] → Status at each venue: [MET / NOT MET / UNKNOWN]
If any venue fails a hard constraint: ELIMINATE it and say so explicitly.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VENUE COMPARISON TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
| Venue | Budget | Capacity | Exhibitor Booths | Footfall Score | Past Events | Composite |
|-------|--------|----------|-----------------|----------------|-------------|-----------|
| [V1]  | Within | [X]      | [X]             | [X]/10         | [X events]  | [X]/100   |
[complete for all 5]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STRATEGY PROFILE AND WEB CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONFERENCE STRATEGY PROFILE:
{strategy_profile}
 
TAVILY WEB CONTEXT (extract ALL venue names from here first):
{web_context}

{ZERO_TRUST_WORKFLOW}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL EXECUTION RULE (NO RAW TOOL CALLS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your Final Answer MUST be the fully written, completed Markdown report. 
- NEVER output raw tool-call tags (like `<tool_call>` or `<function>`) inside your Final Answer.
- If you need to use the SerpAPI tool, you must execute the tool properly in your thought process, wait for the observation, and ONLY write the Final Answer once you have the results.
- Do not output a "plan" to search. Actually perform the searches, read the data, and deliver the final synthesized analysis. 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL QUALITY CHECK:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Did I compute budget ceiling and label every venue WITHIN/BORDERLINE/OVER?
☐ Did I eliminate OVER BUDGET venues (or justify keeping borderline ones)?
☐ Did I extract venue names from Tavily before proposing from memory?
☐ Does every venue have past event usage (Tavily-sourced or INFERRED labeled)?
☐ Does every venue have a footfall analysis with EXHIBITOR FOOTFALL SCORE?
☐ Does every venue have exhibitor booth capacity (standard + premium + demo)?
☐ Does every venue have full accessibility checklist?
☐ Did I check every hard constraint: {constraints}?
☐ Did I flag availability risk for {date}?
☐ Is the venue comparison table complete?
""",
        expected_output=(
            "Venue report with 5 options (Best/Premium/Balanced/Budget/Fallback). "
            "Budget hard gate computed and applied — OVER BUDGET venues eliminated. "
            "Every venue sourced from Tavily/Cvent with confidence label. "
            "Past event usage listed with real event names and dates. "
            "Footfall analysis with EXHIBITOR FOOTFALL SCORE (1–10) per venue. "
            "Exhibitor floor capacity (standard + premium + demo booths). "
            "Full accessibility compliance checklist per venue. "
            "Hard constraints verified per venue. "
            "Availability risk flagged for {date}. "
            "Venue comparison table."
        ),
        agent=agent,
    )


# ─────────────────────────────────────────────
# TASK 6 — PRICING & FOOTFALL
# ─────────────────────────────────────────────
def task_pricing(agent, inputs: dict, strategy_profile: str,
                 speaker_output: str, sponsor_output: str,
                 venue_output: str, exhibitor_output: str,
                 web_context: str = "",
                 pass1_summary: str = "",
                 pass2_summary: str = "") -> Task:
    return Task(
        description=f"""
You are the PRICING AND FOOTFALL AGENT for ConferaX.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREDICTION ENGINE OUTPUT — YOUR QUANTITATIVE FOUNDATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pass1_summary}

{pass2_summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR ROLE — THE ENGINE COMPUTES, YOU REASON:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The ConferaX Prediction Engine has already computed:
- Optimal ticket price across all 3 revenue streams
- Price vs attendance elasticity curve for this specific audience
- Monte Carlo revenue distribution (10,000 simulations)
- Break-even attendance at each tier
- Week-by-week revenue projection
- Tier structure optimized for this audience's VIP propensity

YOUR JOB IS NOT to invent pricing from scratch.
🚨 EDGE CASE HANDLING (READ CAREFULLY):
If the ticketing intent is 'free' or 'invite_only':
- DO NOT attempt to analyze ticket price elasticity or ticket revenue (it is zero).
- INSTEAD, focus 100% of your reasoning on Sponsor ROI, Exhibitor ROI, and how the organizer covers costs without ticket revenue.
- Skip the ticket-related scenario simulations and replace them with risk scenarios about high no-show rates (for free events) or RSVP drop-offs (for invite-only).

If the event is paid (tiered, fixed, hybrid), proceed with the standard analysis:

YOUR JOB IS to:

1. VALIDATE against real Indian market data:
   - Do comparable events (TechSparks, NASSCOM, PyCon India, GITEX India) 
     confirm these price ranges?
   - What do Tavily search results show about actual ticket prices for
     similar events in {inputs['geography_region']}?

2. ADD QUALITATIVE REASONING the model cannot compute:
   - Why does this specific price work for {inputs['expected_audience_persona']}?
   - What inclusions make the VIP tier compelling for this audience?
   - What early bird deadline timing works for this event category?
   - Are there seasonal demand factors in {inputs['event_date_range']}?

3. ADJUST with evidence if market data contradicts the model:
   - If Tavily shows comparable events price significantly differently,
     say so explicitly, cite your source, and explain which to trust
   - Do NOT silently use different numbers without a cited source

4. EXPLAIN the break-even safety margin in practical terms:
   - What does "81% safety margin" mean for the organizer?
   - What scenarios would push them below break-even?

5. ENRICH the scenario simulations with qualitative context:
   - What specifically would cause the P90 outcome?
   - What would push toward P10?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THREE-STREAM REVENUE MODEL (use prediction engine numbers as base):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STREAM 1 — TICKET REVENUE
Validate the computed tier structure. Add qualitative context.
State the recommended payment gateway: Razorpay (primary) / Instamojo (backup).
Note India-specific no-show rates — use computed rate as baseline.

STREAM 2 — SPONSOR REVENUE
Use the reconciled sponsor estimate from the prediction engine.

STREAM 3 — EXHIBITOR BOOTH REVENUE
Use the reconciled exhibitor estimate from the prediction engine.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 SCENARIO SIMULATIONS (exact INR numbers required):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Ticket price +25% — impact on attendance and total revenue?
2. Star keynote confirmed — attendance lift and demand elasticity?
3. Venue downgraded to budget option — savings vs price adjustment?
4. Exhibitor program sells out — total revenue impact?
5. 35% no-show on day — revenue and ops impact across all 3 streams?

{ZERO_TRUST_WORKFLOW}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL EXECUTION RULE (NO RAW TOOL CALLS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your Final Answer MUST be the fully written, completed Markdown report. 
- NEVER output raw tool-call tags (like `<tool_call>` or `<function>`) inside your Final Answer.
- If you need to use the SerpAPI tool, you must execute the tool properly in your thought process, wait for the observation, and ONLY write the Final Answer once you have the results.
- Do not output a "plan" to search. Actually perform the searches, read the data, and deliver the final synthesized analysis. 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USER INPUTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Event Category:          {inputs['event_category']}
Target Audience Size:    {inputs['target_audience_size']}
Budget Range:            {inputs['budget_range']}
Ticketing Intent:        {inputs['ticketing_intent']}
Organizer Objective:     {inputs['organizer_objective']}
Date Range:              {inputs['event_date_range']}

STRATEGY PROFILE:    {strategy_profile}
SPEAKER OUTPUT:      {speaker_output}
SPONSOR OUTPUT:      {sponsor_output}
VENUE OUTPUT:        {venue_output}
EXHIBITOR OUTPUT:    {exhibitor_output}

{web_context}
""",
        expected_output=(
            "Pricing report validating and enriching prediction engine output. "
            "Market validation against comparable Indian events. "
            "Qualitative reasoning for WHY computed prices work for this audience. "
            "Any contradictions with market data explicitly flagged with evidence. "
            "5 scenario simulations with exact INR numbers. "
            "Razorpay/Instamojo payment gateway notes. "
            "Combined 3-stream revenue table referencing prediction engine numbers."
        ),
        agent=agent,
    )


# ─────────────────────────────────────────────
# TASK 7 — GTM & AUDIENCE DISCOVERY
# ─────────────────────────────────────────────
def task_gtm(agent, inputs: dict, strategy_profile: str,
             web_context: str = "") -> Task:
 
    category  = inputs.get("event_category",            "AI & Technology")
    geography = inputs.get("geography_region",           "Delhi, India")
    persona   = inputs.get("expected_audience_persona",  "founders, developers, investors")
    budget    = inputs.get("budget_range",               "₹1 Crore")
    objective = inputs.get("organizer_objective",        "brand building and community growth")
    date      = inputs.get("event_date_range",           "May 2026")
    size      = inputs.get("target_audience_size",       "1000")
    format_   = inputs.get("event_format",               "Summit")
 
    return Task(
        description=f"""
You are the GTM AND AUDIENCE DISCOVERY AGENT for ConferaX v4.0.
 
Your mission: Build a complete, channel-specific, execution-ready GTM plan
covering 8 platform types with named communities, exact posting specs,
paid channel targeting, influencer identification, and cost-per-registration rankings.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  EVENT CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Category:        {category}
Geography:       {geography}
Target Audience: {size} people
Persona:         {persona}
Event Date:      {date}
Format:          {format_}
Budget:          {budget}
Objective:       {objective}
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 1 — AUDIENCE SEGMENTATION (4–6 clusters)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Segment {persona} into 4–6 distinct clusters.
For each cluster define:
  - Who they are (role, seniority, company stage)
  - What they want from this event (their primary motivation)
  - Their FOMO trigger (what makes them register NOW vs later)
  - Which platforms they are most active on
  - Best day + time to reach them
  - Message tone (technical / aspirational / social proof / FOMO)
 
Example cluster format:
  CLUSTER A — [Name]
  Who: [description]
  Primary motivation: [what they want]
  FOMO trigger: [specific fear of missing out]
  Primary platforms: [list]
  Best reach time: [day + time IST]
  Message tone: [type]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 2 — EXTRACT FROM TAVILY WEB CONTEXT FIRST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Before recommending any channel from memory, read ALL web context below.
Extract:
  - Every Discord server name + member count found (from Disboard data)
  - Every Telegram group or channel name found
  - Every Meetup.com group name + member count found
  - Every newsletter or media outlet mentioned
  - Every influencer, creator, or thought leader mentioned
  - Every podcast or YouTube channel mentioned
  - Any college/university tech club or entrepreneurship cell mentioned
 
LIST ALL EXTRACTED NAMES here before proceeding to channel recommendations.
Label each: [Platform] | [Name] | [Members/Subscribers if found] | [Source]
 
You may add channels from knowledge only if labeled [INFERRED].
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 3 — 8-PLATFORM CHANNEL RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For EVERY channel provide the FULL SPEC BLOCK:
 
---
**[CHANNEL NAME]**
Platform:          [Discord / Telegram / Meetup / Newsletter / Podcast / LinkedIn Ads / Influencer / Institutional]
Exact Name:        [searchable name — not generic]
Members/Subs:      [number or estimate]
Source:            [Tavily / Disboard / Meetup.com / INFERRED]
Audience Cluster:  [which of your §B clusters this reaches]
Approach:          [exact first message — not promotional tone, feels organic]
Best Post Time:    [Day, Time IST]
Post Frequency:    [how often during campaign]
Cost:              [Free / ₹X per post / ₹X CPM]
Est. Reach:        [number]
Est. Registrations:[number]
Est. CPR:          [₹X per registration]
Confidence:        [HIGH / MEDIUM / LOW]
---
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLATFORM 1 — DISCORD (from Disboard.org data)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Minimum 3 named Discord servers.
Use Disboard data from web context — name, member count, top tags, activity level.
For each server: which specific channel to post in (#events / #announcements / #general).
Note: Discord requires being a member first — include join + warm-up strategy.
Format: "Server: [Name] | Members: [X] | Tags: [#tag1 #tag2] | Post in: [#channel] | Approach: [message angle]"
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLATFORM 2 — TELEGRAM (India-specific, often more active than Discord)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Minimum 4 named Telegram groups/channels in {geography} or pan-India.
Telegram is CRITICAL for Indian tech communities — do not skip.
Categories to find: {category} builders, startup founders, investors, developers.
Note: many Telegram groups have admin approval for posts — include this in approach.
Examples of types to look for:
  - "{category} India" groups
  - "{geography} Startup Network" groups  
  - "Founders of India" type channels
  - VC/investor Telegram channels
  - Developer community channels (specific to {category})
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLATFORM 3 — MEETUP.COM (in-person community crossover)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Minimum 3 named Meetup.com groups in {geography}.
Use Meetup data from web context if available.
These groups have active members who already attend in-person events —
highest conversion rate for conference registrations.
For each: group name, member count, last event date, organizer contact approach.
Strategy: partner with organizer to cross-promote (not just post in group).
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLATFORM 4 — NEWSLETTERS AND MEDIA PARTNERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Minimum 4 named newsletters/media outlets.
Indian tech media to consider (name specific ones):
  - Inc42 (startup/investor audience, 200K+ subscribers)
  - YourStory (founder/startup audience, 500K+ readers)
  - The Ken (premium subscribers, senior professionals)
  - Entrackr (funding + startup news)
  - AIM (Analytics India Magazine — AI/ML specific)
  - The Morning Context
  - Specific {category} newsletters if found in Tavily data
 
For each: subscriber count, audience profile, placement type (editorial / paid / newsletter ad),
estimated cost, and whether to pitch as MEDIA PARTNER (free coverage) vs PAID PLACEMENT.
Note: pitch as media partner first — they get free event access + coverage opportunity.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLATFORM 5 — PODCASTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Minimum 3 named podcasts whose audience matches {persona}.
Use podcast data from web context if available.
For each: podcast name, host name, episode count, audience size estimate,
topic focus, and outreach angle (speaker as guest / event sponsor mention / episode collab).
Note: podcast placements take 4–8 weeks lead time — must be T-12 or earlier.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLATFORM 6 — PAID CHANNELS (mandatory, at least 1 full spec)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRIMARY PAID RECOMMENDATION: LinkedIn Ads
  Target Audience Spec (fill all fields):
    Job titles:    [list 5–8 specific job titles matching {persona}]
    Geography:     [{geography} + adjacent cities if applicable]
    Industry:      [list 3–5 industries]
    Seniority:     [list seniority levels]
    Company size:  [employee range]
  Ad format:      [Single image / Event / Lead Gen form — recommend best for registrations]
  Budget:         [₹X total / ₹X per day]
  Estimated CPM:  [₹X]
  Estimated CPR:  [₹X per registration]
  Expected regs:  [number]
  A/B test plan:  [2 creative variants — what differs and how to measure winner]
 
SECONDARY PAID OPTIONS (brief):
  - Twitter/X promoted posts: [targeting spec + cost estimate]
  - Reddit ads (r/india, r/indianstartups): [targeting + cost]
  - Google Display Network: [targeting logic for this audience]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLATFORM 7 — INFLUENCERS AND CREATORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Minimum 5 named influencers/creators from Tavily data or knowledge.
Categories:
  - Twitter/X: {category} thought leaders in India with 10K+ followers
  - LinkedIn: practitioners who post about {category} with high engagement
  - YouTube: creators covering {category} for Indian developer/founder audience
  - Newsletter writers with dedicated followings in the space
 
For each influencer provide:
  Name:           [real, searchable name]
  Platform:       [Twitter/X / LinkedIn / YouTube / Newsletter]
  Followers:      [number]
  Engagement:     [estimated rate — high/medium/low]
  Audience match: [% overlap with event persona — be specific]
  Outreach angle: [speaker invite / affiliate / co-promotion / free ticket in exchange for post]
  Cost:           [Free (speaker) / ₹X (paid post) / affiliate (% of registrations)]
  Confidence:     [HIGH = found in Tavily / MEDIUM = known / LOW = inferred]
 
Priority: Speaker-as-influencer first (zero cost, authentic promotion).
Then affiliate (pay per registration). Then paid post (last resort).
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLATFORM 8 — INSTITUTIONAL AND COMMUNITY ORGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sub-section A: College Tech Clubs (free, high-quality, viral within campus)
  Minimum 4 named colleges in or near {geography}:
    - IIT Delhi / IIT Bombay / IIT Madras (depending on geography)
    - IIM chapters in geography
    - BITS Pilani / NIT
    - Local engineering colleges with active tech clubs
  For each: college name, relevant club name (E-Cell / IEEE / CSI / ACM chapter),
  contact approach (email to club head / LinkedIn), what to offer (free student passes),
  expected reach within campus community.
 
Sub-section B: Industry Bodies and Networks (free, senior audience)
  - iSpirt (product startup community) — how to get into their mailing list
  - NASSCOM communities — regional chapter events and newsletters
  - TiE (The Indus Entrepreneurs) — chapter in {geography}
  - FICCI / CII tech committees if relevant
  - Local startup incubators and accelerators (name specific ones in {geography})
  For each: contact person type, what to offer (partner status / free passes), reach.
 
Sub-section C: Slack Workspaces
  Minimum 2 named Slack workspaces in {category} or Indian startup ecosystem.
  Examples: SaaS Insider India, Indian Angel Network Slack, specific {category} Slacks.
 
Sub-section D: WhatsApp Communities
  iSpirt WhatsApp groups, NASSCOM circles, local founder WhatsApp communities.
  Note: WhatsApp requires warm introduction — name who the introduction should come from.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 4 — SEGMENT-SPECIFIC MESSAGE STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For each of your §B audience clusters, write:
  - Primary message (what they care about most)
  - FOMO variant (fear of missing out — scarcity / social proof)
  - Value variant (what they specifically gain from attending)
  - Proof point (specific speaker / workshop / session that clinches it for them)
  - CTA (what action to take and why now)
 
Format per cluster:
  CLUSTER [X] — [Name]
  Primary Message:  [1 sentence]
  FOMO Variant:     [1 sentence — create urgency]
  Value Variant:    [1 sentence — lead with benefit]
  Proof Point:      [specific speaker name or session title]
  CTA:              [Register now at [link] — [X] seats left / Early bird ends [date]]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 5 — A/B MESSAGE TESTING (top 3 channels)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For your top 3 highest-reach channels, provide 2 message variants:
 
  Channel: [Name]
  VARIANT A — [FOMO / Scarcity angle]:
    [Full message, ready to post — platform-appropriate length]
  VARIANT B — [Value / Benefit angle]:
    [Full message, ready to post]
  Success metric: [open rate / click rate / registration count]
  How to pick winner: [run A for first 48 hours, B for next 48 hours, compare registrations]
  Rollout: [use winning variant on all remaining channels of same platform type]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 6 — WEEK-BY-WEEK CAMPAIGN TIMELINE (T-12 to post-event)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Build a detailed campaign calendar for event on {date}.
For each week specify: which platforms are active, what content goes out,
what the campaign milestone is, and what metric to track.
 
Format:
  T-12 WEEKS: [Platform actions + milestone + metric]
  T-11 WEEKS: [...]
  T-10 WEEKS: Podcast outreach (8-week lead time — must go out now)
  T-9 WEEKS:  [...]
  T-8 WEEKS:  Newsletter partnership confirmed — first editorial mention
  T-7 WEEKS:  [...]
  T-6 WEEKS:  Early bird deadline campaign — surge on all channels
  T-5 WEEKS:  [...]
  T-4 WEEKS:  Speaker announcement — influencer posts go live
  T-3 WEEKS:  [...]
  T-2 WEEKS:  College club campaign (student registrations close quickly)
  T-1 WEEK:   Final urgency push — Telegram + WhatsApp priority
  EVENT DAY:  Live social coverage strategy
  POST-EVENT: Community nurture + save-the-date for next edition
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 7 — COST-PER-REGISTRATION RANKING TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rank ALL recommended channels by estimated CPR (lowest = best value).
This tells the organizer where to double down if budget is tight.
 
Format as table:
  | Rank | Channel | Platform | Est. Reach | Est. Regs | Cost | CPR |
  |------|---------|----------|-----------|-----------|------|-----|
  | 1    | [Name]  | Meetup   | [X]       | [X]       | Free | ₹0  |
  | 2    | [Name]  | Telegram | [X]       | [X]       | Free | ₹0  |
  | 3    | [Name]  | Discord  | [X]       | [X]       | Free | ₹0  |
  ...
  | N    | LinkedIn Ads | Paid | [X]  | [X]       | ₹X   | ₹X  |
 
At the bottom: Total estimated registrations from all GTM channels combined.
Compare against target of {size} — what % of target does GTM cover?
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STRATEGY PROFILE AND WEB CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONFERENCE STRATEGY PROFILE:
{strategy_profile}
 
TAVILY WEB CONTEXT (extract ALL channel names from here first):
{web_context}

{ZERO_TRUST_WORKFLOW}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL EXECUTION RULE (NO RAW TOOL CALLS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your Final Answer MUST be the fully written, completed Markdown report. 
- NEVER output raw tool-call tags (like `<tool_call>` or `<function>`) inside your Final Answer.
- If you need to use the SerpAPI tool, you must execute the tool properly in your thought process, wait for the observation, and ONLY write the Final Answer once you have the results.
- Do not output a "plan" to search. Actually perform the searches, read the data, and deliver the final synthesized analysis.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL QUALITY CHECK before submitting:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Did I cover all 8 platform types?
☐ Is every channel a SPECIFIC NAMED instance (not generic type)?
☐ Did I include Telegram (mandatory for India)?
☐ Did I include LinkedIn Ads with full targeting spec?
☐ Did I name at least 4 colleges in {geography}?
☐ Did I identify at least 5 named influencers?
☐ Did I write A/B variants for top 3 channels?
☐ Did I build the week-by-week calendar from T-12 to post-event?
☐ Did I produce the CPR ranking table with ALL channels?
☐ Is total estimated registrations shown vs target of {size}?
""",
        expected_output=(
            "GTM report covering all 8 platform types: "
            "Discord (3+ servers) + Telegram (4+ groups) + Meetup (3+ groups) + "
            "Newsletters (4+) + Podcasts (3+) + Paid/LinkedIn Ads (full targeting spec) + "
            "Influencers (5+ named) + Institutional/College (4+ colleges + industry bodies). "
            "Full channel spec block for every recommendation. "
            "4–6 audience clusters with segment-specific messaging. "
            "A/B test variants for top 3 channels. "
            "Week-by-week campaign calendar T-12 to post-event. "
            "CPR ranking table with total estimated registrations vs target. "
            "All named channels sourced from Tavily or labeled INFERRED."
        ),
        agent=agent,
    )


# ─────────────────────────────────────────────
# TASK 8 — EVENT OPS & RISK
# ─────────────────────────────────────────────
def task_ops(agent, inputs: dict, strategy_profile: str,
             venue_output: str, speaker_output: str,
             sponsor_output: str, exhibitor_output: str) -> Task:
 
    from crewai import Task
 
    date     = inputs.get("event_date_range",     "May 2026")
    duration = inputs.get("expected_duration",     "1 day")
    size     = inputs.get("target_audience_size",  "1000")
    budget   = inputs.get("budget_range",          "₹1 Crore")
    format_  = inputs.get("event_format",          "Summit")
    geography= inputs.get("geography_region",      "Delhi, India")
    constraints = inputs.get("hard_constraints",   "wheelchair accessible")
 
    return Task(
        description=f"""
You are the EVENT OPERATIONS, SCHEDULE BUILDER AND EXECUTION AGENT for ConferaX v4.0.
 
The PS specifically identifies schedule building, conflict detection, and resource planning
as highly recommended features that will impress judges.
These are your PRIMARY deliverables — not optional sections.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  EVENT CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date:        {date}
Duration:    {duration}
Audience:    {size} people
Budget:      {budget}
Format:      {format_}
Geography:   {geography}
Constraints: {constraints}
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DELIVERABLE 1 — STRUCTURED SESSION SCHEDULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Using the Speaker Agent's agenda-speaker mapping table, build a complete
structured schedule for {duration}.
 
For every session produce:
 
| Time Start | Time End | Session Title | Type | Speaker | Room | AV Setup | Buffer After |
|-----------|----------|--------------|------|---------|------|----------|-------------|
| 08:00 | 08:30 | Registration Open | Registration | — | Lobby | — | — |
| 08:30 | 09:00 | Speaker Green Room | Internal | All speakers | Green Room | — | — |
| 09:00 | 09:45 | Opening Keynote | Keynote | [Name] | Main Stage | Lapel mic + slides | 15 min |
[continue for full {duration}]
 
SCHEDULE RULES (enforce all):
  AV crew reset: minimum 10 min between sessions in same room
  Speaker transition: if speaker moves rooms, add 5 min travel buffer
  Registration peak: keep Lobby clear 08:00–09:30 (high traffic)
  Lunch buffer: 60–75 min (include exhibitor floor time explicitly)
  Post-lunch slot: use panel or workshop format (not solo keynote — energy dip)
  Exhibitor floor: schedule 2 dedicated "expo floor" periods (not just lunch)
  Artist/performer: slot at networking transition or closing
  End time: build in 30 min contingency before venue hard-out time
 
PARALLEL TRACK HANDLING (if applicable):
  If event has parallel tracks, show all tracks in the schedule simultaneously.
  Flag any time slot where more tracks run than AV crew can cover.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DELIVERABLE 2 — CONFLICT DETECTION LOG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run ALL 6 conflict checks on the schedule built in §B.
Show results explicitly — do not skip checks that pass.
 
CHECK 1 — SPEAKER DOUBLE-BOOKING:
  Scan: Is any speaker assigned to two sessions with overlapping times?
  Result: ✅ PASS — no conflicts found
       OR ⚠️ CONFLICT: [Speaker X] assigned to [Session A at 10:00] AND [Session B at 10:30]
  Fix: [moved Session B to 11:30, confirmed speaker available]
  Resolved: ✅
 
CHECK 2 — ROOM DOUBLE-BOOKING:
  Scan: Is any room assigned to two sessions at the same time?
  Result: ✅ PASS
       OR ⚠️ CONFLICT: [Room X] has [Session A] and [Session B] both at 14:00
  Fix: [moved Session B to Room Y]
  Resolved: ✅
 
CHECK 3 — AV CREW CAPACITY:
  Available AV crew: [X people] (from venue/ops budget)
  Peak parallel sessions: [X rooms running simultaneously at HH:MM]
  Can crew cover all rooms? YES / NO
  Result: ✅ PASS
       OR ⚠️ CONFLICT: 4 rooms at 14:00 but only 2 AV crew
  Fix: [merge two sessions / hire additional AV tech / use self-run setup for Workshop B]
 
CHECK 4 — EXHIBITOR SETUP CONFLICT:
  Exhibitor move-in time: [day before event, HH:MM–HH:MM]
  Does move-in overlap with any other venue booking or rehearsal? YES / NO
  Result: ✅ PASS
       OR ⚠️ CONFLICT: [detail]
  Fix: [adjusted move-in to earlier slot]
 
CHECK 5 — CATERING CONFLICT:
  F&B service times: [list]
  Do any F&B service periods overlap with sessions in adjacent rooms?
  (trolleys in hallways = noise during sessions)
  Result: ✅ PASS
       OR ⚠️ CONFLICT: lunch service starts at 13:00 but main hall session ends 13:15
  Fix: [delayed lunch service to 13:20]
 
CHECK 6 — ENERGY CONFLICT:
  Post-lunch slot (13:30–14:30): what session format is scheduled?
  Solo keynote at this slot = HIGH RISK (audience energy lowest)
  Result:  PASS (panel/workshop/interactive scheduled)
       OR  CONFLICT: solo keynote scheduled at 13:30
  Fix: [converted to panel format with 4 speakers for higher energy]
 
CONFLICT RESOLUTION SUMMARY:
  Total conflicts found: [X]
  Total conflicts resolved: [X]
  Unresolved conflicts: [X] — [detail and why unresolvable without organizer decision]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DELIVERABLE 3 — RESOURCE PLANNING MATRIX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Produce a ROOMS × SPEAKERS × STAFF matrix for every time slot.
 
FORMAT — TIME BLOCK TABLE:
| Time      | Main Stage              | Breakout A          | Breakout B     | Expo Floor        | Lobby/Reg    |
|-----------|------------------------|---------------------|----------------|-------------------|-------------|
| 08:00–09:00| Setup/AV check         | Setup               | Setup          | Exhibitor move-in | Registration|
| 09:00–09:45| [Speaker] + [AV Tech1] | Empty               | Empty          | Open browsing     | [Reg Staff] |
| 09:45–10:30| [Speaker] + [AV Tech1] | [Workshop] [AV Tech2]| Empty         | Open browsing     | [Reg Staff] |
[continue for full event day]
 
STAFF ASSIGNMENT (show who is responsible for what, at what time):
| Time      | Role              | Name/Title        | Location       | Responsibility |
|-----------|------------------|-------------------|----------------|----------------|
| All day   | Ops Director      | [Title]           | Roving         | Overall command|
| 08:00–10:00| Registration Lead | [Title]           | Lobby          | Check-in flow  |
| All day   | AV Tech 1         | [Title]           | Main Stage     | AV + livestream|
| All day   | AV Tech 2         | [Title]           | Breakout A     | AV             |
| All day   | Exhibitor Manager | [Title]           | Expo Floor     | Booth ops      |
[complete for all staff roles]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DELIVERABLE 4 — RUN-OF-SHOW (event day)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Minute-by-minute event day plan from venue open to venue close.
Every entry: [Time] | [Action] | [Owner] | [Cue/Trigger] | [If Something Goes Wrong]
 
Example format:
07:00 | Venue open for crew | Ops Director | Key handover from venue manager | —
07:00–08:00 | AV setup and soundcheck | AV Lead | All crew on site | Escalate to venue tech if issues
08:00 | Exhibitor doors open | Exhibitor Manager | Ops Director confirms AV ready | —
08:30 | Speaker green room opens | Speaker Coordinator | Speakers arriving | Have backup laptop ready
09:00 | DOORS OPEN — attendee registration | Registration Lead | Ops Director GO cue | Extra staff from expo floor
09:00–09:30 | Registration peak management | Registration Lead | — | Open 2nd check-in lane
09:25 | 5-min warning to opening speaker | Speaker Coordinator | Via earpiece/WhatsApp | —
09:30 | House lights dim — welcome begins | AV Tech 1 | Ops Director cue | —
[continue minute by minute through full event day to venue close]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DELIVERABLE 5 — 16-WEEK MASTER TIMELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Format: Week | Milestone | Owner Role | Depends On | Risk if Delayed
Cover T-16 to event day.
Flag every critical path dependency.
Flag every milestone that unblocks the schedule builder
(e.g., speaker confirmations must be done before room assignments are final).
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DELIVERABLE 6 — 7 WORKSTREAM CHECKLISTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A. VENUE: accessibility compliance, AV, Wi-Fi, day-of schedule, setup/teardown
B. SPEAKER COORDINATION: outreach → confirmation → brief → travel → rehearsal → day-of
C. SPONSOR COORDINATION: onboarding → assets → activation setup → day-of
D. EXHIBITOR COORDINATION:
   - Onboarding pack, floor plan, booth allocation
   - Power: Standard 1×15A / Premium 2×15A / Demo Pod dedicated circuit
   - Internet: 10Mbps dedicated per Demo Pod minimum
   - Move-in schedule (conflict-checked per §C Check 4)
   - Day-of management and strike schedule
E. REGISTRATION & TICKETING:
   - Razorpay (primary): UPI, cards, net banking — KYC docs required, start 8 weeks out
   - Instamojo (backup)
   - QR code check-in, badge printing, waitlist management
F. MARKETING & COMMS: announcement → speaker reveal → early bird → countdown
G. ON-SITE LOGISTICS: staff roles, catering (conflict-checked), emergency protocols
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DELIVERABLE 7 — RISK REGISTER (10 risks minimum)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Format per risk:
| Risk | Trigger | Probability | Impact | Early Warning | Prevention | Mitigation | Contingency |
 
Mandatory risks (must include all):
1. Speaker cancellation (48hrs before)
2. Ticket sales below break-even
3. Venue unavailable / force majeure
4. Sponsor withdrawal
5. AV failure during keynote
6. Payment gateway failure (Razorpay down)
7. Exhibitor cancellation (last minute)
8. Registration system crash on day
9. Schedule conflict discovered on event day
10. Catering delay / F&B quality issue

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL EXECUTION RULE (NO RAW TOOL CALLS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your Final Answer MUST be the fully written, completed Markdown report. 
- NEVER output raw tool-call tags (like `<tool_call>` or `<function>`) inside your Final Answer.
- If you need to use the SerpAPI tool, you must execute the tool properly in your thought process, wait for the observation, and ONLY write the Final Answer once you have the results.
- Do not output a "plan" to search. Actually perform the searches, read the data, and deliver the final synthesized analysis. 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AGENT INPUTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRATEGY PROFILE:    {strategy_profile}
VENUE OUTPUT:        {venue_output}
SPEAKER OUTPUT:      {speaker_output}
SPONSOR OUTPUT:      {sponsor_output}
EXHIBITOR OUTPUT:    {exhibitor_output}
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL QUALITY CHECK:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Is the structured session schedule complete for full {duration}?
☐ Did I run all 6 conflict checks and show results (pass or fail)?
☐ Is the Resource Planning Matrix complete (rooms × speakers × staff)?
☐ Is the Run-of-Show document minute-level for event day?
☐ Is the 16-week master timeline complete?
☐ Are all 7 workstream checklists present?
☐ Does the risk register have 10+ risks with full detail?
☐ Is Razorpay setup included with KYC timeline note?
☐ Is exhibitor move-in conflict-checked against other venue uses?
""",
        expected_output=(
            "Ops report with 7 deliverables: "
            "(1) Structured session schedule (full day, minute-level). "
            "(2) Conflict detection log (6 checks, pass/fail, resolution for each). "
            "(3) Resource planning matrix (rooms × speakers × staff × time). "
            "(4) Run-of-show (event day, minute-by-minute). "
            "(5) 16-week master timeline. "
            "(6) 7 workstream checklists including full exhibitor coordination. "
            "(7) Risk register (10+ risks with full detail). "
            "All scheduling conflicts resolved before output. "
            "Razorpay setup with KYC timeline. "
            "Accessibility compliance checklist."
        ),
        agent=agent,
    )


# ─────────────────────────────────────────────
# TASK 9 — OUTREACH DRAFTS (NEW)
# ─────────────────────────────────────────────
def task_outreach(agent, inputs: dict,
                  sponsor_output: str,
                  speaker_output: str,
                  exhibitor_output: str,
                  pass2_summary: str = "",
                  decision_output: str = "") -> Task:
    return Task(
        description=f"""
You are the AUTONOMOUS OUTREACH DRAFTING AGENT for ConferaX.

Your mission: Write ready-to-send, personalized outreach emails for the top
sponsor candidates, speaker invitees, and exhibitor prospects from the agent outputs.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOLDEN RULE — PERSONALIZATION IS NON-NEGOTIABLE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Every email must reference something SPECIFIC about the target
that proves you did your homework. Generic emails get deleted.

Sponsors want: ROI proof + audience match + specific activation idea
Speakers want: audience quality + credibility signal + logistics clarity
Exhibitors want: lead generation numbers + buyer quality + floor traffic proof

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DECISION LAYER ALIGNMENT (use this to prioritize):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{decision_output}
 
The Decision Layer has committed to specific targets.
Your email drafts MUST align with these decisions:
  - Draft 1/2/3 (Sponsors): use the exact sponsors the DL named in Decision 3
  - Draft 4/5/6 (Speakers): use the exact speakers the DL named in Decision 4
  - Draft 7/8/9 (Exhibitors): use the exact clusters the DL named in Decision 5
  - Ticket price in emails: use the exact price from Decision 2
  - Attendance numbers: use the Pass 2 P50 number
 
If you use a different target than the DL committed to, flag it and explain why.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREDICTION ENGINE CONTEXT (use these numbers in emails):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pass2_summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRODUCE EXACTLY 9 EMAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

=== SPONSOR EMAIL 1 (Title Sponsor — Tier 1 top candidate) ===
Subject: [subject line — create urgency and relevance, max 60 chars]
To: [Name], [Role], [Company]
Body: [full email — 150-200 words]
  - Reference their specific past event sponsorship from the dossier
  - State the EXACT audience match (use prediction engine attendance numbers)
  - Propose ONE specific activation idea from their dossier
  - Clear CTA: calendar link or response request with deadline
  - Signature: [Event Name] Sponsorship Team

=== SPONSOR EMAIL 2 (Gold Sponsor — Tier 1 second candidate) ===
[same format, different company, different hook]

=== SPONSOR EMAIL 3 (Silver Sponsor — Tier 2 top candidate) ===
[same format]

=== SPEAKER EMAIL 1 (Keynote slot — top speaker candidate) ===
Subject: [subject line referencing their specific work]
To: [Name], [Role], [Organization]
Body: [full email — 150-200 words]
  - Reference their specific paper, talk, or research from Scholar/arXiv
  - Describe the audience (use prediction engine attendance numbers)
  - State the slot clearly: keynote, date, duration
  - Mention honorarium/travel coverage (frame as investment in their reach)
  - CTA: availability check with specific date
  - Signature: [Event Name] Programming Team

=== SPEAKER EMAIL 2 (Panel/Workshop slot — alternative speaker) ===
[same format]

=== SPEAKER EMAIL 3 (Fireside chat — backup speaker) ===
[same format]

=== EXHIBITOR EMAIL 1 (Cluster A — Startup booth) ===
Subject: [subject line referencing their product category]
To: [Name], [Role], [Company]
Body: [full email — 120-150 words]
  - Reference their past exhibition history if available
  - State the lead generation opportunity with specific numbers
    (use prediction engine attendance estimates)
  - Describe the booth type and price clearly
  - Explain why the AUDIENCE specifically matches their ICP
  - CTA: booth reservation link with early bird deadline
  - Signature: [Event Name] Exhibitor Relations Team

=== EXHIBITOR EMAIL 2 (Cluster C — Tools & Platform booth) ===
[same format, Demo Pod focus]

=== EXHIBITOR EMAIL 3 (Cluster B — Enterprise booth) ===
[same format, Premium booth focus]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USER INPUTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Event Category:    {inputs['event_category']}
Event Date:        {inputs['event_date_range']}
Geography:         {inputs['geography_region']}
Audience:          {inputs['expected_audience_persona']}
Format:            {inputs['event_format']}

SPONSOR OUTPUT:    {sponsor_output}
SPEAKER OUTPUT:    {speaker_output}
EXHIBITOR OUTPUT:  {exhibitor_output}
""",
        expected_output=(
            "9 ready-to-send outreach emails: "
            "3 sponsor pitches (Title/Gold/Silver), "
            "3 speaker invites (Keynote/Panel/Fireside), "
            "3 exhibitor booth invites (Startup/Tools/Enterprise). "
            "Every email personalized with specific evidence from agent dossiers. "
            "Every email has subject line, recipient, full body, and CTA."
        ),
        agent=agent,
    )


# ─────────────────────────────────────────────
# TASK 10 — FINAL SYNTHESIS
# ─────────────────────────────────────────────
def task_synthesize(agent, inputs: dict, strategy_profile: str,
                    sponsor_output: str, exhibitor_output: str,
                    speaker_output: str, venue_output: str,
                    pricing_output: str, gtm_output: str,
                    ops_output: str, outreach_output: str = "",
                    pass2_summary: str = "") -> Task:
 
    return Task(
        description=f"""
You are the CHIEF STRATEGY OFFICER of ConferaX v4.0.
Synthesize ALL agent outputs into ONE professional, decision-ready report.
 
YOUR MANDATE: Every significant recommendation in this report must show its reasoning chain.
The organizer reading this report must be able to see WHY each decision was made,
WHAT evidence backs it, and WHAT they give up by choosing it.
This is not a report that lists conclusions — it is a report that JUSTIFIES them.

CRITICAL FORMATTING REQUIREMENT: 
Since this report will be viewed in Markdown, you MUST use Rich Markdown Tables to represent all quantitative data, scores, rankings, and budgets. Do not use plain text lists for data that can be tabulated.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREDICTION ENGINE — AUTHORITATIVE NUMBERS (use ONLY these):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pass2_summary}
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MANDATORY CROSS-AGENT CHECKS (complete before writing):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. BUDGET CHECK: Venue + Speakers + Ops vs {inputs['budget_range']}. Name the number gap if any.
2. AUDIENCE ALIGNMENT: Do sponsors + exhibitors match {inputs['expected_audience_persona']}?
3. TIMELINE FEASIBILITY: Is ops timeline realistic for {inputs['event_date_range']}?
4. THREE-STREAM REVENUE CHECK: Do all 3 streams cover costs? Show the arithmetic.
5. SPONSOR TIER CHECK: Does the report include all 5 sponsor tiers?
   (Primary + Fallback + Startup Cluster + In-Kind + Alt Monetization)
6. CONFLICT RESOLUTION: Name which agents disagreed and how you resolved it.
   (e.g., "Sponsor Agent estimated ₹40L sponsor revenue; Prediction Engine baseline was ₹25L.
   Reconciled to ₹32L because [reason].")
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REPORT STRUCTURE — ALL SECTIONS REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 
## COVER PAGE
Event name, date, geography, format, report version, date generated.
 
## EXECUTIVE SUMMARY (400 words max)
Distil the entire strategy into 5 key decisions the organizer must act on today.
Each decision: one sentence summary + confidence score.
End with: overall viability verdict (PROCEED / PROCEED WITH MODIFICATIONS / PAUSE).
 
## CONFERENCE STRATEGY PROFILE
Synthesize the orchestrator's profile. For each major assessment, add:
  > Evidence: [what Tavily/research data supports this]
  > Confidence: [HIGH/MEDIUM/LOW] + reason
 
## SPONSOR STRATEGY
This section must show ALL 5 TIERS clearly.

### Sponsor Fit & Scores Table
You MUST include a table ranking the top sponsors based on the Sponsor Agent's scoring:
  | Sponsor | Tier | Relevance (/100) | Feasibility (/100) | Impact (/100) | Composite Score |
  |---------|------|------------------|--------------------|---------------|-----------------|
 
### Tier 1 — Primary Sponsors
For each: evidence dossier summary, recommended ask, outreach hook.
Add:  WHY NOW: [specific reason this sponsor is motivated right now]
Add:  SOURCE: [Tavily search / event they were found at / INFERRED]
 
### Tier 2 — Fallback Sponsors
Same format. Note why they are Tier 2 vs Tier 1.
 
### Tier 3 — Startup Sponsor Cluster
For each startup: funding stage, product, ICP match, ask amount.
 
### Tier 4 — In-Kind Sponsors
What they provide, INR value equivalent, what we give in return.
 
### Tier 5 — Alternative Monetization
If ALL tiers collapse, what is Plan E?
 
### Fallback Scenario Table
Present the 4 fallback scenarios as a clean table:
  | Scenario | Description | Projected Revenue | Proceed? |
  |----------|-------------|-------------------|----------|
  | S1 | All Tier 1 decline | ₹X | Yes/No |
  | S2 | 50% Tier 2 close | ₹X | Yes/No |
  | S3 | Only startup cluster | ₹X | Yes/No |
  | S4 | Minimum viable | ₹X | Yes/No |
 
### Reasoning Chain
> WHY THIS SPONSOR STRATEGY FOR THIS EVENT:
> Evidence: [comparable events that had similar sponsors]
> Geography logic: [why geo-first filtering matters here]
> Budget logic: [why these tiers match {inputs['budget_range']}]
> Risk: [what happens to budget if sponsors are slow to close]
 
## EXHIBITOR STRATEGY
### Exhibitor Revenue Model Table
  | Cluster | Booth Type | Est. Booths | Fee per Booth | Total Revenue |
  |---------|------------|-------------|---------------|---------------|
For each cluster: evidence, fee rationale.
Add:  WHY THIS CLUSTER FOR THIS AUDIENCE: [1-2 sentences]
Expo floor layout rationale.
 
## SPEAKER AND AGENDA PLAN
### Speaker Influence & Fit Table
  | Speaker | Archetype | Influence Score (/100) | Topic Relevance | Reach/History | Status |
  |---------|-----------|------------------------|-----------------|---------------|--------|
For each keynote/critical slot:
  - Speaker recommended + why (Scholar h-index / arXiv / Sessionize data)
  - Fallback speaker
  - Budget estimate
  > AGENDA NARRATIVE: Why this sequence? What story does the day tell?
 
## VENUE AND CITY STRATEGY
Best option + 4 alternatives with a comparison table:
  | Venue | Status | Day Rate | Footfall Score | Exhibitor Capacity |
  |-------|--------|----------|----------------|--------------------|
Add: ⚡ DECISION LOGIC: [Why Venue A over Venue B in 2 sentences]
 
## THREE-STREAM REVENUE FORECAST & BUDGET
Show the full derivation:
 
  ### Budget Allocation Table
  | Cost Center | INR Amount | % of Total Budget | Notes |
  |-------------|------------|-------------------|-------|
  | Venue | ₹X | X% | |
  | Speakers | ₹X | X% | |
  | Marketing | ₹X | X% | |
  | Ops & Logistics | ₹X | X% | |
  | Contingency | ₹X | X% | |
  | **TOTAL** | **₹X** | **100%** | |

  ### Revenue Summary
  STREAM 1 — TICKET REVENUE:
    Tier structure: [from prediction engine]
    Optimal price: ₹[X] (justification: [why this price for this audience])
    Expected attendance: [X] | No-show rate: [X]%
    Ticket revenue: ₹[X]
 
  STREAM 2 — SPONSOR REVENUE:
    Reconciled (60/40 weighted): ₹[X]
 
  STREAM 3 — EXHIBITOR REVENUE:
    Reconciled: ₹[X]
 
  COMBINED P&L:
    Total Revenue: ₹[X]
    Total Budget:  ₹{inputs['budget_range']}
    Net:           ₹[X] surplus / deficit
    Break-even at: [X] attendees
 
  ### Monte Carlo Risk Table (10,000 simulations)
  | Scenario | Outcome | Projected Revenue | Drivers |
  |----------|---------|-------------------|---------|
  | P90 | Best Case | ₹X | [what drives this] |
  | P50 | Expected | ₹X | [what this looks like] |
  | P10 | Worst Case | ₹X | [what causes this] |
 
## GTM STRATEGY
### Channel Effectiveness Table
  | Rank | Channel | Platform | Est. Reach | Relevance Score | Est. CPR (Cost per Reg) |
  |------|---------|----------|------------|-----------------|-------------------------|
Named communities only. Discord servers with member counts.
Campaign timeline T-12 to post-event.
> WHY THIS CHANNEL FIRST: [1-2 sentences on primary channel choice]
 
## OPERATIONS AND RISK
### Risk Severity Matrix Table
  | Risk | Probability (%) | Impact (%) | Severity Score | Mitigation |
  |------|-----------------|------------|----------------|------------|
7 workstream status (complete / incomplete / flagged).
Top 3 risks requiring action THIS WEEK.
 
## OUTREACH STRATEGY
Confirm 9 emails are ready. Note personalization approach.
> OUTREACH PRIORITY ORDER: [which email to send first and why]
 
## CONFIDENCE AND ASSUMPTIONS
5 highest-risk assumptions that could break this plan.
For each: [Assumption] | [Evidence for] | [Evidence against] | [What to verify]
 
## DECISION REGISTER
Synthesize ALL 10 decisions from the Decision Layer agent into a clean table:
  | # | Decision | Confidence (/100) | Reversal Trigger |
  |---|----------|-------------------|------------------|
Explain your top 3 decisions in 2 sentences each with reasoning.
 
## LEARNING AND FUTURE IMPROVEMENTS
What this pipeline still cannot do well.
What data would improve the next run.
 
## SOURCES AND DATA ATTRIBUTION
List EVERY source used:
  - Tavily search queries that produced usable intelligence
  - Cvent listings referenced by venue or exhibitor agents
  - Comparable events used as pricing benchmarks
  - Academic databases (Scholar/arXiv) searched by speaker agent
  - Disboard searches for community channels
  - Any INFERRED data clearly flagged
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALL AGENT INPUTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Event:     {inputs['event_category']} | {inputs['geography_region']} | {inputs['event_date_range']}
Audience:  {inputs['target_audience_size']} people | {inputs['expected_audience_persona']}
Budget:    {inputs['budget_range']} | Format: {inputs['event_format']}
Objective: {inputs['organizer_objective']}
 
STRATEGY PROFILE: {strategy_profile}
SPONSOR OUTPUT:   {sponsor_output}
EXHIBITOR OUTPUT: {exhibitor_output}
SPEAKER OUTPUT:   {speaker_output}
VENUE OUTPUT:     {venue_output}
PRICING OUTPUT:   {pricing_output}
GTM OUTPUT:       {gtm_output}
OPS OUTPUT:       {ops_output}
OUTREACH OUTPUT:  {outreach_output}
""",
        expected_output=(
            "Complete ConferaX v4.0 report with all sections formatting heavily utilizing Rich Markdown Tables. "
            "Every major recommendation has a Reasoning Chain block. "
            "Sponsor section shows all 5 tiers + Sponsor Fit & Scores Table + fallback scenario table. "
            "Three-stream revenue table, Budget Allocation Table, and Monte Carlo table with full derivation and P&L. "
            "Speaker Influence & Fit Table and GTM Channel Effectiveness Table included. "
            "Every HIGH-confidence claim sourced (Tavily / Cvent / Event name). "
            "Decision Register table from Decision Layer. "
            "Sources and Data Attribution section listing all search queries. "
            "Zero conflicting revenue numbers throughout report."
        ),
        agent=agent,
    )
