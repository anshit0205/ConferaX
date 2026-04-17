# tasks_advanced.py — ConferaX v3.0
# Advanced Tasks: Research, Devil's Advocate, Self-Reflection, Decision Layer
# Decision Layer updated with prediction engine pass2 context

from crewai import Task

ZERO_TRUST_WORKFLOW = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 RESEARCH WORKFLOW & TOOL REQUIREMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Review the provided Phase 0 Tavily context.
2. If the Tavily context lacks specific, up-to-date numbers, budgets, or direct names required for this task, you MUST trigger your Search Tool to fill the gaps.
3. Do not guess, do not hallucinate, and do not use placeholders. If you don't know a fact, search for it.
"""
# ─────────────────────────────────────────────
# TASK 10 — REAL-TIME RESEARCH
# ─────────────────────────────────────────────
def task_research(agent, inputs: dict, strategy_profile: str,
                  web_context: str = "") -> Task:
    return Task(
        description=f"""
You are the REAL-TIME RESEARCH AGENT for ConferaX.

Your mission: Analyze ALL pre-fetched real-world web data across 10 search categories
and extract actionable intelligence that grounds the strategy.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRE-FETCHED REAL-WORLD DATA (analyze ALL 10 categories):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{web_context}

YOUR JOB: ANALYZE — do not search for more. Extract. Cross-reference. Validate.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANALYZE EACH CATEGORY AND REPORT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### CATEGORY 1: COMPARABLE EVENTS
What real comparable events were found? Attendance numbers? Ticket prices?
Venues used? Speaker names mentioned? Validates or contradicts strategy profile?

### CATEGORY 2: SPONSOR LANDSCAPE
What companies appeared as sponsors? Any budget signals?
Validates or contradicts sponsor agent assumptions?

### CATEGORY 3: SPEAKER LANDSCAPE
What real speaker names appeared? What events did they speak at?
Any signals about fees, availability, or topic focus?

### CATEGORY 4: ACADEMIC SPEAKER SIGNALS (Scholar / Semantic Scholar / arXiv)
What researchers appeared with high citation counts or recent papers?
What are their h-index or citation signals? What topics are trending?
Which academic speakers are verified conference-ready?

### CATEGORY 5: EXHIBITOR LANDSCAPE (Cvent / EventLocations)
What companies appeared in past exhibitor lists?
What categories dominated? What booth pricing signals were found?

### CATEGORY 6: VENUE SIGNALS (Cvent / EventLocations)
What real venues appeared? What capacity and pricing data?
What past events used these venues?

### CATEGORY 7: PRICING BENCHMARKS
What real ticket prices for comparable events?
What registration fee ranges for this category and geography?

### CATEGORY 8: DISBOARD COMMUNITIES
What Discord servers appeared? Name each: member count, tags, activity level.
Which are most relevant for GTM?

### CATEGORY 9: CVENT VENUE LISTINGS
What specific venue data appeared? Pricing, capacity, availability signals?

### CATEGORY 10: MARKET CONTEXT
Key trends in {inputs['event_category']} ecosystem in {inputs['geography_region']}?
Funding signals, community growth, market opportunity data?

{ZERO_TRUST_WORKFLOW}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDATION SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For each category: VALIDATED / CONTRADICTED / INSUFFICIENT DATA
Top 5 findings that most impact the strategy.
Top 3 contradictions between web data and strategy profile assumptions.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USER INPUTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Event Category:   {inputs['event_category']}
Geography:        {inputs['geography_region']}
Event Format:     {inputs['event_format']}
Date Range:       {inputs['event_date_range']}
Audience:         {inputs['expected_audience_persona']}

STRATEGY PROFILE:
{strategy_profile}
""",
        expected_output=(
            "Research report covering all 10 categories. "
            "Named Discord servers from Disboard. Named venues from Cvent. "
            "Academic speaker signals from Scholar/arXiv. "
            "Exhibitor evidence from Cvent/EventLocations. "
            "Validation summary with top 5 findings and top 3 contradictions."
        ),
        agent=agent,
    )


# ─────────────────────────────────────────────
# TASK 11 — DEVIL'S ADVOCATE
# ─────────────────────────────────────────────
def task_devils_advocate(agent, inputs: dict,
                          strategy_profile: str,
                          sponsor_output: str,
                          exhibitor_output: str,
                          speaker_output: str,
                          venue_output: str,
                          pricing_output: str,
                          gtm_output: str,
                          ops_output: str,
                          research_output: str,
                          pass2_summary: str = "") -> 'Task':
    from crewai import Task
 
    budget      = inputs.get("budget_range",              "₹1 Crore")
    geography   = inputs.get("geography_region",          "Delhi, India")
    audience    = inputs.get("target_audience_size",      "1000")
    persona     = inputs.get("expected_audience_persona", "founders, developers, investors")
    objective   = inputs.get("organizer_objective",       "brand building")
    date        = inputs.get("event_date_range",          "May 2026")
    ticketing   = inputs.get("ticketing_intent",          "tiered")
    category    = inputs.get("event_category",            "AI")
 
    return Task(
        description=f"""
You are the DEVIL'S ADVOCATE for ConferaX v4.0.
 
Your mission: Challenge every major recommendation using logical, quantitative,
and benchmark scrutiny. Find what will break before the organizer signs anything.
For every flaw: PROBLEM → ROOT CAUSE → SPECIFIC FIX (not generic, not vague).
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§A  EVENT CONTEXT (know this before challenging)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Category:      {category}
Geography:     {geography}
Audience:      {audience} people | Persona: {persona}
Budget:        {budget}
Date:          {date}
Ticketing:     {ticketing}
Objective:     {objective}
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§B  PREDICTION ENGINE CHALLENGE (challenge this first)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREDICTION ENGINE PASS 2 OUTPUT:
{pass2_summary}
 
