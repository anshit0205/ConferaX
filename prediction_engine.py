# prediction_engine.py — ConferaX v3.0
# Two-Pass Quantitative Prediction Engine
#
# PHILOSOPHY:
#   Agents provide judgment, qualitative reasoning, and market intelligence.
#   This engine provides arithmetic, optimization, and quantitative grounding.
#   Neither does the other's job.
#
#   Pass 1: Runs on user inputs ONLY, before any agent starts.
#           Grounds agents in computed reality — price ranges, break-even,
#           elasticity curves — so they reason from a mathematical foundation,
#           not from hallucinated numbers.
#
#   Pass 2: Runs after Sponsor + Exhibitor agents produce their estimates.
#           Reconciles agent qualitative estimates with the quantitative model.
#           Produces ONE authoritative set of numbers used by:
#           - Pricing Agent (to explain and validate)
#           - Decision Layer (to make decisions)
#           - Synthesizer (to write the report)
#           - HTML Generator (to draw all charts)
#
#   PRICING MODE AWARENESS:
#   The engine detects the ticketing intent from user input and routes to
#   the correct model. Free events have zero ticket revenue and different
#   no-show dynamics. Tiered-with-free events have cannibalization risk.
#   Invite-only events skip pricing entirely. The model handles all cases.

import numpy as np
import re


# ─────────────────────────────────────────────────────────────
# PERSONA PROFILES — auto-detected, not hardcoded
# Covers tech AND non-tech audiences
# ─────────────────────────────────────────────────────────────

PERSONA_PROFILES = {
    # High price sensitivity
    "student":        {"elasticity": -0.80, "no_show_base": 0.38, "vip_propensity": 0.02},
    "researcher":     {"elasticity": -0.65, "no_show_base": 0.32, "vip_propensity": 0.05},
    "developer":      {"elasticity": -0.60, "no_show_base": 0.28, "vip_propensity": 0.08},
    "engineer":       {"elasticity": -0.55, "no_show_base": 0.25, "vip_propensity": 0.10},
    "academic":       {"elasticity": -0.65, "no_show_base": 0.30, "vip_propensity": 0.04},
    "teacher":        {"elasticity": -0.70, "no_show_base": 0.30, "vip_propensity": 0.04},
    "freelancer":     {"elasticity": -0.55, "no_show_base": 0.30, "vip_propensity": 0.08},

    # Moderate price sensitivity
    "founder":        {"elasticity": -0.35, "no_show_base": 0.18, "vip_propensity": 0.20},
    "entrepreneur":   {"elasticity": -0.35, "no_show_base": 0.20, "vip_propensity": 0.18},
    "professional":   {"elasticity": -0.30, "no_show_base": 0.22, "vip_propensity": 0.15},
    "manager":        {"elasticity": -0.28, "no_show_base": 0.20, "vip_propensity": 0.18},
    "marketer":       {"elasticity": -0.32, "no_show_base": 0.25, "vip_propensity": 0.12},
    "designer":       {"elasticity": -0.45, "no_show_base": 0.26, "vip_propensity": 0.10},
    "consultant":     {"elasticity": -0.28, "no_show_base": 0.22, "vip_propensity": 0.20},
    "doctor":         {"elasticity": -0.20, "no_show_base": 0.18, "vip_propensity": 0.25},
    "healthcare":     {"elasticity": -0.22, "no_show_base": 0.20, "vip_propensity": 0.22},
    "policy":         {"elasticity": -0.18, "no_show_base": 0.30, "vip_propensity": 0.15},
    "journalist":     {"elasticity": -0.40, "no_show_base": 0.22, "vip_propensity": 0.10},
    "artist":         {"elasticity": -0.55, "no_show_base": 0.28, "vip_propensity": 0.06},
    "hr":             {"elasticity": -0.30, "no_show_base": 0.22, "vip_propensity": 0.15},
    "sales":          {"elasticity": -0.25, "no_show_base": 0.20, "vip_propensity": 0.20},

    # Low price sensitivity
    "investor":       {"elasticity": -0.10, "no_show_base": 0.12, "vip_propensity": 0.55},
    "vc":             {"elasticity": -0.08, "no_show_base": 0.12, "vip_propensity": 0.60},
    "executive":      {"elasticity": -0.12, "no_show_base": 0.14, "vip_propensity": 0.50},
    "cxo":            {"elasticity": -0.08, "no_show_base": 0.12, "vip_propensity": 0.60},
    "ceo":            {"elasticity": -0.10, "no_show_base": 0.14, "vip_propensity": 0.55},
    "vp":             {"elasticity": -0.15, "no_show_base": 0.15, "vip_propensity": 0.45},

    # Default fallback — used when persona is unrecognized
    "default":        {"elasticity": -0.40, "no_show_base": 0.25, "vip_propensity": 0.15},
}

OBJECTIVE_PRICE_BIAS = {
    "revenue":           +0.25,
    "brand building":    -0.15,
    "brand":             -0.10,
    "community":         -0.25,
    "community growth":  -0.25,
    "leads":             +0.10,
    "lead generation":   +0.10,
    "networking":        +0.05,
    "education":         -0.20,
    "awareness":         -0.15,
    "default":            0.00,
}


# ─────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────

