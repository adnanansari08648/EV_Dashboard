import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Fuel Price Dashboard", layout="wide")

# ---------- LOAD DATA ----------
df = pd.read_csv("fuel_prices_monthly.csv")

# ---------- CLEANING ----------
df.columns = df.columns.str.lower()

# Fix month ordering
if "month" in df.columns:
    df["month"] = pd.to_numeric(df["month"], errors="coerce")
    df = df.sort_values("month")

numeric_cols = df.select_dtypes(include='number').columns
cols = df.columns.tolist()



# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align: center; color: #00FFFF;'>⛽ Fuel Price Intelligence Dashboard</h1>
<p style='text-align: center; color: gray;'>Monthly Price Trends & Insights</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- TOP FILTER BAR ----------
st.markdown("### 🔍 Filter Data")

f1, f2, f3 = st.columns(3)

filtered_df = df.copy()

# 🌍 Country Filter
if "country" in df.columns:
    with f1:
        countries = st.multiselect(
            "🌍 Country",
            options=sorted(df["country"].dropna().unique()),
            default=sorted(df["country"].dropna().unique())
        )
    filtered_df = filtered_df[filtered_df["country"].isin(countries)]

# 📅 Year Filter
if "year" in df.columns:
    with f2:
        years = st.multiselect(
            "📅 Year",
            options=sorted(df["year"].dropna().unique()),
            default=sorted(df["year"].dropna().unique())
        )
    filtered_df = filtered_df[filtered_df["year"].isin(years)]

# 🗓 Month Filter
if "month" in df.columns:
    with f3:
        months = st.multiselect(
            "🗓 Month",
            options=sorted(df["month"].dropna().unique()),
            default=sorted(df["month"].dropna().unique())
        )
    filtered_df = filtered_df[filtered_df["month"].isin(months)]
    
# ---------- KPI SECTION ----------
col1, col2, col3, col4 = st.columns(4)

total_records = len(df)
avg_price = df[numeric_cols[0]].mean() if len(numeric_cols) > 0 else 0
max_price = df[numeric_cols[0]].max() if len(numeric_cols) > 0 else 0
min_price = df[numeric_cols[0]].min() if len(numeric_cols) > 0 else 0

col1.metric("📊 Records", total_records)
col2.metric("📈 Avg Price", f"{avg_price:.2f}")
col3.metric("🔺 Max Price", f"{max_price:.2f}")
col4.metric("🔻 Min Price", f"{min_price:.2f}")

st.markdown("---")

# ---------- ROW 1 ----------
c1, c2 = st.columns(2)

# 📈 LINE TREND
if "month" in df.columns and len(numeric_cols) > 0:
    trend = df.groupby("month")[numeric_cols[0]].mean().reset_index()
    trend = trend.sort_values("month")

    fig1 = px.line(
        trend,
        x="month",
        y=numeric_cols[0],
        markers=True,
        title="📈 Monthly Price Trend"
    )

    fig1.update_layout(template="plotly_dark", title_x=0.5)
    c1.plotly_chart(fig1, use_container_width=True)

# 🌊 AREA CHART
if "month" in df.columns and len(numeric_cols) > 0:
    fig2 = px.area(
        trend,
        x="month",
        y=numeric_cols[0],
        title="🌊 Price Movement Area"
    )

    fig2.update_layout(template="plotly_dark", title_x=0.5)
    c2.plotly_chart(fig2, use_container_width=True)

# ---------- ROW 2 ----------
c3, c4 = st.columns(2)

# 🔥 TOP VALUES
if len(numeric_cols) > 0:
    top = df.nlargest(10, numeric_cols[0])

    fig3 = px.bar(
        top,
        x=cols[0],
        y=numeric_cols[0],
        color=numeric_cols[0],
        title="🔥 Top Price Records",
        text_auto=True
    )

    fig3.update_layout(template="plotly_dark", title_x=0.5)
    c3.plotly_chart(fig3, use_container_width=True)

# 🍩 DONUT CHART
if len(cols) > 1 and len(numeric_cols) > 0:
    fig4 = px.pie(
        df,
        names=cols[0],
        values=numeric_cols[0],
        hole=0.5,
        title="🍩 Price Distribution"
    )

    fig4.update_layout(template="plotly_dark", title_x=0.5)
    c4.plotly_chart(fig4, use_container_width=True)

# ---------- ROW 3 ----------
# 🌞 SUNBURST (WITH GRADIENT)
if len(cols) >= 2 and len(numeric_cols) > 0:

    fig5 = px.sunburst(
        df,
        path=[cols[0], cols[1]],
        values=numeric_cols[0],
        color=numeric_cols[0],
        color_continuous_scale="Turbo",
        title="🌞 Fuel Price Hierarchy"
    )

    fig5.update_layout(template="plotly_dark", title_x=0.5)

    fig5.update_traces(
        textinfo="label+percent entry"
    )

    st.plotly_chart(fig5, use_container_width=True)

# ---------- DATA TABLE ----------
st.markdown("---")
with st.expander("📄 Data Preview"):
    st.dataframe(df, use_container_width=True)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>🚀 Designed by Adnan | Fuel Analytics Dashboard</p>",
    unsafe_allow_html=True
)