import os
import io
import zipfile
import sys
import time
import threading
import streamlit as st
import streamlit.components.v1 as components
from streamlit.runtime.scriptrunner import add_script_run_ctx
from dotenv import load_dotenv

from crew import run_conferax, print_serpapi_summary
from html_generator import generate_html_report
from agent_graph_export import generate_pipeline_png
from data_extractor import extract_chart_data_to_json

load_dotenv()

# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────

TOTAL_PHASES = 14

# Ordered list matches ConferaX crew phase sequence.
# Used for progress % and the tqdm bar fill.
PHASE_ORDER = [
    "Orchestrator",
    "Research Analyst",
    "Sponsor Intel",
    "Exhibitor Intel",
    "Speaker & Agenda",
    "Venue Intel",
    "Pricing Agent",
    "GTM & Audience",
    "Ops & Risk",
    "Devil's Advocate",
    "Self-Reflection",
    "Outreach Agent",
    "Decision Layer",
    "Synthesizer CSO",
]

PHASE_ICONS = {
    "Orchestrator":      "🧠",
    "Research Analyst":  "🌐",
    "Sponsor Intel":     "🤝",
    "Exhibitor Intel":   "🏪",
    "Speaker & Agenda":  "🎤",
    "Venue Intel":       "🏛️",
    "Pricing Agent":     "💰",
    "GTM & Audience":    "📣",
    "Ops & Risk":        "⚙️",
    "Devil's Advocate":  "😈",
    "Self-Reflection":   "🪞",
    "Outreach Agent":    "📧",
    "Decision Layer":    "⚖️",
    "Synthesizer CSO":   "📋",
}

# ─────────────────────────────────────────────────────────────
# CSS INJECTION — TQDM-STYLE DARK THEME
# ─────────────────────────────────────────────────────────────

PROGRESS_CSS = """
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Syne:wght@700;800&family=Outfit:wght@400;500;600;700&display=swap');

/* Overall page light theme reinforcement */
[data-testid="stAppViewContainer"] {
    background: #FAFBFC;
}
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E5E7EB;
}

/* TQDM progress container */
.tqdm-container {
    background: #FFFFFF;
    border: 1px solid #F3F4F6;
    border-radius: 16px;
    padding: 24px 28px;
    font-family: 'JetBrains Mono', monospace;
    margin: 8px 0;
    box-shadow: 0 16px 32px rgba(17, 24, 39, 0.05);
}

/* Main progress bar row */
.tqdm-bar-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
}

.tqdm-phase-label {
    font-size: 11px;
    color: #6B7280;
    white-space: nowrap;
    min-width: 90px;
    font-weight: 600;
}

.tqdm-bar-track {
    flex: 1;
    height: 10px;
    background: #F3F4F6;
    border-radius: 5px;
    overflow: hidden;
    position: relative;
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
}

.tqdm-bar-fill {
    height: 100%;
    border-radius: 5px;
    background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%);
    transition: width 0.4s ease;
    box-shadow: 0 0 12px rgba(124, 58, 237, 0.3);
}

.tqdm-pct {
    font-size: 12px;
    color: #7C3AED;
    font-weight: 700;
    min-width: 38px;
    text-align: right;
}

/* Current agent row */
.tqdm-agent-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.tqdm-agent-name {
    font-size: 15px;
    font-weight: 600;
    color: #111827;
    font-family: 'Outfit', sans-serif;
    display: flex;
    align-items: center;
    gap: 8px;
}

.tqdm-timer {
    font-size: 12px;
    color: #6B7280;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.5px;
}

.tqdm-status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #7C3AED;
    display: inline-block;
    animation: pulse-dot 1.2s ease-in-out infinite;
    box-shadow: 0 0 6px rgba(124, 58, 237, 0.6);
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.8); }
}

/* Phase log table */
.phase-log {
    margin-top: 20px;
    border-top: 1px solid #F3F4F6;
    padding-top: 14px;
}

.phase-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}

.phase-row-done  { color: #10B981; font-weight: 500; }
.phase-row-active{ color: #7C3AED; font-weight: 600; }
.phase-row-wait  { color: #9CA3AF; }

.phase-tick  { min-width: 16px; }
.phase-num   { min-width: 50px; color: inherit; }
.phase-icon  { min-width: 20px; font-size: 14px; }
.phase-name  { flex: 1; font-family: 'Outfit', sans-serif; font-size: 13px; }
.phase-time  { min-width: 55px; text-align: right; }

/* Spinner for active row */
.spin {
    display: inline-block;
    animation: spin-anim 0.8s linear infinite;
}
@keyframes spin-anim {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
</style>
"""