def detect_pricing_mode(ticketing_intent: str) -> str:
    """
    Detects pricing mode from ticketing_intent string.
    Returns one of: free | fixed | tiered | tiered_with_free | invite_only | hybrid
    """
    t = ticketing_intent.lower().strip()

    if "invite" in t:
        return "invite_only"

    has_free   = "free" in t
    has_paid   = any(w in t for w in ["paid", "tiered", "ticket", "price"])
    has_hybrid = "hybrid" in t or ("online" in t and "person" in t)
    has_fixed  = "fixed" in t or re.search(r'₹\s*\d+', t)

    if has_hybrid:
        return "hybrid"
    if has_free and has_paid:
        return "tiered_with_free"
    if has_free:
        return "free"
    if has_fixed and not has_paid:
        return "fixed"
    if "tiered" in t or "tier" in t:
        return "tiered"
    if "paid" in t:
        return "tiered"

    return "tiered"  # default


def detect_persona_mix(persona_string: str) -> dict:
    """
    Input:  "Founders, developers, investors"
    Output: {"founder": {weight:0.33, elasticity:-0.35, ...}, ...}
    Works for any audience — tech or non-tech.
    """
    text = persona_string.lower()
    detected = {}
    for persona, profile in PERSONA_PROFILES.items():
        if persona == "default":
            continue
        if persona in text:
            detected[persona] = profile.copy()

    if not detected:
        detected["default"] = PERSONA_PROFILES["default"].copy()

    weight = 1.0 / len(detected)
    for k in detected:
        detected[k]["weight"] = weight

    return detected


def detect_objective_bias(objective_string: str) -> float:
    text = objective_string.lower()
    for key, bias in OBJECTIVE_PRICE_BIAS.items():
        if key in text:
            return bias
    return 0.0


def parse_budget(budget_string: str) -> float:
    text = budget_string.lower().replace(',', '').replace(' ', '')
    numbers = re.findall(r'[\d.]+', text)
    if not numbers:
        return 5_000_000
    n = float(numbers[0])
    if 'crore' in text or 'cr' in text:
        return n * 10_000_000
    if 'lakh' in text or 'lac' in text or text.endswith('l'):
        return n * 100_000
    if 'k' in text and '$' in budget_string:
        return n * 1000 * 83
    if 'k' in text:
        return n * 1000
    return n


def parse_inr_values(text: str) -> list:
    """
    Extracts INR amounts from agent text.
    Handles: ₹50,000 / Rs. 5L / INR 1Cr / ₹2.5 crore
    """
    results = []

    # Match crore
    for m in re.finditer(r'(?:₹|Rs\.?|INR)\s*([\d.]+)\s*(?:crore|cr)', text, re.IGNORECASE):
        results.append(int(float(m.group(1)) * 10_000_000))

    # Match lakh
    for m in re.finditer(r'(?:₹|Rs\.?|INR)\s*([\d.]+)\s*(?:lakh|lac|l\b)', text, re.IGNORECASE):
        results.append(int(float(m.group(1)) * 100_000))

    # Match plain numbers with currency symbol
    for m in re.finditer(r'(?:₹|Rs\.?)\s*([\d,]+)', text):
        n = int(m.group(1).replace(',', ''))
        if n > 100:  # ignore tiny numbers
            results.append(n)

    return results


def _weighted_attr(persona_mix: dict, attr: str) -> float:
    return sum(
        p.get("weight", 0) * p.get(attr, 0)
        for p in persona_mix.values()
    )


# ─────────────────────────────────────────────────────────────
# CORE DEMAND AND NO-SHOW MODELS
# ─────────────────────────────────────────────────────────────

def compute_demand(price: float, base_price: float,
                   target: int, persona_mix: dict) -> float:
    """
    Price elasticity demand model.
    Q = Q0 * (P / P0) ^ elasticity
    Weighted across all detected personas.
    """
    elasticity = _weighted_attr(persona_mix, "elasticity")
    if base_price <= 0:
        base_price = 1000
    if price <= 0:
        return float(target)  # free = full demand up to capacity

    demand = target * ((price / base_price) ** elasticity)
    return float(np.clip(demand, target * 0.05, target * 2.5))


def compute_no_show(price: float, persona_mix: dict,
                    weeks_to_event: int = 8) -> float:
    """
    No-show rate model.
    Base rate from persona, reduced by price paid, increased by lead time.
    Free events use persona base directly (no price reduction).
    """
    base = _weighted_attr(persona_mix, "no_show_base")
    price_reduction = 0.0 if price <= 0 else min(0.15, 0.03 * np.log10(max(price, 100) / 100))
    time_addition   = max(0.0, 0.015 * (weeks_to_event - 6))
    return float(np.clip(base - price_reduction + time_addition, 0.05, 0.55))


# ─────────────────────────────────────────────────────────────
# PRICING MODELS — one per ticketing mode
# ─────────────────────────────────────────────────────────────

def _model_free(target: int, persona_mix: dict,
                budget: float, weeks_to_event: int = 8) -> dict:
    """
    Free event model.
    Ticket revenue = 0. Attendance = capacity-constrained demand.
    No-show rate is high (free events in India: 30-45%).
    Break-even depends entirely on sponsors + exhibitors.
    """
    no_show = compute_no_show(0, persona_mix, weeks_to_event)
    # Free events: registrations often exceed target, actual = lower
    expected_registrations = min(int(target * 1.8), target * 2)
    actual_attendance      = int(expected_registrations * (1 - no_show))

    return {
        "mode":                  "free",
        "tiers": {
            "free": {
                "price":           0,
                "expected_sales":  expected_registrations,
                "revenue":         0,
                "label":           "Free Entry",
            }
        },
        "total_ticket_revenue":  0,
        "total_registrations":   expected_registrations,
        "actual_attendance":     actual_attendance,
        "no_show_rate":          no_show,
        "note": "Free event — ticket revenue is zero. Break-even depends entirely on sponsor and exhibitor revenue."
    }


