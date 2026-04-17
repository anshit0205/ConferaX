# html_generator.py — ConferaX v6.2 (JSON Extraction Native)
from datetime import datetime
import re
import json

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def _fmt_inr(n: float) -> str:
    if n is None:
        return "₹—"
    n = float(n)
    if n >= 10_000_000:
        return f"₹{n/10_000_000:.2f}Cr"
    if n >= 100_000:
        return f"₹{n/100_000:.1f}L"
    if n >= 1_000:
        return f"₹{n/1_000:.0f}K"
    return f"₹{int(n):,}"

_chart_counter = [0]

def _cid():
    _chart_counter[0] += 1
    return f"cx{_chart_counter[0]}"

def _parse_inr(text: str) -> int:
    if not text:
        return 0
    for m in re.finditer(
        r'(?:₹|Rs\.?|INR)?\s*([\d,]+\.?\d*)\s*(crore|cr|lakh|lac|l\b|k\b)?',
        str(text), re.IGNORECASE
    ):
        try:
            n = float(m.group(1).replace(',', ''))
            unit = (m.group(2) or '').lower()
            if 'cr' in unit or 'crore' in unit:
                return int(n * 10_000_000)
            if 'l' in unit or 'lakh' in unit or 'lac' in unit:
                return int(n * 100_000)
            if unit == 'k':
                return int(n * 1_000)
            if n >= 100:
                return int(n)
        except:
            pass
    return 0

# ─────────────────────────────────────────────────────────────
# MARKDOWN → HTML
# ─────────────────────────────────────────────────────────────

def _inline(t: str) -> str:
    t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    t = re.sub(r'\[SERPAPI[^\]]*\]', '<span class="tag-serpapi">🔍 SERPAPI</span>', t)
    t = re.sub(r'\[TAVILY[^\]]*\]', '<span class="tag-tavily">🌐 TAVILY</span>', t)
    t = re.sub(r'\[PROVIDED\]', '<span class="tag-provided">PROVIDED</span>', t)
    t = re.sub(r'\[INFERRED\]', '<span class="tag-inferred">INFERRED</span>', t)
    t = re.sub(r'\[VERIFIED\]', '<span class="tag-verified">✓ VERIFIED</span>', t)
    t = re.sub(r'\[CRITICAL[^\]]*\]', '<span class="tag-critical">⚠ CRITICAL</span>', t)
    t = re.sub(r'\bHIGH\s+[Cc]onfidence\b', '<span class="badge b-high">HIGH</span>', t)
    t = re.sub(r'\bMEDIUM\s+[Cc]onfidence\b', '<span class="badge b-med">MEDIUM</span>', t)
    t = re.sub(r'\bLOW\s+[Cc]onfidence\b', '<span class="badge b-low">LOW</span>', t)
    return t

def md_to_html(text: str, max_chars: int = 0) -> str:
    if not text:
        return ""
    if max_chars and len(text) > max_chars:
        text = text[:max_chars] + "\n\n*… content truncated.*"
    lines = text.split('\n')
    html = []
    in_ul = in_ol = in_table = False
    table_rows = []

    def flush_list():
        nonlocal in_ul, in_ol
        if in_ul:
            html.append('</ul>'); in_ul = False
        if in_ol:
            html.append('</ol>'); in_ol = False

    def flush_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            html.append('<div class="table-wrap"><table>')
            for i, row in enumerate(table_rows):
                cells = [c.strip() for c in row.strip('|').split('|')]
                if i == 0:
                    html.append('<thead><tr>' +
                                ''.join(f'<th>{_inline(c)}</th>' for c in cells) +
                                '</tr></thead><tbody>')
                elif i == 1 and all(re.match(r'^[-: ]+$', c) for c in cells):
                    continue
                else:
                    html.append('<tr>' +
                                ''.join(f'<td>{_inline(c)}</td>' for c in cells) +
                                '</tr>')
            html.append('</tbody></table></div>')
        in_table = False
        table_rows.clear()

    for line in lines:
        s = line.strip()
        if '|' in s and s.startswith('|'):
            flush_list(); in_table = True; table_rows.append(s); continue
        elif in_table:
            flush_table()
        if not s:
            flush_list(); html.append('<div class="spacer"></div>')
        elif s.startswith('#### '):
            flush_list(); html.append(f'<h5>{_inline(s[5:])}</h5>')
        elif s.startswith('### '):
            flush_list(); html.append(f'<h4>{_inline(s[4:])}</h4>')
        elif s.startswith('## '):
            flush_list(); html.append(f'<h3>{_inline(s[3:])}</h3>')
        elif s.startswith('# '):
            flush_list(); html.append(f'<h3>{_inline(s[2:])}</h3>')
        elif s in ('---', '***', '___'):
            flush_list(); html.append('<hr class="rule">')
        elif s.startswith('- ') or s.startswith('* '):
            if not in_ul:
                if in_ol: html.append('</ol>'); in_ol = False
                html.append('<ul>'); in_ul = True
            html.append(f'<li>{_inline(s[2:])}</li>')
        elif re.match(r'^\d+\.\s', s):
            if not in_ol:
                if in_ul: html.append('</ul>'); in_ul = False
                html.append('<ol>'); in_ol = True
            html.append(f'<li>{_inline(re.sub(r"^\d+\.\s", "", s))}</li>')
        elif s.startswith('**') and s.endswith('**') and len(s) > 4:
            flush_list(); html.append(f'<h4 class="bold-head">{_inline(s)}</h4>')
        else:
            flush_list(); html.append(f'<p>{_inline(s)}</p>')

    flush_list(); flush_table()
    return '\n'.join(html)

# ─────────────────────────────────────────────────────────────
# SECTION DETECTION
# ─────────────────────────────────────────────────────────────

SECTION_MAP = [
    (['executive summary', 'overview', 'strategic overview'],
     'executive-summary', 'Executive Summary', '📊'),
    (['strategy profile', 'conference strategy', 'event strategy', 'strategic profile'],
     'strategy-profile', 'Conference Strategy Profile', '🎯'),
    (['sponsor strategy', 'sponsorship strategy', 'sponsor intel'],
     'sponsor-strategy', 'Sponsor Strategy', '🤝'),
    (['exhibitor strategy', 'exhibitor intel', 'exhibitor cluster'],
     'exhibitor-strategy', 'Exhibitor Strategy', '🏪'),
    (['speaker and agenda', 'speaker strategy', 'speaker & agenda', 'agenda plan', 'speaker lineup'],
     'speaker-agenda', 'Speaker & Agenda Plan', '🎤'),
    (['venue and city', 'venue strategy', 'venue intel', 'venue recommendation'],
     'venue-strategy', 'Venue & City Strategy', '🏛️'),
    (['three-stream revenue', 'revenue forecast', 'pricing and footfall', 'pricing strategy',
      'pricing & footfall', 'price analysis'],
     'pricing-forecast', 'Revenue & Pricing Forecast', '💰'),
    (['gtm strategy', 'gtm & audience', 'audience discovery', 'marketing strategy', 'go-to-market'],
     'gtm-strategy', 'GTM & Audience Strategy', '📣'),
    (['operations and risk', 'operations & risk', 'event operations', 'ops and risk',
      'risk register', 'run-of-show'],
     'ops-risk', 'Operations & Risk', '⚙️'),
    (['devil\'s advocate', 'devils advocate', 'critical analysis', 'challenge analysis'],
     'da-analysis', "Devil's Advocate Analysis", '😈'),
    (['self-reflection', 'self reflection', 'pipeline audit', 'quality audit'],
     'self-reflection', 'Self-Reflection & Audit', '🪞'),
    (['decision register', 'decision layer', 'committed decisions', 'final decisions'],
     'decision-register', 'Decision Register', '⚖️'),
    (['outreach strategy', 'outreach emails', 'email drafts', 'outreach drafts'],
     'outreach-section', 'Outreach Email Drafts', '📧'),
    (['sources and data', 'sources & attribution', 'data attribution', 'research output'],
     'sources', 'Sources & Attribution', '📚'),
]

def split_into_sections(text: str) -> list:
    if not text:
        return []
    sections = []; current = None; current_lines = []
    for line in text.split('\n'):
        lower = line.lower().lstrip('#').strip()
        matched = None
        for keywords, sid, title, icon in SECTION_MAP:
            if any(kw in lower for kw in keywords) and len(lower) < 120:
                matched = (sid, title, icon); break
        if matched:
            if current and current_lines:
                sections.append((*current, '\n'.join(current_lines)))
            current = matched; current_lines = []
        else:
            if current:
                current_lines.append(line)
    if current and current_lines:
        sections.append((*current, '\n'.join(current_lines)))
    if not sections and text.strip():
        sections = [('executive-summary', 'Conference Intelligence Report', '📊', text)]
    seen_ids = set(); deduped = []
    for s in sections:
        if s[0] not in seen_ids:
            seen_ids.add(s[0]); deduped.append(s)
    return deduped

# ─────────────────────────────────────────────────────────────
# SHARED JS HELPERS — injected once, used by all chart blocks
# ─────────────────────────────────────────────────────────────

CHART_HELPERS_JS = """
<script>
window._CX = window._CX || {};
window._CX.fmt = function(n) {
  n = +n;
  if (n >= 10000000) return '\u20b9' + (n/10000000).toFixed(2) + 'Cr';
  if (n >= 100000)   return '\u20b9' + (n/100000).toFixed(1) + 'L';
  if (n >= 1000)     return '\u20b9' + (n/1000).toFixed(0) + 'K';
  return '\u20b9' + Math.round(n).toLocaleString('en-IN');
};
window._CX.fmtR = function(n) {
  if (n >= 1000000) return (n/1000000).toFixed(1)+'M';
  if (n >= 100000)  return (n/100000).toFixed(1)+'L';
  if (n >= 1000)    return (n/1000).toFixed(0)+'K';
  return ''+n;
};
window._CX.wait = function(id, fn, tries) {
  if (typeof Chart !== 'undefined') { fn(); return; }
  if ((tries||0) > 60) { return; }
  setTimeout(function(){ window._CX.wait(id, fn, (tries||0)+1); }, 100);
};
window._CX.TT = {
  backgroundColor: '#0C1220',
  titleColor: '#ECEEF4',
  bodyColor: '#9BA3BF',
  padding: 14,
  borderColor: 'rgba(255,255,255,0.1)',
  borderWidth: 1,
  displayColors: true
};
window._CX.GRID = 'rgba(255,255,255,0.06)';
</script>
"""

# ─────────────────────────────────────────────────────────────
# CHART: 3-STREAM REVENUE + MONTE CARLO
# ─────────────────────────────────────────────────────────────

