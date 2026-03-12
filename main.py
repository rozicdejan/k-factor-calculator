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

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #f8faf8;
    color: #1a2e1a;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f0f5f0; }
::-webkit-scrollbar-thumb { background: #b6d4b6; border-radius: 3px; }

/* ── Header ── */
.app-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 28px 0 16px;
    border-bottom: 2px solid #d4ead4;
    margin-bottom: 28px;
}
.header-icon {
    width: 48px; height: 48px;
    background: #16a34a;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 16px rgba(22,163,74,0.22);
    flex-shrink: 0;
}
.header-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: #111d11;
    line-height: 1.15;
    margin: 0;
}
.header-sub {
    font-size: 0.75rem;
    color: #6b9e6b;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.09em;
    margin-top: 3px;
}

/* ── Section labels ── */
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    color: #16a34a;
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* ── Cards ── */
.card {
    background: #ffffff;
    border: 1px solid #d4ead4;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(22,163,74,0.06);
}
.card-green {
    background: #f0faf0;
    border: 1px solid #86c986;
}

/* ── KPI tiles ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 20px 0;
}
.kpi-tile {
    background: #ffffff;
    border: 1px solid #d4ead4;
    border-radius: 12px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(22,163,74,0.07);
}
.kpi-tile::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #16a34a, #4ade80);
    border-radius: 12px 12px 0 0;
}
.kpi-tile.highlight { border-color: #16a34a; box-shadow: 0 2px 12px rgba(22,163,74,0.15); }
.kpi-tile.highlight::before { background: #16a34a; }
.kpi-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.63rem;
    color: #6b9e6b;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: #111d11;
    line-height: 1;
}
.kpi-value.green { color: #16a34a; }
.kpi-unit {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #9ab89a;
    margin-top: 5px;
}

/* ── Info callout ── */
.callout {
    background: #f0faf0;
    border: 1px solid #bbdcbb;
    border-left: 4px solid #16a34a;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 10px 0;
    font-size: 0.83rem;
    color: #2d4a2d;
    line-height: 1.6;
}
.callout.warn {
    background: #fffbeb;
    border-color: #fde68a;
    border-left-color: #d97706;
    color: #7c5700;
}
.callout.success {
    background: #f0fdf4;
    border-color: #bbf7d0;
    border-left-color: #16a34a;
    color: #14532d;
}

/* ── Formula display ── */
.formula {
    background: #f4faf4;
    border: 1px solid #d4ead4;
    border-radius: 8px;
    padding: 14px 18px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: #166534;
    margin: 8px 0;
    line-height: 1.9;
}