def _model_fixed(target: int, persona_mix: dict,
                 budget: float, objective_bias: float,
                 fixed_price: float = None) -> dict:
    """
    Fixed single-price model.
    Finds optimal single price if not specified.
    """
    if fixed_price is None:
        cost_per_head = (budget * 0.55) / max(target, 1)
        fixed_price   = max(200, cost_per_head * 1.3 * (1 + objective_bias))
        fixed_price   = round(fixed_price, -2)

    demand    = compute_demand(fixed_price, fixed_price, target, persona_mix)
    no_show   = compute_no_show(fixed_price, persona_mix)
    actual    = int(demand * (1 - no_show))
    revenue   = int(actual * fixed_price)

    return {
        "mode": "fixed",
        "tiers": {
            "general": {
                "price":          int(fixed_price),
                "expected_sales": int(demand),
                "revenue":        revenue,
                "label":          "Standard Entry",
            }
        },
        "total_ticket_revenue":  revenue,
        "total_registrations":   int(demand),
        "actual_attendance":     actual,
        "no_show_rate":          no_show,
    }


def _model_tiered(target: int, persona_mix: dict,
                  budget: float, objective_bias: float) -> dict:
    """
    Tiered pricing: Early Bird / General / VIP
    Searches optimal combination via grid search.
    VIP propensity from persona mix determines VIP uptake.
    """
    cost_per_head = (budget * 0.55) / max(target, 1)
    base_price    = max(500, cost_per_head * 1.4 * (1 + objective_bias))
    vip_pct       = _weighted_attr(persona_mix, "vip_propensity")

    best_revenue = 0
    best_tiers   = {}

    for eb_discount in [0.30, 0.35, 0.40, 0.45, 0.50]:
        for vip_mult in [2.5, 3.0, 3.5, 4.0, 5.0]:
            eb_price      = max(200, round(base_price * (1 - eb_discount), -2))
            gen_price     = round(base_price, -2)
            vip_price     = round(base_price * vip_mult, -2)

            total_demand  = compute_demand(gen_price, gen_price, target, persona_mix)
            eb_sales      = int(total_demand * 0.25)
            vip_sales     = int(total_demand * vip_pct)
            gen_sales     = int(total_demand * (1 - 0.25 - vip_pct))

            revenue = (eb_sales * eb_price +
                       gen_sales * gen_price +
                       vip_sales * vip_price)

            if revenue > best_revenue:
                best_revenue = revenue
                no_show = compute_no_show(gen_price, persona_mix)
                total_regs = eb_sales + gen_sales + vip_sales
                best_tiers = {
                    "early_bird": {
                        "price":          int(eb_price),
                        "expected_sales": eb_sales,
                        "revenue":        int(eb_sales * eb_price),
                        "discount_pct":   int(eb_discount * 100),
                        "label":          "Early Bird",
                    },
                    "general": {
                        "price":          int(gen_price),
                        "expected_sales": gen_sales,
                        "revenue":        int(gen_sales * gen_price),
                        "label":          "General",
                    },
                    "vip": {
                        "price":          int(vip_price),
                        "expected_sales": vip_sales,
                        "revenue":        int(vip_sales * vip_price),
                        "multiplier":     vip_mult,
                        "label":          "VIP",
                    },
                    "_meta": {
                        "total_ticket_revenue":  int(best_revenue),
                        "total_registrations":   total_regs,
                        "actual_attendance":     int(total_regs * (1 - no_show)),
                        "no_show_rate":          no_show,
                    }
                }

    result = {k: v for k, v in best_tiers.items() if k != "_meta"}
    result.update(best_tiers.get("_meta", {}))
    result["mode"] = "tiered"
    return result