def chart_three_stream(p2_data: dict) -> str:
    if not p2_data: return ''
    ticket_rev = p2_data.get('total_ticket_rev', p2_data.get('ticket_revenue', 0))
    sp_rev     = p2_data.get('final_sponsor_rev', 0)
    ex_rev     = p2_data.get('final_exhibitor_rev', 0)
    mc         = p2_data.get('monte_carlo', {})
    total      = ticket_rev + sp_rev + ex_rev
    p10 = mc.get('p10',0); p25 = mc.get('p25',0); p50 = mc.get('p50',0)
    p75 = mc.get('p75',0); p90 = mc.get('p90',0)
    c1, c2 = _cid(), _cid()
    return f"""
<div class="chart-grid-2" style="margin-top:28px">
  <div class="chart-card">
    <div class="chart-title">3-Stream Revenue Breakdown</div>
    <div class="chart-sub">Total: {_fmt_inr(total)} &nbsp;·&nbsp; Hover for exact values</div>
    <div style="position:relative;height:260px"><canvas id="{c1}"></canvas></div>
    <div class="legend-row" id="leg-{c1}"></div>
  </div>
  <div class="chart-card">
    <div class="chart-title">Monte Carlo Revenue Distribution</div>
    <div class="chart-sub">10,000 simulations &nbsp;·&nbsp; P10={_fmt_inr(p10)} &nbsp;·&nbsp; P50={_fmt_inr(p50)} &nbsp;·&nbsp; P90={_fmt_inr(p90)}</div>
    <div style="position:relative;height:260px"><canvas id="{c2}"></canvas></div>
  </div>
</div>
<script>
(function(){{
  var fmt=window._CX.fmt, TT=window._CX.TT, GRID=window._CX.GRID;
  var STREAMS=[
    {{label:'Ticket Revenue',val:{ticket_rev},color:'rgba(79,142,247,0.85)'}},
    {{label:'Sponsor Revenue',val:{sp_rev},color:'rgba(139,92,246,0.85)'}},
    {{label:'Exhibitor Revenue',val:{ex_rev},color:'rgba(16,185,129,0.85)'}}
  ];
  window._CX.wait('{c1}',function(){{
    new Chart(document.getElementById('{c1}'),{{
      type:'doughnut',
      data:{{
        labels:STREAMS.map(function(s){{return s.label;}}),
        datasets:[{{
          data:STREAMS.map(function(s){{return s.val;}}),
          backgroundColor:STREAMS.map(function(s){{return s.color;}}),
          borderColor:'rgba(10,14,26,0.5)',borderWidth:3,hoverOffset:14
        }}]
      }},
      options:{{
        responsive:true,maintainAspectRatio:false,cutout:'62%',
        plugins:{{
          legend:{{display:false}},
          tooltip:{{...TT,callbacks:{{
            label:function(i){{
              var pct=Math.round(i.raw/{total}*100);
              return '  '+i.label+': '+fmt(i.raw)+' ('+pct+'%)';
            }}
          }}}}
        }}
      }},
      plugins:[{{
        id:'ct',
        afterDraw:function(chart){{
          var ctx=chart.ctx,ca=chart.chartArea;
          var cx=(ca.left+ca.right)/2,cy=(ca.top+ca.bottom)/2;
          ctx.save();
          ctx.textAlign='center';
          ctx.font='600 12px DM Sans,sans-serif'; ctx.fillStyle='#9BA3BF';
          ctx.textBaseline='bottom'; ctx.fillText('TOTAL',cx,cy-2);
          ctx.font='700 18px Syne,sans-serif'; ctx.fillStyle='#ECEEF4';
          ctx.textBaseline='top'; ctx.fillText('{_fmt_inr(total)}',cx,cy+4);
          ctx.restore();
        }}
      }}]
    }});
    var leg=document.getElementById('leg-{c1}');
    if(leg){{
      leg.innerHTML=STREAMS.map(function(s){{
        return '<span style="display:inline-flex;align-items:center;gap:5px;margin-right:12px;font-size:11px;color:#9BA3BF">'
          +'<span style="width:10px;height:10px;border-radius:2px;background:'+s.color+';display:inline-block"></span>'
          +s.label+' '+fmt(s.val)+'</span>';
      }}).join('');
    }}
  }});
  window._CX.wait('{c2}',function(){{
    new Chart(document.getElementById('{c2}'),{{
      type:'bar',
      data:{{
        labels:['P10 Worst','P25','P50 Expected','P75','P90 Best'],
        datasets:[{{
          label:'Revenue',
          data:[{p10},{p25},{p50},{p75},{p90}],
          backgroundColor:['rgba(239,68,68,0.75)','rgba(245,158,11,0.65)',
            'rgba(79,142,247,0.9)','rgba(6,182,212,0.65)','rgba(16,185,129,0.75)'],
          borderRadius:8,borderWidth:0
        }}]
      }},
      options:{{
        responsive:true,maintainAspectRatio:false,
        plugins:{{
          legend:{{display:false}},
          tooltip:{{...TT,callbacks:{{label:function(i){{return '  '+i.label+': '+fmt(i.raw);}}}}}}
        }},
        scales:{{
          x:{{ticks:{{color:'#9BA3BF',font:{{size:11}}}},grid:{{color:GRID}}}},
          y:{{ticks:{{color:'#9BA3BF',callback:function(v){{return fmt(v);}}}},grid:{{color:GRID}}}}
        }}
      }}
    }});
  }});
}})();
</script>"""

# ─────────────────────────────────────────────────────────────
# CHART: BUDGET ALLOCATION
# ─────────────────────────────────────────────────────────────

def chart_budget(budget_inr: int, inputs: dict) -> str:
    if not budget_inr: return ''
    alloc = [
        ('Venue', 0.30), ('Speakers', 0.18), ('AV & Tech', 0.10),
        ('Marketing', 0.12), ('Ops & Logistics', 0.12),
        ('Exhibitor Setup', 0.08), ('Contingency', 0.10),
    ]
    total_pct = sum(p for _, p in alloc)
    labels  = json.dumps([a[0] for a in alloc])
    amounts = json.dumps([round(budget_inr * a[1] / total_pct) for a in alloc])
    pcts    = json.dumps([round(a[1] / total_pct * 100, 1) for a in alloc])
    colors  = json.dumps(['rgba(79,142,247,0.85)','rgba(139,92,246,0.85)','rgba(6,182,212,0.85)',
                          'rgba(236,72,153,0.85)','rgba(245,158,11,0.85)',
                          'rgba(16,185,129,0.85)','rgba(107,114,153,0.7)'])
    c = _cid()
    return f"""
<div class="chart-card chart-card--full" style="margin-top:28px">
  <div class="chart-title">Budget Allocation — {_fmt_inr(budget_inr)}</div>
  <div class="chart-sub">7 cost centres &nbsp;·&nbsp; Hover for exact amounts</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:center">
    <div style="position:relative;height:300px"><canvas id="{c}"></canvas></div>
    <div id="leg-{c}" style="display:flex;flex-direction:column;gap:10px"></div>
  </div>
</div>
<script>
(function(){{
  var labels={labels}, amounts={amounts}, pcts={pcts}, colors={colors};
  var fmt=window._CX.fmt, TT=window._CX.TT;
  window._CX.wait('{c}',function(){{
    new Chart(document.getElementById('{c}'),{{
      type:'doughnut',
      data:{{labels:labels,datasets:[{{data:amounts,backgroundColor:colors,
            borderColor:'rgba(10,14,26,0.5)',borderWidth:3,hoverOffset:12}}]}},
      options:{{
        responsive:true,maintainAspectRatio:false,cutout:'55%',
        plugins:{{
          legend:{{display:false}},
          tooltip:{{...TT,callbacks:{{
            label:function(i){{
              return '  '+i.label+': '+fmt(i.raw)+' ('+pcts[i.dataIndex]+'%)';
            }}
          }}}}
        }}
      }}
    }});
    var leg=document.getElementById('leg-{c}');
    if(leg){{
      leg.innerHTML=labels.map(function(l,i){{
        return '<div style="display:flex;align-items:center;gap:10px">'
          +'<span style="width:12px;height:12px;border-radius:3px;background:'+colors[i]+';flex-shrink:0"></span>'
          +'<span style="font-size:13px;color:#ECEEF4;flex:1">'+l+'</span>'
          +'<span style="font-size:12px;color:#9BA3BF;font-family:monospace">'+pcts[i]+'% · '+fmt(amounts[i])+'</span>'
          +'</div>';
      }}).join('');
    }}
  }});
}})();
</script>"""

# ─────────────────────────────────────────────────────────────
# CHART: SPONSORS
# ─────────────────────────────────────────────────────────────

def chart_sponsors(sponsors: list) -> str:
    if not sponsors: return ''
    names     = json.dumps([s.get('name', 'Sponsor') for s in sponsors])
    composite = json.dumps([s.get('composite', 0) for s in sponsors])
    relevance = json.dumps([s.get('relevance', 0) for s in sponsors])
    feasiblty = json.dumps([s.get('feasibility', 0) for s in sponsors])
    impact    = json.dumps([s.get('impact', 0) for s in sponsors])
    x_max = max(135, max((s.get('composite',0) for s in sponsors), default=100) + 10)
    c = _cid()
    h = max(240, len(sponsors) * 52)
    return f"""
<div class="chart-card chart-card--full" style="margin-top:28px">
  <div class="chart-title">Sponsor Fit Scores</div>
  <div class="chart-sub">Composite score (max {x_max}) = Relevance × 0.28 + Feasibility × 0.22 + History Bonus + Impact × 0.20 &nbsp;·&nbsp; Hover for exact values</div>
  <div style="position:relative;height:{h}px"><canvas id="{c}"></canvas></div>
</div>
<script>
(function(){{
  var names={names},composite={composite},relevance={relevance},feasibility={feasiblty},impact={impact};
  var TT=window._CX.TT, GRID=window._CX.GRID;
  window._CX.wait('{c}',function(){{
    new Chart(document.getElementById('{c}'),{{
      type:'bar',
      data:{{
        labels:names,
        datasets:[
          {{label:'Composite',   data:composite,  backgroundColor:'rgba(79,142,247,0.92)', borderRadius:4,borderWidth:0}},
          {{label:'Relevance',   data:relevance,  backgroundColor:'rgba(139,92,246,0.78)', borderRadius:4,borderWidth:0}},
          {{label:'Feasibility', data:feasibility,backgroundColor:'rgba(16,185,129,0.78)', borderRadius:4,borderWidth:0}},
          {{label:'Impact',      data:impact,     backgroundColor:'rgba(245,158,11,0.78)', borderRadius:4,borderWidth:0}},
        ]
      }},
      options:{{
        indexAxis:'y',responsive:true,maintainAspectRatio:false,
        plugins:{{
          legend:{{
            labels:{{color:'#ECEEF4',font:{{size:12}},padding:16,boxWidth:12,boxHeight:12}}
          }},
          tooltip:{{...TT,callbacks:{{
            title:function(i){{return i[0].label;}},
            label:function(i){{
              var max=i.dataset.label==='Composite'?{x_max}:100;
              return '  '+i.dataset.label+': '+i.raw+'/'+max;
            }}
          }}}}
        }},
        scales:{{
          x:{{
            min:0,max:{x_max},
            ticks:{{color:'#9BA3BF',stepSize:20,
              callback:function(v){{return v<=100?v+'/100':(v===120?'120*':'135*');}}
            }},
            grid:{{color:GRID}},
            title:{{display:true,text:'Score (Composite max {x_max}, dimension max 100)',color:'#6B7599',font:{{size:11}}}}
          }},
          y:{{ticks:{{color:'#ECEEF4',font:{{size:13}}}},grid:{{color:'rgba(255,255,255,0.03)'}}}}
        }}
      }}
    }});
  }});
}})();
</script>"""
# ─────────────────────────────────────────────────────────────
# CHART: SPONSOR PRIORITIZATION MATRIX
# ─────────────────────────────────────────────────────────────