Challenge the engine directly on these 5 points:
 
1. RECONCILIATION WEIGHTING (60% agent / 40% baseline):
   Is 60% agent weight justified here?
   Agent estimates are only as good as the Tavily data quality.
   If Tavily returned thin data, agent estimates are overconfident.
   State: JUSTIFIED / OVERCONFIDENT / UNDERCONFIDENT — with reasoning.
 
2. PRICE ELASTICITY ASSUMPTION:
   The engine uses a weighted persona elasticity.
   For {persona} in {geography} in {ticketing} mode:
   Is the elasticity coefficient realistic for THIS specific event?
   Compare against: what price did comparable {category} events charge in {geography}?
   What happened to attendance when they changed price?
 
3. NO-SHOW RATE ASSUMPTION:
   The engine computes no-show from persona base + price adjustment + lead time.
   For a {ticketing} event in {geography} in {date}:
   Is this the right no-show rate? Factor in: season, day of week, competing events.
   Indian paid tech events average 18-28% no-show.
   Indian free events average 35-55% no-show.
   Is the engine's computed rate within these ranges?
 
4. MONTE CARLO RISK COVERAGE:
   Does the P10-P90 range capture Indian-specific risks?
   - Payment gateway failure on event day (Razorpay has ~0.3% downtime)
   - Last-minute sponsor withdrawal (15-20% probability in Indian market)
   - Monsoon season impact if {date} is June-September
   - Festival season conflict if {date} is October-November
   State which risks are MISSING from the Monte Carlo model.
 
5. THREE-STREAM INTERDEPENDENCY:
   The engine treats ticket/sponsor/exhibitor as partially correlated.
   But in reality they are HIGHLY correlated:
   Low ticket sales → low venue footfall → exhibitors want refunds →
   sponsors lose confidence → overall revenue collapses faster than the model predicts.
   Does the engine capture this cascading failure mode? If not, what is the real P10?
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§C  EVENT-ADAPTIVE CHALLENGE (based on ticketing: {ticketing})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Apply the challenge set matching the ticketing mode:
 
IF FREE EVENT:
  - Registration-to-attendance: does the plan assume this?
    Indian free events: 35-55% show up on the day.
    If expecting 1000 attendees, you need 1,800-2,850 registrations.
    Does the GTM plan target enough reach to get those registrations?
  - Sponsor ROI at a free event: are sponsors paying for a room that's half-empty?
  - Exhibitor ROI: will exhibitors accept foot-traffic uncertainty at a free event?
 
IF PAID/TIERED EVENT:
  - Is the VIP tier genuinely differentiated?
    What specific inclusions justify 3-5× price? List what is and isn't included.
  - Is early bird genuinely discounted enough to drive urgency?
    Indian events need 30-45% early bird discount to move registrations early.
  - Is the general price defensible against comparable events?
    Name 2 comparable {category} events in {geography} and their ticket prices.
    Is this event priced above, below, or at parity? Is that appropriate?
 
IF HYBRID EVENT:
  - Online attendees: are they being counted in audience reach for sponsors?
    Sponsors pay for IN-PERSON only. Is this reflected in sponsor packages?
  - AV/streaming cost: is this in the budget? Hybrid adds ₹2-8L in tech costs.
  - Engagement: online attendees have 15-30% of in-person networking value.
    Is the event content designed for both simultaneously or just one?
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§D  STRATEGY PROFILE CHALLENGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INPUT: {strategy_profile}
 
CHALLENGE 1 — THE LOAD-BEARING ASSUMPTION:
  What single assumption, if wrong, destroys this entire strategy?
  State it precisely. What evidence supports it? What contradicts it?
 
CHALLENGE 2 — AUDIENCE SIZE REALITY CHECK:
  The plan targets {audience} people in {geography} for a {category} event.
  Name a comparable event in this geography and category.
  What was THEIR actual attendance?
  Is {audience} ambitious, realistic, or conservative vs that benchmark?
 
CHALLENGE 3 — OBJECTIVE-REVENUE TENSION:
  The organizer objective is: {objective}
  The revenue model requires maximizing ticket/sponsor/exhibitor revenue.
  Are these in tension? Specifically:
  If objective is "community building" but VIP pricing is ₹15,000, who gets excluded?
  If objective is "revenue" but pricing is kept low for access, what covers the budget?
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§E  SPONSOR STRATEGY CHALLENGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INPUT: {sponsor_output}
 
CHALLENGE 1 — CLOSE RATE MATH:
  Extract the Conservative/Expected/Optimistic revenue estimates.
  Work backwards: what close rate and average deal size do these require?
  Formula: Revenue = (number of sponsors approached) × (close rate) × (avg deal size)
  Is the implied close rate realistic? Indian B2B sponsorship close rates: 25-45%.
 
CHALLENGE 2 — HISTORICAL FREQUENCY VALIDATION:
  The agent assigned Priority 1-4 based on geo/history.
  For the top 2 Tier 1 sponsors: was their historical sponsorship evidence
  actually from Tavily (HIGH confidence) or inferred (MEDIUM/LOW)?
  If INFERRED: the priority score is overstated. What does it become with evidence?
 
CHALLENGE 3 — STARTUP SPONSOR REALITY:
  Name the startups in Tier 3. Are these verifiably funded companies?
  A startup sponsor at Seed stage has a typical marketing budget of ₹2-10L/year.
  Is the proposed booth fee within that range?
  What if 2 of the 5 startups are pre-revenue? Can they pay at all?
 
