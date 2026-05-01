import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="EV Master Report", layout="wide")

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align:center; color:#00FFFF;'>📊 EV Project Master Report</h1>
<p style='text-align:center; color:gray;'>Charging • Market • Trends • Fuel Insights</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- LOAD ALL DATA ----------
charging = pd.read_csv("ev_charging_monthly.csv")
market = pd.read_csv("ev_market_master.csv")
trends = pd.read_csv("ev_trends_monthly.csv")
fuel = pd.read_csv("fuel_prices_monthly.csv")
sales = pd.read_csv("ev_sales_brands.csv")

# lowercase columns
for df in [charging, market, trends, fuel, sales]:
    df.columns = df.columns.str.lower()

# ---------- KPI SECTION ----------
col1, col2, col3, col4, col5 = st.columns(5)

# Total Chargers
total_chargers = charging["total_chargers_cumulative"].max() if "total_chargers_cumulative" in charging.columns else 0

# Total EV Sales
total_sales = market["units_sold"].sum() if "units_sold" in market.columns else 0

# Avg Fuel Price
avg_price = fuel.select_dtypes(include='number').mean().mean()

# Total Records
total_records = len(charging) + len(market) + len(trends) + len(fuel) + len(sales)

col1.metric("🔌 Total Chargers", f"{total_chargers:,}")
col2.metric("🚗 Total EV Sales", f"{total_sales:,}")
col3.metric("⛽ Avg Fuel Price", f"{avg_price:.2f}")
col4.metric("📊 Total Records", total_records)
col5.metric("🏭 Top Brand", market.groupby("brand")["units_sold"].sum().idxmax() if "brand" in market.columns else "N/A")

st.markdown("---")

# ---------- ROW 1 ----------
c1, c2 = st.columns(2)

# 📈 EV Sales Trend
if "year" in market.columns:
    sales_trend = market.groupby("year")["units_sold"].sum().reset_index()

    fig1 = px.line(sales_trend, x="year", y="units_sold",
                   title="📈 EV Sales Growth",
                   markers=True)

    fig1.update_layout(template="plotly_dark")
    c1.plotly_chart(fig1, use_container_width=True)

# 🔌 Charging Growth
if "year" in charging.columns:
    charging_trend = charging.groupby("year")["total_chargers_cumulative"].max().reset_index()

    fig2 = px.bar(charging_trend, x="year", y="total_chargers_cumulative",
                  title="🔌 Charging Infrastructure Growth",
                  color="year")

    fig2.update_layout(template="plotly_dark")
    c2.plotly_chart(fig2, use_container_width=True)

# ---------- ROW 2 ----------
c3, c4 = st.columns(2)

# 🏭 Top Brands
if "brand" in market.columns:
    brand_perf = market.groupby("brand")["units_sold"].sum().reset_index()

    fig3 = px.bar(brand_perf, x="brand", y="units_sold",
                  title="🏆 Top EV Brands",
                  color="brand")

    fig3.update_layout(template="plotly_dark")
    c3.plotly_chart(fig3, use_container_width=True)

# ⛽ Fuel Price Trend
if "month" in fuel.columns:
    fuel_trend = fuel.groupby("month")[fuel.select_dtypes(include='number').columns[0]].mean().reset_index()

    fig4 = px.line(fuel_trend, x="month", y=fuel_trend.columns[1],
                   title="⛽ Fuel Price Trend",
                   markers=True)

    fig4.update_layout(template="plotly_dark")
    c4.plotly_chart(fig4, use_container_width=True)

# ---------- ROW 3 ----------
c5 = st.columns(1)
# EV Sales by Brand    
if "brand" in sales.columns:
    brand_sales = sales.groupby("brand")["units_sold"].sum().reset_index()

    fig5 = px.bar(brand_sales, x="brand", y="units_sold",
                  title="🚗 EV Sales by Brand",
                  color="brand")

    fig5.update_layout(template="plotly_dark")
    c5[0].plotly_chart(fig5, use_container_width=True)

# ---------- INSIGHTS ----------
st.markdown("### 🧠 Key Insights")

top_brand = market.groupby("brand")["units_sold"].sum().idxmax() if "brand" in market.columns else "N/A"

st.success(f"""
✔️ EV adoption is increasing with strong sales growth 📈  
✔️ Charging infrastructure expanding rapidly 🔌  
✔️ Top performing brand: {top_brand} 🏆  
✔️ Fuel prices trend impacts EV demand ⛽  
✔️ Total datasets analyzed: {total_records} 📊  
""")

# ---------- FINAL SUMMARY ----------
st.markdown("### 📌 Project Summary")

st.info("""
This dashboard integrates multiple EV datasets including charging infrastructure,
market performance, adoption trends, and fuel price analysis.

👉 Key Objective:
- Understand EV growth
- Analyze market leaders
- Compare fuel vs EV adoption
- Identify trends over time

👉 Outcome:
- Data-driven EV insights
- Interactive visual analytics
- Real-world dashboard experience
""")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>🚀 Designed by Adnan | Master EV Analytics Dashboard</p>",
    unsafe_allow_html=True
)