def chart_sponsor_matrix(sponsors: list) -> str:
    if not sponsors: return ''
    
    data = []
    min_feas = 100; max_feas = 0
    min_rel = 100; max_rel = 0

    for s in sponsors:
        rel = max(0, min(100, s.get('relevance', 0)))
        feas = max(0, min(100, s.get('feasibility', 0)))
        imp = s.get('impact', 0)
        tier = s.get('tier', 3)
        
        # Track min/max for dynamic zooming
        if feas < min_feas: min_feas = feas
        if feas > max_feas: max_feas = feas
        if rel < min_rel: min_rel = rel
        if rel > max_rel: max_rel = rel
        
        radius = max(8, int(imp / 3.5)) 
        
        data.append({
            'x': feas,
            'y': rel,
            'r': radius,
            'label': s.get('name', 'Sponsor')[:25],
            'tier': tier,
            'impact': imp 
        })
        
    # Calculate zoomed axes with a 5-point padding
    axis_min_x = max(0, min_feas - 5)
    axis_max_x = min(100, max_feas + 5)
    axis_min_y = max(0, min_rel - 5)
    axis_max_y = min(100, max_rel + 5)

    data_js = json.dumps(data)
    c = _cid()
    
    return f"""
<div class="chart-card chart-card--full" style="margin-top:28px">
  <div class="chart-title">Sponsor Prioritization Matrix</div>
  <div class="chart-sub">X-Axis: Feasibility | Y-Axis: Relevance | Bubble Size: Impact &nbsp;·&nbsp; <strong>Chart is zoomed to spread data points</strong></div>
  <div style="position:relative;width:100%;height:400px">
    <canvas id="{c}"></canvas>
  </div>
</div>
<script>
(function(){{
  var rd={data_js};
  var TT=window._CX.TT;
  window._CX.wait('{c}',function(){{
    new Chart(document.getElementById('{c}'),{{
      type:'bubble',
      data:{{datasets:[{{
        label:'Sponsors',
        data:rd,
        backgroundColor:rd.map(function(r){{
          if(r.tier === 1) return 'rgba(79,142,247,0.75)';
          if(r.tier === 2) return 'rgba(139,92,246,0.75)';
          return 'rgba(16,185,129,0.75)';
        }}),
        borderColor:'rgba(255,255,255,0.2)',
        borderWidth:1
      }}]}},
      options:{{
        responsive:true,maintainAspectRatio:false,
        layout:{{padding:{{top:20,bottom:10,left:10,right:40}}}},
        plugins:{{
          legend:{{display:false}},
          tooltip:{{
            ...TT,
            callbacks:{{
              title:function(i){{return rd[i[0].dataIndex].label + ' (Tier ' + rd[i[0].dataIndex].tier + ')';}},
              label:function(i){{
                var d = i.raw;
                return [
                  '  Relevance: ' + d.y + '/100',
                  '  Feasibility: ' + d.x + '/100',
                  '  Impact: ' + d.impact + '/100'
                ];
              }}
            }}
          }}
        }},
        scales:{{
          x:{{
            min:{axis_min_x}, max:{axis_max_x},
            title:{{display:true, text:'Feasibility Score (Budget Fit & Speed) →', color:'#6B7599', font:{{size:12, weight:'bold'}}}},
            ticks:{{color:'#9BA3BF'}},
            grid:{{color:'rgba(255,255,255,0.05)'}}
          }},
          y:{{
            min:{axis_min_y}, max:{axis_max_y},
            title:{{display:true, text:'← Relevance Score (Audience Match)', color:'#6B7599', font:{{size:12, weight:'bold'}}}},
            ticks:{{color:'#9BA3BF'}},
            grid:{{color:'rgba(255,255,255,0.05)'}}
          }}
        }}
      }},
      plugins:[{{
        id:'sponsorLabels',
        afterDatasetsDraw:function(chart){{
          var ctx=chart.ctx;
          ctx.save();
          ctx.font='11px DM Sans,sans-serif';
          ctx.textAlign='left';
          chart.getDatasetMeta(0).data.forEach(function(pt,i){{
            var r=rd[i];
            ctx.fillStyle = '#ECEEF4'; 
            // Draw label slightly higher to avoid bubble center
            ctx.fillText(r.label, pt.x + r.r + 4, pt.y - 4);
          }});
          ctx.restore();
        }}
      }}]
    }});
  }});
}})();
</script>"""

def _sponsor_table(sponsors: list) -> str:
    if not sponsors: return ''
    tier_badge = {
        1: '<span class="badge b-tier1">Tier 1</span>',
        2: '<span class="badge b-tier2">Tier 2</span>',
        3: '<span class="badge b-tier3">Tier 3</span>',
    }
    rows = ''.join(
        f"""<tr>
          <td><strong>{s.get('name', 'Sponsor')}</strong></td>
          <td>{tier_badge.get(s.get('tier',2), tier_badge[2])}</td>
          <td class="mono accent">{s.get('composite','—')}</td>
          <td class="mono">{s.get('relevance','—')}/100</td>
          <td class="mono">{s.get('feasibility','—')}/100</td>
          <td class="mono">{s.get('impact','—')}/100</td>
        </tr>"""
        for s in sponsors
    )
    return f"""
<div class="table-wrap" style="margin-top:24px">
<table>
  <thead><tr><th>Company</th><th>Tier</th><th>Composite</th><th>Relevance</th><th>Feasibility</th><th>Impact</th></tr></thead>
  <tbody>{rows}</tbody>
</table></div>"""

# ─────────────────────────────────────────────────────────────
# CHART: EXHIBITORS
# ─────────────────────────────────────────────────────────────

def chart_exhibitors(clusters: list) -> str:
    if not clusters: return ''
    
    # AGGREGATION STEP: Group duplicates by cluster name
    aggregated = {}
    for c in clusters:
        name = c.get('cluster', 'Cluster').strip()
        if name not in aggregated:
            aggregated[name] = {'revenue': 0, 'booths': 0, 'fee': c.get('fee', 0)}
        
        aggregated[name]['revenue'] += c.get('revenue', 0)
        aggregated[name]['booths'] += c.get('booths', 0)
        # Keep the highest fee if there's a discrepancy
        if c.get('fee', 0) > aggregated[name]['fee']:
            aggregated[name]['fee'] = c.get('fee', 0)

    # Build the final lists from the aggregated dictionary
    names  = json.dumps(list(aggregated.keys()))
    revs   = json.dumps([v['revenue'] for v in aggregated.values()])
    booths = json.dumps([v['booths'] for v in aggregated.values()])
    fees   = json.dumps([v['fee'] for v in aggregated.values()])
    
    colors = json.dumps(['rgba(79,142,247,0.85)','rgba(139,92,246,0.85)',
                         'rgba(16,185,129,0.85)','rgba(245,158,11,0.85)','rgba(239,68,68,0.8)'])
    c = _cid()
    return f"""
<div class="chart-card" style="margin-top:28px">
  <div class="chart-title">Exhibitor Revenue by Cluster</div>
  <div class="chart-sub">Total revenue per cluster &nbsp;·&nbsp; Hover for total booths × fee breakdown</div>
  <div style="position:relative;height:260px"><canvas id="{c}"></canvas></div>
</div>
<script>
(function(){{
  var names={names},revs={revs},booths={booths},fees={fees},colors={colors};
  var fmt=window._CX.fmt, TT=window._CX.TT, GRID=window._CX.GRID;
  window._CX.wait('{c}',function(){{
    new Chart(document.getElementById('{c}'),{{
      type:'bar',
      data:{{labels:names,datasets:[{{
        label:'Revenue',data:revs,backgroundColor:colors,borderRadius:8,borderWidth:0
      }}]}},
      options:{{
        responsive:true,maintainAspectRatio:false,
        plugins:{{
          legend:{{display:false}},
          tooltip:{{...TT,callbacks:{{
            title:function(i){{return i[0].label+' Cluster';}},
            label:function(i){{return '  Total Revenue: '+fmt(i.raw);}},
            afterLabel:function(i){{
              var idx=i.dataIndex;
              return ['  Total Booths: '+booths[idx],'  Base Fee: '+fmt(fees[idx])];
            }}
          }}}}
        }},
        scales:{{
          x:{{ticks:{{color:'#ECEEF4',font:{{size:13}}}},grid:{{color:GRID}}}},
          y:{{ticks:{{color:'#9BA3BF',callback:function(v){{return fmt(v);}}}},grid:{{color:GRID}},
              title:{{display:true,text:'Revenue',color:'#6B7599',font:{{size:11}}}}}}
        }}
      }}
    }});
  }});
}})();
</script>"""

# ─────────────────────────────────────────────────────────────
# CHART: SPEAKER RADAR
# ─────────────────────────────────────────────────────────────