CHALLENGE 4 — FALLBACK SCENARIO MATH:
  Use Scenario 1 (all Tier 1 decline) revenue number.
  Does this cover: venue cost + speaker fees + minimum ops cost?
  If not, what is the actual minimum viable sponsor revenue to proceed?
  Is that achievable from Tier 2 + Tier 3 alone?
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§F  EXHIBITOR STRATEGY CHALLENGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INPUT: {exhibitor_output}
 
CHALLENGE 1 — BOOTH UPTAKE REALITY:
  How many total booths are proposed? What is the fill rate assumption?
  For {audience} attendees, typical exhibitor-to-attendee ratio at Indian tech events:
  1 exhibitor per 30-50 attendees. Is the booth count within this range?
 
CHALLENGE 2 — FOOTFALL DEPENDENCY:
  Exhibitor revenue is tied to footfall through the exhibitor floor.
  What is the venue's exhibitor footfall score (from venue agent)?
  If footfall score < 6, exhibitors will complain and not return next year.
  Is there a plan to drive traffic to the expo floor beyond passive placement?
 
CHALLENGE 3 — EXHIBITOR SOURCE VALIDATION:
  Were the exhibitor candidates sourced from Cvent/EventLocations or hallucinated?
  Name the top 3 exhibitor candidates. Are these verifiably real companies
  that have exhibited at comparable events?
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§G  SPEAKER STRATEGY CHALLENGE 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INPUT: {speaker_output}
 
CHALLENGE 1 — INFLUENCE SCORE INTEGRITY:
  Pick the top 2 speakers by influence score.
  For each: how many of their score dimensions were Tavily-verified vs INFERRED?
  If >50% of dimensions are INFERRED, the score should be reduced by 20+ points.
  What are their corrected scores?
 
CHALLENGE 2 — LINKEDIN DATA RELIABILITY:
  The agent used LinkedIn public profiles via Tavily.
  Were these profiles actually surfaced (HIGH confidence) or labeled INFERRED?
  A practitioner with INFERRED LinkedIn data has unknown current role/company.
  How many top speakers have this risk?
 
CHALLENGE 3 — AVAILABILITY AND BUDGET:
  For the top keynote speaker: what is their estimated fee?
  What % of the speaker budget does this consume?
  If they decline, does the backup have equivalent influence score?
  What is the influence score gap between top choice and backup?
 
CHALLENGE 4 — CONFLICT DETECTION VERIFICATION:
  Did the speaker agent run all 5 conflict checks?
  Are there any CONFLICT flags in the output?
  If no conflicts were found in a multi-track {audience}-person event,
  is that credible or was the check perfunctory?
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VENUE STRATEGY CHALLENGE 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INPUT: {venue_output}
 
CHALLENGE 1 — BUDGET GATE VERIFICATION:
  Was the budget hard gate actually applied?
  What is the day rate of the recommended Best Option?
  What is 25-35% of {budget}? Does the day rate fit within this range?
  If not, the budget gate failed.
 
CHALLENGE 2 — FOOTFALL SCORE BASIS:
  What is the exhibitor footfall score of the Best Option venue?
  Was this score based on: floor plan analysis / comparable event reports / assumption?
  A footfall score without a floor plan is an estimate.
  What would the score be if the floor plan shows the expo hall is separate from sessions?
 
CHALLENGE 3 — AVAILABILITY RISK:
  The event is on {date}. Is this a peak booking period in {geography}?
  (Delhi: October-February is peak conference season — 6-9 month lead needed)
  Has the venue confirmed availability for this date or is it assumed?
  What is the cost of the fallback venue if Best Option is already booked?
 
CHALLENGE 4 — PAST EVENT USAGE VERIFICATION:
  Were the past events cited for venues sourced from Tavily or INFERRED?
  A venue claimed to have hosted [Event] needs Tavily confirmation.
  Without it, the organizer could visit expecting one thing and find another.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PRICING AND GTM CHALLENGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRICING INPUT: {pricing_output} 
PRICING:
  At the recommended optimal price point, what CPR is implied from GTM?
  Formula: CPR = Marketing budget / Expected registrations
  Is the implied CPR achievable from the channels identified?
  If GTM channels can reach 50,000 people with 2% conversion = 1,000 registrations.
  What marketing budget does that require? Is it in the plan?
GTM INPUT: {gtm_output} 
GTM:
  Are Discord servers named from Disboard ACTUALLY active?
  (Check: were member counts > 1,000 AND activity level = active?)
  Is the Telegram outreach plan realistic?
  (Admin approval required in most groups — is this lead time accounted for?)
  Is the college ecosystem outreach timed correctly?
  (IIT/IIM students plan 8-12 weeks ahead for paid events)
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OPS AND SCHEDULE CHALLENGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INPUT: {ops_output[:1500]}
 
CHALLENGE 1 — SCHEDULE BUILDER COMPLETENESS:
  Is the session schedule minute-level or just rough timing?
  A rough schedule is a risk register item, not an ops plan.
 
CHALLENGE 2 — CONFLICT DETECTION RESULTS:
  Were all 6 conflict checks run with explicit PASS/CONFLICT results?
  Or were they listed as checks without results?
  Any unresolved CONFLICT flags are blockers — name them.
 
CHALLENGE 3 — RAZORPAY KYC TIMELINE:
  Razorpay requires business KYC documents and 3-7 days for approval.
  For new accounts: up to 14 days for full activation.
  Is this lead time accounted for in the master timeline?
  If the event is in {date}, when must Razorpay setup begin?
 
