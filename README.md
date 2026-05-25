# 🏥 SAHI-Pulse

**Standalone Health Insurer — P&L Intelligence Dashboard**

*India's 5 Major SAHIs · FY22–Q3 FY26 · Python + Streamlit + Plotly*

**Live app:** `sahi-pulse.streamlit.app`

| 5 Companies | FY22–Q3 FY26 | 25+ Charts | AI Forecasts |
|---|---|---|---|
| Covered | Historical + current period | Interactive visual analysis | Scenario-based projections |

---

## 1. What is SAHI-Pulse?

SAHI-Pulse is an **interactive financial analytics dashboard** built with Python and Streamlit, designed to analyse the Profit & Loss performance of India's **Standalone Health Insurers (SAHIs)**. It covers **five major SAHIs** from FY22 through Q3 FY26 (October–December 2025), combining underwriting metrics, profitability trends, ratio analysis, and AI-powered forecasting in one interface.

> **💡 Why does this matter?**  
> India's health insurance market grew 20%+ in FY25, yet fewer than 3% of Indians have private health cover. Tracking how SAHIs manage premiums, claims, and expenses helps explain the sustainability and expansion of health coverage in one of the world's largest underpenetrated insurance markets.

The dashboard is aimed at:

- Finance and insurance professionals analysing peer performance
- Students and researchers studying the Indian insurance sector
- Investors evaluating listed SAHIs — Star Health (NSE: STARHEALTH) and Niva Bupa (NSE: NIVABUPA)
- Policy enthusiasts tracking IRDAI regulatory compliance and sector trends

### Companies Covered

| Company | Listed | Type | Founded | GWP FY25 (₹ Cr) | Key Differentiator |
|---|---|---|---:|---:|---|
| Star Health | NSE / BSE | SAHI | 2006 | 16,781 | Largest SAHI; retail-focused |
| Niva Bupa | NSE / BSE | SAHI | 2008 | 6,745 | Digital-first; fastest growing |
| Care Health | Unlisted | SAHI | 2012 | 6,864 | Strong retail + OPD products |
| Aditya Birla | Unlisted | SAHI | 2016 | 3,714 | Highest growth CAGR; chronic management focus |
| ManipalCigna | Unlisted | SAHI | 2014 | 1,320 | Group + SME segment specialist |

### Data Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                  SAHI-Pulse — Data Flow Architecture                │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  IRDAI Data  │    │  Quarterly   │    │  Analyst     │
│  FY22–FY26   │    │  Filings     │    │  Estimates   │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │  Python / Pandas │
                 │  Data Layer      │
                 └────────┬─────────┘
                          │
           ┌──────────────┼──────────────┐
           │              │              │
           ▼              ▼              ▼
      ┌──────────┐  ┌──────────┐  ┌──────────────┐
      │  Plotly  │  │ Scikit-  │  │  Streamlit   │
      │  Charts  │  │  learn   │  │  UI + Tabs   │
      │          │  │ Forecast │  │              │
      └──────────┘  └──────────┘  └──────────────┘
                           │
                           ▼
            ┌────────────────────────────────────┐
            │     sahi-pulse.streamlit.app       │
            │       Live Web Dashboard           │
            └────────────────────────────────────┘