def _model_tiered_with_free(target: int, persona_mix: dict,
                             budget: float, objective_bias: float) -> dict:
    """
    Tiered pricing with a free base tier.
    Free tier drives attendance; paid tiers depend on upgrade rate.

    Upgrade rate: % of free registrants who also buy a paid tier.
    Depends on persona — investors upgrade more than students.
    Cannibalization factor: if free tier is too generous, paid tier collapses.

    Key insight: paid tier must add clear, tangible value that free doesn't offer.
    (workshops, networking dinner, certificate, speaker meet-and-greet)
    """
    vip_pct    = _weighted_attr(persona_mix, "vip_propensity")
    elasticity = _weighted_attr(persona_mix, "elasticity")

    # Upgrade rates by persona sensitivity
    # More price-sensitive personas upgrade less
    upgrade_to_paid = float(np.clip(0.35 + elasticity * 0.3, 0.05, 0.60))
    upgrade_to_vip  = float(np.clip(vip_pct * 0.6, 0.01, 0.30))

    # Free registrations — higher than paid, limited by capacity
    free_regs    = min(int(target * 1.6), target * 2)
    paid_regs    = int(free_regs * upgrade_to_paid)
    vip_regs     = int(free_regs * upgrade_to_vip)

    cost_per_head = (budget * 0.45) / max(target, 1)
    paid_price    = max(299, round(cost_per_head * 0.8 * (1 + objective_bias), -2))
    vip_price     = max(999, round(paid_price * 3.5, -2))

    paid_revenue = paid_regs * paid_price
    vip_revenue  = vip_regs  * vip_price
    total_revenue = paid_revenue + vip_revenue

    no_show_free = compute_no_show(0, persona_mix)
    no_show_paid = compute_no_show(paid_price, persona_mix)

    return {
        "mode": "tiered_with_free",
        "tiers": {
            "free": {
                "price":           0,
                "expected_sales":  free_regs,
                "revenue":         0,
                "label":           "Free Entry",
                "no_show":         no_show_free,
            },
            "paid": {
                "price":           int(paid_price),
                "expected_sales":  paid_regs,
                "revenue":         int(paid_revenue),
                "upgrade_rate_pct": int(upgrade_to_paid * 100),
                "label":           "Workshop Access",
                "no_show":         no_show_paid,
            },
            "vip": {
                "price":           int(vip_price),
                "expected_sales":  vip_regs,
                "revenue":         int(vip_revenue),
                "upgrade_rate_pct": int(upgrade_to_vip * 100),
                "label":           "VIP + Networking",
                "no_show":         no_show_paid,
            },
        },
        "total_ticket_revenue":  int(total_revenue),
        "total_registrations":   free_regs + paid_regs + vip_regs,
        "actual_attendance":     int(free_regs * (1 - no_show_free)),
        "no_show_rate":          no_show_free,
        "cannibalization_risk":  "HIGH" if upgrade_to_paid < 0.10 else
                                 "MEDIUM" if upgrade_to_paid < 0.20 else "LOW",
        "note": (
            f"Free tier drives attendance. "
            f"Estimated {int(upgrade_to_paid*100)}% will upgrade to paid tier. "
            f"Cannibalization risk: {'HIGH — paid tier needs strong differentiators' if upgrade_to_paid < 0.10 else 'MEDIUM' if upgrade_to_paid < 0.20 else 'LOW'}."
        )
    }


def _model_invite_only(target: int, budget: float) -> dict:
    """
    Invite-only: no public ticket sales.
    Zero ticket revenue. Break-even depends entirely on sponsors/organizer.
    """
    return {
        "mode":                 "invite_only",
        "tiers":                {},
        "total_ticket_revenue": 0,
        "total_registrations":  target,
        "actual_attendance":    int(target * 0.85),  # invite-only shows up
        "no_show_rate":         0.15,
        "note": "Invite-only event — no public ticket revenue. Costs covered by sponsors and organizer budget."
    }


def _model_hybrid(target: int, persona_mix: dict,
                  budget: float, objective_bias: float) -> dict:
    """
    Hybrid: free online + paid in-person.
    Two attendance pools. In-person uses fixed price model.
    Online multiplier adds sponsor value.
    """
    in_person_target = int(target * 0.6)
    online_target    = int(target * 2.5)   # online often 3-4x in-person

    fixed = _model_fixed(in_person_target, persona_mix, budget, objective_bias)

    return {
        "mode":                 "hybrid",
        "tiers":                fixed["tiers"],
        "total_ticket_revenue": fixed["total_ticket_revenue"],
        "total_registrations":  in_person_target + online_target,
        "in_person_attendance": fixed["actual_attendance"],
        "online_attendance":    online_target,
        "actual_attendance":    fixed["actual_attendance"],
        "no_show_rate":         fixed["no_show_rate"],
        "online_multiplier":    round(online_target / max(in_person_target, 1), 1),
        "note": f"Hybrid event. In-person: ~{in_person_target} paid. Online: ~{online_target} free. Sponsor value enhanced by online reach."
    }


# ─────────────────────────────────────────────────────────────
# PRICING vs ATTENDANCE CURVE
# ─────────────────────────────────────────────────────────────

def compute_pricing_curve(target: int, persona_mix: dict,
                           base_sponsor_rev: float,
                           base_exhibitor_rev: float,
                           pricing_mode: str = "tiered") -> dict:
    """
    The core pricing vs attendance forecast.

    For each price point, computes attendance AND total revenue
    across all 3 streams simultaneously.

    Key insight: ticket price affects exhibitor and sponsor revenue too.
    Fewer attendees = less foot traffic = exhibitors pay less.
    Fewer attendees = smaller audience = sponsors pay less.
    Optimal ticket price is where TOTAL revenue (not just ticket) is highest.

    Free and invite-only modes return simplified curves.
    """
    if pricing_mode in ("free", "invite_only"):
        # No price to optimize — return flat curve
        return {
            "curve": [],
            "optimal_total":      {"price": 0, "actual_attendance": target, "total_revenue": base_sponsor_rev + base_exhibitor_rev},
            "optimal_ticket":     {"price": 0, "actual_attendance": target, "ticket_revenue": 0},
            "optimal_attendance": {"price": 0, "actual_attendance": target},
        }

    price_points = [200, 500, 750, 1000, 1500, 2000, 2500,
                    3000, 4000, 5000, 6000, 8000, 10000, 15000]
    base_price   = 3000

    curve = []
    for price in price_points:
        attendance = compute_demand(price, base_price, target, persona_mix)
        no_show    = compute_no_show(price, persona_mix)
        actual     = attendance * (1 - no_show)

        # Revenue interaction effect:
        # Exhibitors care about foot traffic (power 0.6)
        # Sponsors care about brand reach (power 0.4)
        ft_ratio      = actual / max(target, 1)
        exhibitor_rev = base_exhibitor_rev * (ft_ratio ** 0.6)
        sponsor_rev   = base_sponsor_rev   * (ft_ratio ** 0.4)
        ticket_rev    = actual * price
        total_rev     = ticket_rev + exhibitor_rev + sponsor_rev

        curve.append({
            "price":              int(price),
            "registrations":      int(attendance),
            "actual_attendance":  int(actual),
            "no_show_rate":       round(no_show, 2),
            "ticket_revenue":     int(ticket_rev),
            "exhibitor_revenue":  int(exhibitor_rev),
            "sponsor_revenue":    int(sponsor_rev),
            "total_revenue":      int(total_rev),
        })

    optimal_total   = max(curve, key=lambda x: x["total_revenue"])
    optimal_ticket  = max(curve, key=lambda x: x["ticket_revenue"])
    optimal_attend  = max(curve, key=lambda x: x["registrations"])

    return {
        "curve":              curve,
        "optimal_total":      optimal_total,
        "optimal_ticket":     optimal_ticket,
        "optimal_attendance": optimal_attend,
    }