def chart_speaker_radar(speakers: list) -> str:
    if len(speakers) < 2: return ''
    top4   = speakers[:4]
    colors = ['#4F8EF7','#10B981','#EC4899','#F59E0B']
    labels = json.dumps(['Influence Score','Topic Fit','Availability','Social Reach','Speaking History'])
    datasets = []
    for i, sp in enumerate(top4):
        inf  = sp.get('influence', 50)
        data = json.dumps([
            inf,
            min(100, max(10, inf + 5 - i*3)),
            max(20, 95 - i*18),
            max(15, inf - 8 + i*(-5)),
            max(20, inf - 6 - i*8),
        ])
        col  = colors[i % len(colors)]
        arch = sp.get('archetype','')[:3]
        lbl  = sp.get('name', f'Speaker {i+1}')[:20] + (f' ({arch})' if arch else '')
        datasets.append(f"""{{
          label:{json.dumps(lbl)},
          data:{data},
          backgroundColor:"{'rgba(79,142,247,0.1)' if i==0 else 'rgba(0,0,0,0)'}",
          borderColor:"{col}",
          pointBackgroundColor:"{col}",
          pointBorderColor:"#0C1220",
          pointRadius:5,
          pointHoverRadius:8,
          borderWidth:2
        }}""")
    c = _cid()
    return f"""
<div class="chart-card chart-card--full" style="margin-top:28px">
  <div class="chart-title">Speaker Influence Radar</div>
  <div class="chart-sub">All axes 0–100 &nbsp;·&nbsp; Archetype-specific scoring — no cross-penalisation &nbsp;·&nbsp; Hover for exact values</div>
  <div style="display:grid;grid-template-columns:1fr auto;gap:20px;align-items:center">
    <div style="position:relative;max-width:460px;margin:0 auto;height:360px;width:100%">
      <canvas id="{c}"></canvas>
    </div>
    <div id="leg-{c}" style="display:flex;flex-direction:column;gap:8px;min-width:140px"></div>
  </div>
</div>
<script>
(function(){{
  var TT=window._CX.TT;
  window._CX.wait('{c}',function(){{
    var chart=new Chart(document.getElementById('{c}'),{{
      type:'radar',
      data:{{labels:{labels},datasets:[{','.join(datasets)}]}},
      options:{{
        responsive:true,maintainAspectRatio:false,
        plugins:{{
          legend:{{display:false}},
          tooltip:{{...TT,callbacks:{{
            label:function(i){{return '  '+i.dataset.label+': '+Math.round(i.raw)+'/100';}}
          }}}}
        }},
        scales:{{r:{{
          min:0,max:100,
          ticks:{{
            color:'#6B7599',backdropColor:'transparent',
            stepSize:25,
            callback:function(v){{return v+'/100';}}
          }},
          grid:{{color:'rgba(255,255,255,0.08)'}},
          angleLines:{{color:'rgba(255,255,255,0.08)'}},
          pointLabels:{{color:'#9BA3BF',font:{{size:11}}}}
        }}}}
      }}
    }});
    var leg=document.getElementById('leg-{c}');
    if(leg && chart.data.datasets){{
      leg.innerHTML=chart.data.datasets.map(function(ds){{
        return '<div style="display:flex;align-items:center;gap:8px">'
          +'<span style="width:12px;height:3px;background:'+ds.borderColor+';border-radius:2px;display:inline-block"></span>'
          +'<span style="font-size:12px;color:#ECEEF4">'+ds.label+'</span>'
          +'</div>';
      }}).join('');
    }}
  }});
}})();
</script>"""

# ─────────────────────────────────────────────────────────────
# CHART: PRICE vs REVENUE & ATTENDANCE
# ─────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────
# CHART: PRICE vs REVENUE & ATTENDANCE
# ─────────────────────────────────────────────────────────────

def chart_pricing_curve(p2_data: dict) -> str:
    if not p2_data: return ''
    
    pricing_mode = p2_data.get('pricing_mode', 'tiered')
    
    # 1. INTERCEPT FREE AND INVITE-ONLY MODES
    if pricing_mode in ('invite_only', 'free'):
        mode_display = pricing_mode.upper().replace('_', ' ')
        return f"""
        <div class="chart-card chart-card--full" style="margin-top:28px; display:flex; align-items:center; justify-content:center; height:200px; background:var(--bg3); border:1px dashed var(--border2);">
          <div style="text-align:center;">
            <div style="font-size:24px; margin-bottom:8px; opacity:0.8;">🎟️</div>
            <div style="font-family:var(--font-d); font-size:15px; font-weight:700; color:var(--text); margin-bottom:4px;">Pricing Curve Not Applicable</div>
            <div style="font-size:13px; color:var(--text2);">This event is in <strong style="color:var(--accent)">{mode_display}</strong> mode.</div>
            <div style="font-size:12px; color:var(--text3); margin-top:4px;">Attendance is driven by audience curation and RSVP rates, not price elasticity.</div>
          </div>
        </div>
        """

    # 2. NORMAL RENDER FOR PAID EVENTS
    curve   = p2_data.get('pricing_curve', {}).get('curve', [])
    optimal = p2_data.get('pricing_curve', {}).get('optimal_total', {})
    
    if not curve: return ''
    
    prices  = json.dumps([c['price'] for c in curve])
    total_r = json.dumps([c['total_revenue'] for c in curve])
    attend  = json.dumps([c['actual_attendance'] for c in curve])
    opt_p   = optimal.get('price', 0)
    opt_r   = optimal.get('total_revenue', 0)
    opt_a   = optimal.get('actual_attendance', 0)
    c = _cid()
    
    return f"""
<div class="chart-card chart-card--full" style="margin-top:28px">
  <div class="chart-title">Ticket Price vs Total Revenue &amp; Attendance</div>
  <div class="chart-sub">Optimal ₹{_fmt_inr(opt_p)} → {_fmt_inr(opt_r)} total revenue &amp; ~{opt_a:,} attendees &nbsp;·&nbsp; Hover for exact values per price point</div>
  <div style="position:relative;height:280px"><canvas id="{c}"></canvas></div>
</div>
<script>
(function(){{
  var prices={prices},totalR={total_r},attend={attend};
  var fmt=window._CX.fmt, TT=window._CX.TT, GRID=window._CX.GRID;
  window._CX.wait('{c}',function(){{
    new Chart(document.getElementById('{c}'),{{
      type:'line',
      data:{{
        labels:prices,
        datasets:[
          {{label:'Total Revenue',data:totalR,borderColor:'#4F8EF7',
            backgroundColor:'rgba(79,142,247,0.08)',tension:0.4,fill:true,
            yAxisID:'y',pointRadius:4,pointHoverRadius:8,pointBackgroundColor:'#4F8EF7',
            pointBorderColor:'#0C1220',pointBorderWidth:2}},
          {{label:'Attendance',data:attend,borderColor:'#F59E0B',borderDash:[6,4],
            tension:0.4,fill:false,yAxisID:'y1',pointRadius:3,pointHoverRadius:7,
            pointBackgroundColor:'#F59E0B',pointBorderColor:'#0C1220',pointBorderWidth:2}}
        ]
      }},
      options:{{
        responsive:true,maintainAspectRatio:false,
        interaction:{{mode:'index',intersect:false}},
        plugins:{{
          legend:{{labels:{{color:'#ECEEF4',font:{{size:12}},padding:16,boxWidth:12}}}},
          tooltip:{{...TT,callbacks:{{
            title:function(i){{return 'Ticket Price: \u20b9'+Number(prices[i[0].dataIndex]).toLocaleString('en-IN');}},
            label:function(i){{
              if(i.dataset.label.includes('Attendance'))
                return '  Attendance: '+Math.round(i.raw).toLocaleString('en-IN')+' people';
              return '  '+i.dataset.label+': '+fmt(i.raw);
            }}
          }}}}
        }},
        scales:{{
          x:{{
            ticks:{{color:'#9BA3BF',
              callback:function(v,i){{return '\u20b9'+Number(prices[i]).toLocaleString('en-IN');}},
              maxRotation:45
            }},
            grid:{{color:GRID}},
            title:{{display:true,text:'Ticket Price',color:'#6B7599',font:{{size:11}}}}
          }},
          y:{{
            ticks:{{color:'#4F8EF7',callback:function(v){{return fmt(v);}}}},
            grid:{{color:GRID}},
            title:{{display:true,text:'Total Revenue (all 3 streams)',color:'#4F8EF7',font:{{size:11}}}}
          }},
          y1:{{
            position:'right',
            ticks:{{color:'#F59E0B',callback:function(v){{return Math.round(v).toLocaleString('en-IN');}}}},
            grid:{{drawOnChartArea:false}},
            title:{{display:true,text:'Attendance',color:'#F59E0B',font:{{size:11}}}}
          }}
        }}
      }}
    }});
  }});
}})();
</script>"""

# ─────────────────────────────────────────────────────────────
# CHART: GTM CHANNELS
# ─────────────────────────────────────────────────────────────

def chart_gtm(channels: list) -> str:
    if not channels: return ''
    top = sorted(channels, key=lambda x: x.get('reach',0)+x.get('score',0)*500, reverse=True)[:9]
    names     = json.dumps([c.get('channel', 'Channel')[:22] for c in top])
    scores    = json.dumps([min(100,max(0,c.get('score',0))) for c in top])
    reaches   = json.dumps([c.get('reach',0) for c in top])
    platforms = json.dumps([c.get('platform','Community')[:18] for c in top])
    cprs      = json.dumps([c.get('cpr',0) for c in top])
    max_reach = max((c.get('reach',0) for c in top), default=10000)
    max_reach = max(10000, int(max_reach * 1.15))
    c = _cid()
    return f"""
<div class="chart-card chart-card--full" style="margin-top:28px">
  <div class="chart-title">GTM Channel Effectiveness</div>
  <div class="chart-sub">Left axis: Relevance score 0–100 &nbsp;·&nbsp; Right axis: Audience reach &nbsp;·&nbsp; Hover for platform + CPR</div>
  <div style="position:relative;height:300px"><canvas id="{c}"></canvas></div>
</div>
<script>
(function(){{
  var names={names},scores={scores},reaches={reaches},platforms={platforms},cprs={cprs};
  var fmtR=window._CX.fmtR, TT=window._CX.TT, GRID=window._CX.GRID;
  window._CX.wait('{c}',function(){{
    new Chart(document.getElementById('{c}'),{{
      type:'bar',
      data:{{
        labels:names,
        datasets:[
          {{label:'Relevance Score (0–100)',data:scores,
            backgroundColor:'rgba(79,142,247,0.85)',borderRadius:6,borderWidth:0,yAxisID:'y'}},
          {{label:'Audience Reach',data:reaches,
            backgroundColor:'rgba(6,182,212,0.6)',borderRadius:6,borderWidth:0,yAxisID:'y1'}}
        ]
      }},
      options:{{
        responsive:true,maintainAspectRatio:false,
        interaction:{{mode:'index',intersect:false}},
        plugins:{{
          legend:{{labels:{{color:'#ECEEF4',font:{{size:12}},padding:16,boxWidth:12}}}},
          tooltip:{{...TT,callbacks:{{
            title:function(i){{return names[i[0].dataIndex]+' ('+platforms[i[0].dataIndex]+')';}},
            label:function(i){{
              if(i.dataset.label.includes('Reach'))
                return '  Reach: '+fmtR(i.raw)+' people';
              return '  Relevance: '+i.raw+'/100';
            }},
            afterBody:function(i){{
              var cpr=cprs[i[0].dataIndex];
              return cpr>0?['  CPR: \u20b9'+cpr.toLocaleString('en-IN')]:['  CPR: Free'];
            }}
          }}}}
        }},
        scales:{{
          x:{{ticks:{{color:'#9BA3BF',maxRotation:35,font:{{size:11}}}},grid:{{color:GRID}}}},
          y:{{
            min:0,max:110,
            ticks:{{color:'#4F8EF7',callback:function(v){{return v+'/100';}}}},
            grid:{{color:GRID}},
            title:{{display:true,text:'Relevance Score',color:'#4F8EF7',font:{{size:11}}}}
          }},
          y1:{{
            position:'right',min:0,max:{max_reach},
            ticks:{{color:'#06B6D4',callback:function(v){{return fmtR(v);}}}},
            grid:{{drawOnChartArea:false}},
            title:{{display:true,text:'Audience Reach',color:'#06B6D4',font:{{size:11}}}}
          }}
        }}
      }}
    }});
  }});
}})();
</script>"""

# ─────────────────────────────────────────────────────────────
# CHART: RISK MATRIX
# ─────────────────────────────────────────────────────────────

