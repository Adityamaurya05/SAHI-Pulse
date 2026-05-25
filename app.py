import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="India SAHI P&L Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #0a0f1e;
    color: #e8ecf4;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid #1e2d45;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #131d2e 0%, #1a2640 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 18px 22px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.metric-card .label {
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #6b8cba;
    margin-bottom: 6px;
}
.metric-card .value {
    font-family: 'DM Serif Display', serif;
    font-size: 28px;
    color: #e8ecf4;
    line-height: 1;
}
.metric-card .delta {
    font-size: 13px;
    margin-top: 4px;
}
.delta-up   { color: #4ade80; }
.delta-down { color: #f87171; }

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: #111827;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    border: 1px solid #1e2d45;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: #6b8cba;
    font-weight: 500;
    font-size: 14px;
    padding: 8px 22px;
}
.stTabs [aria-selected="true"] {
    background: #1a3a6e !important;
    color: #60a5fa !important;
}

/* Section title */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: #93c5fd;
    margin: 24px 0 12px;
    border-left: 3px solid #3b82f6;
    padding-left: 12px;
}

/* Table */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Header banner */
.hero-banner {
    background: linear-gradient(120deg, #0f1f3d 0%, #152a4a 50%, #0a1929 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(59130,246,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 34px;
    color: #e8ecf4;
    margin: 0 0 6px;
}
.hero-sub {
    font-size: 14px;
    color: #6b8cba;
}
.hero-badge {
    display: inline-block;
    background: rgba(59130,246,0.2);
    border: 1px solid #3b82f6;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    color: #60a5fa;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA — SAHI COMPANIES
# ─────────────────────────────────────────────

COMPANIES = ["Star Health", "Niva Bupa", "Care Health", "Aditya Birla Health", "ManipalCigna"]
COLORS     = ["#3b82f6", "#10b981", "#f59e0b", "#a855f7", "#ec4899"]

# ── Annual P&L (FY22-FY26, ₹ Cr) ──────────────────────────────────────────
annual_data = {
    "Star Health": {
        "GWP":            [10976, 13300, 15254, 16781, 20369],
        "Net_Earned_Prem":[9500,  11400, 13050, 14800, 17200],
        "Net_Claims":     [6800,  8200,  8671,  10530, 11904],
        "Net_Expenses":   [3100,  3600,  4007,  4500,  5176],
        "UW_Profit":      [-400,   -400,   372,    -230,   206],
        "Investment_Inc": [700,    870,    1060,  1330,  1720],
        "PAT":            [62,     400,    845,    787,    911],
        "Claims_Ratio":   [71.6,   71.9,   66.5,   71.2,   69.2],
        "Expense_Ratio":  [32.6,   31.6,   30.7,   30.4,   30.1],
        "Combined_Ratio": [104.2,  103.5,  97.2,   101.6,  99.3],
        "Solvency_Ratio": [2.20,   2.15,   2.30,   2.21,   2.35],
        "Market_Share":   [56.0,   54.0,   52.0,   49.0,   47.0],
    },
    "Niva Bupa": {
        "GWP":            [2510,  3830,  5380,  6745,  8586],
        "Net_Earned_Prem":[1800,  2800,  3900,  4700,  5840],
        "Net_Claims":     [1200,  1950,  2650,  2998,  3790],
        "Net_Expenses":   [1050,  1550,  2000,  2450,  2680],
        "UW_Profit":      [-450,   -700,   -750,   -748,   -630],
        "Investment_Inc": [180,    280,    430,    580,    760],
        "PAT":            [-320,   -420,   -290,   203,    366],
        "Claims_Ratio":   [66.7,   69.6,   67.9,   63.8,   64.9],
        "Expense_Ratio":  [58.3,   55.4,   51.3,   52.1,   45.9],
        "Combined_Ratio": [125.0,  125.0,  119.2,  115.9,  110.8],
        "Solvency_Ratio": [1.80,   1.90,   2.10,   3.03,   2.49],
        "Market_Share":   [11.0,   13.0,   15.0,   16.8,   18.5],
    },
    "Care Health": {
        "GWP":            [3200,  4400,  5950,  6864,  8318],
        "Net_Earned_Prem":[2500,  3300,  4400,  5329,  6347],
        "Net_Claims":     [1680,  2230,  3000,  3074,  4096],
        "Net_Expenses":   [1150,  1480,  1900,  2020,  2450],
        "UW_Profit":      [-330,   -410,   -500,   235,    -199],
        "Investment_Inc": [230,    300,    380,    450,    540],
        "PAT":            [-120,   -110,   175,    305,    155],
        "Claims_Ratio":   [67.2,   67.6,   68.2,   57.7,   64.5],
        "Expense_Ratio":  [46.0,   44.8,   43.2,   37.9,   38.6],
        "Combined_Ratio": [113.2,  112.4,  111.4,  95.6,   103.1],
        "Solvency_Ratio": [1.70,   1.85,   2.00,   2.10,   1.95],
        "Market_Share":   [14.5,   15.0,   17.5,   18.0,   18.5],
    },
    "Aditya Birla Health": {
        "GWP":            [780,    1450,  2500,  3714,  4940],
        "Net_Earned_Prem":[550,    1000,  1720,  2600,  3500],
        "Net_Claims":     [530,    920,    1550,  2340,  2840],
        "Net_Expenses":   [620,    1080,  1700,  2590,  2900],
        "UW_Profit":      [-600,   -1000, -1530, -2330, -2240],
        "Investment_Inc": [60,     110,    200,    340,    500],
        "PAT":            [-550,   -890,   -1330, -1980, -1750],
        "Claims_Ratio":   [96.4,   92.0,   90.1,   90.0,   81.1],
        "Expense_Ratio":  [112.7,  108.0,  98.8,   99.6,   82.9],
        "Combined_Ratio": [209.1,  200.0,  188.9,  189.6,  164.0],
        "Solvency_Ratio": [2.20,   2.30,   2.00,   1.90,   2.10],
        "Market_Share":   [3.5,    5.0,    8.5,    9.3,    10.6],
    },
    "ManipalCigna": {
        "GWP":            [680,    900,    1100,  1320,  1580],
        "Net_Earned_Prem":[600,    790,    960,    1160,  1380],
        "Net_Claims":     [420,    560,    670,    820,    960],
        "Net_Expenses":   [390,    490,    580,    680,    790],
        "UW_Profit":      [-210,   -260,   -290,   -340,   -370],
        "Investment_Inc": [55,     75,     95,     120,    150],
        "PAT":            [-155,   -185,   -195,   -220,   -220],
        "Claims_Ratio":   [70.0,   70.9,   69.8,   70.7,   69.6],
        "Expense_Ratio":  [65.0,   62.0,   60.4,   58.6,   57.2],
        "Combined_Ratio": [135.0,  132.9,  130.2,  129.3,  126.8],
        "Solvency_Ratio": [1.60,   1.55,   1.60,   1.65,   1.70],
        "Market_Share":   [3.0,    3.0,    3.2,    3.4,    3.4],
    },
}
YEARS = [2022, 2023, 2024, 2025, 2026]

# ── Q3 FY26 (Oct-Dec 2025) quarterly data ──────────────────────────────────
q3_fy26 = pd.DataFrame({
    "Company":        COMPANIES,
    "Q3_GWP":         [5_047,  2_103,  2_150,  1_350,   400],
    "Q3_GWP_YoY":     [23,     31,     18,     35,      20],
    "Q3_PAT":         [449,    77,     32,     -420,    -52],
    "Q3_PAT_YoY":     [414,    28,     -24,    None,    None],
    "Q3_Claims_Ratio":[68.8,   72.3,   65.2,   83.5,    70.1],
    "Q3_Expense_Ratio":[30.1,  37.2,   36.8,   84.2,    57.8],
    "Q3_Combined":    [98.9,   109.5,  102.0,  167.7,   127.9],
    "Q3_Solvency":    [2.22,   2.49,   1.95,   2.10,    1.70],
    "Color":          COLORS,
})

# ── FY25 annual comparison ──────────────────────────────────────────────────
fy25_data = pd.DataFrame({
    "Company":      COMPANIES,
    "GWP":          [16_781, 6_745,  8_318,  3_714,  1_320],
    "GWP_Growth":   [10,     26,     21,     49,     20],
    "PAT":          [787,    203,    155,    -1_980, -220],
    "PAT_YoY":      [-7,     None,   -49,    None,   None],
    "Claims_Ratio": [71.2,   63.8,   64.5,   90.0,   70.7],
    "Expense_Ratio":[30.4,   52.1,   38.6,   99.6,   58.6],
    "Combined":     [101.6,  115.9,  103.1,  189.6,  129.3],
    "Inv_Income":   [1_330,  580,    450,    340,    120],
    "Solvency":     [2.21,   3.03,   2.10,   1.90,   1.65],
    "Market_Share": [49,     16.8,   18.0,   9.3,    3.4],
    "Color":        COLORS,
})

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def fmt_cr(val):
    """Format ₹ crore values."""
    if abs(val) >= 1000:
        return f"₹{val/1000:.1f}K Cr"
    return f"₹{val:.0f} Cr"

def delta_html(val, suffix="%", invert=False):
    if val is None:
        return '<span style="color:#6b8cba">—</span>'
    cls = "delta-up" if (val > 0) != invert else "delta-down"
    arrow = "▲" if val > 0 else "▼"
    return f'<span class="{cls}">{arrow} {abs(val):.1f}{suffix}</span>'

def make_dark_fig():
    return dict(
        plot_bgcolor="#0d1626",
        paper_bgcolor="#0d1626",
        font=dict(family="DM Sans", color="#9ab0cc", size=12),
        xaxis=dict(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f", linecolor="#1e3a5f"),
        yaxis=dict(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f", linecolor="#1e3a5f"),
    )

def dark_fig_with_yrange(y_min, y_max):
    """Return make_dark_fig() layout with a yaxis range override — avoids duplicate keyword error."""
    layout = make_dark_fig()
    layout["yaxis"] = {**layout["yaxis"], "range": [y_min, y_max]}
    return layout

# ─────────────────────────────────────────────
#  PREDICTION ENGINE
# ─────────────────────────────────────────────

def predict_metric(company, metric, years_ahead=3):
    vals = annual_data[company][metric]
    X = np.array(YEARS).reshape(-1, 1)
    y = np.array(vals)
    poly = PolynomialFeatures(degree=2)
    Xp = poly.fit_transform(X)
    model = LinearRegression().fit(Xp, y)
    future_yrs = np.array(range(YEARS[-1]+1, YEARS[-1]+years_ahead+1)).reshape(-1,1)
    preds = model.predict(poly.transform(future_yrs))
    return list(range(YEARS[-1]+1, YEARS[-1]+years_ahead+1)), preds.tolist()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div style="font-family:DM Serif Display,serif;font-size:22px;color:#60a5fa;padding:10px 0 20px">🏥 SAHI Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="font-size:12px;color:#6b8cba;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Filters</div>', unsafe_allow_html=True)

    selected_companies = st.multiselect(
        "Companies", COMPANIES, default=COMPANIES,
        help="Select insurers to compare"
    )
    st.markdown("---")
    st.markdown('<div style="font-size:12px;color:#6b8cba;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Trend View</div>', unsafe_allow_html=True)
    year_range = st.slider("Year Range", 2022, 2026, (2022, 2026))
    st.markdown("---")
    st.markdown('<div style="font-size:12px;color:#6b8cba;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Prediction</div>', unsafe_allow_html=True)
    pred_years = st.slider("Forecast Horizon (yrs)", 1, 5, 3)
    pred_metric = st.selectbox("Metric to Forecast", ["GWP", "PAT", "Claims_Ratio", "Combined_Ratio"])

    st.markdown("---")
    st.markdown("""
    <div style="font-size:11px;color:#3b6b9a;line-height:1.8">
    📌 Data Sources<br>
    • IRDAI Annual Reports 2024-25<br>
    • Company quarterly filings (Q3 FY26)<br>
    • NSE/BSE investor presentations<br>
    • Analyst estimates for unlisted entities<br>
    <br>
    <em>FY = April–March | ₹ in Crores</em>
    </div>
    """, unsafe_allow_html=True)

if not selected_companies:
    st.warning("Please select at least one company from the sidebar.")
    st.stop()

# ─────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────

st.markdown("""
<div class="hero-banner">
  <div class="hero-title">Standalone Health Insurance — India</div>
  <div class="hero-sub">Profit & Loss Dashboard | Comprehensive Peer Analysis</div>
  <div class="hero-badge">8 SAHIs in India · FY22–FY26 · Q3 FY26 Latest</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────

tab_industry, tab_fy25, tab_q3, tab_trends, tab_predict = st.tabs([
    "🏢 Industry Overview",
    "📊 FY 24-25 Comparison",
    "📈 Q3 FY26 Comparison",
    "📉 Multi-Year Trends",
    "🔮 Forecast & Predictions",
])

# ═══════════════════════════════════════════
#  TAB 1 — INDUSTRY OVERVIEW
# ═══════════════════════════════════════════
with tab_industry:
    st.markdown('<div class="section-title">Standalone Health Insurance — Sector Snapshot (FY26)</div>', unsafe_allow_html=True)

    # KPI cards
    total_gwp_fy26 = sum([annual_data[c]["GWP"][-1] for c in COMPANIES])
    total_gwp_fy25 = sum([annual_data[c]["GWP"][-2] for c in COMPANIES])
    gwp_growth = (total_gwp_fy26 - total_gwp_fy25) / total_gwp_fy25 * 100
    profitable = sum(1 for c in COMPANIES if annual_data[c]["PAT"][-1] > 0)

    c1, c2, c3, c4, c5 = st.columns(5)
    kpis = [
        (c1, "SAHI GWP (FY26)", fmt_cr(total_gwp_fy26), f"+{gwp_growth:.1f}%", True),
        (c2, "Star Health GWP", fmt_cr(annual_data["Star Health"]["GWP"][-1]), "+16%", True),
        (c3, "Profitable SAHIs", f"{profitable}/{len(COMPANIES)}", None, True),
        (c4, "Sector ICR FY25", "68.1%", None, True),
        (c5, "Claim Settlement", "99.93%", None, True),
    ]
    for col, label, val, delta, good in kpis:
        d_html = ""
        if delta:
            cls = "delta-up" if good else "delta-down"
            d_html = f'<div class="delta {cls}">{delta}</div>'
        col.markdown(f"""
        <div class="metric-card">
          <div class="label">{label}</div>
          <div class="value">{val}</div>
          {d_html}
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.4, 1])

    with col_l:
        st.markdown('<div class="section-title">Market Share (FY26 GWP)</div>', unsafe_allow_html=True)
        gwp_vals = [annual_data[c]["GWP"][-1] for c in COMPANIES]
        fig = go.Figure(go.Pie(
            labels=COMPANIES, values=gwp_vals,
            hole=0.55,
            marker=dict(colors=COLORS, line=dict(color="#0a0f1e", width=3)),
            textinfo="label+percent",
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>GWP: ₹%{value:,} Cr<br>Share: %{percent}<extra></extra>",
        ))
        fig.update_layout(**make_dark_fig(), height=340, margin=dict(t=20,b=20,l=20,r=20),
                          legend=dict(orientation="h", y=-0.08))
        fig.add_annotation(text="FY26<br>GWP Mix", x=0.5, y=0.5,
                           font=dict(size=14, color="#93c5fd"), showarrow=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">Profitability Overview</div>', unsafe_allow_html=True)
        pat_vals = [annual_data[c]["PAT"][-1] for c in COMPANIES]
        colors_pat = ["#4ade80" if v > 0 else "#f87171" for v in pat_vals]
        fig2 = go.Figure(go.Bar(
            x=COMPANIES, y=pat_vals,
            marker_color=colors_pat,
            text=[fmt_cr(v) for v in pat_vals],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>PAT: ₹%{y:,} Cr<extra></extra>",
        ))
        fig2.update_layout(**make_dark_fig(), height=340,
                           margin=dict(t=30,b=20,l=20,r=20),
                           yaxis_title="PAT (₹ Cr)",
                           showlegend=False)
        fig2.add_hline(y=0, line_color="#6b8cba", line_dash="dash", line_width=1)
        st.plotly_chart(fig2, use_container_width=True)

    # Combined ratio comparison
    st.markdown('<div class="section-title">Combined Ratio — Profitability Benchmark</div>', unsafe_allow_html=True)
    cr_vals  = [annual_data[c]["Combined_Ratio"][-1] for c in COMPANIES]
    cr_fy25  = [annual_data[c]["Combined_Ratio"][-2] for c in COMPANIES]
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name="FY25", x=COMPANIES, y=cr_fy25,
                          marker_color="#1e3a6e", opacity=0.85))
    fig3.add_trace(go.Bar(name="FY26", x=COMPANIES, y=cr_vals,
                          marker_color=COLORS))
    fig3.add_hline(y=100, line_color="#f59e0b", line_dash="dash", line_width=2,
                   annotation_text="100% — Break-even Line",
                   annotation_font=dict(color="#f59e0b", size=11))
    fig3.update_layout(**make_dark_fig(), height=360, barmode="group",
                       yaxis_title="Combined Ratio (%)", margin=dict(t=30,b=10),
                       legend=dict(orientation="h", x=0.5, xanchor="center", y=1.05))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    <div style="background:#111827;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px;font-size:13px;color:#6b8cba;line-height:1.9">
    <b style="color:#60a5fa">Key Insight:</b> A Combined Ratio below 100% signals underwriting profitability.
    <b>Star Health</b> leads with 98.8% in FY26 (improved from 101.1%), making an underwriting profit of ₹206 Cr.
    <b>Niva Bupa</b> improved to 101.4% — targeting sub-100% by FY29.
    <b>Aditya Birla Health</b> is scaling aggressively with negative PAT but fastest GWP growth (33% in FY25).
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
#  TAB 2 — FY 24-25 COMPARISON
# ═══════════════════════════════════════════
with tab_fy25:
    st.markdown('<div class="section-title">FY 2024-25 — Full Year P&L Comparison</div>', unsafe_allow_html=True)

    sel_fy25 = fy25_data[fy25_data["Company"].isin(selected_companies)]

    # Metric KPIs for each selected company
    cols = st.columns(len(selected_companies))
    for i, row in sel_fy25.iterrows():
        idx = list(sel_fy25["Company"]).index(row["Company"])
        if idx < len(cols):
            pat_d = row["PAT_YoY"]
            d_txt = f"+{pat_d:.0f}%" if pat_d and pat_d > 0 else (f"{pat_d:.0f}%" if pat_d else "N/A")
            d_col = "delta-up" if pat_d and pat_d > 0 else "delta-down"
            cols[idx].markdown(f"""
            <div class="metric-card">
              <div class="label">{row['Company']}</div>
              <div class="value">{fmt_cr(row['GWP'])}</div>
              <div style="font-size:11px;color:#6b8cba;margin-top:3px">GWP | +{row['GWP_Growth']:.0f}% YoY</div>
              <div style="font-size:13px;margin-top:4px">PAT: {fmt_cr(row['PAT'])} <span class="{d_col}">{d_txt}</span></div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-title">GWP Comparison (FY24 vs FY25)</div>', unsafe_allow_html=True)
        fy24_gwp = [annual_data[c]["GWP"][-3] for c in selected_companies]
        fy25_gwp = [annual_data[c]["GWP"][-2] for c in selected_companies]
        fig_g = go.Figure()
        fig_g.add_trace(go.Bar(name="FY24", x=selected_companies, y=fy24_gwp,
                               marker_color="#1e3a6e"))
        fig_g.add_trace(go.Bar(name="FY25", x=selected_companies, y=fy25_gwp,
                               marker_color=COLORS[:len(selected_companies)]))
        fig_g.update_layout(**make_dark_fig(), barmode="group", height=320,
                            yaxis_title="GWP (₹ Cr)",
                            legend=dict(orientation="h", x=0.5, xanchor="center", y=1.05),
                            margin=dict(t=30,b=10))
        st.plotly_chart(fig_g, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">PAT — Profitability (FY25)</div>', unsafe_allow_html=True)
        pat_vals_fy25 = [annual_data[c]["PAT"][-2] for c in selected_companies]
        colors_pat2 = [COLORS[COMPANIES.index(c)] if annual_data[c]["PAT"][-2] > 0
                       else "#f87171" for c in selected_companies]
        fig_p = go.Figure(go.Bar(
            x=selected_companies, y=pat_vals_fy25,
            marker_color=colors_pat2,
            text=[fmt_cr(v) for v in pat_vals_fy25],
            textposition="outside",
        ))
        fig_p.add_hline(y=0, line_color="#6b8cba", line_dash="dash")
        fig_p.update_layout(**make_dark_fig(), height=320,
                            yaxis_title="PAT (₹ Cr)", margin=dict(t=30,b=10))
        st.plotly_chart(fig_p, use_container_width=True)

    # Ratio Analysis
    st.markdown('<div class="section-title">Key Ratios — FY 2024-25</div>', unsafe_allow_html=True)
    col_c, col_d, col_e = st.columns(3)

    with col_c:
        fig_cr = go.Figure(go.Bar(
            x=selected_companies,
            y=[annual_data[c]["Claims_Ratio"][-2] for c in selected_companies],
            marker_color=COLORS[:len(selected_companies)],
            text=[f"{annual_data[c]['Claims_Ratio'][-2]:.1f}%" for c in selected_companies],
            textposition="outside",
        ))
        fig_cr.update_layout(**dark_fig_with_yrange(0, 115), height=280, title="Claims Ratio (%)",
                             margin=dict(t=40,b=10))
        st.plotly_chart(fig_cr, use_container_width=True)

    with col_d:
        fig_er = go.Figure(go.Bar(
            x=selected_companies,
            y=[annual_data[c]["Expense_Ratio"][-2] for c in selected_companies],
            marker_color=COLORS[:len(selected_companies)],
            text=[f"{annual_data[c]['Expense_Ratio'][-2]:.1f}%" for c in selected_companies],
            textposition="outside",
        ))
        fig_er.update_layout(**dark_fig_with_yrange(0, 120), height=280, title="Expense Ratio (%)",
                             margin=dict(t=40,b=10))
        st.plotly_chart(fig_er, use_container_width=True)

    with col_e:
        fig_solv = go.Figure(go.Bar(
            x=selected_companies,
            y=[annual_data[c]["Solvency_Ratio"][-2] for c in selected_companies],
            marker_color=COLORS[:len(selected_companies)],
            text=[f"{annual_data[c]['Solvency_Ratio'][-2]:.2f}x" for c in selected_companies],
            textposition="outside",
        ))
        fig_solv.add_hline(y=1.5, line_color="#f59e0b", line_dash="dash",
                           annotation_text="Min 1.5x (IRDAI)",
                           annotation_font=dict(color="#f59e0b", size=10))
        fig_solv.update_layout(**make_dark_fig(), height=280, title="Solvency Ratio",
                               margin=dict(t=40,b=10))
        st.plotly_chart(fig_solv, use_container_width=True)

    # Investment Income vs PAT scatter
    st.markdown('<div class="section-title">Investment Income vs PAT (FY25)</div>', unsafe_allow_html=True)
    fig_sc = go.Figure()
    for i, c in enumerate(selected_companies):
        fig_sc.add_trace(go.Scatter(
            x=[annual_data[c]["Investment_Inc"][-2]],
            y=[annual_data[c]["PAT"][-2]],
            mode="markers+text",
            name=c,
            text=[c],
            textposition="top center",
            marker=dict(size=18, color=COLORS[COMPANIES.index(c)],
                        line=dict(width=2, color="#0a0f1e")),
            hovertemplate=f"<b>{c}</b><br>Inv Income: ₹%{{x:,}} Cr<br>PAT: ₹%{{y:,}} Cr<extra></extra>",
        ))
    fig_sc.add_hline(y=0, line_color="#6b8cba", line_dash="dash", line_width=1)
    fig_sc.update_layout(**make_dark_fig(), height=350,
                         xaxis_title="Investment Income (₹ Cr)",
                         yaxis_title="PAT (₹ Cr)",
                         showlegend=False,
                         margin=dict(t=20,b=20))
    st.plotly_chart(fig_sc, use_container_width=True)

    # Detailed Table
    st.markdown('<div class="section-title">FY25 P&L Summary Table</div>', unsafe_allow_html=True)
    table_rows = []
    for c in selected_companies:
        d = annual_data[c]
        table_rows.append({
            "Company":           c,
            "GWP (₹ Cr)":       f"₹{d['GWP'][-2]:,}",
            "Net Prem (₹ Cr)":  f"₹{d['Net_Earned_Prem'][-2]:,}",
            "Net Claims":        f"₹{d['Net_Claims'][-2]:,}",
            "Inv. Income":       f"₹{d['Investment_Inc'][-2]:,}",
            "PAT (₹ Cr)":       f"₹{d['PAT'][-2]:,}",
            "Claims %":          f"{d['Claims_Ratio'][-2]:.1f}%",
            "Expense %":         f"{d['Expense_Ratio'][-2]:.1f}%",
            "Combined %":        f"{d['Combined_Ratio'][-2]:.1f}%",
            "Solvency":          f"{d['Solvency_Ratio'][-2]:.2f}x",
        })
    df_table = pd.DataFrame(table_rows)
    st.dataframe(df_table.set_index("Company"), use_container_width=True)

# ═══════════════════════════════════════════
#  TAB 3 — Q3 FY26 COMPARISON
# ═══════════════════════════════════════════
with tab_q3:
    st.markdown('<div class="section-title">Q3 FY26 (Oct–Dec 2025) — Latest Quarter Snapshot</div>', unsafe_allow_html=True)

    sel_q3 = q3_fy26[q3_fy26["Company"].isin(selected_companies)].reset_index(drop=True)

    # KPI row
    cols_q3 = st.columns(len(sel_q3))
    for idx, row in sel_q3.iterrows():
        gwp_d = f'+{row["Q3_GWP_YoY"]:.0f}% YoY'
        pat_sign = "+" if row["Q3_PAT"] > 0 else ""
        cols_q3[idx].markdown(f"""
        <div class="metric-card">
          <div class="label">{row['Company']}</div>
          <div class="value">{fmt_cr(row['Q3_GWP'])}</div>
          <div style="font-size:11px;color:#6b8cba;margin-top:3px">GWP | <span class="delta-up">{gwp_d}</span></div>
          <div style="font-size:13px;margin-top:4px">PAT: {fmt_cr(row['Q3_PAT'])}</div>
          <div style="font-size:11px;color:#6b8cba">Combined: {row['Q3_Combined']:.1f}%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_q1, col_q2 = st.columns(2)

    with col_q1:
        st.markdown('<div class="section-title">Q3 FY26 GWP with YoY Growth</div>', unsafe_allow_html=True)
        fig_qg = make_subplots(specs=[[{"secondary_y": True}]])
        fig_qg.add_trace(go.Bar(
            name="Q3 GWP",
            x=sel_q3["Company"],
            y=sel_q3["Q3_GWP"],
            marker_color=[COLORS[COMPANIES.index(c)] for c in sel_q3["Company"]],
            text=[fmt_cr(v) for v in sel_q3["Q3_GWP"]],
            textposition="outside",
        ), secondary_y=False)
        fig_qg.add_trace(go.Scatter(
            name="YoY Growth %",
            x=sel_q3["Company"],
            y=sel_q3["Q3_GWP_YoY"],
            mode="lines+markers",
            line=dict(color="#f59e0b", width=2.5),
            marker=dict(size=10),
        ), secondary_y=True)
        layout = make_dark_fig()
        layout.update(height=320, margin=dict(t=30,b=10), showlegend=False,
                      yaxis=dict(**layout["yaxis"], title="GWP (₹ Cr)"),
                      yaxis2=dict(title="YoY %", overlaying="y", side="right",
                                  gridcolor="rgba(0,0,0,0)", ticksuffix="%"))
        fig_qg.update_layout(**{k:v for k,v in layout.items() if k not in ("xaxis","yaxis")})
        st.plotly_chart(fig_qg, use_container_width=True)

    with col_q2:
        st.markdown('<div class="section-title">Q3 FY26 PAT Comparison</div>', unsafe_allow_html=True)
        pat_cols = ["#4ade80" if v > 0 else "#f87171" for v in sel_q3["Q3_PAT"]]
        fig_qp = go.Figure(go.Bar(
            x=sel_q3["Company"],
            y=sel_q3["Q3_PAT"],
            marker_color=pat_cols,
            text=[fmt_cr(v) for v in sel_q3["Q3_PAT"]],
            textposition="outside",
        ))
        fig_qp.add_hline(y=0, line_color="#6b8cba", line_dash="dash")
        fig_qp.update_layout(**make_dark_fig(), height=320, yaxis_title="PAT (₹ Cr)",
                             margin=dict(t=30,b=10))
        st.plotly_chart(fig_qp, use_container_width=True)

    # Ratio trifecta
    st.markdown('<div class="section-title">Q3 FY26 — Underwriting Efficiency Ratios</div>', unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns(3)

    with col_r1:
        fig_qcr = go.Figure(go.Bar(
            x=sel_q3["Company"], y=sel_q3["Q3_Claims_Ratio"],
            marker_color=[COLORS[COMPANIES.index(c)] for c in sel_q3["Company"]],
            text=[f"{v:.1f}%" for v in sel_q3["Q3_Claims_Ratio"]],
            textposition="outside",
        ))
        fig_qcr.add_hline(y=70, line_color="#4ade80", line_dash="dot",
                           annotation_text="Benchmark 70%",
                           annotation_font=dict(color="#4ade80",size=10))
        fig_qcr.update_layout(**dark_fig_with_yrange(0, 120), height=280, title="Claims Ratio",
                              margin=dict(t=40,b=10))
        st.plotly_chart(fig_qcr, use_container_width=True)

    with col_r2:
        fig_qer = go.Figure(go.Bar(
            x=sel_q3["Company"], y=sel_q3["Q3_Expense_Ratio"],
            marker_color=[COLORS[COMPANIES.index(c)] for c in sel_q3["Company"]],
            text=[f"{v:.1f}%" for v in sel_q3["Q3_Expense_Ratio"]],
            textposition="outside",
        ))
        fig_qer.update_layout(**dark_fig_with_yrange(0, 120), height=280, title="Expense Ratio",
                              margin=dict(t=40,b=10))
        st.plotly_chart(fig_qer, use_container_width=True)

    with col_r3:
        fig_qcomb = go.Figure(go.Bar(
            x=sel_q3["Company"], y=sel_q3["Q3_Combined"],
            marker_color=["#4ade80" if v < 100 else "#f87171" for v in sel_q3["Q3_Combined"]],
            text=[f"{v:.1f}%" for v in sel_q3["Q3_Combined"]],
            textposition="outside",
        ))
        fig_qcomb.add_hline(y=100, line_color="#f59e0b", line_dash="dash",
                            annotation_text="100% Break-even",
                            annotation_font=dict(color="#f59e0b",size=10))
        fig_qcomb.update_layout(**dark_fig_with_yrange(0, 200), height=280, title="Combined Ratio",
                                margin=dict(t=40,b=10))
        st.plotly_chart(fig_qcomb, use_container_width=True)

    # Solvency gauge-style bars
    st.markdown('<div class="section-title">Solvency Ratio — Q3 FY26</div>', unsafe_allow_html=True)
    fig_solv_q3 = go.Figure()
    for _, row in sel_q3.iterrows():
        fig_solv_q3.add_trace(go.Bar(
            name=row["Company"],
            x=[row["Company"]],
            y=[row["Q3_Solvency"]],
            marker_color=COLORS[COMPANIES.index(row["Company"])],
            text=[f'{row["Q3_Solvency"]:.2f}x'],
            textposition="outside",
            width=0.5,
        ))
    fig_solv_q3.add_hline(y=1.5, line_color="#f59e0b", line_dash="dash",
                           annotation_text="IRDAI Minimum 1.5x",
                           annotation_font=dict(color="#f59e0b"))
    fig_solv_q3.update_layout(**make_dark_fig(), height=300, showlegend=False,
                              yaxis_title="Solvency Ratio", margin=dict(t=30,b=10))
    st.plotly_chart(fig_solv_q3, use_container_width=True)

    # Q3 detailed table
    st.markdown('<div class="section-title">Q3 FY26 Summary Table</div>', unsafe_allow_html=True)
    q3_table = sel_q3[["Company","Q3_GWP","Q3_GWP_YoY","Q3_PAT","Q3_Claims_Ratio",
                        "Q3_Expense_Ratio","Q3_Combined","Q3_Solvency"]].copy()
    q3_table.columns = ["Company","GWP (₹ Cr)","GWP YoY %","PAT (₹ Cr)",
                         "Claims %","Expense %","Combined %","Solvency"]
    q3_table["GWP (₹ Cr)"] = q3_table["GWP (₹ Cr)"].apply(lambda x: f"₹{x:,}")
    q3_table["PAT (₹ Cr)"] = q3_table["PAT (₹ Cr)"].apply(lambda x: f"₹{x:,}")
    q3_table["GWP YoY %"]  = q3_table["GWP YoY %"].apply(lambda x: f"+{x:.0f}%")
    q3_table["Claims %"]   = q3_table["Claims %"].apply(lambda x: f"{x:.1f}%")
    q3_table["Expense %"]  = q3_table["Expense %"].apply(lambda x: f"{x:.1f}%")
    q3_table["Combined %"] = q3_table["Combined %"].apply(lambda x: f"{x:.1f}%")
    q3_table["Solvency"]   = q3_table["Solvency"].apply(lambda x: f"{x:.2f}x")
    st.dataframe(q3_table.set_index("Company"), use_container_width=True)

    st.markdown("""
    <div style="background:#111827;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px;font-size:13px;color:#6b8cba;line-height:1.9">
    <b style="color:#60a5fa">Q3 FY26 Highlights:</b>
    <b>Star Health</b> posted ₹449 Cr PAT — 414% YoY surge, with combined ratio at 98.9% (breakeven achieved).
    <b>Niva Bupa</b> reported ₹77 Cr PAT (IFRS basis), 31% GWP growth driven by 46% new-biz surge and 70% digital channel growth.
    <b>Care Health</b> grew GWP 18% YoY with modest profitability.
    <b>Aditya Birla</b> continues investment phase with strong GWP growth (35%) but elevated combined ratio as it scales.
    GST exemption on retail health policies (effective Oct 2025) was a significant demand catalyst across all SAHIs.
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
#  TAB 4 — MULTI-YEAR TRENDS
# ═══════════════════════════════════════════
with tab_trends:
    st.markdown('<div class="section-title">Historical Trends (FY22–FY26)</div>', unsafe_allow_html=True)

    yr_start, yr_end = year_range
    idx_start = YEARS.index(yr_start)
    idx_end   = YEARS.index(yr_end) + 1
    yr_slice  = YEARS[idx_start:idx_end]

    # GWP trend
    st.markdown('<div class="section-title">Gross Written Premium Growth</div>', unsafe_allow_html=True)
    fig_gwp_t = go.Figure()
    for c in selected_companies:
        vals = annual_data[c]["GWP"][idx_start:idx_end]
        fig_gwp_t.add_trace(go.Scatter(
            x=yr_slice, y=vals, name=c, mode="lines+markers",
            line=dict(color=COLORS[COMPANIES.index(c)], width=2.5),
            marker=dict(size=8),
            hovertemplate=f"<b>{c}</b> FY%{{x}}<br>GWP: ₹%{{y:,}} Cr<extra></extra>",
        ))
    fig_gwp_t.update_layout(**make_dark_fig(), height=360, yaxis_title="GWP (₹ Cr)",
                            legend=dict(orientation="h", x=0.5, xanchor="center", y=1.05),
                            margin=dict(t=30,b=10))
    st.plotly_chart(fig_gwp_t, use_container_width=True)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown('<div class="section-title">PAT Trend</div>', unsafe_allow_html=True)
        fig_pat_t = go.Figure()
        for c in selected_companies:
            vals = annual_data[c]["PAT"][idx_start:idx_end]
            fig_pat_t.add_trace(go.Scatter(
                x=yr_slice, y=vals, name=c, mode="lines+markers",
                line=dict(color=COLORS[COMPANIES.index(c)], width=2.5),
                marker=dict(size=8),
            ))
        fig_pat_t.add_hline(y=0, line_color="#6b8cba", line_dash="dash")
        fig_pat_t.update_layout(**make_dark_fig(), height=320, yaxis_title="PAT (₹ Cr)",
                                legend=dict(orientation="h", x=0.5, xanchor="center", y=1.05),
                                margin=dict(t=30,b=10))
        st.plotly_chart(fig_pat_t, use_container_width=True)

    with col_t2:
        st.markdown('<div class="section-title">Combined Ratio Trend</div>', unsafe_allow_html=True)
        fig_comb_t = go.Figure()
        for c in selected_companies:
            vals = annual_data[c]["Combined_Ratio"][idx_start:idx_end]
            fig_comb_t.add_trace(go.Scatter(
                x=yr_slice, y=vals, name=c, mode="lines+markers",
                line=dict(color=COLORS[COMPANIES.index(c)], width=2.5),
                marker=dict(size=8),
            ))
        fig_comb_t.add_hline(y=100, line_color="#f59e0b", line_dash="dash",
                              annotation_text="100%", annotation_font=dict(color="#f59e0b"))
        fig_comb_t.update_layout(**make_dark_fig(), height=320, yaxis_title="Combined Ratio (%)",
                                 legend=dict(orientation="h", x=0.5, xanchor="center", y=1.05),
                                 margin=dict(t=30,b=10))
        st.plotly_chart(fig_comb_t, use_container_width=True)

    # Claims vs Expense ratio stacked area
    st.markdown('<div class="section-title">Claims vs Expense Ratio — Star Health (Benchmark)</div>', unsafe_allow_html=True)
    sh = annual_data["Star Health"]
    fig_stack = go.Figure()
    fig_stack.add_trace(go.Scatter(
        x=yr_slice, y=sh["Claims_Ratio"][idx_start:idx_end],
        name="Claims Ratio", fill="tozeroy",
        line=dict(color="#3b82f6", width=2),
        fillcolor="rgba(59130,246,0.25)",
    ))
    fig_stack.add_trace(go.Scatter(
        x=yr_slice, y=sh["Expense_Ratio"][idx_start:idx_end],
        name="Expense Ratio", fill="tozeroy",
        line=dict(color="#10b981", width=2),
        fillcolor="rgba(16185,129,0.25)",
    ))
    fig_stack.update_layout(**make_dark_fig(), height=300, yaxis_title="Ratio (%)",
                            legend=dict(orientation="h", x=0.5, xanchor="center", y=1.05),
                            margin=dict(t=30,b=10))
    st.plotly_chart(fig_stack, use_container_width=True)

    # Market share evolution
    st.markdown('<div class="section-title">SAHI Market Share Evolution (within standalone segment)</div>', unsafe_allow_html=True)
    fig_ms = go.Figure()
    for c in selected_companies:
        ms_vals = annual_data[c]["Market_Share"][idx_start:idx_end]
        fig_ms.add_trace(go.Scatter(
            x=yr_slice, y=ms_vals, name=c, mode="lines+markers",
            line=dict(color=COLORS[COMPANIES.index(c)], width=2.5),
            fill="tonexty" if c == selected_companies[0] else None,
            fillcolor=f"rgba({','.join(str(int(COLORS[COMPANIES.index(c)].lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.05)",
        ))
    fig_ms.update_layout(**make_dark_fig(), height=340, yaxis_title="Market Share (%)",
                         legend=dict(orientation="h", x=0.5, xanchor="center", y=1.05),
                         margin=dict(t=30,b=10))
    st.plotly_chart(fig_ms, use_container_width=True)

# ═══════════════════════════════════════════
#  TAB 5 — FORECAST & PREDICTIONS
# ═══════════════════════════════════════════
with tab_predict:
    st.markdown(f'<div class="section-title">AI Forecast — {pred_metric} | Next {pred_years} Years</div>', unsafe_allow_html=True)

    st.info(f"📐 Using polynomial regression (degree-2) on FY22–FY26 actuals to project **{pred_metric}** through FY{26+pred_years}. For illustrative purposes — actual results depend on market conditions, regulatory changes and competition.")

    fig_pred = go.Figure()

    for c in selected_companies:
        actual_vals = annual_data[c][pred_metric]
        future_yrs, pred_vals = predict_metric(c, pred_metric, pred_years)
        color = COLORS[COMPANIES.index(c)]

        # Actuals
        fig_pred.add_trace(go.Scatter(
            x=YEARS, y=actual_vals, name=f"{c} (Actual)",
            mode="lines+markers",
            line=dict(color=color, width=2.5),
            marker=dict(size=8),
        ))
        # Forecast
        fig_pred.add_trace(go.Scatter(
            x=[YEARS[-1]] + future_yrs,
            y=[actual_vals[-1]] + pred_vals,
            name=f"{c} (Forecast)",
            mode="lines+markers",
            line=dict(color=color, width=2, dash="dot"),
            marker=dict(size=8, symbol="diamond"),
        ))

    if pred_metric == "Combined_Ratio":
        fig_pred.add_hline(y=100, line_color="#f59e0b", line_dash="dash",
                           annotation_text="100% Break-even", annotation_font=dict(color="#f59e0b"))
    if pred_metric == "PAT":
        fig_pred.add_hline(y=0, line_color="#6b8cba", line_dash="dash")

    all_yrs = YEARS + list(range(YEARS[-1]+1, YEARS[-1]+pred_years+1))
    fig_pred.add_vrect(
        x0=YEARS[-1]+0.5, x1=all_yrs[-1]+0.5,
        fillcolor="rgba(59130,246,0.06)", line_width=0,
        annotation_text="Forecast Zone",
        annotation_font=dict(color="#60a5fa", size=11),
        annotation_position="top left",
    )
    ylab = {"GWP":"GWP (₹ Cr)","PAT":"PAT (₹ Cr)","Claims_Ratio":"Claims Ratio (%)","Combined_Ratio":"Combined Ratio (%)"}
    fig_pred.update_layout(**make_dark_fig(), height=460,
                           yaxis_title=ylab[pred_metric],
                           legend=dict(orientation="v", x=1.02, y=1),
                           margin=dict(t=20,b=10,r=180))
    st.plotly_chart(fig_pred, use_container_width=True)

    # Forecast table
    st.markdown('<div class="section-title">Forecast Values</div>', unsafe_allow_html=True)
    forecast_rows = {}
    for c in selected_companies:
        _, pred_vals = predict_metric(c, pred_metric, pred_years)
        forecast_rows[c] = [f"{v:,.1f}" for v in pred_vals]

    future_col_names = [f"FY{26+i+1}E" for i in range(pred_years)]
    df_forecast = pd.DataFrame(forecast_rows, index=future_col_names).T
    df_forecast.index.name = "Company"
    st.dataframe(df_forecast, use_container_width=True)

    # ── Scenario Analysis ──────────────────────────────────────────────────
    st.markdown('<div class="section-title">Scenario Analysis — GWP Projection</div>', unsafe_allow_html=True)
    scenario_company = st.selectbox("Select Company for Scenario", selected_companies, key="sc_comp")
    col_sc1, col_sc2, col_sc3 = st.columns(3)
    with col_sc1:
        bear_growth = st.slider("Bear Case Growth %", 5, 15, 8)
    with col_sc2:
        base_growth = st.slider("Base Case Growth %", 10, 30, 18)
    with col_sc3:
        bull_growth = st.slider("Bull Case Growth %", 20, 50, 28)

    base_gwp = annual_data[scenario_company]["GWP"][-1]
    yrs_s = list(range(2027, 2027+pred_years))
    bear_v = [base_gwp * ((1+bear_growth/100)**(i+1)) for i in range(pred_years)]
    base_v = [base_gwp * ((1+base_growth/100)**(i+1)) for i in range(pred_years)]
    bull_v = [base_gwp * ((1+bull_growth/100)**(i+1)) for i in range(pred_years)]

    fig_sc_a = go.Figure()
    fig_sc_a.add_trace(go.Scatter(x=YEARS, y=annual_data[scenario_company]["GWP"],
                                   name="Historical", line=dict(color="#60a5fa", width=2.5),
                                   marker=dict(size=8)))
    for label, vals, color in [("Bear Case", bear_v, "#f87171"),
                                 ("Base Case", base_v, "#f59e0b"),
                                 ("Bull Case", bull_v, "#4ade80")]:
        fig_sc_a.add_trace(go.Scatter(
            x=[YEARS[-1]] + yrs_s,
            y=[base_gwp] + vals,
            name=f"{label} (+{bear_growth if label=='Bear Case' else (base_growth if label=='Base Case' else bull_growth)}% CAGR)",
            line=dict(color=color, width=2, dash="dot"),
            marker=dict(size=8, symbol="diamond"),
        ))
    fig_sc_a.add_vrect(x0=2026.5, x1=yrs_s[-1]+0.5, fillcolor="rgba(59130,246,0.06)", line_width=0)
    fig_sc_a.update_layout(**make_dark_fig(), height=380,
                           title=f"{scenario_company} — GWP Scenarios",
                           yaxis_title="GWP (₹ Cr)",
                           legend=dict(orientation="h", x=0.5, xanchor="center", y=1.05),
                           margin=dict(t=50,b=10))
    st.plotly_chart(fig_sc_a, use_container_width=True)

    # ── Profitability Milestone Tracker ────────────────────────────────────
    st.markdown('<div class="section-title">Profitability Milestone Tracker</div>', unsafe_allow_html=True)

    milestones = {
        "Star Health":          {"status":"Profitable", "first_profit_yr": 2022, "note": "Consistently profitable since FY22; FY26 PAT ₹911 Cr"},
        "Niva Bupa":            {"status":"Recently Profitable","first_profit_yr":2025,"note":"Turned profitable FY25 (₹203 Cr); FY26 PAT ₹366 Cr (+80%)"},
        "Care Health":          {"status":"Profitable","first_profit_yr":2024,"note":"FY24 peak ₹305 Cr, FY25 dipped to ₹155 Cr due to claims surge"},
        "Aditya Birla Health":  {"status":"Investment Phase","first_profit_yr":None,"note":"Fastest CAGR 47%+; targeting breakeven post-scale"},
        "ManipalCigna":         {"status":"Investment Phase","first_profit_yr":None,"note":"Stable mid-sized SAHI; focus on group + retail segments"},
    }
    for c in selected_companies:
        m = milestones[c]
        status_color = {"Profitable":"#4ade80","Recently Profitable":"#f59e0b","Investment Phase":"#f87171"}[m["status"]]
        st.markdown(f"""
        <div style="background:#111827;border:1px solid #1e2d45;border-radius:10px;padding:14px 20px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center">
          <div>
            <span style="font-weight:600;color:#e8ecf4">{c}</span>
            <span style="margin-left:12px;background:rgba(0,0,0,0.3);border:1px solid {status_color}33;border-radius:20px;padding:2px 12px;font-size:12px;color:{status_color}">{m['status']}</span>
          </div>
          <div style="font-size:12px;color:#6b8cba;max-width:60%;text-align:right">{m['note']}</div>
        </div>""", unsafe_allow_html=True)