# ─────────────────────────────────────────────────────────────
# LIVE AGENT TRACKER
# ─────────────────────────────────────────────────────────────

class StreamlitAgentTracker:
    """
    Intercepts CrewAI stdout to detect agent transitions.
    Updates a Streamlit placeholder with a TQDM-style progress UI.
    """

    def __init__(self, progress_placeholder):
        self.placeholder       = progress_placeholder
        self.start_time        = time.time()
        self.original_stdout   = sys.stdout
        self.running           = True

        # State
        self.completed_phases  = 0          # phases fully done
        self.current_phase_idx = 0          # 0-based index into PHASE_ORDER
        self.current_agent     = PHASE_ORDER[0]
        self.phase_times: list[float | None] = [None] * TOTAL_PHASES
        self.phase_start_time  = time.time()

        # We use a lock just in case of multiple stdout streams, 
        # but WE DO NOT SPAWN A 1-SEC THREAD. The clock is ticked by JS inside the HTML overlay.
        self._lock = threading.Lock()

    # ── stdout interface ──────────────────────────────────────

    def write(self, text: str):
        self.original_stdout.write(text)

        # CrewAI emits lines like:
        #   "== Working Agent: Sponsor Intel =="          (new agent starting)
        #   "[DEBUG]: == Working Agent: GTM & Audience =="
        if "Working Agent:" in text:
            raw = text.split("Working Agent:")[-1]
            raw = raw.replace("=", "").replace("[", "").replace("]", "").strip()
            # Match against known names (partial OK)
            for name in PHASE_ORDER:
                if name.lower() in raw.lower():
                    with self._lock:
                        self._on_agent_start(name)
                    break

        # Task finished signals
        elif any(s in text for s in ("Task output:", "Finished chain.", ">> Finished")):
            with self._lock:
                self._on_task_done()

    def flush(self):
        self.original_stdout.flush()

    def stop(self):
        self.running = False
        sys.stdout = self.original_stdout

    # ── state transitions ─────────────────────────────────────

    def _on_agent_start(self, name: str):
        # Record finish time for whatever just completed
        if self.completed_phases > 0:
            prev_idx = self.completed_phases - 1
            if self.phase_times[prev_idx] is None:
                self.phase_times[prev_idx] = time.time() - self.phase_start_time

        new_idx = PHASE_ORDER.index(name)
        self.current_phase_idx = new_idx
        self.current_agent     = name
        self.phase_start_time  = time.time()
        self._render()

    def _on_task_done(self):
        idx = self.current_phase_idx
        if self.phase_times[idx] is None:
            self.phase_times[idx] = time.time() - self.phase_start_time
        self.completed_phases = max(self.completed_phases, idx + 1)
        self._render()

    # ── rendering ─────────────────────────────────────────────

    def _render(self):
        # Only called when an Agent starts or finishes, so this ONLY generates 
        # a new Streamlit iFrame 1-2 times per minute instead of 60x a minute!
        elapsed_total = time.time() - self.start_time
        phase_elapsed = time.time() - self.phase_start_time
        done_count    = self.completed_phases
        cur_idx       = self.current_phase_idx
        cur_agent     = self.current_agent
        cur_icon      = PHASE_ICONS.get(cur_agent, "⚡")

        # Progress % — count completed + fraction of current
        frac    = min(1.0, (done_count + 0.5) / TOTAL_PHASES)
        pct     = int(frac * 100)

        # Bar string (20 chars wide) for the tqdm fill width
        bar_fill_pct = frac * 100  # used as CSS width %

        # Timer strings
        def fmt_time(secs: float) -> str:
            m, s = divmod(int(secs), 60)
            return f"{m:02d}:{s:02d}"

        total_timer   = fmt_time(elapsed_total)
        phase_timer   = fmt_time(phase_elapsed)

        # ── Phase log rows ────────────────────────────────────
        rows_html = ""
        for i, name in enumerate(PHASE_ORDER):
            icon = PHASE_ICONS.get(name, "⚡")
            if i < done_count:
                cls   = "phase-row-done"
                tick  = "✓"
                t     = fmt_time(self.phase_times[i]) if self.phase_times[i] else "—"
                spin  = ""
            elif i == cur_idx and done_count < TOTAL_PHASES:
                cls   = "phase-row-active"
                tick  = '<span class="spin">◌</span>'
                t     = phase_timer
                spin  = ""
            else:
                cls   = "phase-row-wait"
                tick  = "·"
                t     = ""

            # Assign an ID to the active phase's time span so JS can target it
            time_id = 'id="active-phase-time"' if cls == "phase-row-active" else ''

            rows_html += f"""
<div class="phase-row {cls}">
  <span class="phase-tick">{tick}</span>
  <span class="phase-num">Phase {i+1:02d}</span>
  <span class="phase-icon">{icon}</span>
  <span class="phase-name">{name}</span>
  <span class="phase-time" {time_id}>{t}</span>
</div>"""

        # ── Full HTML block ───────────────────────────────────
        html = f"""
{PROGRESS_CSS}
<div class="tqdm-container">

  <!-- Progress bar -->
  <div class="tqdm-bar-row">
    <span class="tqdm-phase-label">Phase {done_count + 1}/{TOTAL_PHASES}</span>
    <div class="tqdm-bar-track">
      <div class="tqdm-bar-fill" style="width:{bar_fill_pct:.1f}%"></div>
    </div>
    <span class="tqdm-pct">{pct}%</span>
  </div>

  <!-- Current agent + timers -->
  <div class="tqdm-agent-row">
    <div class="tqdm-agent-name">
      <span class="tqdm-status-dot"></span>
      {cur_icon}&nbsp; {cur_agent}
    </div>
    <div style="display:flex;gap:18px;align-items:center">
      <span class="tqdm-timer" title="Time on this agent" id="live-phase-timer">⏱ {phase_timer}</span>
      <span class="tqdm-timer" title="Total elapsed" id="live-total-timer">&nbsp;🕐 {total_timer}</span>
    </div>
  </div>

  <!-- Phase log -->
  <div class="phase-log">
    {rows_html}
  </div>

</div>
<script>
(function() {{
    let totalSecs = {int(elapsed_total)};
    let phaseSecs = {int(phase_elapsed)};
    setInterval(function() {{
        totalSecs++;
        phaseSecs++;
        const fmt = (s) => String(Math.floor(s/60)).padStart(2,'0') + ':' + String(s%60).padStart(2,'0');
        
        let tElem = document.getElementById('live-total-timer');
        if (tElem) tElem.innerText = '🕐 ' + fmt(totalSecs);
        
        let pElem = document.getElementById('live-phase-timer');
        if (pElem) pElem.innerText = '⏱ ' + fmt(phaseSecs);
        
        let aElem = document.getElementById('active-phase-time');
        if (aElem) aElem.innerText = fmt(phaseSecs);
    }}, 1000);
}})();
</script>
"""
        try:
            self.placeholder.html(html, height=520, scrolling=False)
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────
# PAGE SETUP & SECRETS
# ─────────────────────────────────────────────────────────────