/* ── Status badge ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 99px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.67rem;
    font-weight: 500;
    letter-spacing: 0.04em;
}
.badge-soft  { background: #dbeafe; color: #1d4ed8; }
.badge-med   { background: #dcfce7; color: #15803d; }
.badge-hard  { background: #fee2e2; color: #b91c1c; }
.badge-good  { background: #dcfce7; color: #15803d; }
.badge-warn  { background: #fef9c3; color: #a16207; }
.badge-user  { background: #dcfce7; color: #166534; }

/* ── Streamlit widget overrides ── */
div[data-testid="stNumberInput"] > div > div > input,
div[data-testid="stSelectbox"] > div > div {
    background-color: #ffffff !important;
    border-color: #d4ead4 !important;
    color: #1a2e1a !important;
    border-radius: 8px !important;
}
div[data-testid="stNumberInput"] > div > div > input:focus {
    border-color: #16a34a !important;
    box-shadow: 0 0 0 2px rgba(22,163,74,0.18) !important;
}
.stCheckbox > label { color: #2d4a2d !important; font-size: 0.88rem !important; }
.stButton > button {
    background: #16a34a !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #15803d !important; }
.stDownloadButton > button {
    background: #f0faf0 !important;
    color: #16a34a !important;
    border: 1px solid #d4ead4 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
div[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #d4ead4 !important;
    border-radius: 10px !important;
}
div[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #d4ead4;
    border-radius: 10px;
    padding: 14px 16px;
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
    "Aluminum 1100-O":      {"typical_k": 0.33, "uts_mpa": 90,  "yield_mpa": 35,  "elongation": 35, "min_rb_factor": 0.0},
    "Aluminum 5052-H32":    {"typical_k": 0.34, "uts_mpa": 228, "yield_mpa": 193, "elongation": 12, "min_rb_factor": 1.0},
    "Aluminum 6061-T6":     {"typical_k": 0.35, "uts_mpa": 310, "yield_mpa": 276, "elongation": 8,  "min_rb_factor": 1.5},
    "Steel – Mild (1020)":  {"typical_k": 0.42, "uts_mpa": 380, "yield_mpa": 210, "elongation": 25, "min_rb_factor": 0.5},
    "Steel – HSLA 350":     {"typical_k": 0.44, "uts_mpa": 450, "yield_mpa": 350, "elongation": 20, "min_rb_factor": 1.5},
    "Steel – SS 304":       {"typical_k": 0.45, "uts_mpa": 515, "yield_mpa": 205, "elongation": 40, "min_rb_factor": 1.0},
    "Steel – SS 316":       {"typical_k": 0.46, "uts_mpa": 485, "yield_mpa": 170, "elongation": 40, "min_rb_factor": 1.0},
    "Steel – Spring":       {"typical_k": 0.48, "uts_mpa": 1200,"yield_mpa": 1000,"elongation": 5,  "min_rb_factor": 3.0},
    "Copper (C110)":        {"typical_k": 0.35, "uts_mpa": 220, "yield_mpa": 70,  "elongation": 40, "min_rb_factor": 0.0},
    "Brass C260":           {"typical_k": 0.38, "uts_mpa": 340, "yield_mpa": 103, "elongation": 43, "min_rb_factor": 0.5},
    "Titanium Gr2":         {"typical_k": 0.45, "uts_mpa": 345, "yield_mpa": 276, "elongation": 20, "min_rb_factor": 2.5},
}

# ─── Math Engine ─────────────────────────────────────────────────────────

@st.cache_data
def k_logistic(r_s: float) -> float:
    """Logistic fit (original formula, validated against DIN 6935)."""
    a, b, c, d = 0.277833218, 1.056058295, 0.608320238, 0.502506534
    return d + (a - d) / (1 + (r_s / c) ** b)

@st.cache_data
def k_analytical(r_s: float) -> float:
    """
    Semi-analytical model based on Hallquist / Wang-Wenner approach.
    K = ln(1 + 1/(2*r_s+1)) / ln(1 + 1/r_s)  (simplified neutral-axis shift)
    Blends to 0.5 for large r/s, approaches 1/3 for very tight bends.
    """
    if r_s <= 0:
        return 0.33
    return np.log(1 + 1 / (2 * r_s + 1)) / np.log(1 + 1 / r_s)

@st.cache_data
def k_din6935(r_s: float) -> float:
    """
    Piecewise empirical fit based on DIN 6935 / Trumpf reference data.
    """
    if r_s < 0.65:
        return 0.33
    elif r_s < 1.0:
        return 0.33 + 0.125 * (r_s - 0.65) / 0.35
    elif r_s < 3.0:
        return 0.4575 + 0.0325 * (r_s - 1.0) / 2.0
    else:
        return min(0.5, 0.49 + 0.01 * (r_s - 3.0) / 7.0)

def bend_allowance(k: float, angle_deg: float, r: float, t: float) -> float:
    return np.radians(angle_deg) * (r + k * t)

def outside_setback(angle_deg: float, r: float, t: float) -> float:
    return np.tan(np.radians(angle_deg / 2)) * (r + t)

def bend_deduction(ba: float, r: float, t: float, angle_deg: float) -> float:
    return 2 * outside_setback(angle_deg, r, t) - ba

def springback_angle(angle_deg: float, r: float, t: float, yield_mpa: float, E_mpa: float = 200_000) -> float:
    """
    Simplified springback estimate using elastic recovery:
    Δθ = θ_bend × (3 × σ_y × r / (E × t)) — Gardiner formula
    Returns the required overbend angle.
    """
    ratio = 3 * yield_mpa * r / (E_mpa * t)
    delta = angle_deg * ratio
    return delta  # degrees to overbend

def min_bend_radius(t: float, elongation_pct: float) -> float:
    """
    Minimum inside bend radius from tensile elongation:
    r_min = t × (50/A - 1)  where A = elongation %
    """
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

    unit = st.selectbox("Unit system", ["mm", "inches"], label_visibility="visible")
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
    method = st.radio("Calculation method", ["Logistic fit", "Analytical (Wang-Wenner)", "DIN 6935 empirical"], index=0)

    st.markdown('<div class="section-label" style="margin-top:20px">Flat Pattern</div>', unsafe_allow_html=True)
    show_flat = st.checkbox("Flat pattern development", value=True)
    if show_flat:
        leg1 = st.number_input(f"Flange A ({unit_lbl})", min_value=0.0, value=50.0, step=1.0, format="%.1f")
        leg2 = st.number_input(f"Flange B ({unit_lbl})", min_value=0.0, value=30.0, step=1.0, format="%.1f")

    show_springback = st.checkbox("Springback estimation", value=bool(mat))

# ─── Calculations ────────────────────────────────────────────────────────
r_s = r / t

if method == "Logistic fit":
    K = k_logistic(r_s)
elif method == "Analytical (Wang-Wenner)":
    K = k_analytical(r_s)
else:
    K = k_din6935(r_s)

BA  = bend_allowance(K, bend_angle, r, t)
BD  = bend_deduction(BA, r, t, bend_angle)
OSB = outside_setback(bend_angle, r, t)

# ─── Results Panel ───────────────────────────────────────────────────────
with col_res:
    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)

    # KPI tiles
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

    # Formula trace
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

    # Flat pattern
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

    # Springback
    if show_springback and mat:
        E_mpa = 200_000 if "Steel" in mat_choice else (69_000 if "Aluminum" in mat_choice else (110_000 if "Copper" in mat_choice or "Brass" in mat_choice else 110_000))
        sb = springback_angle(bend_angle, r, t, mat["yield_mpa"], E_mpa)
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
            rb_ok = r >= rb_min
            rb_color = "#16a34a" if rb_ok else "#dc2626"
            rb_icon  = "✓" if rb_ok else "✗"
            st.markdown(f"""
            <div class="card">
              <div class="section-label">Min Bend Radius</div>
              <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.6rem;font-weight:700;color:{rb_color};">{rb_icon} {rb_min:.2f} {unit_lbl}</div>
              <div style="font-size:0.78rem;color:#6b9e6b;margin-top:4px;font-family:'IBM Plex Mono',monospace;">Your r={r:.2f} — {'OK' if rb_ok else 'RISK OF CRACKING'}</div>
            </div>
            """, unsafe_allow_html=True)

    # Method comparison
    k_log  = k_logistic(r_s)
    k_ana  = k_analytical(r_s)
    k_din  = k_din6935(r_s)

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
    method_tile(c1, "Logistic fit",    k_log, method == "Logistic fit")
    method_tile(c2, "Wang-Wenner",     k_ana, method == "Analytical (Wang-Wenner)")
    method_tile(c3, "DIN 6935",        k_din, method == "DIN 6935 empirical")

# ─── Charts ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-label">K-Factor Curve Analysis</div>', unsafe_allow_html=True)

rs_range = np.linspace(0.05, 25, 400)
k_log_arr = np.array([k_logistic(x) for x in rs_range])
k_ana_arr = np.array([k_analytical(x) for x in rs_range])
k_din_arr = np.array([k_din6935(x) for x in rs_range])

fig = make_subplots(rows=1, cols=2,
                    subplot_titles=["K-Factor vs r/t (All Methods)", "Bend Allowance vs Bend Angle"],
                    horizontal_spacing=0.1)

# Left: K curves
for arr, name, color, dash in [
    (k_log_arr, "Logistic",    "#16a34a", "solid"),
    (k_ana_arr, "Wang-Wenner", "#7c3aed", "dash"),
    (k_din_arr, "DIN 6935",    "#0891b2", "dot"),
]:
    fig.add_trace(go.Scatter(x=rs_range, y=arr, name=name,
                             line=dict(color=color, width=2, dash=dash),
                             hovertemplate="r/t=%{x:.2f}<br>K=%{y:.4f}<extra></extra>"),
                  row=1, col=1)

# User point
fig.add_trace(go.Scatter(x=[r_s], y=[K], name="Your calc",
                         mode="markers",
                         marker=dict(color="#16a34a", size=12, symbol="star",
                                     line=dict(color="white", width=2)),
                         hovertemplate=f"r/t={r_s:.3f}<br>K={K:.4f}<extra>Your calc</extra>"),
              row=1, col=1)

# Ref line 0.5
fig.add_hline(y=0.5, line=dict(color="#9ab89a", dash="dot", width=1), row=1, col=1)

# Right: BA vs angle
angles = np.linspace(1, 180, 360)
ba_arr = np.array([bend_allowance(K, a, r, t) for a in angles])
fig.add_trace(go.Scatter(x=angles, y=ba_arr, name="Bend Allowance",
                         line=dict(color="#16a34a", width=2),
                         fill="tozeroy", fillcolor="rgba(22,163,74,0.08)",
                         hovertemplate="Angle=%{x}°<br>BA=%{y:.3f}<extra></extra>",
                         showlegend=False),
              row=1, col=2)
fig.add_vline(x=bend_angle, line=dict(color="#16a34a", dash="dot", width=1.5), row=1, col=2)
fig.add_trace(go.Scatter(x=[bend_angle], y=[BA], name="Current angle",
                         mode="markers",
                         marker=dict(color="#16a34a", size=10, symbol="circle",
                                     line=dict(color="white", width=2)),
                         showlegend=False,
                         hovertemplate=f"{bend_angle}°<br>BA={BA:.3f}<extra></extra>"),
              row=1, col=2)

fig.update_layout(
    height=360,
    paper_bgcolor="#f8faf8",
    plot_bgcolor="#ffffff",
    font=dict(family="Plus Jakarta Sans", color="#4a6e4a", size=12),
    legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor="#d4ead4", borderwidth=1),
    margin=dict(l=10, r=10, t=40, b=10),
)
for ax in ["xaxis", "xaxis2", "yaxis", "yaxis2"]:
    fig.update_layout(**{ax: dict(gridcolor="#e8f5e8", zerolinecolor="#d4ead4", linecolor="#d4ead4")})

fig.update_xaxes(title_text="r/t ratio", row=1, col=1)
fig.update_yaxes(title_text="K-Factor", row=1, col=1, range=[0.28, 0.52])
fig.update_xaxes(title_text="Bend angle (°)", row=1, col=2)
fig.update_yaxes(title_text=f"Bend Allowance ({unit_lbl})", row=1, col=2)
fig.update_annotations(font=dict(color="#4a6e4a", size=12))

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ─── Reference + Material Table ─────────────────────────────────────────
st.markdown("---")
col_t1, col_t2 = st.columns([1, 1], gap="large")

with col_t1:
    st.markdown('<div class="section-label">K-Factor Reference Table</div>', unsafe_allow_html=True)

    rs_vals = [0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 15.0, 25.0]
    df_ref = pd.DataFrame({
        "r/t":         rs_vals,
        "Logistic K":  [round(k_logistic(x), 4) for x in rs_vals],
        "Analytical K":[round(k_analytical(x), 4) for x in rs_vals],
        "DIN 6935 K":  [round(k_din6935(x), 4) for x in rs_vals],
        "Zone":        ["Sharp" if x < 1 else "Standard" if x < 5 else "Gentle" for x in rs_vals],
    })

    # Highlight closest row
    closest_idx = int(np.argmin([abs(x - r_s) for x in rs_vals]))
    st.dataframe(
        df_ref.style
            .highlight_between(subset=["Logistic K","Analytical K","DIN 6935 K"],
                                left=0.33, right=0.42, color="#dcfce7")
            .highlight_between(subset=["Logistic K","Analytical K","DIN 6935 K"],
                                left=0.42, right=0.48, color="#fef9c3")
            .highlight_between(subset=["Logistic K","Analytical K","DIN 6935 K"],
                                left=0.48, right=0.5,  color="#dbeafe"),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown(f'<div class="callout">Closest table row: r/t = {rs_vals[closest_idx]} · DIN 6935 K = {k_din6935(rs_vals[closest_idx]):.4f} · Your K = {K:.4f} · Δ = {abs(K - k_din6935(rs_vals[closest_idx])):.4f}</div>', unsafe_allow_html=True)

with col_t2:
    st.markdown('<div class="section-label">Material Properties & Reference K</div>', unsafe_allow_html=True)

    df_mat = pd.DataFrame([
        {"Material": m,
         "Ref K": p["typical_k"],
         "UTS (MPa)": p["uts_mpa"],
         "Yield (MPa)": p["yield_mpa"],
         "Elong. (%)": p["elongation"],
         "Min r factor": p["min_rb_factor"]}
        for m, p in MATERIALS.items()
    ])
    st.dataframe(df_mat, use_container_width=True, hide_index=True)

    # ── Export ──
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
"""
    if show_flat:
        report += f"""
Flat Pattern
------------
Flange A          : {leg1:.3f} {unit_lbl}
Flange B          : {leg2:.3f} {unit_lbl}
Flat Length       : {flat_length(leg1, leg2, BA):.4f} {unit_lbl}
"""
    if show_springback and mat:
        report += f"""
Springback (Gardiner)
---------------------
Springback angle  : {sb:.2f}°
Required overbend : {overbend:.1f}°
Min bend radius   : {rb_min:.3f} {unit_lbl}
"""
    st.download_button("📥 Download Report (.txt)", data=report,
                        file_name=f"k_factor_r{r}_t{t}.txt", mime="text/plain")

# ─── Tips ────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("💡 Engineering Notes"):
    st.markdown("""
    **K-Factor Methods**  
    - *Logistic fit* — empirically calibrated curve, good all-purpose default.  
    - *Wang-Wenner analytical* — derived from neutral-axis shift theory; underestimates K at very low r/t.  
    - *DIN 6935 empirical* — German standard piecewise table; use for Euronorm/DIN compliance work.

    **Springback**  
    Estimated via the Gardiner formula: Δθ ≈ θ × (3σ_y·r / E·t). Actual springback depends on tooling, lubrication, and work-hardening. Always validate with test bends.

    **Minimum Bend Radius**  
    Calculated from tensile elongation A%: r_min = t × (50/A − 1). Bending tighter than this risks cracking on the outer fibre.

    **Grain Direction**  
    Bending perpendicular to the rolling direction needs 15–30 % larger r_min. Bending parallel to grain allows tighter radii but may cause cracking.
    """)