CHALLENGE 4 — RESOURCE MATRIX REALITY:
  The resource planning matrix assigns staff to rooms.
  How many ops staff are assumed? Is that number in the budget?
  Typical Indian tech event ops cost: ₹800-2,000 per staff member per day
  plus agency markup if outsourced. Is this in the ops budget?
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RESEARCH DATA CHALLENGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INPUT: {research_output[:2000]}
 
  Which of the 22 Tavily searches returned HIGH quality data vs thin/empty results?
  Where the research agent found little data, which agent claims are most at risk?
  Are there any contradictions between Tavily data and agent recommendations?
  State the top 3 data gaps that most endanger the plan.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WEAKNESS SCORE (derive with arithmetic)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score each area 0-10 (10 = serious flaw, 0 = solid):
 
  Strategy Profile:          [X/10] — [1 sentence reason]
  Sponsor Strategy:          [X/10] — [1 sentence reason]
  Exhibitor Strategy:        [X/10] — [1 sentence reason]
  Speaker Strategy:          [X/10] — [1 sentence reason]
  Venue Strategy:            [X/10] — [1 sentence reason]
  Prediction Engine:         [X/10] — [1 sentence reason]
  GTM Strategy:              [X/10] — [1 sentence reason]
  Ops / Schedule:            [X/10] — [1 sentence reason]
  Data Quality:              [X/10] — [1 sentence reason]
 
  OVERALL WEAKNESS SCORE = (sum / 9) × 10 = [X]/100
  Interpretation: 0-30 = solid plan | 31-60 = proceed with fixes | 61-100 = serious rework needed

{ZERO_TRUST_WORKFLOW}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL EXECUTION RULE (NO RAW TOOL CALLS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your Final Answer MUST be the fully written, completed Markdown report. 
- NEVER output raw tool-call tags (like `<tool_call>` or `<function>`) inside your Final Answer.
- If you need to use the SerpAPI tool, you must execute the tool properly in your thought process, wait for the observation, and ONLY write the Final Answer once you have the results.
- Do not output a "plan" to search. Actually perform the searches, read the data, and deliver the final synthesized analysis. 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 FINAL VERDICT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 
TOP 3 THINGS THAT MUST CHANGE BEFORE THIS PLAN IS VIABLE:
  1. [Specific change — name the agent, the number, the fix]
  2. [Specific change]
  3. [Specific change]
 
TOP 3 THINGS THE AGENTS GOT RIGHT (keep these):
  1. [Specific strength]
  2. [Specific strength]
  3. [Specific strength]
 
ALL FIXES SUMMARY (PROBLEM → ROOT CAUSE → SPECIFIC FIX):
  [Complete list of every flaw found with its specific fix]
""",
        expected_output=(
            "Devil's Advocate report covering: "
            "Prediction Engine challenge (5 points), "
            "event-adaptive challenge (pricing mode specific), "
            "9 challenge areas with quantitative counter-analysis and benchmark comparisons, "
            "v4.0 feature scrutiny (footfall scores, influence scores, LinkedIn data), "
            "weakness score derived with arithmetic (not asserted), "
            "final verdict with top 3 must-fix items and top 3 strengths. "
            "Every fix: PROBLEM → ROOT CAUSE → SPECIFIC FIX."
        ),
        agent=agent,
    )


# ─────────────────────────────────────────────
# TASK 12 — SELF-REFLECTION
# ─────────────────────────────────────────────
def task_self_reflection(agent, inputs: dict,
                          all_outputs: dict,
                          devils_advocate_output: str,
                          pass2_summary: str = "") -> 'Task':
    
 
    category  = inputs.get("event_category",            "AI")
    geography = inputs.get("geography_region",          "Delhi, India")
    date      = inputs.get("event_date_range",          "May 2026")
    budget    = inputs.get("budget_range",              "₹1 Crore")
    persona   = inputs.get("expected_audience_persona", "founders, developers, investors")
    objective = inputs.get("organizer_objective",       "brand building")
    ticketing = inputs.get("ticketing_intent",          "tiered")
    audience  = inputs.get("target_audience_size",      "1000")
    return Task(
        description=f"""
You are the SELF-REFLECTION AND PIPELINE QUALITY AUDITOR for ConferaX v4.0.
 
Your output is the bridge between all specialist agents and the Decision Layer.
The Decision Layer depends on your structured priority list to order its decisions.
Be honest. Be specific. Be actionable.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§A  EVENT CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Category:   {category} | Geography: {geography} | Date: {date}
Budget:     {budget} | Ticketing: {ticketing}
Persona:    {persona} | Objective: {objective}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   PREDICTION ENGINE PASS 2 (audit this):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pass2_summary}
Did agents use these reconciled numbers correctly?
Did any agent output contradict Pass 2 without citing evidence?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§B  SECTION 1 — AGENT SCORECARD TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rate every agent on 4 dimensions (0-10 each). Show the table.
 
| Agent | Evidence Quality | Reasoning Depth | Actionability | Completeness | TOTAL /40 |
|-------|-----------------|-----------------|---------------|--------------|-----------|
| Orchestrator      | [X] | [X] | [X] | [X] | [X] |
| Research Analyst  | [X] | [X] | [X] | [X] | [X] |
| Sponsor Intel     | [X] | [X] | [X] | [X] | [X] |
| Exhibitor Intel   | [X] | [X] | [X] | [X] | [X] |
| Speaker & Agenda  | [X] | [X] | [X] | [X] | [X] |
| Venue Intel       | [X] | [X] | [X] | [X] | [X] |
| Pricing & Footfall| [X] | [X] | [X] | [X] | [X] |
| GTM & Audience    | [X] | [X] | [X] | [X] | [X] |
| Ops & Risk        | [X] | [X] | [X] | [X] | [X] |
 