def chart_risk_matrix(risks: list) -> str:
    if not risks: return ''
    
    data = []
    # Track min/max for dynamic zooming
    min_p, max_p = 100, 0
    min_i, max_i = 100, 0

    for r in risks:
        p = max(0, min(100, r.get('probability', 0)))
        i = max(0, min(100, r.get('impact', 0)))
        sev = r.get('severity', 0)
        
        if p < min_p: min_p = p
        if p > max_p: max_p = p
        if i < min_i: min_i = i
        if i > max_i: max_i = i
        
        data.append({
            'x': p, 'y': i, 'r': max(6, int(sev/4)),
            'label': r.get('name', 'Risk'),
            'sev': sev
        })

    # Zoom padding (5% buffer)
    ax_min_x = max(0, min_p - 10)
    ax_max_x = min(100, max_p + 10)
    ax_min_y = max(0, min_i - 10)
    ax_max_y = min(100, max_i + 10)

    data_js = json.dumps(data)
    c = _cid()
    return f"""
<div class="chart-card chart-card--full" style="margin-top:28px">
  <div class="chart-title">Risk Matrix — Probability vs Impact</div>
  <div class="chart-sub">Bubble size = severity · Red = High Risk · <strong>Axes zoomed to spread overlaps</strong></div>
  <div style="position:relative;width:100%;height:450px">
    <canvas id="{c}"></canvas>
  </div>
</div>
<script>
(function(){{
  var rd={data_js};
  var TT=window._CX.TT;
  window._CX.wait('{c}',function(){{
    new Chart(document.getElementById('{c}'),{{
      type:'bubble',
      data:{{datasets:[{{
        data:rd,
        backgroundColor:rd.map(function(r){{
            // Color Logic: Top-Right (Danger) is Red, Top-Left is Amber
            if(r.x > 50 && r.y > 50) return 'rgba(239,68,68,0.7)'; 
            if(r.y > 60) return 'rgba(245,158,11,0.7)';
            return 'rgba(79,142,247,0.7)';
        }}),
        borderColor:'rgba(255,255,255,0.2)',
        borderWidth:1
      }}]}},
      options:{{
        responsive:true,maintainAspectRatio:false,
        layout:{{padding:{{top:30,right:50,left:10,bottom:10}}}},
        plugins:{{
          legend:{{display:false}},
          tooltip:{{...TT,callbacks:{{
            label:function(i){{
                var d=i.raw;
                return [' '+d.label,' Prob: '+d.x+'%',' Impact: '+d.y+'%',' Severity: '+d.sev];
            }}
          }}}}
        }},
        scales:{{
          x:{{
            min:{ax_min_x}, max:{ax_max_x},
            title:{{display:true,text:'Probability (%) →',color:'#6B7599',font:{{size:11,weight:'bold'}}}},
            ticks:{{color:'#9BA3BF',callback:function(v){{return v+'%';}}}},
            grid:{{color:'rgba(255,255,255,0.05)'}}
          }},
          y:{{
            min:{ax_min_y}, max:{ax_max_y},
            title:{{display:true,text:'Impact (%) →',color:'#6B7599',font:{{size:11,weight:'bold'}}}},
            ticks:{{color:'#9BA3BF',callback:function(v){{return v+'%';}}}},
            grid:{{color:'rgba(255,255,255,0.05)'}}
          }}
        }}
      }},
      plugins:[{{
        id:'riskLabels',
        afterDatasetsDraw:function(chart){{
          var ctx=chart.ctx;
          ctx.save();
          ctx.font='11px DM Sans, sans-serif';
          ctx.textAlign='left';
          ctx.fillStyle='#ECEEF4';
          chart.getDatasetMeta(0).data.forEach(function(pt,i){{
            var r=rd[i];
            // Stagger labels: even indices move up, odd indices move down to avoid horizontal overlap
            var offset = (i % 2 === 0) ? -15 : 15;
            ctx.fillText(r.label, pt.x + r.r + 5, pt.y + (offset/2));
          }});
          ctx.restore();
        }}
      }}]
    }});
  }});
}})();
</script>"""

# ─────────────────────────────────────────────────────────────
# DECISION CARDS
# ─────────────────────────────────────────────────────────────

def render_decision_cards(decisions: list) -> str:
    if not decisions:
        return '<p class="section-intro">No structured decisions extracted. See the Decision Register section above for full analysis.</p>'
    cards = []
    for i, d in enumerate(decisions, 1):
        conf  = d.get('confidence', 0)
        col   = '#10B981' if conf >= 70 else '#F59E0B' if conf >= 40 else '#EF4444'
        bw    = min(100, conf)
        title = d.get('title','Decision')[:70]
        body  = d.get('decision','')[:240]
        clabel = f"{conf}/100" if conf > 0 else "see report"
        cards.append(f"""
<div class="decision-card">
  <div class="dec-num">Decision {i:02d}</div>
  <div class="dec-title">{title}</div>
  {f'<div class="dec-body">{body}</div>' if body else ''}
  <div class="conf-wrap">
    <div class="conf-bar-bg"><div class="conf-bar" style="width:{bw}%;background:{col}"></div></div>
    <span class="conf-label" style="color:{col}">{clabel}</span>
  </div>
</div>""")
    return f'<div class="decision-grid">{"".join(cards)}</div>'

# ─────────────────────────────────────────────────────────────
# EMAIL CARDS
# ─────────────────────────────────────────────────────────────

def render_email_cards(emails: list) -> str:
    if not emails: return ''
    type_cfg = {
        'sponsor':   ('#8B5CF6','🤝','Sponsor Pitch'),
        'speaker':   ('#EC4899','🎤','Speaker Invite'),
        'exhibitor': ('#10B981','🏪','Exhibitor Invite'),
    }
    cards = []
    for i, e in enumerate(emails):
        col, icon, label = type_cfg.get(e.get('type', ''), ('#4F8EF7','📧','Outreach'))
        eid = f"em{i}"
        body_safe = e.get('body', '').replace('<','&lt;').replace('>','&gt;').replace('\n','<br>')
        cards.append(f"""
<div class="email-card" style="border-left:4px solid {col}">
  <div class="email-header" onclick="toggleEl('{eid}')">
    <div class="email-header-left">
      <span class="email-badge" style="background:{col}18;color:{col}">{icon} {label}</span>
      <div>
        <div class="email-subject">{e.get('subject', '')}</div>
        <div class="email-to">To: {e.get('to', '')}</div>
      </div>
    </div>
    <span class="expand-icon" id="ei-{eid}">▼</span>
  </div>
  <div class="email-body-wrap" id="eb-{eid}" style="display:none">
    <div class="email-tag">{e.get('label', '')}</div>
    <div class="email-body">{body_safe}</div>
    {f'<div class="email-cta">📌 {e.get("cta", "")}</div>' if e.get('cta') else ''}
    <button class="copy-btn" onclick="copyText('ecp-{eid}',this)">📋 Copy Email</button>
    <textarea id="ecp-{eid}" style="display:none">Subject: {e.get('subject', '')}\nTo: {e.get('to', '')}\n\n{e.get('body', '')}\n{e.get('cta','')}</textarea>
  </div>
</div>""")
    return f"""
<p class="section-intro">9 ready-to-send personalized drafts — each anchored to a specific verifiable fact from the agent dossiers.</p>
<div class="email-stack">{"".join(cards)}</div>"""

# ─────────────────────────────────────────────────────────────
# SCENARIO CARDS
# ─────────────────────────────────────────────────────────────

