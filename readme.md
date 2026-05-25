# 🏥 India Standalone Health Insurers — P&L Dashboard

A comprehensive Streamlit dashboard covering P&L analytics, peer comparison, 
and forecasting for India's 5 major Standalone Health Insurers (SAHIs).

## Companies Covered
| Company | Listed | Type |
|---------|--------|------|
| Star Health & Allied Insurance | NSE/BSE | SAHI |
| Niva Bupa Health Insurance | NSE/BSE | SAHI |
| Care Health Insurance | Unlisted | SAHI |
| Aditya Birla Health Insurance | Unlisted | SAHI |
| ManipalCigna Health Insurance | Unlisted | SAHI |

## Dashboard Tabs

1. **🏢 Industry Overview** — Sector-wide KPIs, market share pie, GWP/PAT/Combined ratio overview
2. **📊 FY 24-25 Comparison** — Full-year P&L head-to-head with ratio analysis and tables
3. **📈 Q3 FY26 Comparison** — Latest quarter (Oct–Dec 2025) snapshot with efficiency ratios
4. **📉 Multi-Year Trends** — FY22–FY26 historical trend lines for all key metrics
5. **🔮 Forecast & Predictions** — Polynomial regression forecasts + scenario analysis

## Setup & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Launch dashboard
streamlit run dashboard.py
```

## Data Sources
- IRDAI Annual Report 2024-25
- Company quarterly investor presentations (Q3 FY26)
- NSE/BSE exchange filings
- Analyst estimates for unlisted entities (Care Health, ABHI, ManipalCigna)

> ⚠️ Note: All figures in ₹ Crores. FY = April–March.
> Unlisted company data based on publicly available regulatory filings and news.
> Forecasts are model-generated — not investment advice.