# ─────────────────────────────────────────────────────────────
# BREAK-EVEN ANALYSIS
# ─────────────────────────────────────────────────────────────

def compute_breakeven(budget: float, tier_structure: dict,
                      base_sponsor_rev: float,
                      base_exhibitor_rev: float,
                      target: int,
                      pricing_mode: str = "tiered") -> dict:
    """
    Break-even analysis per ticket tier.
    Handles zero-ticket-revenue modes gracefully.

    For free/invite-only: break-even is whether sponsors + exhibitors cover costs.
    For paid modes: break-even attendance per tier.
    """
    fixed_cost    = budget * 0.60
    variable_cost = (budget * 0.15) / max(target, 1)

    if pricing_mode in ("free", "invite_only"):
        gap = fixed_cost - base_sponsor_rev - base_exhibitor_rev
        return {
            "mode": pricing_mode,
            "fixed_cost":           int(fixed_cost),
            "sponsor_rev":          int(base_sponsor_rev),
            "exhibitor_rev":        int(base_exhibitor_rev),
            "funding_gap":          int(max(0, gap)),
            "status":               "COVERED" if gap <= 0 else "AT RISK",
            "note": (
                "Break-even from sponsor + exhibitor revenue only. "
                f"Gap: ₹{int(max(0,gap)):,}" if gap > 0
                else "Costs covered by sponsor + exhibitor revenue."
            )
        }

    results = {}
    tiers_to_check = {
        k: v for k, v in tier_structure.items()
        if isinstance(v, dict) and "price" in v and v["price"] > 0
    }

    for tier_name, tier in tiers_to_check.items():
        price  = tier["price"]
        margin = price - variable_cost
        if margin <= 0:
            continue

        be_tickets    = fixed_cost / margin
        be_with_all   = max(0, (fixed_cost - base_sponsor_rev - base_exhibitor_rev) / margin)
        expected      = tier.get("expected_sales", target * 0.6)
        safety        = (expected - be_with_all) / max(expected, 1)

        results[tier_name] = {
            "ticket_price":                   price,
            "fixed_cost":                     int(fixed_cost),
            "variable_per_person":            int(variable_cost),
            "contribution_margin":            int(margin),
            "breakeven_tickets_only":         int(be_tickets),
            "breakeven_with_all_revenue":     int(be_with_all),
            "expected_sales":                 int(expected),
            "safety_margin_pct":              round(safety * 100, 1),
            "status": (
                "SAFE"     if safety > 0.40 else
                "MODERATE" if safety > 0.10 else
                "RISKY"
            )
        }

    return results


# ─────────────────────────────────────────────────────────────
# MONTE CARLO SIMULATION
# ─────────────────────────────────────────────────────────────

def monte_carlo(tier_structure: dict,
                base_sponsor_rev: float,
                base_exhibitor_rev: float,
                pricing_mode: str = "tiered",
                n: int = 10000) -> dict:
    """
    10,000 revenue simulations with randomized inputs.
    Each variable drawn from a realistic probability distribution.

    Returns full revenue probability distribution:
    P10 = worst realistic case (only 10% of outcomes are worse)
    P50 = median expected outcome
    P90 = best realistic case (only 10% of outcomes are better)

    This replaces the 3-scenario model with a full distribution,
    showing not just the range but the SHAPE of risk.
    """
    rng = np.random.default_rng(42)

    # Extract tier data
    tiers = {k: v for k, v in tier_structure.items()
             if isinstance(v, dict) and "price" in v}

    def get(t, k, d): return t.get(k, d)

    results = []
    for _ in range(n):
        ticket_rev = 0.0
        for tier_name, tier in tiers.items():
            price    = get(tier, "price", 0)
            sales    = get(tier, "expected_sales", 0)
            if price <= 0 or sales <= 0:
                continue
            # Attendance uncertainty ±20%
            actual_sales = max(0, rng.normal(sales, sales * 0.20))
            ticket_rev  += actual_sales * price

        # Sponsor: beta distribution (uncertain conversion)
        sp_conv    = rng.beta(3, 2)
        ex_conv    = rng.beta(2, 2)
        sponsor_r  = base_sponsor_rev  * sp_conv
        exhibitor_r = base_exhibitor_rev * ex_conv

        results.append(ticket_rev + sponsor_r + exhibitor_r)

    arr = np.array(results)
    hist, edges = np.histogram(arr, bins=40)

    return {
        "p10":   int(np.percentile(arr, 10)),
        "p25":   int(np.percentile(arr, 25)),
        "p50":   int(np.percentile(arr, 50)),
        "p75":   int(np.percentile(arr, 75)),
        "p90":   int(np.percentile(arr, 90)),
        "mean":  int(np.mean(arr)),
        "std":   int(np.std(arr)),
        "histogram": {
            "counts": hist.tolist(),
            "edges":  [int(e) for e in edges.tolist()],
        }
    }