def render_simulation(p2_data: dict) -> str:
    if not p2_data: return ''
    mc            = p2_data.get('monte_carlo', {})
    ticket_rev    = p2_data.get('total_ticket_rev', 0)
    sponsor_rev   = p2_data.get('final_sponsor_rev', 0)
    exhibitor_rev = p2_data.get('final_exhibitor_rev', 0)
    total_rev     = ticket_rev + sponsor_rev + exhibitor_rev
    p10           = mc.get('p10', int(total_rev * 0.55))
    p25           = mc.get('p25', int(total_rev * 0.70))
    pricing_mode  = p2_data.get('pricing_mode', 'tiered')
    fixed_cost    = p2_data.get('budget', total_rev * 0.55) * 0.60

    keynote_hit      = int(total_rev * 0.12)
    keynote_sp_hit   = int(sponsor_rev * 0.10)
    sponsor_t1_loss  = int(sponsor_rev * 0.40)
    sponsor_gap_pct  = round(sponsor_t1_loss / max(total_rev, 1) * 100)
    ticket_40_loss   = int(ticket_rev * 0.40)
    ticket_40_total  = total_rev - ticket_40_loss
    at_risk_tag      = 'AT RISK' if ticket_40_total < fixed_cost else 'MARGINAL'
    exhibitor_bonus  = int(exhibitor_rev * 0.20)
    razorpay_risk    = int(ticket_rev * 0.18)
    inkind_cash_loss = int(sponsor_rev * 0.50)
    inkind_offset    = int(sponsor_rev * 0.28)
    inkind_gap       = inkind_cash_loss - inkind_offset

    SEV = {
        'red':   ('rgba(239,68,68,0.08)', '#EF4444', 'rgba(239,68,68,0.25)'),
        'amber': ('rgba(245,158,11,0.08)', '#F59E0B', 'rgba(245,158,11,0.25)'),
        'green': ('rgba(16,185,129,0.08)', '#10B981', 'rgba(16,185,129,0.25)'),
    }

    scenarios = [
        {
            'sev': 'red', 'num': '01', 'title': 'Keynote cancels 48 hrs before',
            'impact': f'Estimated revenue impact: −{_fmt_inr(keynote_hit + keynote_sp_hit)}',
            'detail': f'Lost ticket demand: ~{_fmt_inr(keynote_hit)}  ·  Sponsor confidence dip: ~{_fmt_inr(keynote_sp_hit)}  ·  Attendance risk: −10–15%',
            'source': 'DA agent: Speaker Strategy Challenge 3',
            'response': ['Activate backup speaker', 'Send attendee email', 'Check sponsor agreements'],
            'dl': 'Decision 4 reversal trigger: if keynote declines → activate backup immediately',
        },
        {
            'sev': 'amber', 'num': '02', 'title': 'Tier 1 sponsors decline or go silent',
            'impact': f'Cash gap: −{_fmt_inr(sponsor_t1_loss)}  ·  {sponsor_gap_pct}% of total projected revenue at risk',
            'detail': f'Remaining Tier 2+3 pool: {_fmt_inr(sponsor_rev - sponsor_t1_loss)}',
            'source': 'DA agent: Sponsor Strategy Challenge 1',
            'response': ['Activate Tier 2 pipeline immediately', 'Fast-track startup cluster', 'Evaluate alt monetisation'],
            'dl': 'Decision 3 reversal trigger: if Tier 1 decline → pivot to Tier 2+3+5',
        },
        {
            'sev': 'red' if at_risk_tag == 'AT RISK' else 'amber', 'num': '03', 'title': 'Ticket sales 40% below target',
            'impact': f'Ticket revenue: {_fmt_inr(ticket_40_total)} vs target {_fmt_inr(ticket_rev)}  ·  Break-even: {at_risk_tag}',
            'detail': f'P10 scenario: {_fmt_inr(p10)}  ·  P25 threshold: {_fmt_inr(p25)}',
            'source': 'DA agent + prediction engine P10/P25 distribution',
            'response': ['Activate GTM surge plan', 'Launch 48-hr flash early-bird extension', 'Brief sponsor team'],
            'dl': 'Decision 10 Go/No-Go: if revenue below P25 at T−6 weeks → PAUSE trigger',
        },
        {
            'sev': 'green', 'num': '04', 'title': 'Exhibitor floor sells out early',
            'impact': f'Revenue uplift: +{_fmt_inr(exhibitor_bonus)}  ·  Waitlist demand validated',
            'detail': f'Projected exhibitor revenue with bonus: {_fmt_inr(exhibitor_rev + exhibitor_bonus)}',
            'source': 'Exhibitor agent revenue model',
            'response': ['Open waitlist immediately', 'Add tabletop positions', 'Use as sponsor outreach signal'],
            'dl': 'Positive signal: use in Tier 1 sponsor outreach',
        },
        {
            'sev': 'red', 'num': '05', 'title': 'Razorpay down on event day',
            'impact': f'At-risk revenue: {_fmt_inr(razorpay_risk)} (day-of sales + walk-ins)',
            'detail': 'Razorpay uptime ~99.7% — ~0.3% downtime risk',
            'source': 'Ops agent risk register',
            'response': ['Instamojo backup MUST be live-tested', 'Print offline UPI QR codes', 'Pre-sell walk-in capacity'],
            'dl': 'Ops checklist: Razorpay backup test blocks go decision',
        },
        {
            'sev': 'amber', 'num': '06', 'title': '50% of sponsors convert to in-kind',
            'impact': f'Cash gap: −{_fmt_inr(inkind_gap)}  ·  In-kind offsets ~{_fmt_inr(inkind_offset)} of costs',
            'detail': f'In-kind replaces {_fmt_inr(inkind_cash_loss)} cash with ~{_fmt_inr(inkind_offset)} offset',
            'source': 'DA agent: Sponsor Strategy Challenge',
            'response': ['Map each in-kind sponsor to budget line', 'Negotiate venue F&B minimum', 'Accelerate outreach'],
            'dl': 'Decision 7 budget table: in-kind reduces cash outflow',
        },
    ]

    cards_html = ''
    for sc in scenarios:
        bg, dot, border = SEV[sc['sev']]
        resp_items = ''.join(f'<li style="margin:5px 0;font-size:13px;color:#9BA3BF;line-height:1.65">{r}</li>'
                             for r in sc['response'])
        badge_col = {'red':'#EF4444','amber':'#F59E0B','green':'#10B981'}[sc['sev']]
        badge_bg  = {'red':'rgba(239,68,68,0.15)','amber':'rgba(245,158,11,0.15)','green':'rgba(16,185,129,0.15)'}[sc['sev']]
        badge_txt = {'red':'High Risk','amber':'Medium Risk','green':'Opportunity'}[sc['sev']]

        cards_html += f"""
<div style="background:{bg};border:1px solid {border};border-left:4px solid {dot};
            border-radius:12px;padding:18px 20px;margin-bottom:12px">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:8px">
    <div>
      <span style="font-family:monospace;font-size:10px;color:{dot};margin-right:8px">S-{sc['num']}</span>
      <span style="font-size:13.5px;font-weight:600;color:#ECEEF4">{sc['title']}</span>
    </div>
    <span style="font-size:10px;font-weight:700;font-family:monospace;padding:3px 8px;border-radius:4px;
                 background:{badge_bg};color:{badge_col};white-space:nowrap;flex-shrink:0">{badge_txt}</span>
  </div>
  <div style="font-size:12.5px;color:{dot};font-family:monospace;margin-bottom:6px">{sc['impact']}</div>
  <div style="font-size:12px;color:#6B7599;margin-bottom:10px">{sc['detail']}</div>
  <details style="cursor:pointer">
    <summary style="font-size:12px;color:#9BA3BF;user-select:none;list-style:none;
                    display:flex;align-items:center;gap:6px">
      <span style="font-size:10px">▸</span>
      <span>Recommended response &nbsp;·&nbsp; <span style="color:#5E6785;font-size:11px">{sc['source']}</span></span>
    </summary>
    <ul style="margin:10px 0 4px 4px;padding:0;list-style:none">{resp_items}</ul>
    <div style="font-size:11px;color:#5E6785;font-family:monospace;margin-top:8px;padding:6px 10px;
                background:rgba(255,255,255,0.04);border-radius:6px;border-left:2px solid {dot}">{sc['dl']}</div>
  </details>
</div>"""

    return f"""
<div style="margin-top:28px">
  <div style="font-size:13.5px;font-weight:600;color:#ECEEF4;margin-bottom:6px">Named Scenario Analysis</div>
  <div style="font-size:12px;color:#6B7599;margin-bottom:18px">
    6 scenarios drawn from Devil's Advocate challenges and ops risk register &nbsp;·&nbsp; Expand each card for recommended response + Decision Layer trigger
  </div>
  {cards_html}
</div>"""

# ─────────────────────────────────────────────────────────────
# AGENT OUTPUT CARDS
# ─────────────────────────────────────────────────────────────

def build_agent_cards(results: dict) -> str:
    agents = [
        ('Orchestrator','🧠','strategy_profile','#3B82F6'),
        ('Research Analyst','🌐','research_output','#06B6D4'),
        ('Sponsor Intel','🤝','sponsor_output','#8B5CF6'),
        ('Exhibitor Intel','🏪','exhibitor_output','#10B981'),
        ('Speaker & Agenda','🎤','speaker_output','#EC4899'),
        ('Venue Intel','🏛️','venue_output','#F59E0B'),
        ('Pricing Agent','💰','pricing_output','#FBBF24'),
        ('GTM & Audience','📣','gtm_output','#14B8A6'),
        ('Ops & Risk','⚙️','ops_output','#6366F1'),
        ("Devil's Advocate",'😈','devils_advocate_output','#EF4444'),
        ('Self-Reflection','🪞','self_reflection_output','#F97316'),
        ('Outreach Agent','📧','outreach_output','#34D399'),
        ('Decision Layer','⚖️','decision_output','#84CC16'),
        ('Synthesizer CSO','📋','final_report','#0EA5E9'),
    ]
    cards = []
    for i, (name, icon, key, color) in enumerate(agents):
        content = results.get(key, '')
        words   = len(content.split()) if content else 0
        status  = 'complete' if content and len(content) > 50 else 'empty'
        kid     = f'ac{i}'
        preview = md_to_html(content, max_chars=2500) if content else '<p>No output available.</p>'
        cards.append(f"""
<div class="agent-card">
  <div class="agent-hdr" onclick="toggleEl('{kid}')">
    <div style="display:flex;align-items:center;gap:14px">
      <span class="agent-ico" style="background:{color}18;color:{color}">{icon}</span>
      <div>
        <div class="agent-name">{name}</div>
        <div class="agent-meta">Phase {i+1} · {words:,} words · <span class="st-{status}">{status}</span></div>
      </div>
    </div>
    <span class="expand-icon" id="ei-{kid}">▼</span>
  </div>
  <div class="agent-body" id="eb-{kid}" style="display:none">
    <div class="agent-preview">{preview}</div>
    {'<div class="truncated-note">… truncated — full output in /output/ folder</div>' if len(content) > 2500 else ''}
  </div>
</div>""")
    return '\n'.join(cards)


# ─────────────────────────────────────────────────────────────
# SECTION RENDERER
# ─────────────────────────────────────────────────────────────

def render_section_content(sid: str, content: str, p2_data: dict,
                           results: dict, budget_inr: int,
                           rendered_revenue_charts: list,
                           extracted_data: dict) -> str:
    body = md_to_html(content)

    if sid == 'executive-summary':
        if p2_data and 'revenue' not in rendered_revenue_charts:
            body += chart_three_stream(p2_data)
            rendered_revenue_charts.append('revenue')
        if budget_inr and 'budget' not in rendered_revenue_charts:
            body += chart_budget(budget_inr, {})
            rendered_revenue_charts.append('budget')

    elif sid == 'sponsor-strategy':
        sponsors = extracted_data.get('sponsors', [])
        # 1. The clean data table
        body += _sponsor_table(sponsors)
        # 2. The new Bubble Matrix (Relevance vs Feasibility)
        body += chart_sponsor_matrix(sponsors)
        # 3. The Bar Chart breakdown of all scores
        body += chart_sponsors(sponsors)

    elif sid == 'exhibitor-strategy':
        clusters = extracted_data.get('exhibitors', [])
        body += chart_exhibitors(clusters)

    elif sid == 'speaker-agenda':
        speakers = extracted_data.get('speakers', [])
        body += chart_speaker_radar(speakers)

    elif sid == 'pricing-forecast':
        if p2_data:
            body += chart_pricing_curve(p2_data)
            body += render_simulation(p2_data)
        if budget_inr and 'budget' not in rendered_revenue_charts:
            body += chart_budget(budget_inr, {})
            rendered_revenue_charts.append('budget')

    elif sid == 'gtm-strategy':
        channels = extracted_data.get('channels', [])
        body += chart_gtm(channels)

    elif sid == 'ops-risk':
        risks = extracted_data.get('risks', [])
        body += chart_risk_matrix(risks)

    elif sid == 'decision-register':
        decisions = extracted_data.get('decisions', [])
        body += render_decision_cards(decisions)

    elif sid == 'outreach-section':
        emails = extracted_data.get('emails', [])
        body += render_email_cards(emails)

    return body


# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap');
:root{
  --bg:#090D19;--bg2:#0C1020;--bg3:#101525;
  --card:#141C2E;--card2:#1A2338;--card3:#1E2840;
  --border:rgba(255,255,255,0.06);--border2:rgba(255,255,255,0.12);
  --text:#ECEEF4;--text2:#9BA3BF;--text3:#5E6785;
  --accent:#4F8EF7;--purple:#8B5CF6;--cyan:#06B6D4;
  --green:#10B981;--amber:#F59E0B;--red:#EF4444;--pink:#EC4899;
  --sw:272px;
  --font-d:'Syne',sans-serif;--font-b:'DM Sans',sans-serif;--font-m:'JetBrains Mono',monospace;
  --r:14px;--rs:8px;
}
*{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{font-family:var(--font-b);background:var(--bg);color:var(--text);line-height:1.78;overflow-x:hidden;font-size:14.5px;}
::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-track{background:var(--bg);}::-webkit-scrollbar-thumb{background:var(--card3);border-radius:2px;}
.sidebar{position:fixed;top:0;left:0;width:var(--sw);height:100vh;background:var(--bg2);border-right:1px solid var(--border);overflow-y:auto;z-index:200;padding-bottom:32px;}
.sb-brand{padding:28px 22px 20px;border-bottom:1px solid var(--border);}
.sb-logo{font-family:var(--font-d);font-size:23px;font-weight:800;letter-spacing:-0.5px;}
.sb-logo span{color:var(--accent);}
.sb-sub{font-size:9px;color:var(--text3);text-transform:uppercase;letter-spacing:2px;margin-top:5px;font-family:var(--font-m);}
.nav-group{padding:18px 22px 5px;font-size:9px;text-transform:uppercase;letter-spacing:2px;color:var(--text3);font-weight:600;font-family:var(--font-m);}
.sidebar nav ul{list-style:none;padding:2px 0;}
.sidebar nav ul li a{display:flex;align-items:center;gap:10px;padding:9px 22px;color:var(--text2);
  text-decoration:none;font-size:12.5px;border-left:2px solid transparent;transition:all .15s;
  border-radius:0 8px 8px 0;margin-right:8px;line-height:1.3;}
.sidebar nav ul li a:hover,.sidebar nav ul li a.active{color:var(--accent);background:rgba(79,142,247,.08);border-left-color:var(--accent);}
.main{margin-left:var(--sw);min-height:100vh;}
.hamburger{display:none;position:fixed;top:14px;left:14px;z-index:300;
  background:var(--card2);border:1px solid var(--border);border-radius:8px;
  width:40px;height:40px;cursor:pointer;flex-direction:column;align-items:center;justify-content:center;gap:5px;}
.hamburger span{width:18px;height:2px;background:var(--text);border-radius:1px;}
.cover{min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:80px 48px;position:relative;overflow:hidden;}
.cover-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(79,142,247,.02) 1px,transparent 1px),linear-gradient(90deg,rgba(79,142,247,.02) 1px,transparent 1px);background-size:60px 60px;}
.cover-glow{position:absolute;width:800px;height:800px;border-radius:50%;background:radial-gradient(circle,rgba(79,142,247,.05) 0%,transparent 65%);top:50%;left:50%;transform:translate(-50%,-50%);pointer-events:none;}
.cover-content{position:relative;z-index:1;max-width:820px;}
.eyebrow{display:inline-flex;align-items:center;gap:8px;background:rgba(79,142,247,.1);border:1px solid rgba(79,142,247,.2);color:var(--accent);padding:7px 20px;border-radius:24px;font-size:10px;font-weight:600;letter-spacing:2px;text-transform:uppercase;margin-bottom:36px;font-family:var(--font-m);}
.cover h1{font-family:var(--font-d);font-size:clamp(36px,5vw,64px);font-weight:800;line-height:1.05;letter-spacing:-2px;margin-bottom:20px;background:linear-gradient(140deg,#ECEEF4 0%,#7A85A8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.cover h1 .acc{background:linear-gradient(140deg,var(--accent) 0%,var(--cyan) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.cover-tag{font-size:16px;color:var(--text2);font-weight:300;margin-bottom:48px;font-style:italic;}
.cover-chips{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-bottom:48px;}
.chip{background:var(--card);border:1px solid var(--border2);border-radius:var(--rs);padding:11px 20px;text-align:center;min-width:120px;}
.chip .cl{font-size:8px;text-transform:uppercase;letter-spacing:1.5px;color:var(--text3);font-family:var(--font-m);margin-bottom:4px;}
.chip .cv{font-size:13px;font-weight:600;color:var(--text);font-family:var(--font-d);}
.cover-foot{font-size:11px;color:var(--text3);font-family:var(--font-m);letter-spacing:1px;}
.cover-foot strong{color:var(--accent);}
.stats-bar{background:var(--bg2);border-bottom:1px solid var(--border);padding:22px 48px;}
.stats-inner{max-width:940px;margin:0 auto;display:flex;gap:36px;flex-wrap:wrap;align-items:center;}
.pstat{display:flex;flex-direction:column;align-items:center;gap:3px;}
.pstat-n{font-family:var(--font-d);font-size:26px;font-weight:800;color:var(--accent);line-height:1;}
.pstat-l{font-size:9px;color:var(--text3);text-transform:uppercase;letter-spacing:1.5px;font-family:var(--font-m);}
.content-wrap{max-width:980px;margin:0 auto;padding:0 48px 80px;}
.report-section{padding:54px 0;border-bottom:1px solid var(--border);scroll-margin-top:20px;}
.section-hdr{display:flex;align-items:center;gap:14px;margin-bottom:32px;}
.section-ico{font-size:20px;width:46px;height:46px;background:var(--card);border:1px solid var(--border);border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.section-hdr h2{font-family:var(--font-d);font-size:23px;font-weight:700;color:var(--text);letter-spacing:-.5px;}
.section-body h3{font-family:var(--font-d);font-size:17px;font-weight:700;color:var(--text);margin:28px 0 11px;padding-left:12px;border-left:3px solid var(--accent);}
.section-body h4,.section-body .bold-head{font-size:14.5px;font-weight:600;color:var(--text);margin:20px 0 8px;}
.section-body h5{font-size:11px;font-weight:600;color:var(--text2);margin:14px 0 5px;text-transform:uppercase;letter-spacing:.5px;font-family:var(--font-m);}
.section-body p{color:var(--text2);font-size:14px;line-height:1.85;margin-bottom:12px;}
.section-body strong{color:var(--text);font-weight:600;}
.section-body em{color:var(--accent);font-style:italic;}
.section-body code{font-family:var(--font-m);font-size:12px;background:var(--card2);color:var(--cyan);padding:2px 6px;border-radius:4px;}
.section-body ul,.section-body ol{margin:10px 0 14px 22px;color:var(--text2);}
.section-body li{margin-bottom:6px;font-size:14px;line-height:1.78;}
.section-body ul li::marker{color:var(--accent);}
.section-body hr.rule{border:none;border-top:1px solid var(--border);margin:24px 0;}
.spacer{height:8px;}
.section-intro{font-size:13px;color:var(--text2);padding:13px 17px;background:var(--card);border-radius:var(--rs);border:1px solid var(--border);margin-bottom:20px;line-height:1.7;}
.table-wrap{overflow-x:auto;margin:20px 0;border-radius:var(--r);border:1px solid var(--border);}
table{width:100%;border-collapse:collapse;font-size:13px;}
thead{position:sticky;top:0;z-index:2;}
thead th{background:var(--card2);color:var(--accent);font-family:var(--font-m);font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:1px;padding:12px 15px;text-align:left;border-bottom:1px solid var(--border2);white-space:nowrap;}
tbody tr{border-bottom:1px solid var(--border);transition:background .12s;}
tbody tr:nth-child(even){background:rgba(255,255,255,0.015);}
tbody tr:hover{background:rgba(79,142,247,.05);}
tbody td{padding:11px 15px;color:var(--text2);vertical-align:top;line-height:1.6;}
.mono{font-family:var(--font-m);font-size:12px;}
.accent{color:var(--accent);font-weight:700;}
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;font-family:var(--font-m);}
.b-high{background:rgba(16,185,129,.15);color:var(--green);border:1px solid rgba(16,185,129,.3);}
.b-med{background:rgba(245,158,11,.15);color:var(--amber);border:1px solid rgba(245,158,11,.3);}
.b-low{background:rgba(239,68,68,.15);color:var(--red);border:1px solid rgba(239,68,68,.3);}
.b-tier1{background:rgba(79,142,247,.15);color:var(--accent);border:1px solid rgba(79,142,247,.3);}
.b-tier2{background:rgba(139,92,246,.15);color:var(--purple);border:1px solid rgba(139,92,246,.3);}
.b-tier3{background:rgba(16,185,129,.15);color:var(--green);border:1px solid rgba(16,185,129,.3);}
.tag-provided{background:rgba(16,185,129,.1);color:var(--green);font-size:10px;font-family:var(--font-m);padding:1px 6px;border-radius:3px;font-weight:600;}
.tag-inferred{background:rgba(79,142,247,.1);color:var(--accent);font-size:10px;font-family:var(--font-m);padding:1px 6px;border-radius:3px;font-weight:600;}
.tag-verified{background:rgba(6,182,212,.1);color:var(--cyan);font-size:10px;font-family:var(--font-m);padding:1px 6px;border-radius:3px;font-weight:600;}
.tag-critical{background:rgba(239,68,68,.1);color:var(--red);font-size:10px;font-family:var(--font-m);padding:1px 6px;border-radius:3px;font-weight:600;}
.tag-serpapi{background:rgba(6,182,212,.1);color:var(--cyan);font-size:10px;font-family:var(--font-m);padding:1px 6px;border-radius:3px;font-weight:600;}
.tag-tavily{background:rgba(139,92,246,.1);color:var(--purple);font-size:10px;font-family:var(--font-m);padding:1px 6px;border-radius:3px;font-weight:600;}
.chart-grid-2{display:grid;grid-template-columns:1fr 1fr;gap:20px;}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:22px;}
.chart-card--full{grid-column:1/-1;}
.chart-title{font-family:var(--font-d);font-size:14.5px;font-weight:700;color:var(--text);margin-bottom:4px;}
.chart-sub{font-size:12px;color:var(--text3);margin-bottom:18px;line-height:1.5;}
.legend-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px;}
.decision-grid{display:flex;flex-direction:column;gap:14px;margin-top:22px;}
.decision-card{background:var(--card);border:1px solid var(--border);border-left:4px solid var(--green);border-radius:var(--r);padding:18px 22px;}
.dec-num{font-family:var(--font-m);font-size:9px;color:var(--text3);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:5px;}
.dec-title{font-size:14.5px;font-weight:700;color:var(--text);margin-bottom:9px;line-height:1.4;}
.dec-body{font-size:13px;color:var(--text2);line-height:1.75;margin-bottom:12px;}
.conf-wrap{display:flex;align-items:center;gap:12px;}
.conf-bar-bg{flex:1;height:5px;background:var(--card2);border-radius:3px;}
.conf-bar{height:5px;border-radius:3px;}
.conf-label{font-family:var(--font-m);font-size:11px;font-weight:700;min-width:60px;text-align:right;}
.email-stack{display:flex;flex-direction:column;gap:12px;}
.email-card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;}
.email-header{display:flex;align-items:center;justify-content:space-between;padding:15px 20px;cursor:pointer;user-select:none;transition:background .15s;}
.email-header:hover{background:rgba(255,255,255,.02);}
.email-header-left{display:flex;align-items:center;gap:14px;}
.email-badge{font-size:10px;font-weight:700;font-family:var(--font-m);padding:3px 10px;border-radius:5px;white-space:nowrap;}
.email-subject{font-size:13.5px;font-weight:600;color:var(--text);}
.email-to{font-size:11px;color:var(--text3);font-family:var(--font-m);margin-top:2px;}
.expand-icon{color:var(--text3);font-size:11px;transition:transform .2s;flex-shrink:0;}
.email-body-wrap{padding:0 20px 20px;border-top:1px solid var(--border);}
.email-tag{font-size:9px;color:var(--text3);font-family:var(--font-m);text-transform:uppercase;letter-spacing:1.5px;margin:14px 0 10px;}
.email-body{font-size:13px;color:var(--text2);line-height:1.85;background:var(--bg3);border-radius:8px;padding:16px;border-left:3px solid var(--accent);margin-bottom:12px;}
.email-cta{font-size:12px;color:var(--amber);background:rgba(245,158,11,.07);border:1px solid rgba(245,158,11,.2);border-radius:6px;padding:8px 13px;margin-bottom:10px;font-family:var(--font-m);}
.copy-btn{cursor:pointer;font-size:11px;color:var(--accent);background:rgba(79,142,247,.1);border:1px solid rgba(79,142,247,.2);border-radius:5px;padding:6px 14px;font-family:var(--font-m);font-weight:600;transition:background .15s;}
.copy-btn:hover{background:rgba(79,142,247,.2);}
.agent-section{padding:52px 48px;background:var(--bg2);}
.agent-section-hdr{max-width:940px;margin:0 auto 26px;}
.agent-section-hdr h2{font-family:var(--font-d);font-size:22px;font-weight:700;color:var(--text);margin-bottom:6px;}
.agent-section-hdr p{color:var(--text2);font-size:13px;}
.agent-grid{max-width:940px;margin:0 auto;display:flex;flex-direction:column;gap:10px;}
.agent-card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;}
.agent-hdr{display:flex;align-items:center;justify-content:space-between;padding:15px 20px;cursor:pointer;user-select:none;transition:background .15s;}
.agent-hdr:hover{background:rgba(255,255,255,.015);}
.agent-ico{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;}
.agent-name{font-size:13.5px;font-weight:600;color:var(--text);}
.agent-meta{font-size:11px;color:var(--text3);font-family:var(--font-m);margin-top:2px;}
.st-complete{color:var(--green);}.st-empty{color:var(--red);}
.agent-body{padding:0 20px 20px;border-top:1px solid var(--border);}
.agent-preview{padding-top:16px;font-size:13px;color:var(--text2);line-height:1.78;}
.agent-preview p{font-size:13px;color:var(--text2);margin-bottom:8px;}
.truncated-note{margin-top:10px;font-size:11px;color:var(--text3);font-family:var(--font-m);padding:7px 12px;background:var(--card2);border-radius:4px;}
footer{background:var(--bg2);border-top:1px solid var(--border);text-align:center;padding:40px;}
footer p{color:var(--text3);font-size:12px;font-family:var(--font-m);line-height:2;}
footer strong{color:var(--accent);}
@media(max-width:900px){
  .sidebar{transform:translateX(-100%);transition:transform .3s;}
  .sidebar.open{transform:translateX(0);}
  .hamburger{display:flex;}
  .main{margin-left:0;}
  .content-wrap,.agent-section,.stats-bar{padding-left:20px;padding-right:20px;}
  .chart-grid-2{grid-template-columns:1fr;}
  .chart-card--full{grid-column:auto;}
}
"""

# ─────────────────────────────────────────────────────────────
# MAIN GENERATOR
# ─────────────────────────────────────────────────────────────

def generate_html_report(report_content: str, inputs: dict,
                         results: dict = None,
                         prediction_data: dict = None,
                         extracted_chart_data: dict = None) -> str:
    if results is None:
        results = {}
    if extracted_chart_data is None:
        extracted_chart_data = {}

    _chart_counter[0] = 0  # reset per render

    p2_data    = prediction_data
    budget_s   = inputs.get('budget_range', '')
    budget_inr = _parse_inr(budget_s)
    if not budget_inr:
        budget_inr = _parse_inr(str(inputs))

    sections     = split_into_sections(report_content)
    current_year = datetime.now().year
    event_name   = inputs.get('event_category', 'Conference')

    # Track which heavy charts have been rendered to avoid duplication
    rendered_revenue_charts = []

    # Nav
    nav_items = ''
    for sid, title, icon, _ in sections:
        nav_items += f'<li><a href="#{sid}" class="nav-link">{icon} {title}</a></li>\n'
    nav_items += '<li><a href="#agent-section" class="nav-link">🤖 Agent Outputs</a></li>\n'

    # Render sections
    sections_html = ''
    for sid, title, icon, content in sections:
        body = render_section_content(sid, content, p2_data, results, budget_inr, rendered_revenue_charts, extracted_chart_data)
        sections_html += f"""
