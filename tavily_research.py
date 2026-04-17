# tavily_research_v5.py — ConferaX v5.0 (Speaker Upgrades)
# IMPROVED: 22 parallel searches
# New searches added:
#   - sponsor_history, startup_ecosystem, marketing_signals
#   - speaker_linkedin_events, speaker_academic, speaker_github, speaker_social
#   - venue_past_events, venue_pricing
#
# PHILOSOPHY: The agents' #1 improvement need is better raw intelligence.
# More Tavily data = more real names/venues/prices = less hallucination = highly realistic outputs.

import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from dotenv import load_dotenv
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
TAVILY_URL = "https://api.tavily.com/search"

INDIVIDUAL_AGENT_MAX_CHARS   = 8700
RESEARCH_AGENT_MAX_CHARS     = 8500
INDIVIDUAL_AGENT_MAX_RESULTS = 8
RESEARCH_AGENT_MAX_RESULTS   = 8


def tavily_search(query: str, max_results: int = 5) -> list[dict]:
    if not TAVILY_API_KEY:
        print(f"  ⚠️  TAVILY_API_KEY not set — skipping: {query[:60]}")
        return []

    try:
        response = requests.post(
            TAVILY_URL,
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "advanced",
                "max_results": max_results,
                "include_answer": True,
                "include_raw_content": False,
            },
            timeout=20,
        )
        response.raise_for_status()
        data    = response.json()
        results = data.get("results", [])
        answer  = data.get("answer", "")

        if answer:
            results.insert(0, {
                "title":   "Tavily AI Summary",
                "url":     "",
                "content": answer,
                "score":   1.0,
            })

        return results

    except requests.exceptions.Timeout:
        print(f"\n  ⚠️  Tavily timeout: {query[:60]}")
        return []
    except Exception as e:
        print(f"\n  ⚠️  Tavily error: {str(e)[:80]}")
        return []


def trim_results(results: list[dict],
                 max_chars_per_result: int = 3000,
                 max_results: int = 5) -> str:
    if not results:
        return "No data found for this query."

    lines = []
    for i, r in enumerate(results[:max_results]):
        title   = r.get("title", "")[:120]
        url     = r.get("url", "")
        content = r.get("content", "")[:max_chars_per_result]
        score   = r.get("score", 0)

        lines.append(f"[{i+1}] {title}" + (f" (relevance: {score:.2f})" if score else ""))
        if url:
            lines.append(f"    Source: {url}")
        lines.append(f"    {content}")
        lines.append("")

    return "\n".join(lines)