Scoring criteria:
Evidence Quality:   10 = 3+ Tavily-sourced claims | 5 = mixed | 0 = fully inferred
Reasoning Depth:    10 = shows math/logic | 5 = partial | 0 = assertions only
Actionability:      10 = names specific things | 5 = partial | 0 = generic
Completeness:       10 = all required sections | 5 = some gaps | 0 = major gaps
 
FOR THE 2 LOWEST-SCORING AGENTS:
Write an improvement prescription:
  Agent: [Name]
  Total Score: [X]/40
  Worst dimension: [dimension] — [specific reason]
  Prescription: [specific change to agent prompt or task that would fix this]
  Expected improvement: [what would change in the output]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§C  SECTION 2 — DATA QUALITY AUDIT (22 Tavily searches)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rate each search category: HIGH / MEDIUM / LOW quality data returned.
 
| Search | Data Quality | Agent That Uses It | Risk if Low |
|--------|-------------|-------------------|-------------|
| comparable_events       | [H/M/L] | Orchestrator, Pricing | [risk] |
| sponsor_landscape       | [H/M/L] | Sponsor              | [risk] |
| sponsor_history         | [H/M/L] | Sponsor              | [risk] |
| startup_ecosystem       | [H/M/L] | Sponsor (Tier 3)     | [risk] |
| marketing_signals       | [H/M/L] | Sponsor              | [risk] |
| speaker_academic        | [H/M/L] | Speaker              | [risk] |
| speaker_linkedin_events | [H/M/L] | Speaker              | [risk] |
| speaker_github          | [H/M/L] | Speaker (dev events) | [risk] |
| speaker_social          | [H/M/L] | Speaker              | [risk] |
| exhibitor_landscape     | [H/M/L] | Exhibitor            | [risk] |
| cvent_venues            | [H/M/L] | Venue                | [risk] |
| venue_signals           | [H/M/L] | Venue                | [risk] |
| venue_past_events       | [H/M/L] | Venue                | [risk] |
| venue_pricing           | [H/M/L] | Venue                | [risk] |
| pricing_benchmarks      | [H/M/L] | Pricing              | [risk] |
| disboard_communities    | [H/M/L] | GTM                  | [risk] |
| meetup_communities      | [H/M/L] | GTM                  | [risk] |
| media_newsletters       | [H/M/L] | GTM                  | [risk] |
| influencer_creators     | [H/M/L] | GTM                  | [risk] |
| market_context          | [H/M/L] | Orchestrator, GTM    | [risk] |
| academic_speakers       | [H/M/L] | Speaker              | [risk] |
| speaker_landscape       | [H/M/L] | Speaker              | [risk] |
 
TOP 3 DATA GAPS:
  Gap 1: [search] returned LOW quality → [specific agent claim at risk] → [what to verify manually]
  Gap 2: [search] returned LOW quality → [specific agent claim at risk] → [what to verify manually]
  Gap 3: [search] returned LOW quality → [specific agent claim at risk] → [what to verify manually]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§D  SECTION 3 — CONFIDENCE CALIBRATION CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Standard: HIGH = 3+ Tavily sources confirmed. MEDIUM = 1-2 confirmed. LOW = fully inferred.
 
Find every case where a HIGH confidence label was applied without 3+ confirmed sources.
These are the overconfident claims.
 
OVERCONFIDENT CLAIMS FOUND:
  Claim 1: [Agent] labeled [X] as HIGH confidence but evidence shows [Y sources only]
    Corrected confidence: MEDIUM
    Impact on Decision Layer: [what decision is affected by this overclaim]
 
  Claim 2: [repeat format]
  [continue for all found]
 
CORRECTLY CALIBRATED CLAIMS (examples of good practice):
  [List 2-3 claims that were correctly labeled — reinforce what worked]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§E  SECTION 4 — DA FIX EVALUATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEVIL'S ADVOCATE OUTPUT:
{devils_advocate_output[:3000]}
 
For each fix the DA proposed, rate it:
 
| DA Fix | Rating | Issue (if any) | Rewritten Fix (if needed) |
|--------|--------|----------------|--------------------------|
| [Fix 1 summary] | ACTIONABLE / NEEDS CLARIFICATION / TOO VAGUE | [issue] | [rewrite] |
[continue for all fixes]
 
For every TOO VAGUE fix: rewrite it with the specific action, owner, and deadline.
 
DA OVERALL ASSESSMENT:
  Was the DA appropriately critical or too lenient/too harsh?
  Did the DA miss any major risk that the pipeline should have caught?
  [Name the missed risk and add it to the must-fix list]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§F  SECTION 5 — EVENT-ADAPTIVE MISSED ITEMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is NOT a generic list. Every item must be specific to THIS event:
{category} summit | {geography} | {date} | {persona} | {budget}
 
MISSED ITEMS (minimum 8, all event-specific):
 
1. PERMITS AND LICENSING:
   For a {category} event in {geography} with {persona} audience:
   [Specific permits needed — noise permits, assembly permits, fire safety certificates]
   Which agent should have flagged this? [name] — Ops Agent typically.
   Action: [specific action + timeline]
 
2. COMPETING EVENTS ON {date}:
   Were any competing {category} events in {geography} on or near {date} checked?
   Competing events split the audience and sponsor pool.
   Action: [specific search to verify + decision if conflict found]
 