```

---

## 2. Key Terms & Metrics

Insurance P&L uses sector-specific ratios that differ from standard corporate finance. This glossary explains the metrics used in the dashboard.

| Term | Full Form | What It Means |
|---|---|---|
| GWP | Gross Written Premium | Total premium collected before reinsurance ceded |
| Claims Ratio | Incurred Claims / Net Premium | Percentage of premium paid out as claims; lower is generally better |
| Expense Ratio | Management Expenses / Premium | Operating cost efficiency; lower is better |
| Combined Ratio | Claims % + Expense % | Below 100% means underwriting profit; above 100% means underwriting loss |
| PAT | Profit After Tax | Net bottom-line profit after all deductions and tax |
| Solvency Ratio | Available / Required Capital | IRDAI mandates minimum 1.5x; higher indicates stronger capital cushion |
| UW Profit | Underwriting Profit/Loss | Core insurance profitability before investment income |
| ICR | Incurred Claims Ratio | IRDAI-reported industry-wide claims metric |
| SAHI | Standalone Health Insurer | Insurer licensed exclusively for health insurance |
| IRDAI | Insurance Regulatory and Development Authority of India | India's insurance sector regulator |
| FY | Financial Year | April 1 to March 31 in India |
| CAGR | Compound Annual Growth Rate | Multi-year annualized growth rate |

### How to Read the Ratios

#### The Combined Ratio — The Most Important Number

**Combined Ratio = Claims Ratio + Expense Ratio**

- Below 100% → the insurer makes an underwriting profit
- Above 100% → the insurer makes an underwriting loss and depends on investment income to support profitability
- Star Health achieved sub-100% (98.9%) in Q3 FY26, making it the only SAHI near underwriting breakeven

> **📊 Benchmark Reference**  
> Global best-in-class health insurers often target a combined ratio of 85–95%. Indian SAHIs are improving: Star Health at 98.9%, Care Health at 102%, Niva Bupa at 109.5% in Q3 FY26. Aditya Birla Health at 167.7% reflects a scale-first investment phase.

#### Solvency Ratio — Capital Adequacy

IRDAI mandates a minimum solvency ratio of **1.5x**. All five SAHIs exceed this threshold. A higher ratio signals greater resilience against sudden claim surges such as pandemic-like events.

#### Investment Income — The Profitability Bridge

Because several SAHIs operate with combined ratios above 100%, **investment income on float** becomes critical in supporting positive PAT. Premiums collected but not yet paid out as claims can materially influence reported profitability.

---

## 3. Dashboard Features & How to Use Them

### Dashboard Overview

```text
┌────────────────────────────────────────────────────────────────────┐
│                        Dashboard Tabs                              │
├──────────┬──────────┬──────────┬──────────┬────────────────────────┤
│🏢Industry│📊 FY25   │📈 Q3 FY26│📉 Trends │ 🔮 Forecast            │
│Overview  │Comparison│Comparison│FY22-FY26 │ & Predictions          │
├──────────┼──────────┼──────────┼──────────┼────────────────────────┤
│• Mkt Shr │• GWP     │• GWP+YoY │• GWP     │• Poly Regression       │
│• PAT Bar │• PAT     │• PAT Qtrl│• PAT     │• 3-Scenario GWP        │
│• Combined│• Ratios  │• Ratios  │• Combined│• Forecast Table        │
│  Ratio   │• Scatter │• Solvency│• Mkt Shr │• Profitability Tracker │
└──────────┴──────────┴──────────┴──────────┴────────────────────────┘
```

| Tab | Focus Area | Charts & Components |
|---|---|---|
| 🏢 Industry Overview | Sector-level KPIs | Market share pie, PAT bar, combined ratio comparison |
| 📊 FY 24-25 Comparison | Full-year P&L | GWP, PAT, claims/expense/solvency ratios, scatter plots |
| 📈 Q3 FY26 Comparison | Latest quarterly data | Quarterly GWP with YoY growth, PAT, efficiency ratios |
| 📉 Multi-Year Trends | FY22–FY26 history | GWP, PAT, combined ratio, market share evolution |
| 🔮 Forecast | AI-powered projections | Polynomial regression and bear/base/bull scenario analysis |

### Sidebar Controls

All filters apply live across the active dashboard tab:

- Company Filter — select one or more of the 5 SAHIs
- Year Range Slider — narrow trend analysis from FY22 to FY26
- Forecast Horizon — choose 1 to 5 years ahead
- Metric to Forecast — select GWP, PAT, Claims Ratio, or Combined Ratio

### Tab-by-Tab Guide

#### 🏢 Tab 1 — Industry Overview

Start here for a macro view. KPI cards summarize total sector GWP, Star Health's GWP, number of profitable SAHIs, sector ICR, and claim settlement rate. Supporting visuals show market share, PAT by company, and combined ratio movement.

#### 📊 Tab 2 — FY 24-25 Comparison

This tab compares the most recently completed financial year. The Investment Income vs PAT scatter plot helps identify which companies rely more heavily on investment income rather than underwriting profitability.

#### 📈 Tab 3 — Q3 FY26 Comparison

This tab focuses on October–December 2025 performance. A dual-axis chart overlays GWP bars with a YoY growth line, while ratio charts use green/red visual cues for faster interpretation.

#### 📉 Tab 4 — Multi-Year Trends

Use this section to track long-term performance from FY22 to FY26. It highlights premium growth, profitability trends, combined ratio shifts, and market share changes over time.

#### 🔮 Tab 5 — Forecast & Predictions

This tab includes two forecasting methods:

- Polynomial Regression Forecast — fits a degree-2 curve on FY22–FY26 actuals and projects forward
- Scenario Analysis — applies Bear, Base, and Bull CAGR assumptions to future GWP paths

A profitability milestone tracker summarizes each company's path toward sustainable profitability.

---

## 4. Future Scope & Use Cases

### Planned Enhancements

#### Live Data Integration

- Connect to IRDAI open data sources for automated quarterly updates
- Integrate NSE/BSE filing feeds for listed SAHIs
- Expand coverage to additional SAHIs as more public data becomes available

#### Advanced Analytics

- LSTM and time-series models for more sophisticated forecasting
- Monte Carlo simulation for claims ratio stress testing
- Correlation analysis linking macro variables to claims trends
- Benchmarking against South-East Asian and global health insurers

#### User & Product Enhancements

- PDF export for boardroom-style reporting
- Custom date range selectors for intra-year quarterly drill-down
- Alerting when solvency approaches regulatory minimum thresholds
- Dark/light mode toggle improvements

### Real-World Applications

> **🏦 Investment Research**  
> Equity analysts covering Star Health or Niva Bupa can benchmark quarterly performance against peers before publishing notes.

> **🏛️ Regulatory Monitoring**  
> Compliance teams can track combined ratio trends and solvency headroom across the SAHI universe.

> **🎓 Academic Research**  
> Researchers can study the effect of regulatory shifts, claims shocks, and healthcare inflation on insurer profitability.

> **💼 Corporate Strategy**  
> SAHI strategy teams can benchmark expense ratios, claims ratios, and growth trajectories against competitors.

---

## 5. Setup & Installation

### Prerequisites

- Python 3.9 or higher
- `pip` package manager
- Git

### Quick Start

#### Step 1 — Clone the repository

```bash
git clone https://github.com/yourusername/sahi-pulse.git
cd sahi-pulse
```

#### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

#### Step 3 — Run locally

```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501` in your browser.

### Tech Stack

| Library | Purpose | Version |
|---|---|---|
| Streamlit | Web UI and deployment | 1.32+ |
| Plotly | Interactive charts | 5.18+ |
| Pandas | Data wrangling | 2.0+ |
| NumPy | Numerical operations | 1.24+ |
| Scikit-learn | ML forecasting (polynomial regression) | 1.3+ |

### Deployment (Streamlit Cloud)

1. Fork or push the repository to your GitHub account
2. Go to Streamlit Cloud and connect GitHub
3. Select the repository and set main file path to `app.py`
4. Click **Deploy** — dependencies from `requirements.txt` will install automatically
5. Your live URL will look like `yourusername-sahi-pulse.streamlit.app`

---

## 6. Data Sources & Methodology

### Primary Sources

- IRDAI Annual Report 2024–25 — sector GWP, ICR, and expense ratios
- Star Health quarterly investor presentations (Q1–Q3 FY26)
- Niva Bupa IPO prospectus and quarterly results
- Care Health, Aditya Birla Health, and ManipalCigna public filings and disclosures

### Methodology Notes

- Unlisted company data is sourced from regulatory filings and publicly available disclosures
- FY26 full-year values are estimates extrapolated from Q1–Q3 FY26 actuals
- Market share is calculated within the standalone health insurance segment only
- All values are in Indian Rupees (₹), crores unless stated otherwise
- Forecasts use degree-2 polynomial regression and are illustrative only, not investment advice

> **⚠️ Disclaimer**  
> This dashboard is intended for educational and analytical purposes. Data for unlisted companies is based on publicly available sources and may differ from audited figures. It should not be used as investment advice.

---

*Built with ♥ for India's health insurance ecosystem*  
**Live app:** `sahi-pulse.streamlit.app` · Star the repo if you find it useful.