def run_phase0_research(inputs: dict) -> dict:
    """
    Runs 22 Tavily searches IN PARALLEL.
    """
    category     = inputs.get("event_category",            "AI")
    geography    = inputs.get("geography_region",          "India")
    event_format = inputs.get("event_format",              "Summit")
    sponsor_prio = inputs.get("sponsor_priority",          "tech companies VCs")
    audience     = inputs.get("expected_audience_persona", "founders developers investors")

    print("\n  🌐 Phase 0: Tavily parallel batch search (22 queries simultaneously)...")

    search_jobs = {
        # ── Original 10 (v3.0) ─────────────────────────────────
        "comparable_events": (
            f"{category} conference summit {geography} 2024 2025 attendees ticket sponsors exhibitors",
            7
        ),
        "sponsor_landscape": (
            f"{category} tech event sponsor {geography} {sponsor_prio} 2024 2025 marketing partnership conference",
            7
        ),
        "speaker_landscape": (
            f"top {category} speakers keynote India {geography} 2024 2025 conference summit invited talk",
            7
        ),
        "venue_signals": (
            f"best conference venue {event_format} {geography} 2024 2025 capacity premium indoor site:cvent.com OR site:eventlocations.com OR venue",
            7
        ),
        "pricing_benchmarks": (
            f"{category} tech conference ticket price registration fee India 2024 2025 paid tiered",
            7
        ),
        "market_context": (
            f"{category} startup ecosystem {geography} India 2025 2026 funding growth trends community",
            7
        ),
        "exhibitor_landscape": (
            f"companies exhibited {category} conference expo India {geography} 2024 2025 exhibitor list booth startup enterprise",
            7
        ),
        "disboard_communities": (
            f"site:disboard.org {category} AI startup developer India discord server community members",
            5
        ),
        "cvent_venues": (
            f"site:cvent.com conference venue {geography} India capacity {event_format} 2025",
            5
        ),
        "academic_speakers": (
            f"{category} researcher author India 2024 2025 site:scholar.google.com OR site:semanticscholar.org OR site:arxiv.org h-index citations keynote",
            7
        ),

        # ── v4.0: Sponsor intelligence searches ─────────────────
        "sponsor_history": (
            f"sponsors of {category} conference {geography} India 2024 2025 title sponsor gold silver partnership brand",
            7
        ),
        "startup_ecosystem": (
            f"{category} startup funding {geography} India 2024 2025 Series A Series B raised launched product developer",
            7
        ),
        "marketing_signals": (
            f"{category} company India {geography} 2025 developer program launch expansion partnership marketing budget",
            7
        ),
        "meetup_communities": (
            f"meetup.com {category} tech startup {geography} India group members events 2024 2025",
            5
        ),
        "media_newsletters": (
            f"Inc42 OR YourStory OR TheKen OR AIM OR Entrackr {category} {geography} newsletter subscribers startup founders India 2025",
            5
        ),
        "influencer_creators": (
            f"{category} India Twitter LinkedIn YouTube creator influencer {geography} followers community podcast 2024 2025",
            7
        ),

        # ── v5: Speaker searches (replaces v4.0 speaker_linkedin + speaker_events) ──
        "speaker_linkedin_events": (
            # Practitioner discovery:
            # Public LinkedIn profile snippets + Luma/Konfhub/HasGeek/NASSCOM history
            f"{category} {geography} speaker keynote panelist site:linkedin.com/in OR "
            f"site:lu.ma OR site:konfhub.com OR site:hasgeek.com OR nasscom 2024 2025",
            7
        ),
        "speaker_academic": (
            # Academic discovery: Scholar, arXiv, Semantic Scholar
            f"{category} researcher India 2024 2025 "
            f"site:scholar.google.com OR site:semanticscholar.org OR site:arxiv.org "
            f"h-index citations keynote conference speaker",
            7
        ),
        "speaker_github": (
            # Practitioner credibility for developer/tech events
            f"{category} India developer engineer creator "
            f"site:github.com stars repositories contributions 2024 2025",
            5
        ),
        "speaker_social": (
            # Covers ALL non-academic social platforms in one search
            f"{category} India speaker creator artist performer influencer "
            f"Instagram OR YouTube OR Substack OR Spotify OR podcast OR SoundCloud "
            f"followers subscribers 2024 2025 {geography}",
            7
        ),

        # ── v4.0: Venue intelligence searches ───────────────────
        "venue_past_events": (
            # Finds real events held at specific venues in geography
            f"conference summit expo {geography} India venue held 2024 2025 attendees review",
            7
        ),
        "venue_pricing": (
            # Gets real day rate signals for venues in geography
            f"conference venue {geography} India day rate pricing per day hire cost 2024 2025",
            5
        ),
    }

    raw_results = {}
    start = time.time()

    # Increased to 22 workers for the expanded query set
    with ThreadPoolExecutor(max_workers=22) as executor:
        future_to_key = {
            executor.submit(tavily_search, query, max_r): key
            for key, (query, max_r) in search_jobs.items()
        }
        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                raw_results[key] = future.result()
                print(f"  ✓ {key.replace('_', ' ').title()} search complete")
            except Exception as e:
                print(f"  ⚠️  {key} failed: {str(e)[:60]}")
                raw_results[key] = []

    elapsed = time.time() - start
    print(f"\n  ✅ All 22 searches complete in {elapsed:.1f}s")

    def trim_individual(raw):
        return trim_results(raw,
                            max_chars_per_result=INDIVIDUAL_AGENT_MAX_CHARS,
                            max_results=INDIVIDUAL_AGENT_MAX_RESULTS)

    def trim_research(raw):
        return trim_results(raw,
                            max_chars_per_result=RESEARCH_AGENT_MAX_CHARS,
                            max_results=RESEARCH_AGENT_MAX_RESULTS)

    searches_individual = {k: trim_individual(v) for k, v in raw_results.items()}
    searches_research   = {k: trim_research(v)  for k, v in raw_results.items()}

    def _build_snippet(header: str, sections: dict) -> str:
        lines = [f"\n{'='*60}", f"  {header}", f"{'='*60}"]
        for name, content in sections.items():
            lines.append(f"\n### {name}")
            lines.append(content if content.strip() else "No data found.")
        lines.append(f"{'='*60}\n")
        return "\n".join(lines)

    agent_context = {

        "orchestrator": _build_snippet(
            "REAL-WORLD MARKET CONTEXT (Tavily — pre-fetched, advanced depth)",
            {
                "Comparable Events":      searches_individual["comparable_events"],
                "Current Market Context": searches_individual["market_context"],
                "Exhibitor Landscape":    searches_individual["exhibitor_landscape"],
                "Startup Ecosystem":      searches_individual["startup_ecosystem"],
            }
        ),

        # Research agent gets ALL 22 searches
        "research": _build_snippet(
            "REAL-WORLD RESEARCH DATA (Tavily — 22 parallel searches, advanced depth)",
            {
                "Comparable Events":          searches_research["comparable_events"],
                "Active Sponsor Landscape":   searches_research["sponsor_landscape"],
                "Sponsor History (New)":      searches_research["sponsor_history"],
                "Startup Ecosystem (New)":    searches_research["startup_ecosystem"],
                "Marketing Signals (New)":    searches_research["marketing_signals"],
                "Speaker Landscape":          searches_research["speaker_landscape"],
                "Academic Speaker Signals":   searches_research["academic_speakers"],
                "Speaker Academic Signals":          searches_research["speaker_academic"],
                "Speaker LinkedIn + Event History":  searches_research["speaker_linkedin_events"],
                "Speaker GitHub Credibility":        searches_research["speaker_github"],
                "Speaker Social (All Platforms)":    searches_research["speaker_social"],
                "Exhibitor Landscape":        searches_research["exhibitor_landscape"],
                "Venue Signals":              searches_research["venue_signals"],
                "Cvent Venue Listings":       searches_research["cvent_venues"],
                "Venue Past Events (New)":    searches_research["venue_past_events"],
                "Venue Pricing Signals (New)":    searches_research["venue_pricing"],
                "Pricing Benchmarks":         searches_research["pricing_benchmarks"],
                "Disboard Communities":       searches_research["disboard_communities"],
                "Market Context":             searches_research["market_context"],
            }
        ),

        # SPONSOR AGENT
        "sponsor": _build_snippet(
            "REAL-WORLD SPONSOR DATA — v4.0 ENHANCED (Tavily — 5 targeted sources)",
            {
                "=== PHASE 1 EXTRACTION SOURCE: Sponsor History ===\n"
                "READ THIS FIRST. Extract every company name near 'sponsor' keywords.":
                    searches_individual["sponsor_history"],
                "=== PHASE 1 EXTRACTION SOURCE: Comparable Events ===\n"
                "Extract any sponsor names mentioned near event descriptions.":
                    searches_individual["comparable_events"],
                "=== PHASE 1 EXTRACTION SOURCE: Active Sponsor Landscape ===\n"
                "Any company marketing signals near event/conference sponsorship context.":
                    searches_individual["sponsor_landscape"],
                "=== TIER 3 STARTUP CLUSTER SOURCE: Startup Ecosystem ===\n"
                "These funded startups are your Tier 3 (startup) sponsor candidates.":
                    searches_individual["startup_ecosystem"],
                "=== OPPORTUNISTIC SPONSORS SOURCE: Marketing Signals ===\n"
                "Companies with product launches, India expansion, or developer programs.":
                    searches_individual["marketing_signals"],
            }
        ),

        "exhibitor": _build_snippet(
            "REAL-WORLD EXHIBITOR DATA (Tavily — Cvent + EventLocations + comparable events)",
            {
                "Exhibitor Landscape":   searches_individual["exhibitor_landscape"],
                "Cvent Listings":        searches_individual["cvent_venues"],
                "Comparable Events":     searches_individual["comparable_events"],
            }
        ),

        "speaker": _build_snippet(
            "REAL-WORLD SPEAKER DATA — v5 ENHANCED (Tavily — 5 sources, all archetypes)",
            {
                "=== ACADEMIC ARCHETYPE: Scholar / arXiv / Semantic Scholar ===\n"
                "Extract: researcher names, h-index, citations, recent papers.\n"
                "These candidates are scored on the ACADEMIC formula.":
                    searches_individual["speaker_academic"],

                "=== PRACTITIONER ARCHETYPE: LinkedIn + Event History ===\n"
                "Extract: speaker names from LinkedIn snippets, Luma, Konfhub, HasGeek, NASSCOM.\n"
                "Label LinkedIn data: [PUBLIC PROFILE — via web search].\n"
                "These candidates are scored on the PRACTITIONER formula.":
                    searches_individual["speaker_linkedin_events"],

                "=== PRACTITIONER CREDIBILITY: GitHub (developer events) ===\n"
                "Extract: names with notable repos, star counts, contribution activity.\n"
                "Strong signal for developer-category events. Skip if non-tech event.":
                    searches_individual["speaker_github"],

                "=== ARTIST + PRACTITIONER SOCIAL: All non-academic platforms ===\n"
                "Extract: names with Instagram/YouTube/Substack/Spotify/Podcast presence.\n"
                "Artists: scored on ARTIST formula.\n"
                "Practitioners with social presence: add to Social Reach score.":
                    searches_individual["speaker_social"],

                "=== COMPARABLE EVENTS: Agenda and speaker benchmarks ===\n"
                "Extract: speaker names mentioned in past comparable event coverage.":
                    searches_individual["comparable_events"],
            }
        ),

        "venue": _build_snippet(
            "REAL-WORLD VENUE DATA — v4.0 ENHANCED (Tavily — 5 sources)",
            {
                "=== PHASE 1 BUDGET SOURCE: Venue pricing signals ===\n"
                "Extract day rates and pricing for venues in geography.":
                    searches_individual["venue_pricing"],

                "=== PHASE 3 PAST EVENT SOURCE: Real events at venues ===\n"
                "Extract event names, attendance, dates at specific venues.":
                    searches_individual["venue_past_events"],

                "=== CVENT LISTINGS ===":
                    searches_individual["cvent_venues"],

                "=== VENUE SIGNALS: General capacity and specs ===":
                    searches_individual["venue_signals"],

                "=== COMPARABLE EVENTS: What venues were used ===":
                    searches_individual["comparable_events"],
            }
        ),

        "pricing": _build_snippet(
            "REAL-WORLD PRICING BENCHMARKS (Tavily)",
            {
                "Ticket Pricing Benchmarks": searches_individual["pricing_benchmarks"],
                "Comparable Events":         searches_individual["comparable_events"],
                "Exhibitor Landscape":       searches_individual["exhibitor_landscape"],
            }
        ),

        "gtm": _build_snippet(
            "REAL-WORLD GTM & COMMUNITY DATA — v4.0 ENHANCED (Tavily — 7 sources)",
            {
                "=== PLATFORM 1: Discord Communities (Disboard) ===\n"
                "Extract every Discord server name, member count, and tags found.":
                    searches_individual["disboard_communities"],

                "=== PLATFORM 2+3: Telegram + Meetup Communities ===\n"
                "Extract every Telegram group and Meetup.com group name + member count.":
                   searches_individual["meetup_communities"],

                "=== PLATFORM 4+5: Newsletters and Media Partners ===\n"
                "Extract every newsletter name, subscriber count, and media outlet found.":
                   searches_individual["media_newsletters"],

                "=== PLATFORM 7: Influencers and Creators ===\n"
                "Extract every creator name, platform, and follower count found.":
                   searches_individual["influencer_creators"],

                "=== MARKET CONTEXT for messaging ===":
                   searches_individual["market_context"],

                "=== COMPARABLE EVENTS for community crossover ===":
                   searches_individual["comparable_events"],

                "=== STARTUP ECOSYSTEM for community identification ===":
                   searches_individual["startup_ecosystem"],
            }
       ),

    }

    # Token budget summary
    print("\n  📊 Web context token budget per agent (Gemma 4 — 256K window):")
    for agent, ctx in agent_context.items():
        tokens_est = len(ctx) // 4
        print(f"     {agent:<20} ~{tokens_est:,} tokens")
    print()

    return agent_context