st.set_page_config(page_title="ConferaX v3.0", page_icon="⚡", layout="wide")

NVIDIA_API_KEY = st.secrets.get("NVIDIA_API_KEY", os.getenv("NVIDIA_API_KEY"))
TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY", os.getenv("TAVILY_API_KEY"))
SERPER_API_KEY = st.secrets.get("SERPER_API_KEY", os.getenv("SERPER_API_KEY"))

if NVIDIA_API_KEY: os.environ["NVIDIA_API_KEY"] = NVIDIA_API_KEY
if TAVILY_API_KEY: os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
if SERPER_API_KEY: os.environ["SERPER_API_KEY"] = SERPER_API_KEY

# ─────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
.conf-title {
    font-family: 'Syne', sans-serif;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #111827;
    margin-bottom: 2px;
}
.conf-title span { 
    background: linear-gradient(90deg, #7C3AED 0%, #EC4899 50%, #F97316 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.conf-sub {
    font-size: 14px;
    color: #6B7280;
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    letter-spacing: 0.5px;
    margin-bottom: 28px;
}
</style>
<div class="conf-title">Confera<span>X</span></div>
<div class="conf-sub">Powered by a Smart Multi Agent System</div>
""", unsafe_allow_html=True)

if not NVIDIA_API_KEY:
    st.error("❌ NVIDIA_API_KEY is missing. App cannot run.")
    st.stop()
if not TAVILY_API_KEY or not SERPER_API_KEY:
    st.warning("⚠️ Tavily or Serper API keys are missing. Web search tools may fail.")

# ─────────────────────────────────────────────────────────────
# SIDEBAR — EVENT PARAMETERS
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] h2 {
        font-family: 'Syne', sans-serif !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #111827 !important;
    }
    .stTextInput label, .stSelectbox label, .stTextArea label {
        color: #374151 !important;
        font-weight: 500 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.header("⚙️ Event Parameters")

    event_category             = st.text_input("Event Category",     "AI & Technology")
    geography_region           = st.text_input("Target Region",      "Delhi, India")
    target_audience_size       = st.text_input("Audience Size",      "1000")
    event_date_range           = st.text_input("Event Date",         "May 4, 2026")
    expected_duration          = st.selectbox("Duration",
                                    ["Half-day","1 day","2 days","3 days"], index=1)
    event_format               = st.selectbox("Format",
                                    ["Summit","Conference","Expo","Workshop","Hybrid"])
    budget_range               = st.text_input("Budget Range",       "₹1 Crore INR")
    expected_audience_persona  = st.text_area("Audience Persona",
                                    "Founders, developers, investors", height=80)
    venue_preference_constraints = st.text_input("Venue Preferences","Indoor, premium, city-center")
    sponsor_priority           = st.text_input("Sponsor Priority",   "Tech companies and VCs")
    speaker_priority           = st.text_area("Speaker Priority",
                                    "Global AI thought leaders and practitioners", height=80)
    ticketing_intent           = st.selectbox("Ticketing Intent",
                                    ["Tiered pricing","Free","Paid","Invite-only"])
    organizer_objective        = st.text_area("Organizer Objective",
                                    "Brand building and community growth", height=80)
    hard_constraints           = st.text_area("Hard Constraints",
                                    "English primary, wheelchair accessible, max 2000 capacity",
                                    height=80)

    launch_button = st.button(
        "🚀 Launch ConferaX Engine",
        type="primary",
        use_container_width=True
    )

# ─────────────────────────────────────────────────────────────
# EXECUTION
# ─────────────────────────────────────────────────────────────

if launch_button:
    inputs = {
        "event_category":              event_category,
        "geography_region":            geography_region,
        "target_audience_size":        target_audience_size,
        "event_date_range":            event_date_range,
        "expected_duration":           expected_duration,
        "event_format":                event_format,
        "budget_range":                budget_range,
        "expected_audience_persona":   expected_audience_persona,
        "venue_preference_constraints":venue_preference_constraints,
        "sponsor_priority":            sponsor_priority,
        "speaker_priority":            speaker_priority,
        "ticketing_intent":            ticketing_intent,
        "organizer_objective":         organizer_objective,
        "hard_constraints":            hard_constraints,
    }

    pipeline_start = time.time()

    # ── Section header ────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
                color:#111827;margin:12px 0 4px">
        ⏳ Pipeline Running
    </div>
    <div style="font-size:13px;color:#6B7280;font-family:'Outfit',sans-serif;
                margin-bottom:14px; font-weight:500;">
        Each phase completes sequentially · Do not close this tab
    </div>
    """, unsafe_allow_html=True)

    # Single placeholder — tracker will .html() into this every second
    progress_placeholder = st.empty()

    # Render initial idle state immediately so the UI isn't blank
    components.html(f"""
    {PROGRESS_CSS}
    <div class="tqdm-container">
      <div class="tqdm-bar-row">
        <span class="tqdm-phase-label">Phase 0/{TOTAL_PHASES}</span>
        <div class="tqdm-bar-track">
          <div class="tqdm-bar-fill" style="width:0%"></div>
        </div>
        <span class="tqdm-pct">0%</span>
      </div>
      <div class="tqdm-agent-row">
        <div class="tqdm-agent-name">
          <span class="tqdm-status-dot" style="background:#E5E7EB;box-shadow:none;animation:none;"></span>
          🧠&nbsp; Initializing pipeline...
        </div>
        <span class="tqdm-timer">00:00</span>
      </div>
    </div>
    """, height=120)

    # Start tracker + hijack stdout
    tracker = StreamlitAgentTracker(progress_placeholder)
    sys.stdout = tracker

    results = {}
    try:
        results = run_conferax(inputs)
    except Exception as e:
        sys.stdout = tracker.original_stdout
        tracker.stop()
        st.error(f"❌ Pipeline error: {e}")
        st.stop()
    finally:
        sys.stdout = tracker.original_stdout
        tracker.stop()

    total_elapsed = int(time.time() - pipeline_start)
    total_mins, total_secs = divmod(total_elapsed, 60)

    # Show final completed state
    final_rows = ""
    for i, name in enumerate(PHASE_ORDER):
        icon = PHASE_ICONS.get(name,"⚡")
        t    = f"{int(tracker.phase_times[i] // 60):02d}:{int(tracker.phase_times[i] % 60):02d}" \
               if tracker.phase_times[i] else "—"
        final_rows += f"""
<div class="phase-row phase-row-done">
  <span class="phase-tick">✓</span>
  <span class="phase-num">Phase {i+1:02d}</span>
  <span class="phase-icon">{icon}</span>
  <span class="phase-name">{name}</span>
  <span class="phase-time">{t}</span>
</div>"""

    progress_placeholder.empty()
    components.html(f"""
    {PROGRESS_CSS}
    <div class="tqdm-container">
      <div class="tqdm-bar-row">
        <span class="tqdm-phase-label">Phase {TOTAL_PHASES}/{TOTAL_PHASES}</span>
        <div class="tqdm-bar-track">
          <div class="tqdm-bar-fill" style="width:100%;background:linear-gradient(90deg,#10B981,#06B6D4)"></div>
        </div>
        <span class="tqdm-pct" style="color:#10B981">100%</span>
      </div>
      <div class="tqdm-agent-row">
        <div class="tqdm-agent-name" style="color:#10B981">
          <span style="width:7px;height:7px;border-radius:50%;background:#10B981;display:inline-block"></span>
          ✅&nbsp; All phases complete — {total_mins}m {total_secs}s
        </div>
        <span class="tqdm-timer" style="color:#10B981">🕐 {total_mins:02d}:{total_secs:02d}</span>
      </div>
      <div class="phase-log">{final_rows}</div>
    </div>
    """, height=520)

    # ── Post-processing ───────────────────────────────────────
    with st.spinner("🧩 Extracting chart data..."):
        extracted_json_data = extract_chart_data_to_json(results, inputs)

    prediction_data = results.get("prediction_data")
    report_content  = results.get("final_report", "")

    with st.spinner("🖼️ Generating HTML report..."):
        raw_html = generate_html_report(
            report_content=report_content,
            inputs=inputs,
            results=results,
            prediction_data=prediction_data,
            extracted_chart_data=extracted_json_data,
        )

    with st.spinner("📊 Drawing agent pipeline graph..."):
        graph_bytes = None
        try:
            generate_pipeline_png("temp_pipeline.png")
            with open("temp_pipeline.png", "rb") as f:
                graph_bytes = f.read()
            os.remove("temp_pipeline.png")
        except Exception:
            pass

    st.divider()

    # ── Research summary ──────────────────────────────────────
    st.subheader("🔍 Research Summary")
    with st.expander("View Phase 0 Search Data"):
        old_out = sys.stdout
        buf     = io.StringIO()
        sys.stdout = buf
        try:
            print_serpapi_summary(results)
        finally:
            sys.stdout = old_out
        txt = buf.getvalue()
        st.text(txt if txt.strip() else "No SerpAPI summary generated.")

    # ── Report preview ────────────────────────────────────────
    st.subheader("📊 Interactive Intelligence Report")
    components.html(raw_html, height=1000, scrolling=True)

    # ── Download zip ──────────────────────────────────────────
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("conferax_report.html", raw_html)
        if graph_bytes:
            zf.writestr("agent_pipeline.png", graph_bytes)
        file_map = {
            "01_strategy_profile.txt":  "strategy_profile",
            "02_research_output.txt":   "research_output",
            "03a_sponsor_output.txt":   "sponsor_output",
            "03b_exhibitor_output.txt": "exhibitor_output",
            "04_speaker_output.txt":    "speaker_output",
            "05_venue_output.txt":      "venue_output",
            "06_pricing_output.txt":    "pricing_output",
            "07_gtm_output.txt":        "gtm_output",
            "08_ops_output.txt":        "ops_output",
            "09_devils_advocate.txt":   "devils_advocate_output",
            "10_self_reflection.txt":   "self_reflection_output",
            "11_outreach_emails.txt":   "outreach_output",
            "12_decisions.txt":         "decision_output",
            "13_final_report.txt":      "final_report",
        }
        for filename, key in file_map.items():
            content = results.get(key, "")
            if content:
                zf.writestr(filename, content)

    st.download_button(
        label="📦 Download ALL Outputs (.zip)",
        data=zip_buf.getvalue(),
        file_name="ConferaX_Intelligence_Folder.zip",
        mime="application/zip",
        type="primary",
        use_container_width=True,
    )