3. GST IMPLICATIONS:
   Ticket sales in India are subject to GST (18% on entertainment tickets above ₹250).
   Sponsor invoices require GST registration.
   Exhibitor booth fees require GST.
   Was this factored into the revenue model? If not, revenue is overstated by 18%.
   Action: [specific accounting action]
 
4. RAZORPAY KYC TIMELINE:
   New Razorpay accounts require business documents + 3-14 days for activation.
   For {date}: KYC must begin by [computed date].
   Was this in the master timeline? If not, this is a blocker.
 
5. EVENT INSURANCE:
   Public liability insurance for {audience} people in {geography}.
   Exhibitor insurance requirements.
   Speaker cancellation insurance (especially for international speakers).
   Was any insurance cost in the budget? Typical: ₹50K-2L for this event size.
 
6. CONTENT IP AND RECORDING RIGHTS:
   Are sessions being recorded? Streamed? Posted online?
   Speaker agreements must include recording consent.
   If speakers have academic affiliation, institutional IP policies may apply.
 
7. DIETARY AND ACCESSIBILITY:
   {persona} audience in {geography}:
   Likely dietary requirements: [estimate based on persona]
   Accessibility: was the venue's accessibility compliance checklist completed?
   Language: is English primary? Any regional language needs?
 
8. POST-EVENT DATA PRIVACY:
   Attendee data collected during registration is subject to India's DPDP Act 2023.
   Sponsor lead data sharing requires explicit consent.
   Was a privacy policy included in the registration flow?
   Action: [specific legal step needed]
 