# ─────────────────────────────────────────────────────────────
# REVENUE PROJECTION — WEEK BY WEEK
# ─────────────────────────────────────────────────────────────

def compute_revenue_projection(tier_structure: dict,
                                weeks_to_event: int = 12,
                                pricing_mode: str = "tiered") -> dict:
    """
    Projects registrations and cash flow week by week.
    Based on Indian tech event registration patterns:
    - Slow launch (weeks 1-4)
    - Spike at speaker announcement (weeks 5-6)
    - Surge at early bird deadline (weeks 7-8)
    - Final urgency push (weeks 9-11)
    - Walk-ins on day

    Organizer knows WHEN money comes in, not just total.
    Critical for cash flow management.
    """
    tiers        = {k: v for k, v in tier_structure.items()
                    if isinstance(v, dict) and "expected_sales" in v}
    total_regs   = sum(t.get("expected_sales", 0) for t in tiers.values())
    gen_price    = 0
    for t in tiers.values():
        if t.get("price", 0) > 0:
            gen_price = t["price"]
            break

    # Registration curve weights (sum to 1.0)
    WEEK_WEIGHTS = {
        1: 0.02, 2: 0.03, 3: 0.03, 4: 0.04,
        5: 0.08, 6: 0.10,           # speaker announcement
        7: 0.12, 8: 0.14,           # early bird deadline
        9: 0.10, 10: 0.11,          # general urgency
        11: 0.10, 12: 0.05,         # final push
        13: 0.08                    # walk-ins
    }

    weeks        = list(range(1, min(weeks_to_event + 2, 14)))
    total_weight = sum(WEEK_WEIGHTS.get(w, 0.03) for w in weeks)

    projection    = []
    cum_regs      = 0
    cum_revenue   = 0

    for week in weeks:
        weight    = WEEK_WEIGHTS.get(week, 0.03) / total_weight
        regs      = int(total_regs * weight)
        rev       = regs * gen_price
        cum_regs += regs
        cum_revenue += rev

        label = _week_label(week, weeks_to_event)

        projection.append({
            "week":                     week,
            "label":                    label,
            "new_registrations":        regs,
            "cumulative_registrations": cum_regs,
            "weekly_revenue":           int(rev),
            "cumulative_revenue":       int(cum_revenue),
        })

    return {
        "weekly_projection": projection,
        "total_weeks":       weeks_to_event,
        "total_registrations": total_regs,
    }


def _week_label(week: int, total: int) -> str:
    remaining = total - week
    if remaining <= 0:
        return "Event Day"
    if remaining == 1:
        return "Final Week"
    if week <= 2:
        return "Launch Phase"
    if week in [5, 6]:
        return "Speaker Announcement"
    if week in [7, 8]:
        return "Early Bird Deadline"
    if remaining <= 3:
        return "Final Push"
    return f"T-{remaining} weeks"


# ─────────────────────────────────────────────────────────────
# PRICING MODE ROUTER
# ─────────────────────────────────────────────────────────────

def route_pricing_model(pricing_mode: str, target: int,
                         persona_mix: dict, budget: float,
                         objective_bias: float) -> dict:
    """
    Routes to the correct pricing model based on detected mode.
    All models return identical output structure so the rest of the
    system (charts, agent prompts, HTML) is mode-agnostic.
    """
    if pricing_mode == "free":
        return _model_free(target, persona_mix, budget)
    elif pricing_mode == "fixed":
        return _model_fixed(target, persona_mix, budget, objective_bias)
    elif pricing_mode == "tiered_with_free":
        return _model_tiered_with_free(target, persona_mix, budget, objective_bias)
    elif pricing_mode == "invite_only":
        return _model_invite_only(target, budget)
    elif pricing_mode == "hybrid":
        return _model_hybrid(target, persona_mix, budget, objective_bias)
    else:  # default: tiered
        return _model_tiered(target, persona_mix, budget, objective_bias)


# ─────────────────────────────────────────────────────────────
# PASS 1 — runs before any agent
# ─────────────────────────────────────────────────────────────

