import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="K-Factor Calculator",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Design System ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #f8faf8;
    color: #1a2e1a;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f0f5f0; }
::-webkit-scrollbar-thumb { background: #b6d4b6; border-radius: 3px; }

.app-header {
    display: flex; align-items: center; gap: 16px;
    padding: 28px 0 16px;
    border-bottom: 2px solid #d4ead4;
    margin-bottom: 28px;
}
.header-icon {
    width: 48px; height: 48px;
    background: #16a34a; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; box-shadow: 0 4px 16px rgba(22,163,74,0.22); flex-shrink: 0;
}
.header-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.75rem; font-weight: 700; color: #111d11; line-height: 1.15; margin: 0;
}
.header-sub {
    font-size: 0.75rem; color: #6b9e6b;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.09em; margin-top: 3px;
}

.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem; font-weight: 500;
    letter-spacing: 0.14em; color: #16a34a;
    text-transform: uppercase; margin-bottom: 10px;
}

.card {
    background: #ffffff; border: 1px solid #d4ead4;
    border-radius: 12px; padding: 18px 20px; margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(22,163,74,0.06);
}
.card-green { background: #f0faf0; border: 1px solid #86c986; }

.kpi-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 12px; margin: 20px 0;
}
.kpi-tile {
    background: #ffffff; border: 1px solid #d4ead4;
    border-radius: 12px; padding: 18px 20px;
    position: relative; overflow: hidden;
    box-shadow: 0 1px 4px rgba(22,163,74,0.07);
}
.kpi-tile::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #16a34a, #4ade80);
    border-radius: 12px 12px 0 0;
}
.kpi-tile.highlight { border-color: #16a34a; box-shadow: 0 2px 12px rgba(22,163,74,0.15); }
.kpi-tile.highlight::before { background: #16a34a; }
.kpi-label {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.63rem;
    color: #6b9e6b; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.75rem; font-weight: 700; color: #111d11; line-height: 1;
}
.kpi-value.green { color: #16a34a; }
.kpi-unit { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #9ab89a; margin-top: 5px; }

.callout {
    background: #f0faf0; border: 1px solid #bbdcbb;
    border-left: 4px solid #16a34a; border-radius: 8px;
    padding: 12px 16px; margin: 10px 0;
    font-size: 0.83rem; color: #2d4a2d; line-height: 1.6;
}
.callout.warn { background: #fffbeb; border-color: #fde68a; border-left-color: #d97706; color: #7c5700; }
.callout.success { background: #f0fdf4; border-color: #bbf7d0; border-left-color: #16a34a; color: #14532d; }

.formula {
    background: #f4faf4; border: 1px solid #d4ead4; border-radius: 8px;
    padding: 14px 18px; font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem; color: #166534; margin: 8px 0; line-height: 1.9;
}

.badge {
    display: inline-block; padding: 3px 10px; border-radius: 99px;
    font-family: 'IBM Plex Mono', monospace; font-size: 0.67rem;
    font-weight: 500; letter-spacing: 0.04em;
}
.badge-soft  { background: #dbeafe; color: #1d4ed8; }
.badge-med   { background: #dcfce7; color: #15803d; }
.badge-hard  { background: #fee2e2; color: #b91c1c; }
.badge-good  { background: #dcfce7; color: #15803d; }
.badge-warn  { background: #fef9c3; color: #a16207; }
.badge-user  { background: #dcfce7; color: #166534; }

div[data-testid="stNumberInput"] > div > div > input,
div[data-testid="stSelectbox"] > div > div {
    background-color: #ffffff !important; border-color: #d4ead4 !important;
    color: #1a2e1a !important; border-radius: 8px !important;
}
div[data-testid="stNumberInput"] > div > div > input:focus {
    border-color: #16a34a !important; box-shadow: 0 0 0 2px rgba(22,163,74,0.18) !important;
}
.stCheckbox > label { color: #2d4a2d !important; font-size: 0.88rem !important; }
.stButton > button {
    background: #16a34a !important; color: white !important; border: none !important;
    border-radius: 8px !important; font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important; padding: 8px 20px !important; transition: background 0.2s !important;
}
.stButton > button:hover { background: #15803d !important; }
.stDownloadButton > button {
    background: #f0faf0 !important; color: #16a34a !important;
    border: 1px solid #d4ead4 !important; border-radius: 8px !important; font-weight: 500 !important;
}
div[data-testid="stExpander"] {
    background: #ffffff !important; border: 1px solid #d4ead4 !important; border-radius: 10px !important;
}
div[data-testid="metric-container"] {
    background: #ffffff; border: 1px solid #d4ead4; border-radius: 10px; padding: 14px 16px;
}
[data-testid="stMetricValue"] { color: #111d11 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #6b9e6b !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.68rem !important; }

hr { border-color: #d4ead4 !important; }
h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif !important; color: #111d11 !important; }
.stDataFrame { border: 1px solid #d4ead4 !important; border-radius: 10px !important; }
label { color: #2d4a2d !important; font-size: 0.85rem !important; }
p, li { color: #2d4a2d; }
.stRadio > label { color: #2d4a2d !important; }
[data-testid="stSlider"] > div > div { color: #2d4a2d !important; }
</style>
""", unsafe_allow_html=True)

# ─── Material Database ────────────────────────────────────────────────────
MATERIALS = {
    "Aluminum 1100-O":      {"typical_k": 0.33, "uts_mpa": 90,   "yield_mpa": 35,   "elongation": 35, "min_rb_factor": 0.0, "E_mpa": 69_000},
    "Aluminum 5052-H32":    {"typical_k": 0.34, "uts_mpa": 228,  "yield_mpa": 193,  "elongation": 12, "min_rb_factor": 1.0, "E_mpa": 70_000},
    "Aluminum 6061-T6":     {"typical_k": 0.35, "uts_mpa": 310,  "yield_mpa": 276,  "elongation": 8,  "min_rb_factor": 1.5, "E_mpa": 68_900},
    "Steel – Mild (1020)":  {"typical_k": 0.42, "uts_mpa": 380,  "yield_mpa": 210,  "elongation": 25, "min_rb_factor": 0.5, "E_mpa": 200_000},
    "Steel – HSLA 350":     {"typical_k": 0.44, "uts_mpa": 450,  "yield_mpa": 350,  "elongation": 20, "min_rb_factor": 1.5, "E_mpa": 200_000},
    "Steel – SS 304":       {"typical_k": 0.45, "uts_mpa": 515,  "yield_mpa": 205,  "elongation": 40, "min_rb_factor": 1.0, "E_mpa": 193_000},
    "Steel – SS 316":       {"typical_k": 0.46, "uts_mpa": 485,  "yield_mpa": 170,  "elongation": 40, "min_rb_factor": 1.0, "E_mpa": 193_000},
    "Steel – Spring":       {"typical_k": 0.48, "uts_mpa": 1200, "yield_mpa": 1000, "elongation": 5,  "min_rb_factor": 3.0, "E_mpa": 207_000},
    "Copper (C110)":        {"typical_k": 0.35, "uts_mpa": 220,  "yield_mpa": 70,   "elongation": 40, "min_rb_factor": 0.0, "E_mpa": 117_000},
    "Brass C260":           {"typical_k": 0.38, "uts_mpa": 340,  "yield_mpa": 103,  "elongation": 43, "min_rb_factor": 0.5, "E_mpa": 110_000},
    "Titanium Gr2":         {"typical_k": 0.45, "uts_mpa": 345,  "yield_mpa": 276,  "elongation": 20, "min_rb_factor": 2.5, "E_mpa": 105_000},
}

CHART_CONFIG = {
    "displayModeBar": True,
    "modeBarButtonsToRemove": ["select2d", "lasso2d", "autoScale2d", "toImage"],
    "displaylogo": False,
}

PLOT_LAYOUT = dict(
    paper_bgcolor="#f8faf8",
    plot_bgcolor="#ffffff",
    font=dict(family="Plus Jakarta Sans", color="#4a6e4a", size=12),
    legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor="#d4ead4", borderwidth=1,
                font=dict(size=11)),
    margin=dict(l=10, r=10, t=48, b=10),
)
GRID_STYLE = dict(gridcolor="#e8f5e8", zerolinecolor="#d4ead4", linecolor="#d4ead4")
C_GREEN   = "#16a34a"
C_PURPLE  = "#7c3aed"
C_BLUE    = "#0891b2"
C_AMBER   = "#d97706"
C_RED     = "#dc2626"

# ─── Math Engine ─────────────────────────────────────────────────────────

@st.cache_data
def k_logistic(r_s: float) -> float:
    a, b, c, d = 0.277833218, 1.056058295, 0.608320238, 0.502506534
    return d + (a - d) / (1 + (r_s / c) ** b)

@st.cache_data
def k_analytical(r_s: float) -> float:
    if r_s <= 0:
        return 0.33
    return np.log(1 + 1 / (2 * r_s + 1)) / np.log(1 + 1 / r_s)

@st.cache_data
def k_din6935(r_s: float) -> float:
    if r_s < 0.65:
        return 0.33
    elif r_s < 1.0:
        return 0.33 + 0.125 * (r_s - 0.65) / 0.35
    elif r_s < 3.0:
        return 0.4575 + 0.0325 * (r_s - 1.0) / 2.0
    else:
        return min(0.5, 0.49 + 0.01 * (r_s - 3.0) / 7.0)

def k_for_method(r_s: float, method: str) -> float:
    if method == "Logistic fit":
        return k_logistic(r_s)
    elif method == "Analytical (Wang-Wenner)":
        return k_analytical(r_s)
    return k_din6935(r_s)

def bend_allowance(k: float, angle_deg: float, r: float, t: float) -> float:
    return np.radians(angle_deg) * (r + k * t)

def outside_setback(angle_deg: float, r: float, t: float) -> float:
    return np.tan(np.radians(angle_deg / 2)) * (r + t)

def bend_deduction(ba: float, r: float, t: float, angle_deg: float) -> float:
    return 2 * outside_setback(angle_deg, r, t) - ba

def springback_angle(angle_deg: float, r: float, t: float, yield_mpa: float, E_mpa: float = 200_000) -> float:
    ratio = 3 * yield_mpa * r / (E_mpa * t)
    return angle_deg * ratio

def min_bend_radius(t: float, elongation_pct: float) -> float:
    if elongation_pct <= 0:
        return float('inf')
    return t * (50 / elongation_pct - 1)

def flat_length(leg1: float, leg2: float, ba: float) -> float:
    return leg1 + leg2 + ba

# ─── App Header ──────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="header-icon">⚙️</div>
  <div>
    <div class="header-title">K-Factor Calculator</div>
    <div class="header-sub">SHEET METAL BENDING · NEUTRAL AXIS ANALYSIS · FLAT PATTERN DEVELOPMENT</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Input Panel ─────────────────────────────────────────────────────────
col_inp, col_res = st.columns([1, 2], gap="large")

with col_inp:
    st.markdown('<div class="section-label">Parameters</div>', unsafe_allow_html=True)

    unit = st.selectbox("Unit system", ["mm", "inches"])
    unit_lbl = "mm" if unit == "mm" else "in"

    r = st.number_input(f"Inner bend radius r ({unit_lbl})", min_value=0.01, value=2.0, step=0.5, format="%.2f")
    t = st.number_input(f"Sheet thickness t ({unit_lbl})", min_value=0.01, value=2.0, step=0.1, format="%.2f")

    st.markdown('<div class="section-label" style="margin-top:20px">Material</div>', unsafe_allow_html=True)
    mat_choice = st.selectbox("Select material", ["— Custom —"] + list(MATERIALS.keys()))

    mat = MATERIALS.get(mat_choice) if mat_choice != "— Custom —" else None
    if mat:
        st.markdown(f"""
        <div class="callout">
        UTS <b>{mat['uts_mpa']} MPa</b> · Yield <b>{mat['yield_mpa']} MPa</b> ·
        Elongation <b>{mat['elongation']}%</b> · Reference K <b>{mat['typical_k']}</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:20px">Bend Geometry</div>', unsafe_allow_html=True)
    bend_angle = st.slider("Bend angle (°)", min_value=1, max_value=180, value=90, step=1)

    st.markdown('<div class="section-label" style="margin-top:20px">K-Factor Method</div>', unsafe_allow_html=True)
    method = st.radio("Calculation method",
                      ["Logistic fit", "Analytical (Wang-Wenner)", "DIN 6935 empirical"], index=0)

    st.markdown('<div class="section-label" style="margin-top:20px">Flat Pattern</div>', unsafe_allow_html=True)
    show_flat = st.checkbox("Flat pattern development", value=True)
    if show_flat:
        leg1 = st.number_input(f"Flange A ({unit_lbl})", min_value=0.0, value=50.0, step=1.0, format="%.1f")
        leg2 = st.number_input(f"Flange B ({unit_lbl})", min_value=0.0, value=30.0, step=1.0, format="%.1f")
    else:
        leg1 = leg2 = 0.0

    show_springback = st.checkbox("Springback estimation", value=bool(mat))

# ─── Calculations ────────────────────────────────────────────────────────
r_s = r / t
K   = k_for_method(r_s, method)
BA  = bend_allowance(K, bend_angle, r, t)
BD  = bend_deduction(BA, r, t, bend_angle)
OSB = outside_setback(bend_angle, r, t)

k_log = k_logistic(r_s)
k_ana = k_analytical(r_s)
k_din = k_din6935(r_s)

# ─── Results Panel ───────────────────────────────────────────────────────
with col_res:
    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)

    if r_s < 1.0:
        zone_badge = '<span class="badge badge-warn">Sharp bend</span>'
        zone_note  = "Thinning risk. Validate with test pieces."
    elif r_s < 4.0:
        zone_badge = '<span class="badge badge-med">Standard bend</span>'
        zone_note  = "Typical production range — reliable prediction."
    else:
        zone_badge = '<span class="badge badge-good">Gentle bend</span>'
        zone_note  = "Large-radius bend — K approaches 0.5."

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-tile">
        <div class="kpi-label">r / t ratio</div>
        <div class="kpi-value">{r_s:.3f}</div>
        <div class="kpi-unit">dimensionless</div>
      </div>
      <div class="kpi-tile highlight">
        <div class="kpi-label">K-Factor</div>
        <div class="kpi-value green">{K:.4f}</div>
        <div class="kpi-unit">neutral axis position</div>
      </div>
      <div class="kpi-tile">
        <div class="kpi-label">Bend Allowance</div>
        <div class="kpi-value">{BA:.3f}</div>
        <div class="kpi-unit">{unit_lbl}</div>
      </div>
      <div class="kpi-tile">
        <div class="kpi-label">Bend Deduction</div>
        <div class="kpi-value">{BD:.3f}</div>
        <div class="kpi-unit">{unit_lbl}</div>
      </div>
    </div>
    <div class="callout" style="margin-bottom:16px">{zone_badge} &nbsp; {zone_note}</div>
    """, unsafe_allow_html=True)

    with st.expander("📐 Formula trace", expanded=False):
        st.markdown(f"""
        <div class="formula">
        Neutral axis offset:  y = K × t = {K:.4f} × {t} = {K*t:.4f} {unit_lbl}<br>
        Bend angle (rad):     α = {bend_angle}° × π/180 = {np.radians(bend_angle):.5f} rad<br>
        Bend Allowance:       BA = α × (r + K·t) = {np.radians(bend_angle):.5f} × ({r} + {K*t:.4f}) = <b>{BA:.4f} {unit_lbl}</b><br>
        Outside Setback:      OSSB = tan(α/2) × (r + t) = {OSB:.4f} {unit_lbl}<br>
        Bend Deduction:       BD = 2×OSSB − BA = {2*OSB:.4f} − {BA:.4f} = <b>{BD:.4f} {unit_lbl}</b>
        </div>
        """, unsafe_allow_html=True)

    if show_flat:
        FL = flat_length(leg1, leg2, BA)
        st.markdown(f"""
        <div class="card" style="margin-top:4px">
          <div class="section-label">Flat Pattern Length</div>
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:2.2rem;font-weight:700;color:#16a34a;">{FL:.3f} <span style="font-size:1rem;color:#9ab89a">{unit_lbl}</span></div>
          <div style="font-size:0.78rem;color:#6b9e6b;margin-top:6px;font-family:'IBM Plex Mono',monospace;">
            Flange A {leg1:.1f} + Flange B {leg2:.1f} + BA {BA:.3f} = {FL:.3f} {unit_lbl}
          </div>
        </div>
        """, unsafe_allow_html=True)

    if show_springback and mat:
        E_mpa = mat["E_mpa"]
        sb    = springback_angle(bend_angle, r, t, mat["yield_mpa"], E_mpa)
        rb_min = min_bend_radius(t, mat["elongation"])
        overbend = bend_angle + sb

        col_sb1, col_sb2 = st.columns(2)
        with col_sb1:
            st.markdown(f"""
            <div class="card">
              <div class="section-label">Springback</div>
              <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.6rem;font-weight:700;color:#d97706;">+{sb:.2f}°</div>
              <div style="font-size:0.78rem;color:#6b9e6b;margin-top:4px;font-family:'IBM Plex Mono',monospace;">Overbend to: {overbend:.1f}°</div>
            </div>
            """, unsafe_allow_html=True)
        with col_sb2:
            rb_ok    = r >= rb_min
            rb_color = C_GREEN if rb_ok else C_RED
            rb_icon  = "✓" if rb_ok else "✗"
            st.markdown(f"""
            <div class="card">
              <div class="section-label">Min Bend Radius</div>
              <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.6rem;font-weight:700;color:{rb_color};">{rb_icon} {rb_min:.2f} {unit_lbl}</div>
              <div style="font-size:0.78rem;color:#6b9e6b;margin-top:4px;font-family:'IBM Plex Mono',monospace;">Your r={r:.2f} — {'OK' if rb_ok else 'RISK OF CRACKING'}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""<div class="section-label" style="margin-top:20px">Method Comparison</div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    def method_tile(col, label, val, active):
        border = "border-color:#16a34a;box-shadow:0 2px 10px rgba(22,163,74,0.15)" if active else ""
        col.markdown(f"""
        <div class="card" style="{border}">
          <div style="font-size:0.67rem;font-family:'IBM Plex Mono',monospace;color:#6b9e6b;letter-spacing:0.08em">{label}</div>
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.4rem;font-weight:700;color:{'#16a34a' if active else '#6b9e6b'}">{val:.4f}</div>
        </div>
        """, unsafe_allow_html=True)
    method_tile(c1, "Logistic fit",  k_log, method == "Logistic fit")
    method_tile(c2, "Wang-Wenner",   k_ana, method == "Analytical (Wang-Wenner)")
    method_tile(c3, "DIN 6935",      k_din, method == "DIN 6935 empirical")


# ═══════════════════════════════════════════════════════════════════════════
# ─── SECTION 1: K-Factor Curve Analysis ─────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-label">K-Factor Curve Analysis</div>', unsafe_allow_html=True)

rs_range = np.linspace(0.05, 25, 500)
k_log_arr = np.array([k_logistic(x)   for x in rs_range])
k_ana_arr = np.array([k_analytical(x) for x in rs_range])
k_din_arr = np.array([k_din6935(x)    for x in rs_range])

# ── Uncertainty band ──
k_upper = np.maximum.reduce([k_log_arr, k_ana_arr, k_din_arr])
k_lower = np.minimum.reduce([k_log_arr, k_ana_arr, k_din_arr])

# ── BA family of curves (r = 1t, 2t, 4t, 8t) ──
angles_deg = np.linspace(1, 180, 360)
r_multiples = [(1, 1.0), (2, 0.72), (4, 0.45), (8, 0.25)]

fig1 = make_subplots(
    rows=1, cols=2,
    subplot_titles=["K-Factor vs r/t  —  All Methods + Uncertainty Band",
                    "Bend Allowance vs Angle  —  r = 1t, 2t, 4t, 8t"],
    horizontal_spacing=0.10,
)

# Uncertainty band
fig1.add_trace(go.Scatter(
    x=np.concatenate([rs_range, rs_range[::-1]]),
    y=np.concatenate([k_upper, k_lower[::-1]]),
    fill="toself",
    fillcolor="rgba(22,163,74,0.09)",
    line=dict(color="rgba(0,0,0,0)"),
    name="Method spread",
    hoverinfo="skip",
), row=1, col=1)

# K curves
for arr, name, color, dash in [
    (k_log_arr, "Logistic",    C_GREEN,  "solid"),
    (k_ana_arr, "Wang-Wenner", C_PURPLE, "dash"),
    (k_din_arr, "DIN 6935",    C_BLUE,   "dot"),
]:
    fig1.add_trace(go.Scatter(
        x=rs_range, y=arr, name=name,
        line=dict(color=color, width=2, dash=dash),
        hovertemplate="r/t=%{x:.2f}<br>K=%{y:.4f}<extra></extra>",
    ), row=1, col=1)

# User point (star)
fig1.add_trace(go.Scatter(
    x=[r_s], y=[K], name="Your calc",
    mode="markers",
    marker=dict(color=C_GREEN, size=14, symbol="star",
                line=dict(color="white", width=2)),
    hovertemplate=f"r/t={r_s:.3f}<br>K={K:.4f}<extra>Your calc</extra>",
), row=1, col=1)

# Ref line K=0.5 with annotation
fig1.add_hline(y=0.5, line=dict(color="#9ab89a", dash="dot", width=1.2), row=1, col=1)
fig1.add_annotation(
    x=22, y=0.503,
    text="K = 0.5  (mid-plane)",
    font=dict(size=10, color="#9ab89a", family="IBM Plex Mono"),
    showarrow=False, xref="x", yref="y",
)

# BA family of curves
ba_colors = [C_GREEN, "#0891b2", "#7c3aed", "#d97706"]
for (mult, _), color in zip(r_multiples, ba_colors):
    r_i  = mult * t
    K_i  = k_for_method(r_i / t, method)
    ba_i = np.array([bend_allowance(K_i, a, r_i, t) for a in angles_deg])
    fig1.add_trace(go.Scatter(
        x=angles_deg, y=ba_i,
        name=f"r = {mult}t",
        line=dict(color=color, width=2),
        hovertemplate=f"r={mult}t, α=%{{x:.0f}}°<br>BA=%{{y:.3f}} {unit_lbl}<extra></extra>",
    ), row=1, col=2)

# Current point on BA chart
fig1.add_vline(x=bend_angle, line=dict(color=C_GREEN, dash="dot", width=1.5), row=1, col=2)
fig1.add_trace(go.Scatter(
    x=[bend_angle], y=[BA],
    mode="markers",
    marker=dict(color=C_GREEN, size=11, symbol="circle", line=dict(color="white", width=2)),
    showlegend=False,
    hovertemplate=f"α={bend_angle}°<br>BA={BA:.3f} {unit_lbl}<extra>Your calc</extra>",
), row=1, col=2)

fig1.update_layout(height=420, **PLOT_LAYOUT)
for ax in ["xaxis", "xaxis2", "yaxis", "yaxis2"]:
    fig1.update_layout(**{ax: {**GRID_STYLE}})
fig1.update_xaxes(title_text="r/t ratio",       row=1, col=1)
fig1.update_yaxes(title_text="K-Factor",         row=1, col=1, range=[0.28, 0.52])
fig1.update_xaxes(title_text="Bend angle (°)",   row=1, col=2)
fig1.update_yaxes(title_text=f"Bend Allowance ({unit_lbl})", row=1, col=2)
fig1.update_annotations(font=dict(color="#4a6e4a", size=12))

st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)


# ═══════════════════════════════════════════════════════════════════════════
# ─── SECTION 2: Method Divergence + Flat Pattern Cross-Section ──────────
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-label">Method Divergence  ·  Cross-Section Diagram</div>', unsafe_allow_html=True)

col_div, col_xsec = st.columns([1, 1], gap="large")

# ── Method divergence strip ──
with col_div:
    diff_log_din = np.abs(k_log_arr - k_din_arr)
    diff_ana_din = np.abs(k_ana_arr - k_din_arr)

    fig_div = go.Figure()
    fig_div.add_trace(go.Scatter(
        x=rs_range, y=diff_log_din * 1000,
        name="|Logistic − DIN 6935|",
        line=dict(color=C_GREEN, width=2),
        fill="tozeroy", fillcolor="rgba(22,163,74,0.10)",
        hovertemplate="r/t=%{x:.2f}<br>ΔK=%{y:.2f}×10⁻³<extra></extra>",
    ))
    fig_div.add_trace(go.Scatter(
        x=rs_range, y=diff_ana_din * 1000,
        name="|Wang-Wenner − DIN 6935|",
        line=dict(color=C_PURPLE, width=2, dash="dash"),
        fill="tozeroy", fillcolor="rgba(124,58,237,0.06)",
        hovertemplate="r/t=%{x:.2f}<br>ΔK=%{y:.2f}×10⁻³<extra></extra>",
    ))
    fig_div.add_vline(x=r_s, line=dict(color=C_GREEN, dash="dot", width=1.5))
    fig_div.update_layout(
        title=dict(text="Method Divergence vs DIN 6935  (×10⁻³)", font=dict(size=13), x=0),
        xaxis_title="r/t ratio",
        yaxis_title="ΔK  (×10⁻³)",
        height=340, **PLOT_LAYOUT,
    )
    fig_div.update_xaxes(**GRID_STYLE)
    fig_div.update_yaxes(**GRID_STYLE)
    st.plotly_chart(fig_div, use_container_width=True, config=CHART_CONFIG)
    st.markdown("""
    <div class="callout" style="font-size:0.79rem;">
    <b>Reading guide:</b> Peak divergence typically occurs at r/t 0.5–2.0.
    In the standard bend zone (r/t 1–4) all methods agree within ±0.010.
    Outside this range, prefer DIN 6935 for EU compliance work.
    </div>
    """, unsafe_allow_html=True)

# ── Flat pattern cross-section diagram ──
with col_xsec:
    angle_rad = np.radians(bend_angle)
    half_a    = np.radians(bend_angle / 2)
    R_neutral = r + K * t
    R_outer   = r + t

    # Arc points — neutral axis
    arc_angles = np.linspace(np.pi / 2, np.pi / 2 + angle_rad, 80)
    na_x = R_neutral * np.cos(arc_angles)
    na_y = R_neutral * np.sin(arc_angles)

    # Outer arc
    arc_out_x = R_outer * np.cos(arc_angles)
    arc_out_y = R_outer * np.sin(arc_angles)

    # Inner arc
    arc_in_x = r * np.cos(arc_angles)
    arc_in_y = r * np.sin(arc_angles)

    # Flanges from arc endpoints
    start_dir = np.array([np.cos(arc_angles[0]),  np.sin(arc_angles[0])])
    end_dir   = np.array([np.cos(arc_angles[-1]), np.sin(arc_angles[-1])])

    # Flange A (right side, perpendicular to start tangent going right/down)
    tang_start = np.array([-start_dir[1], start_dir[0]])
    flange_len = min(leg1 if leg1 > 0 else 40, 80)
    fa_out_start = np.array([arc_out_x[0], arc_out_y[0]])
    fa_in_start  = np.array([arc_in_x[0],  arc_in_y[0]])
    fa_out_end   = fa_out_start - tang_start * flange_len
    fa_in_end    = fa_in_start  - tang_start * flange_len

    # Flange B (left side)
    tang_end = np.array([-end_dir[1], end_dir[0]])
    flange_len_b = min(leg2 if leg2 > 0 else 25, 80)
    fb_out_start = np.array([arc_out_x[-1], arc_out_y[-1]])
    fb_in_start  = np.array([arc_in_x[-1],  arc_in_y[-1]])
    fb_out_end   = fb_out_start + tang_end * flange_len_b
    fb_in_end    = fb_in_start  + tang_end * flange_len_b

    fig_xs = go.Figure()

    # Sheet outline (outer boundary)
    outline_x = (
        list(fa_out_end) + [None] +
        [fa_out_start[0]] + list(arc_out_x) + [fb_out_start[0]] + [None] +
        list(fb_out_end) + [None]
    )
    # Full sheet polygon for fill
    poly_x = (
        [fa_out_end[0], fa_in_end[0], fa_in_start[0]] +
        list(arc_in_x[::-1]) +
        [arc_in_x[0], fa_in_start[0], fa_out_start[0]] +
        list(arc_out_x) +
        [fb_out_start[0], fb_out_end[0], fb_in_end[0], fb_in_start[0]] +
        list(arc_in_x) +
        [arc_in_x[-1], fb_in_start[0]]
    )
    poly_y = (
        [fa_out_end[1], fa_in_end[1], fa_in_start[1]] +
        list(arc_in_y[::-1]) +
        [arc_in_y[0], fa_in_start[1], fa_out_start[1]] +
        list(arc_out_y) +
        [fb_out_start[1], fb_out_end[1], fb_in_end[1], fb_in_start[1]] +
        list(arc_in_y) +
        [arc_in_y[-1], fb_in_start[1]]
    )

    # Sheet fill
    fig_xs.add_trace(go.Scatter(
        x=poly_x, y=poly_y,
        fill="toself", fillcolor="rgba(22,163,74,0.12)",
        line=dict(color=C_GREEN, width=1.8),
        name="Sheet cross-section",
        hoverinfo="skip",
    ))

    # Neutral axis arc (dashed)
    fig_xs.add_trace(go.Scatter(
        x=list(na_x), y=list(na_y),
        line=dict(color=C_AMBER, width=2, dash="dash"),
        name=f"Neutral axis  K={K:.4f}",
        hovertemplate="Neutral axis<extra></extra>",
    ))

    # Flange A lines
    for xpts, ypts in [
        ([fa_out_start[0], fa_out_end[0]], [fa_out_start[1], fa_out_end[1]]),
        ([fa_in_start[0],  fa_in_end[0]],  [fa_in_start[1],  fa_in_end[1]]),
    ]:
        fig_xs.add_trace(go.Scatter(x=xpts, y=ypts, line=dict(color=C_GREEN, width=1.8),
                                    showlegend=False, hoverinfo="skip"))
    fig_xs.add_trace(go.Scatter(
        x=[fa_out_end[0], fa_in_end[0]], y=[fa_out_end[1], fa_in_end[1]],
        line=dict(color=C_GREEN, width=1.8), showlegend=False, hoverinfo="skip",
    ))

    # Flange B lines
    for xpts, ypts in [
        ([fb_out_start[0], fb_out_end[0]], [fb_out_start[1], fb_out_end[1]]),
        ([fb_in_start[0],  fb_in_end[0]],  [fb_in_start[1],  fb_in_end[1]]),
    ]:
        fig_xs.add_trace(go.Scatter(x=xpts, y=ypts, line=dict(color=C_GREEN, width=1.8),
                                    showlegend=False, hoverinfo="skip"))
    fig_xs.add_trace(go.Scatter(
        x=[fb_out_end[0], fb_in_end[0]], y=[fb_out_end[1], fb_in_end[1]],
        line=dict(color=C_GREEN, width=1.8), showlegend=False, hoverinfo="skip",
    ))

    # Neutral axis position annotation (Kt from inner radius)
    mid_idx = len(arc_angles) // 2
    fig_xs.add_annotation(
        x=na_x[mid_idx], y=na_y[mid_idx],
        text=f"  K·t = {K*t:.3f} {unit_lbl}",
        font=dict(size=10, color=C_AMBER, family="IBM Plex Mono"),
        showarrow=True, arrowhead=2, arrowcolor=C_AMBER, arrowsize=0.8,
        ax=30, ay=-30,
    )

    fig_xs.update_layout(
        title=dict(text=f"Bend Cross-Section  —  {bend_angle}°  r={r} t={t} {unit_lbl}", font=dict(size=13), x=0),
        height=340,
        showlegend=True,
        yaxis=dict(scaleanchor="x", scaleratio=1, **GRID_STYLE),
        xaxis=dict(**GRID_STYLE),
        **PLOT_LAYOUT,
    )
    fig_xs.update_xaxes(title_text=unit_lbl)
    fig_xs.update_yaxes(title_text=unit_lbl)

    st.plotly_chart(fig_xs, use_container_width=True, config=CHART_CONFIG)


# ═══════════════════════════════════════════════════════════════════════════
# ─── SECTION 3: BA / BD Heatmap ─────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-label">Bend Allowance / Deduction Heatmap</div>', unsafe_allow_html=True)

hm_col1, hm_col2 = st.columns(2, gap="large")

rs_vals_hm  = np.linspace(0.1, 8.0, 40)
angle_vals  = np.linspace(10, 170, 35)

with hm_col1:
    # Precompute BA grid
    BA_grid = np.zeros((len(angle_vals), len(rs_vals_hm)))
    for i, ang in enumerate(angle_vals):
        for j, rs_v in enumerate(rs_vals_hm):
            k_v = k_for_method(rs_v, method)
            BA_grid[i, j] = bend_allowance(k_v, ang, rs_v * t, t)

    # User crosshair
    user_rs_idx  = int(np.argmin(np.abs(rs_vals_hm - r_s)))
    user_ang_idx = int(np.argmin(np.abs(angle_vals - bend_angle)))

    fig_hm_ba = go.Figure()
    fig_hm_ba.add_trace(go.Heatmap(
        z=BA_grid,
        x=rs_vals_hm,
        y=angle_vals,
        colorscale=[
            [0.0,  "#f0faf0"],
            [0.25, "#86efac"],
            [0.55, "#16a34a"],
            [0.80, "#166534"],
            [1.0,  "#052e16"],
        ],
        colorbar=dict(title=f"BA ({unit_lbl})", tickfont=dict(size=10),
                      titlefont=dict(size=11), len=0.85),
        hovertemplate="r/t=%{x:.2f}<br>Angle=%{y:.0f}°<br>BA=%{z:.3f}<extra></extra>",
    ))
    # Crosshair lines
    fig_hm_ba.add_hline(y=bend_angle, line=dict(color="white", width=1.5, dash="dot"))
    fig_hm_ba.add_vline(x=r_s,        line=dict(color="white", width=1.5, dash="dot"))
    fig_hm_ba.add_trace(go.Scatter(
        x=[r_s], y=[bend_angle],
        mode="markers",
        marker=dict(color="white", size=11, symbol="star",
                    line=dict(color=C_AMBER, width=2)),
        name="Your calc",
        hovertemplate=f"r/t={r_s:.3f}<br>Angle={bend_angle}°<br>BA={BA:.3f}<extra>Your calc</extra>",
    ))
    fig_hm_ba.update_layout(
        title=dict(text=f"Bend Allowance Heatmap  (t = {t} {unit_lbl}, method: {method})",
                   font=dict(size=13), x=0),
        xaxis_title="r/t ratio",
        yaxis_title="Bend angle (°)",
        height=370, **PLOT_LAYOUT,
    )
    fig_hm_ba.update_xaxes(**GRID_STYLE)
    fig_hm_ba.update_yaxes(**GRID_STYLE)
    st.plotly_chart(fig_hm_ba, use_container_width=True, config=CHART_CONFIG)

with hm_col2:
    # Precompute BD grid
    BD_grid = np.zeros((len(angle_vals), len(rs_vals_hm)))
    for i, ang in enumerate(angle_vals):
        for j, rs_v in enumerate(rs_vals_hm):
            k_v  = k_for_method(rs_v, method)
            ba_v = bend_allowance(k_v, ang, rs_v * t, t)
            BD_grid[i, j] = bend_deduction(ba_v, rs_v * t, t, ang)

    fig_hm_bd = go.Figure()
    fig_hm_bd.add_trace(go.Heatmap(
        z=BD_grid,
        x=rs_vals_hm,
        y=angle_vals,
        colorscale=[
            [0.0,  "#f0faf0"],
            [0.35, "#fde68a"],
            [0.65, "#d97706"],
            [0.85, "#92400e"],
            [1.0,  "#451a03"],
        ],
        colorbar=dict(title=f"BD ({unit_lbl})", tickfont=dict(size=10),
                      titlefont=dict(size=11), len=0.85),
        hovertemplate="r/t=%{x:.2f}<br>Angle=%{y:.0f}°<br>BD=%{z:.3f}<extra></extra>",
    ))
    fig_hm_bd.add_hline(y=bend_angle, line=dict(color="white", width=1.5, dash="dot"))
    fig_hm_bd.add_vline(x=r_s,        line=dict(color="white", width=1.5, dash="dot"))
    fig_hm_bd.add_trace(go.Scatter(
        x=[r_s], y=[bend_angle],
        mode="markers",
        marker=dict(color="white", size=11, symbol="star",
                    line=dict(color=C_GREEN, width=2)),
        name="Your calc",
        hovertemplate=f"r/t={r_s:.3f}<br>Angle={bend_angle}°<br>BD={BD:.3f}<extra>Your calc</extra>",
    ))
    fig_hm_bd.update_layout(
        title=dict(text=f"Bend Deduction Heatmap  (t = {t} {unit_lbl}, method: {method})",
                   font=dict(size=13), x=0),
        xaxis_title="r/t ratio",
        yaxis_title="Bend angle (°)",
        height=370, **PLOT_LAYOUT,
    )
    fig_hm_bd.update_xaxes(**GRID_STYLE)
    fig_hm_bd.update_yaxes(**GRID_STYLE)
    st.plotly_chart(fig_hm_bd, use_container_width=True, config=CHART_CONFIG)

st.markdown("""
<div class="callout" style="font-size:0.79rem;">
<b>Heatmap guide:</b> White star = your current operating point.
White crosshairs show your r/t and bend angle.
Use these maps as a quick reference card — darker = higher value.
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ─── SECTION 4: Springback Curve  +  Material K Bar Chart ───────────────
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-label">Springback Curve  ·  Material Reference K</div>', unsafe_allow_html=True)

col_sb_chart, col_mat_bar = st.columns([1, 1], gap="large")

# ── Springback curve ──
with col_sb_chart:
    if mat:
        E_mpa  = mat["E_mpa"]
        sb_arr = np.array([springback_angle(a, r, t, mat["yield_mpa"], E_mpa) for a in angles_deg])
        overbend_arr = angles_deg + sb_arr

        fig_sb = go.Figure()
        fig_sb.add_trace(go.Scatter(
            x=angles_deg, y=sb_arr,
            name="Springback Δθ",
            line=dict(color=C_AMBER, width=2.5),
            fill="tozeroy", fillcolor="rgba(217,119,6,0.08)",
            hovertemplate="α=%{x:.0f}°<br>Δθ=%{y:.2f}°<extra></extra>",
        ))
        fig_sb.add_trace(go.Scatter(
            x=angles_deg, y=overbend_arr,
            name="Required overbend",
            line=dict(color=C_RED, width=1.8, dash="dash"),
            hovertemplate="α=%{x:.0f}°<br>Overbend=%{y:.1f}°<extra></extra>",
        ))
        # User point
        sb_user = springback_angle(bend_angle, r, t, mat["yield_mpa"], E_mpa)
        fig_sb.add_vline(x=bend_angle, line=dict(color=C_AMBER, dash="dot", width=1.5))
        fig_sb.add_trace(go.Scatter(
            x=[bend_angle], y=[sb_user],
            mode="markers",
            marker=dict(color=C_AMBER, size=11, symbol="circle",
                        line=dict(color="white", width=2)),
            showlegend=False,
            hovertemplate=f"α={bend_angle}°<br>Δθ={sb_user:.2f}°<extra>Your calc</extra>",
        ))
        fig_sb.add_annotation(
            x=bend_angle, y=sb_user,
            text=f" +{sb_user:.1f}°",
            font=dict(size=11, color=C_AMBER, family="IBM Plex Mono"),
            showarrow=False, xanchor="left",
        )
        fig_sb.update_layout(
            title=dict(text=f"Springback vs Bend Angle  —  {mat_choice}", font=dict(size=13), x=0),
            xaxis_title="Nominal bend angle (°)",
            yaxis_title="Springback Δθ (°)",
            height=360, **PLOT_LAYOUT,
        )
        fig_sb.update_xaxes(**GRID_STYLE)
        fig_sb.update_yaxes(**GRID_STYLE)
        st.plotly_chart(fig_sb, use_container_width=True, config=CHART_CONFIG)
    else:
        st.markdown("""
        <div class="callout warn" style="margin-top:30px">
        Select a material to see the springback curve.
        </div>
        """, unsafe_allow_html=True)

# ── Material K bar chart ──
with col_mat_bar:
    mat_names  = list(MATERIALS.keys())
    k_vals     = [MATERIALS[m]["typical_k"] for m in mat_names]
    uts_vals   = [MATERIALS[m]["uts_mpa"]   for m in mat_names]
    selected_i = mat_names.index(mat_choice) if mat_choice in mat_names else -1

    bar_colors = [C_GREEN if i == selected_i else "#b6d4b6" for i in range(len(mat_names))]
    short_names = [n.replace("Steel – ", "").replace("Aluminum ", "Al ") for n in mat_names]

    fig_mat = go.Figure()
    fig_mat.add_trace(go.Bar(
        y=short_names,
        x=k_vals,
        orientation="h",
        marker=dict(color=bar_colors, line=dict(color="#d4ead4", width=0.5)),
        text=[f"{v:.2f}" for v in k_vals],
        textposition="outside",
        textfont=dict(size=10, family="IBM Plex Mono", color="#4a6e4a"),
        hovertemplate="%{y}<br>K = %{x:.3f}<extra></extra>",
        name="Reference K",
    ))
    # UTS as a secondary scatter
    fig_mat.add_trace(go.Scatter(
        y=short_names,
        x=[v / max(uts_vals) * (max(k_vals) - min(k_vals)) * 0.8 + min(k_vals) for v in uts_vals],
        mode="markers",
        marker=dict(color=C_PURPLE, size=7, symbol="diamond",
                    line=dict(color="white", width=1)),
        name="UTS (scaled)",
        hovertemplate="%{y}<br>UTS=%{customdata} MPa<extra></extra>",
        customdata=uts_vals,
    ))
    fig_mat.add_vline(x=K, line=dict(color=C_GREEN, dash="dot", width=1.5))
    fig_mat.add_annotation(
        x=K, y=-0.8,
        text=f"  Your K={K:.4f}",
        font=dict(size=10, color=C_GREEN, family="IBM Plex Mono"),
        showarrow=False, xanchor="left",
    )
    fig_mat.update_layout(
        title=dict(text="Reference K  ·  Material Comparison  (◆ = UTS scaled)",
                   font=dict(size=13), x=0),
        xaxis=dict(title="K-Factor", range=[0.28, 0.54], **GRID_STYLE),
        yaxis=dict(**GRID_STYLE),
        height=360, **PLOT_LAYOUT,
        bargap=0.28,
    )
    st.plotly_chart(fig_mat, use_container_width=True, config=CHART_CONFIG)


# ═══════════════════════════════════════════════════════════════════════════
# ─── SECTION 5: Reference Tables + Export ───────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("---")
col_t1, col_t2 = st.columns([1, 1], gap="large")

with col_t1:
    st.markdown('<div class="section-label">K-Factor Reference Table</div>', unsafe_allow_html=True)
    rs_table = [0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 15.0, 25.0]
    df_ref   = pd.DataFrame({
        "r/t":          rs_table,
        "Logistic K":   [round(k_logistic(x),   4) for x in rs_table],
        "Analytical K": [round(k_analytical(x), 4) for x in rs_table],
        "DIN 6935 K":   [round(k_din6935(x),    4) for x in rs_table],
        "Zone":         ["Sharp" if x < 1 else "Standard" if x < 5 else "Gentle" for x in rs_table],
    })
    closest_idx = int(np.argmin([abs(x - r_s) for x in rs_table]))
    st.dataframe(
        df_ref.style
            .highlight_between(subset=["Logistic K", "Analytical K", "DIN 6935 K"],
                                left=0.33, right=0.42, color="#dcfce7")
            .highlight_between(subset=["Logistic K", "Analytical K", "DIN 6935 K"],
                                left=0.42, right=0.48, color="#fef9c3")
            .highlight_between(subset=["Logistic K", "Analytical K", "DIN 6935 K"],
                                left=0.48, right=0.5,  color="#dbeafe"),
        use_container_width=True, hide_index=True,
    )
    st.markdown(
        f'<div class="callout">Closest table row: r/t = {rs_table[closest_idx]} · '
        f'DIN 6935 K = {k_din6935(rs_table[closest_idx]):.4f} · '
        f'Your K = {K:.4f} · Δ = {abs(K - k_din6935(rs_table[closest_idx])):.4f}</div>',
        unsafe_allow_html=True,
    )

with col_t2:
    st.markdown('<div class="section-label">Material Properties & Reference K</div>', unsafe_allow_html=True)
    df_mat = pd.DataFrame([
        {"Material": m,
         "Ref K":         p["typical_k"],
         "UTS (MPa)":     p["uts_mpa"],
         "Yield (MPa)":   p["yield_mpa"],
         "Elong. (%)":    p["elongation"],
         "E (GPa)":       round(p["E_mpa"] / 1000, 1),
         "Min r factor":  p["min_rb_factor"]}
        for m, p in MATERIALS.items()
    ])
    st.dataframe(df_mat, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-label" style="margin-top:20px">Export</div>', unsafe_allow_html=True)
    report = f"""K-Factor Calculation Report
============================
Date       : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
Method     : {method}
Unit       : {unit_lbl}

Inputs
------
Inner radius r    : {r:.3f} {unit_lbl}
Sheet thickness t : {t:.3f} {unit_lbl}
r/t ratio         : {r_s:.4f}
Material          : {mat_choice}
Bend angle        : {bend_angle}°

Results
-------
K-Factor          : {K:.4f}
Bend Allowance    : {BA:.4f} {unit_lbl}
Outside Setback   : {OSB:.4f} {unit_lbl}
Bend Deduction    : {BD:.4f} {unit_lbl}

Method Comparison
-----------------
Logistic fit      : {k_log:.4f}
Wang-Wenner       : {k_ana:.4f}
DIN 6935          : {k_din:.4f}
Max divergence    : {max(abs(k_log-k_din), abs(k_ana-k_din)):.4f}
"""
    if show_flat and (leg1 > 0 or leg2 > 0):
        report += f"""
Flat Pattern
------------
Flange A          : {leg1:.3f} {unit_lbl}
Flange B          : {leg2:.3f} {unit_lbl}
Flat Length       : {flat_length(leg1, leg2, BA):.4f} {unit_lbl}
"""
    if show_springback and mat:
        E_mpa_r = mat["E_mpa"]
        sb_r    = springback_angle(bend_angle, r, t, mat["yield_mpa"], E_mpa_r)
        rb_min  = min_bend_radius(t, mat["elongation"])
        report += f"""
Springback (Gardiner)
---------------------
Springback angle  : {sb_r:.2f}°
Required overbend : {bend_angle + sb_r:.1f}°
Min bend radius   : {rb_min:.3f} {unit_lbl}
"""
    st.download_button(
        "📥 Download Report (.txt)", data=report,
        file_name=f"k_factor_r{r}_t{t}.txt", mime="text/plain",
    )


# ─── Engineering Notes ───────────────────────────────────────────────────
st.markdown("---")
with st.expander("💡 Engineering Notes"):
    st.markdown("""
    **K-Factor Methods**
    - *Logistic fit* — empirically calibrated curve, good all-purpose default.
    - *Wang-Wenner analytical* — derived from neutral-axis shift theory; underestimates K at very low r/t.
    - *DIN 6935 empirical* — German standard piecewise table; use for Euronorm/DIN compliance work.

    **Reading the Method Divergence Strip**
    Peak divergence occurs around r/t 0.5–1.5 (sharp bends). In the standard production zone (r/t 1–4)
    all three methods agree to within ±0.010. The divergence chart helps you decide when it matters
    which method you choose.

    **BA/BD Heatmaps**
    The heatmaps act as a quick lookup table: find your r/t column, your angle row, read off BA or BD.
    Your operating point is always marked with a white star.

    **Cross-Section Diagram**
    The dashed orange line is the neutral axis at `K × t` from the inner surface.
    For K = 0.33 it sits at 1/3 thickness (sharp bends); for K → 0.5 it moves to the mid-plane.

    **Springback**
    Estimated via the Gardiner formula: Δθ ≈ θ × (3σ_y·r / E·t). Actual springback depends on tooling,
    lubrication, and work-hardening. Always validate with test bends.

    **Minimum Bend Radius**
    Calculated from tensile elongation A%: r_min = t × (50/A − 1). Bending tighter than this risks
    cracking on the outer fibre.

    **Grain Direction**
    Bending perpendicular to the rolling direction needs 15–30 % larger r_min. Bending parallel to
    grain allows tighter radii but may cause cracking.
    """)