[Add more missed items specific to this event's category/geography/date]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§G  SECTION 6 — PIPELINE IMPROVEMENT PRESCRIPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Minimum 5 specific prescriptions for the NEXT pipeline run.
Each must name the specific file, agent, or task to change.
 
| # | Prescription | File/Agent to Change | Specific Change | Expected Improvement |
|---|-------------|---------------------|-----------------|---------------------|
| 1 | [prescription] | [agents.py / tasks.py / tavily_research.py] | [exact change] | [what improves] |
[continue for 5+]
 
HIGHEST PRIORITY PRESCRIPTION:
  [The single change that would most improve output quality next run]
  Why: [reasoning]
  How: [exact implementation]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§H  SECTION 7 — STRUCTURED PRIORITY LIST FOR DECISION LAYER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THIS IS YOUR MOST IMPORTANT OUTPUT.
The Decision Layer uses this list to order its 10 decisions.
Make it structured, specific, and actionable.
 
TOP 10 DECISIONS — IN PRIORITY ORDER:
 
DECISION 1 (Most urgent — decide in 48 hours):
  DECISION NEEDED: [specific choice — name venue, name price, name sponsor]
  WHY URGENT: [what breaks/expires if not decided in 48 hours]
  BEST OPTION: [specific recommendation from agent outputs]
  CONFIDENCE: [HIGH/MEDIUM/LOW] — [reason]
  RISK IF WRONG: [specific consequence]
  DA CHALLENGE TO CONSIDER: [relevant DA challenge the Decision Layer must address]
 
DECISION 2:
  [same format]
 
[continue through Decision 10]
 
SINGLE BIGGEST BLIND SPOT IN THE ENTIRE STRATEGY:
  [The one thing that, if wrong, destroys the plan]
  [Why it wasn't caught by any agent]
  [What to do about it immediately]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALL PIPELINE OUTPUTS FOR AUDIT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Strategy Profile:    {all_outputs.get('strategy_profile', '')[:1500]}
Sponsor Output:      {all_outputs.get('sponsor_output', '')[:1500]}
Exhibitor Output:    {all_outputs.get('exhibitor_output', '')[:1000]}
Speaker Output:      {all_outputs.get('speaker_output', '')[:1500]}
Venue Output:        {all_outputs.get('venue_output', '')[:1000]}
Pricing Output:      {all_outputs.get('pricing_output', '')[:1000]}
GTM Output:          {all_outputs.get('gtm_output', '')[:1000]}
Ops Output:          {all_outputs.get('ops_output', '')[:1000]}
Research Output:     {all_outputs.get('research_output', '')[:1000]}
""",
        expected_output=(
            "Self-reflection report with 7 sections: "
            "(1) Agent scorecard table with scores on 4 dimensions + improvement prescriptions for 2 lowest. "
            "(2) Data quality audit table for all 22 Tavily searches with risk assessment. "
            "(3) Confidence calibration check — every overconfident HIGH label identified. "
            "(4) DA fix evaluation table — ACTIONABLE/NEEDS CLARIFICATION/TOO VAGUE rating + rewrites. "
            "(5) Event-adaptive missed items (8+, all specific to this event). "
            "(6) Pipeline improvement prescriptions (5+) with specific file/agent changes. "
            "(7) Structured priority list of top 10 decisions for Decision Layer — "
            "each with DECISION NEEDED, WHY URGENT, BEST OPTION, CONFIDENCE, RISK IF WRONG."
        ),
        agent=agent,
    )

# ─────────────────────────────────────────────
# TASK 13 — DECISION LAYER
# ─────────────────────────────────────────────
def task_decision_layer(agent, inputs: dict,
                         all_outputs: dict,
                         devils_advocate_output: str,
                         self_reflection_output: str,
                         pass2_summary: str = "",
                         outreach_output: str = "") -> 'Task':
    from crewai import Task
 
    budget    = inputs.get("budget_range",              "₹1 Crore")
    geography = inputs.get("geography_region",          "Delhi, India")
    date      = inputs.get("event_date_range",          "May 2026")
    category  = inputs.get("event_category",            "AI")
    objective = inputs.get("organizer_objective",       "brand building")
    audience  = inputs.get("target_audience_size",      "1000")
    constraints = inputs.get("hard_constraints",        "wheelchair accessible")
 
    return Task(
        description=f"""
You are the DECISION LAYER — the final arbiter of ConferaX.
 
USE THE SELF-REFLECTION PRIORITY LIST to ORDER your 10 decisions.
The Self-Reflection agent spent significant compute identifying which decisions
are most urgent. Respect that ordering unless you have a specific reason to disagree.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§A  AUTHORITATIVE INPUTS — READ ALL BEFORE DECIDING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 
EVENT: {category} | {geography} | {date} | {audience} people | {budget}
OBJECTIVE: {objective} | CONSTRAINTS: {constraints}
 
PREDICTION ENGINE PASS 2 — AUTHORITATIVE NUMBERS:
{pass2_summary}
 
SELF-REFLECTION PRIORITY LIST (use this to order your decisions):
{self_reflection_output[:4000]}
 
DEVIL'S ADVOCATE CHALLENGES (address these in your decisions):
{devils_advocate_output[:3000]}
 
OUTREACH EMAIL DRAFTS AVAILABLE (reference by number in action plan):
{outreach_output[:2000]}
 
ALL SPECIALIST OUTPUTS:
Strategy:   {all_outputs.get('strategy_profile', '')[:800]}
Sponsors:   {all_outputs.get('sponsor_output', '')[:1500]}
Exhibitors: {all_outputs.get('exhibitor_output', '')[:800]}
Speakers:   {all_outputs.get('speaker_output', '')[:1500]}
Venue:      {all_outputs.get('venue_output', '')[:1000]}
Pricing:    {all_outputs.get('pricing_output', '')[:800]}
GTM:        {all_outputs.get('gtm_output', '')[:800]}
Ops:        {all_outputs.get('ops_output', '')[:800]}
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§B  CONFIDENCE SCORE FORMULA (use for every decision)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Confidence = (Evidence Quality × 0.4) + (Feasibility × 0.3) +
             ((100 - DA Challenge Severity) × 0.2) + (Data Source Quality × 0.1)
 
Where:
  Evidence Quality:      0-100 (was this recommendation Tavily-sourced or inferred?)
  Feasibility:           0-100 (is this achievable within budget and timeline?)
  DA Challenge Severity: 0-100 (how hard did DA challenge this? 100 = destroyed the claim)
  Data Source Quality:   0-100 (Cvent-verified=100, comparable=60, general knowledge=30)
 
Show the arithmetic for every decision.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§C  DECISION BLOCK FORMAT (use for all 10 decisions)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 
---
## DECISION [N]: [Title]
(Ordered by Self-Reflection priority list — state if you are reordering and why)
 
**THE DECISION:**
[Specific, committed, named choice. Include INR amounts, venue names, speaker names,
email draft numbers, dates. No hedging. No "the best option."]
 
**JUSTIFICATION:**
[Why this specific choice over alternatives — cite specific agent outputs]
 
**DA CHALLENGE ADDRESSED:**
[Which DA challenge does this decision face? How does this decision address it?
If the DA found a serious flaw in this area, acknowledge it and explain
whether the decision mitigates it or accepts the risk]
 
**SELF-REFLECTION INPUT USED:**
[Which SR recommendation or data quality finding influenced this decision?]
 
**CONFIDENCE SCORE DERIVATION:**
  Evidence Quality:      [X]/100 — [reason]
  Feasibility:           [X]/100 — [reason]
  DA Challenge Severity: [X]/100 — [reason]
  Data Source Quality:   [X]/100 — [reason]
  CONFIDENCE = ([EQ]×0.4) + ([F]×0.3) + ([100-DA]×0.2) + ([DS]×0.1) = **[X]/100**
 
**TRADE-OFF ACCEPTED:**
[What you give up by choosing this over the alternatives]
 
**REVERSAL TRIGGER:**
[Exact condition that changes this decision — date, threshold, or event]
---
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§D  THE 10 DECISIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Use the Self-Reflection priority list to determine order.
Apply the decision block format above to each.
 
DECISION 1: VENUE (typically most urgent — venue availability is time-critical)
  Name the venue. Include day rate. Confirm it passes budget gate.
  Note exhibitor footfall score. Address DA's footfall/availability challenge.
  State: call venue by [date] for availability confirmation.
 
DECISION 2: TICKET PRICING STRUCTURE
  Exact INR prices for each tier (must align with Prediction Engine Pass 2 optimal price).
  If deviating from engine's optimal: state why and what revenue impact is accepted.
  State payment gateway: Razorpay primary, Instamojo backup.
  State early bird deadline and what % discount.
 
DECISION 3: TOP 3 SPONSORS TO APPROACH FIRST
  Name all 3 in priority order. For each:
  Which outreach email draft to send (1, 2, or 3).
  Exact first-message hook (one sentence).
  Expected response timeline.
  Address DA's close rate math challenge.
 
DECISION 4: KEYNOTE SPEAKER
  Name top choice. State influence score and how many dimensions were Tavily-verified.
  Name backup with influence score gap vs top choice.
  Which outreach email draft to send (4, 5, or 6).
  State honorarium range and travel coverage decision.
 
DECISION 5: EXHIBITOR STRATEGY
  Which cluster to target first. How many booths. At what fee.
  Which outreach email drafts to send (7, 8, or 9).
  What footfall-driving mechanism is in place (not just hoping people wander in).
  Address DA's exhibitor footfall challenge.
 
DECISION 6: PRIMARY GTM CHANNEL
  Name ONE channel and commit to it as primary.
  State first 3 messages (or reference them from GTM output).
  State budget allocation for paid channels (if any).
  Address DA's GTM math challenge (CPR × reach = registrations).
 
DECISION 7: BUDGET ALLOCATION
  Show the arithmetic. Total must equal {budget}.
 
  | Cost Center      | INR Amount | % of Budget | Notes |
  |-----------------|-----------|-------------|-------|
  | Venue            | ₹X        | X%          | [venue name] |
  | Speaker Fees     | ₹X        | X%          | [top 3 speakers] |
  | Marketing        | ₹X        | X%          | [channels] |
  | AV & Tech        | ₹X        | X%          | [hybrid cost if applicable] |
  | Ops & Logistics  | ₹X        | X%          | [staff, F&B] |
  | Exhibitor Setup  | ₹X        | X%          | [floor setup] |
  | Contingency      | ₹X        | X%          | [minimum 8%] |
  | **TOTAL**        | **₹X**    | **100%**    | ✅ balanced / ⚠️ gap |
 
  If total > {budget}: state which line item to cut and by how much.
 
DECISION 8: SCHEDULE CONFIRMATION
  Confirm the conflict detection results from Ops agent.
  If any ⚠️ CONFLICT flags remain unresolved: decide now.
  State the final session count, room count, and AV crew needed.
  State: by what date must speaker slot assignments be confirmed
  (this gates the Ops agent's resource matrix finalization).
 
DECISION 9: HIGHEST RISK TO MITIGATE THIS WEEK
  Name the single highest-risk item (from risk register + DA challenges).
  State the specific mitigation action and who owns it.
  State the deadline and what the contingency is if mitigation fails.
 
DECISION 10: GO / NO-GO CRITERIA
  Linked to Prediction Engine Pass 2 numbers.
 
  Using Pass 2 Monte Carlo results:
  | Criterion       | Threshold                    | Current Projection | Status |
  |----------------|------------------------------|--------------------|--------|
  | GO             | Revenue ≥ P50 = ₹[X]        | ₹[projected]       | [GO/RISK] |
  | CONDITIONAL GO | Revenue ≥ P25 = ₹[X] + 2 Tier 1 confirmed | [status] | [status] |
  | PAUSE          | Revenue < P25 = ₹[X] OR all Tier 1 decline | [trigger] | [status] |
  | NO-GO          | P10 = ₹[X] < fixed costs ₹[X] | [current P10] | [safe/risky] |
 
  CURRENT RECOMMENDATION: [GO / CONDITIONAL GO / PAUSE / NO-GO]
  REASON: [specific financial reasoning using Pass 2 numbers]
 
  MINIMUM VIABLE EVENT:
  What is the smallest version of this event that is financially viable?
  (reduced speaker count? smaller venue? no exhibitor floor?)
  At what point does scope reduction make this a different event entirely?
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§E  7-DAY ACTION PLAN (with outreach email integration)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Every day must reference specific outputs from the pipeline.
No generic "contact sponsors" — name the email draft, the company, the contact.
 
DAY 1 (Today):
  Action 1: [specific action] — Owner: [role] — Output: [what is produced]
  Action 2: Send Outreach Email Draft [N] to [Company/Person] — Subject: [from draft]
  Action 3: [specific action]
  Success criteria: [what must be true by end of Day 1]
 
DAY 2:
  Action 1: [specific action]
  Action 2: Send Outreach Email Draft [N] to [Company/Person]
  [etc.]
  Success criteria: [measurable outcome]
 
DAY 3: [same format]
DAY 4: [same format]
DAY 5: [same format]
DAY 6: [same format]
DAY 7: [same format]
 
END OF WEEK 1 SUCCESS METRICS:
  [ ] Venue availability confirmed for {date}
  [ ] Tier 1 sponsor outreach sent (Drafts 1, 2, 3)
  [ ] Keynote speaker outreach sent (Draft 4)
  [ ] Razorpay KYC process started
  [ ] [Add event-specific metrics]

 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FINAL VERDICT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 
OVERALL PLAN VIABILITY: [X]/100
  Scoring: Average of all 10 decision confidence scores.
  [X] = sum of confidence scores / 10
 
RECOMMENDED PATH:
  [ ] PROCEED — all major risks mitigated, revenue model viable
  [ ] PROCEED WITH MODIFICATIONS — [specific modifications required before proceeding]
  [ ] PAUSE AND REASSESS — [specific condition that must change before proceeding]
 
ONE-SENTENCE STRATEGIC RECOMMENDATION:
  [The single clearest statement of what the organizer should do tomorrow morning]
 
DECISIONS THAT MUST BE MADE BY TOMORROW (or the plan degrades):
  1. [Decision + what degrades if delayed]
  2. [Decision + what degrades if delayed]
  3. [Decision + what degrades if delayed]
""",
        expected_output=(
            "Decision Layer report with 10 committed, specific decisions. "
            "Decisions ordered by Self-Reflection priority list. "
            "Every decision uses the full block format: "
            "DECISION + JUSTIFICATION + DA CHALLENGE ADDRESSED + SR INPUT USED + "
            "CONFIDENCE DERIVATION (with arithmetic) + TRADE-OFF + REVERSAL TRIGGER. "
            f"Budget allocation table adds to {budget} exactly. "
            "Go/No-Go criteria linked to P10/P25/P50 from Pass 2 with real numbers. "
            "7-day action plan references specific outreach email drafts by number. "
            "Final verdict with viability score derived from confidence scores."
        ),
        agent=agent,
    )