def pass1(inputs: dict) -> dict:
    """
    Runs on user inputs ONLY. No agent output needed.

    Computes baseline quantitative reality before agents reason.
    The agent_summary string is injected into agent prompts so
    agents know the mathematical foundation they must reason around.

    Agents are NOT required to use these numbers blindly.
    Their job: validate with market data, add qualitative reasoning,
    adjust with evidence if Tavily data contradicts the model.
    """
    persona_str    = inputs.get("expected_audience_persona", "")
    objective_str  = inputs.get("organizer_objective", "")
    budget_str     = inputs.get("budget_range", "₹50L")
    target_str     = inputs.get("target_audience_size", "500")
    ticketing_str  = inputs.get("ticketing_intent", "tiered")

    persona_mix    = detect_persona_mix(persona_str)
    objective_bias = detect_objective_bias(objective_str)
    budget         = parse_budget(budget_str)
    target         = int(re.sub(r'[^\d]', '', target_str) or 500)
    pricing_mode   = detect_pricing_mode(ticketing_str)

    # Baseline revenue estimates (before agent data)
    base_sponsor_rev   = budget * 0.25
    base_exhibitor_rev = budget * 0.12

    tier_structure = route_pricing_model(
        pricing_mode, target, persona_mix, budget, objective_bias
    )
    pricing_curve  = compute_pricing_curve(
        target, persona_mix, base_sponsor_rev, base_exhibitor_rev, pricing_mode
    )
    breakeven      = compute_breakeven(
        budget, tier_structure, base_sponsor_rev, base_exhibitor_rev, target, pricing_mode
    )
    projection     = compute_revenue_projection(tier_structure, pricing_mode=pricing_mode)

    persona_lines = "\n".join([
        f"  - {k}: price elasticity {v['elasticity']:+.2f}, "
        f"no-show base {v['no_show_base']:.0%}, "
        f"VIP propensity {v['vip_propensity']:.0%}"
        for k, v in persona_mix.items()
    ])

    tier_lines = "\n".join([
        f"  - {k.replace('_',' ').title()}: "
        f"₹{v.get('price',0):,} × {v.get('expected_sales',0)} expected = "
        f"₹{v.get('revenue',0):,}"
        for k, v in tier_structure.get("tiers", tier_structure).items()
        if isinstance(v, dict) and "price" in v
    ])

    optimal = pricing_curve.get("optimal_total", {})
    be_gen  = breakeven.get("general", breakeven) if isinstance(breakeven, dict) else {}

    agent_summary = f"""
╔══════════════════════════════════════════════════════════════╗
║  PREDICTION ENGINE — PASS 1 OUTPUT                          ║
║  Computed from user inputs before any agent reasoning       ║
╚══════════════════════════════════════════════════════════════╝

DETECTED PRICING MODE: {pricing_mode.upper().replace('_', ' ')}
{tier_structure.get('note', '')}

AUDIENCE ANALYSIS:
{persona_lines}
  Composite price sensitivity: {_weighted_attr(persona_mix, 'elasticity'):+.2f}
  Composite no-show rate: {_weighted_attr(persona_mix, 'no_show_base'):.0%}
  Organizer objective price bias: {objective_bias:+.0%}

COMPUTED TIER STRUCTURE:
{tier_lines}
  Total projected ticket revenue: ₹{tier_structure.get('total_ticket_revenue', 0):,}
  Total projected registrations:  {tier_structure.get('total_registrations', 0):,}
  Expected actual attendance:     {tier_structure.get('actual_attendance', 0):,}

OPTIMAL TICKET PRICE (total revenue across all 3 streams):
  Optimal price:    ₹{optimal.get('price', 0):,}
  At this price:    {optimal.get('actual_attendance', 0):,} attendees
  Total revenue:    ₹{optimal.get('total_revenue', 0):,}

BREAK-EVEN (General tier, including sponsor + exhibitor revenue):
  Break-even attendance: {be_gen.get('breakeven_with_all_revenue', 'N/A')} people
  Safety margin:         {be_gen.get('safety_margin_pct', 'N/A')}%
  Status:                {be_gen.get('status', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOW TO USE THIS DATA — IMPORTANT FOR ALL AGENTS:

This engine handles arithmetic. You handle judgment.

These are COMPUTED BASELINES — not final answers.
Your role is to:
1. Validate these numbers against real market data from Tavily
2. Add qualitative reasoning the model cannot compute:
   - "Developers in Delhi are price-sensitive in Q2 specifically"
   - "VIP tier only works if networking dinner is explicitly included"
   - "Early bird should close 8 weeks out for this event category"
3. Adjust with explicit reasoning if comparable event data contradicts
4. Reference these numbers in your output — do not invent different ones
   without citing your evidence source
5. The pricing agent must explain WHY these numbers work for this
   specific audience — not just repeat them
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return {
        "persona_mix":          persona_mix,
        "objective_bias":       objective_bias,
        "budget":               budget,
        "target":               target,
        "pricing_mode":         pricing_mode,
        "base_sponsor_rev":     base_sponsor_rev,
        "base_exhibitor_rev":   base_exhibitor_rev,
        "tier_structure":       tier_structure,
        "pricing_curve":        pricing_curve,
        "breakeven":            breakeven,
        "revenue_projection":   projection,
        "optimal_price":        optimal.get("price", 0),
        "agent_summary":        agent_summary,
    }


# ─────────────────────────────────────────────────────────────
# PASS 2 — runs after sponsor + exhibitor agents
# ─────────────────────────────────────────────────────────────

def pass2(pass1_data: dict,
          sponsor_output: str,
          exhibitor_output: str) -> dict:
    """
    Reconciles pass1 baseline with agent estimates.

    Parses actual INR estimates from sponsor and exhibitor agent outputs.
    Re-runs the full model with real estimates.
    Produces FINAL authoritative numbers — single source of truth for:
    - Pricing Agent prompt (validates and explains)
    - Decision Layer prompt (makes decisions on real numbers)
    - Synthesizer prompt (writes report using real numbers)
    - HTML Generator (draws all charts)

    Reconciliation logic:
    Agent estimates get 60% weight (event-specific intelligence)
    Model baseline gets 40% weight (mathematical floor / sanity check)
    """
    sponsor_vals   = parse_inr_values(sponsor_output)
    exhibitor_vals = parse_inr_values(exhibitor_output)

    sp_agent  = int(np.median(sponsor_vals))   if sponsor_vals   else pass1_data["base_sponsor_rev"]
    ex_agent  = int(np.median(exhibitor_vals)) if exhibitor_vals else pass1_data["base_exhibitor_rev"]

    final_sponsor_rev   = int(0.60 * sp_agent  + 0.40 * pass1_data["base_sponsor_rev"])
    final_exhibitor_rev = int(0.60 * ex_agent  + 0.40 * pass1_data["base_exhibitor_rev"])

    pricing_mode = pass1_data.get("pricing_mode", "tiered")

    pricing_curve = compute_pricing_curve(
        pass1_data["target"],
        pass1_data["persona_mix"],
        final_sponsor_rev,
        final_exhibitor_rev,
        pricing_mode,
    )
    breakeven = compute_breakeven(
        pass1_data["budget"],
        pass1_data["tier_structure"],
        final_sponsor_rev,
        final_exhibitor_rev,
        pass1_data["target"],
        pricing_mode,
    )
    mc = monte_carlo(
        pass1_data["tier_structure"],
        final_sponsor_rev,
        final_exhibitor_rev,
        pricing_mode,
    )
    projection = compute_revenue_projection(
        pass1_data["tier_structure"],
        pricing_mode=pricing_mode,
    )

    optimal  = pricing_curve.get("optimal_total", {})
    be_gen   = breakeven.get("general", breakeven) if isinstance(breakeven, dict) else {}
    tier_str = pass1_data["tier_structure"]

    tier_lines = "\n".join([
        f"  {k.replace('_',' ').title():15}: ₹{v.get('price',0):>8,} "
        f"× {v.get('expected_sales',0):>4} sales = ₹{v.get('revenue',0):,}"
        for k, v in tier_str.get("tiers", tier_str).items()
        if isinstance(v, dict) and "price" in v
    ])

    total_ticket = tier_str.get("total_ticket_revenue", 0)
    total_all    = total_ticket + final_sponsor_rev + final_exhibitor_rev

    agent_summary = f"""