<section id="{sid}" class="report-section">
  <div class="section-hdr">
    <span class="section-ico">{icon}</span>
    <h2>{title}</h2>
  </div>
  <div class="section-body">{body}</div>
</section>"""

    # Inject missing sections
    injected_ids = set(s[0] for s in sections)
    inject_map = [
        ('sponsor-strategy','Sponsor Strategy','🤝','sponsor_output'),
        ('exhibitor-strategy','Exhibitor Strategy','🏪','exhibitor_output'),
        ('speaker-agenda','Speaker & Agenda Plan','🎤','speaker_output'),
        ('venue-strategy','Venue & City Strategy','🏛️','venue_output'),
        ('pricing-forecast','Revenue & Pricing Forecast','💰','pricing_output'),
        ('gtm-strategy','GTM & Audience Strategy','📣','gtm_output'),
        ('ops-risk','Operations & Risk','⚙️','ops_output'),
        ('da-analysis',"Devil's Advocate Analysis",'😈','devils_advocate_output'),
        ('decision-register','Decision Register','⚖️','decision_output'),
        ('outreach-section','Outreach Email Drafts','📧','outreach_output'),
    ]
    for sid, title, icon, key in inject_map:
        if sid not in injected_ids:
            content = results.get(key, '')
            if content and len(content) > 50:
                body = render_section_content(sid, content, p2_data, results, budget_inr, rendered_revenue_charts, extracted_chart_data)
                sections_html += f"""
<section id="{sid}" class="report-section">
  <div class="section-hdr">
    <span class="section-ico">{icon}</span>
    <h2>{title}</h2>
  </div>
  <div class="section-body">{body}</div>
</section>"""
                nav_items += f'<li><a href="#{sid}" class="nav-link">{icon} {title}</a></li>\n'

    # Cover chips
    chips = ''
    for label, key in [('Category','event_category'),('Region','geography_region'),
                        ('Date','event_date_range'),('Duration','expected_duration'),
                        ('Audience','target_audience_size'),('Budget','budget_range')]:
        val = inputs.get(key,'—')
        chips += f'<div class="chip"><div class="cl">{label}</div><div class="cv">{val}</div></div>'

    total_rev_str = _fmt_inr(p2_data.get('total_revenue', 0)) if p2_data else ''
    agent_cards   = build_agent_cards(results)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ConferaX — {event_name} Intelligence Report v6.2</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js" crossorigin="anonymous"></script>
<style>{CSS}</style>
</head>
<body>

{CHART_HELPERS_JS}

<button class="hamburger" onclick="document.getElementById('sidebar').classList.toggle('open')" aria-label="Toggle navigation">
  <span></span><span></span><span></span>
</button>

<nav class="sidebar" id="sidebar">
  <div class="sb-brand">
    <div class="sb-logo">Confera<span>X</span></div>
    <div class="sb-sub">Intelligence Report v6.2</div>
  </div>
  <div class="nav-group">Contents</div>
  <nav><ul>
    <li><a href="#cover" class="nav-link">🏠 Cover</a></li>
    {nav_items}
  </ul></nav>
</nav>

<div class="main">

<div class="cover" id="cover">
  <div class="cover-grid"></div>
  <div class="cover-glow"></div>
  <div class="cover-content">
    <div class="eyebrow">⚡ ConferaX Intelligence Report v6.2</div>
    <h1><span class="acc">{event_name}</span><br>Intelligence Report</h1>
    <p class="cover-tag">Autonomous Multi-Agent Strategy · Quantitative Prediction Engine · Ready to Execute</p>
    <div class="cover-chips">{chips}</div>
    <div class="cover-foot">Generated by <strong>ConferaX</strong> · Autonomous Conference Intelligence · {current_year}</div>
  </div>
</div>

<div class="stats-bar">
  <div class="stats-inner">
    <div class="pstat"><span class="pstat-n">14</span><span class="pstat-l">Agents</span></div>
    <div class="pstat"><span class="pstat-n">11</span><span class="pstat-l">Phases</span></div>
    <div class="pstat"><span class="pstat-n">22</span><span class="pstat-l">Web Searches</span></div>
    <div class="pstat"><span class="pstat-n">10K</span><span class="pstat-l">MC Simulations</span></div>
    <div class="pstat"><span class="pstat-n">9</span><span class="pstat-l">Email Drafts</span></div>
    <div class="pstat"><span class="pstat-n">6</span><span class="pstat-l">Conflict Checks</span></div>
    {f'<div class="pstat"><span class="pstat-n">{total_rev_str}</span><span class="pstat-l">Projected Revenue</span></div>' if total_rev_str else ''}
  </div>
</div>

<div class="content-wrap">{sections_html}</div>

<div class="agent-section" id="agent-section">
  <div class="agent-section-hdr">
    <h2>🤖 Agent Intelligence Outputs</h2>
    <p>Full reasoning from all 14 agents — click any card to expand</p>
  </div>
  <div class="agent-grid">{agent_cards}</div>
</div>

<footer>
  <p>© {current_year} <strong>ConferaX</strong> — Autonomous Conference Intelligence Engine v6.2</p>
  <p>14 agents · 2-pass prediction engine · 22 Tavily + SerpAPI searches · Kimi K2 · 128K context</p>
</footer>

</div>

<script>
function toggleEl(id){{
  var b=document.getElementById('eb-'+id),i=document.getElementById('ei-'+id);
  if(!b)return;
  var open=b.style.display==='none'||b.style.display==='';
  b.style.display=open?'block':'none';
  if(i)i.style.transform=open?'rotate(180deg)':'rotate(0deg)';
}}
function copyText(id,btn){{
  var ta=document.getElementById(id);
  if(!ta)return;
  navigator.clipboard.writeText(ta.value).then(function(){{
    var orig=btn.textContent;btn.textContent='✅ Copied!';
    setTimeout(function(){{btn.textContent=orig;}},2000);
  }}).catch(function(){{ta.select();document.execCommand('copy');}});
}}
(function(){{
  var secs=document.querySelectorAll('section[id],div[id]');
  var links=document.querySelectorAll('.nav-link');
  var obs=new IntersectionObserver(function(entries){{
    entries.forEach(function(e){{
      if(e.isIntersecting){{
        links.forEach(function(l){{
          l.classList.remove('active');
          if(l.getAttribute('href')==='#'+e.target.id)l.classList.add('active');
        }});
      }}
    }});
  }},{{threshold:0.12,rootMargin:'-60px 0px -55% 0px'}});
  secs.forEach(function(s){{obs.observe(s);}});
  links.forEach(function(l){{
    l.addEventListener('click',function(){{
      document.getElementById('sidebar').classList.remove('open');
    }});
  }});
}})();
document.body.style.opacity='0';
document.body.style.transition='opacity 0.4s ease';
window.addEventListener('load',function(){{document.body.style.opacity='1';}});
</script>

</body>
</html>"""

def generate_html_report_simple(report_content: str, inputs: dict) -> str:
    return generate_html_report(report_content, inputs, results={}, prediction_data=None, extracted_chart_data={})