╔══════════════════════════════════════════════════════════════╗
║  PREDICTION ENGINE — PASS 2 OUTPUT (FINAL RECONCILED)       ║
║  Single source of truth for all decisions and report        ║
╚══════════════════════════════════════════════════════════════╝

PRICING MODE: {pricing_mode.upper().replace('_', ' ')}

RECONCILED REVENUE ESTIMATES:
  Sponsor Revenue:    ₹{final_sponsor_rev:,}
                      (Agent estimate: ₹{sp_agent:,} | 
                       Model baseline: ₹{int(pass1_data['base_sponsor_rev']):,})
  Exhibitor Revenue:  ₹{final_exhibitor_rev:,}
                      (Agent estimate: ₹{ex_agent:,} |
                       Model baseline: ₹{int(pass1_data['base_exhibitor_rev']):,})

TICKET TIER STRUCTURE:
{tier_lines}
  Total Ticket Revenue: ₹{total_ticket:,}

THREE-STREAM REVENUE TOTAL:
  Ticket:    ₹{total_ticket:,}
  Sponsor:   ₹{final_sponsor_rev:,}
  Exhibitor: ₹{final_exhibitor_rev:,}
  ─────────────────────────────
  TOTAL:     ₹{total_all:,}

OPTIMAL PRICE (maximizes total 3-stream revenue):
  Optimal ticket price:      ₹{optimal.get('price', 0):,}
  Expected attendance:       {optimal.get('actual_attendance', 0):,} people
  Total revenue at optimal:  ₹{optimal.get('total_revenue', 0):,}

MONTE CARLO DISTRIBUTION (10,000 simulations):
  Worst case  (P10): ₹{mc['p10']:,}
  Expected    (P50): ₹{mc['p50']:,}
  Best case   (P90): ₹{mc['p90']:,}
  Uncertainty  (±σ): ₹{mc['std']:,}

BREAK-EVEN:
  Break-even attendance: {be_gen.get('breakeven_with_all_revenue', 'N/A')} people
  Expected attendance:   {be_gen.get('expected_sales', 'N/A')}
  Safety margin:         {be_gen.get('safety_margin_pct', 'N/A')}%
  Status:                {be_gen.get('status', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHILOSOPHY NOTE FOR DECISION LAYER AND SYNTHESIZER:

These are the AUTHORITATIVE numbers for this event.
All pricing decisions, revenue projections, and P&L statements
in the final report MUST reference these figures.

If you believe these numbers are wrong based on your analysis:
- State the discrepancy explicitly
- Cite the specific market evidence that contradicts the model
- Provide your alternative estimate with full reasoning
- Do NOT silently use different numbers

The prediction engine reconciles mathematics with agent intelligence.
You are the final layer that adds strategic judgment.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return {
        # For charts
        "tier_structure":        tier_str,
        "pricing_curve":         pricing_curve,
        "breakeven":             breakeven,
        "monte_carlo":           mc,
        "revenue_projection":    projection,
        "pricing_mode":          pricing_mode,

        # Final numbers
        "final_sponsor_rev":     final_sponsor_rev,
        "final_exhibitor_rev":   final_exhibitor_rev,
        "total_ticket_rev":      total_ticket,
        "total_revenue":         total_all,
        "optimal_price":         optimal.get("price", 0),
        "optimal_attendance":    optimal.get("actual_attendance", 0),

        # For agent prompts
        "agent_summary":         agent_summary,
    }