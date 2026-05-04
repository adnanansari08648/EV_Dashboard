import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="EV Charging Dashboard", layout="wide")

st.title("🔌 EV Charging Infrastructure Dashboard")

# ---------- LOAD DATA ----------
df = pd.read_csv("ev_charging_monthly.csv")

# ---------- CLEANING ----------
df.columns = df.columns.str.lower()

# Convert date if exists
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["month"] = df["date"].dt.month_name()
    df["year"] = df["date"].dt.year

# Month ordering
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

if "month" in df.columns:
    df["month"] = pd.Categorical(df["month"], categories=month_order, ordered=True)

# ---------- FILTER UI ----------
st.markdown("## 🔍 Filters")

col1, col2 = st.columns(2)

# Year Filter
if "year" in df.columns:
    with col1:
        years = st.multiselect(
            "📅 Select Year",
            options=sorted(df["year"].dropna().unique()),
            default=sorted(df["year"].dropna().unique())
        )
else:
    years = None

# State Filter
if "state" in df.columns:
    with col2:
        states = st.multiselect(
            "🌍 Select State",
            options=sorted(df["state"].dropna().unique()),
            default=sorted(df["state"].dropna().unique())
        )
else:
    states = None

# ---------- APPLY FILTER ----------
filtered_df = df.copy()

if years is not None:
    filtered_df = filtered_df[filtered_df["year"].isin(years)]

if states is not None:
    filtered_df = filtered_df[filtered_df["state"].isin(states)]

# ---------- EMPTY CHECK ----------
if filtered_df.empty:
    st.warning("⚠️ No data available for selected filters")
    st.stop()

# ---------- KPI SECTION ----------
col1, col2, col3 = st.columns(3)

if "total_chargers_cumulative" in filtered_df.columns:
    total_chargers = int(filtered_df["total_chargers_cumulative"].max())
    growth = int(
        filtered_df["total_chargers_cumulative"].max()
        - filtered_df["total_chargers_cumulative"].min()
    )
else:
    total_chargers = growth = 0

col1.metric("🔌 Total Chargers (Latest)", total_chargers)
col2.metric("📈 Growth in Chargers", growth)
col3.metric("📊 Records", len(filtered_df))

st.markdown("---")

# ---------- CHARTS ----------

# 1. Growth Trend
if "year" in filtered_df.columns and "total_chargers_cumulative" in filtered_df.columns:
    trend = filtered_df.sort_values(["year"])

    fig1 = px.line(
        trend,
        x="year",
        y="total_chargers_cumulative",
        title="📈 EV Charging Growth (Cumulative)",
        markers=True
    )
    fig1.update_layout(template="plotly_dark", title_x=0.5)
    st.plotly_chart(fig1, use_container_width=True)

# 2. Year-wise Growth
if "year" in filtered_df.columns and "total_chargers_cumulative" in filtered_df.columns:
    yearly = (
        filtered_df
        .groupby("year")["total_chargers_cumulative"]
        .max()
        .reset_index()
    )

    fig2 = px.bar(
        yearly,
        x="year",
        y="total_chargers_cumulative",
        title="📊 Year-wise Charging Growth",
        color="year"
    )
    fig2.update_layout(template="plotly_dark", title_x=0.5)
    st.plotly_chart(fig2, use_container_width=True)

# 3. Top Countries
if "country" in filtered_df.columns and "total_chargers_cumulative" in filtered_df.columns:
    country_data = (
        filtered_df
        .groupby("country")["total_chargers_cumulative"]
        .max()
        .reset_index()
    )

    fig3 = px.bar(
        country_data,
        x="country",
        y="total_chargers_cumulative",
        title="📍 Top Countries by EV Chargers",
        color="country"
    )
    fig3.update_layout(template="plotly_dark", title_x=0.5)
    st.plotly_chart(fig3, use_container_width=True)

# 4. Country Share (Pie)
if "country" in filtered_df.columns and "total_chargers_cumulative" in filtered_df.columns:
    fig4 = px.pie(
        country_data,
        names="country",
        values="total_chargers_cumulative",
        title="🥧 Country-wise Charger Share"
    )
    fig4.update_layout(template="plotly_dark", title_x=0.5)
    st.plotly_chart(fig4, use_container_width=True)

# 5. Distribution Pie (Styled)
if "country" in filtered_df.columns and "total_chargers_cumulative" in filtered_df.columns:
    fig5 = px.pie(
        filtered_df,
        values='total_chargers_cumulative',
        names='country',
        title='EV Charger Distribution by Country',
        template='plotly_dark',
        color_discrete_sequence=px.colors.sequential.Blackbody
    )
    fig5.update_traces(textposition='inside')
    st.plotly_chart(fig5, use_container_width=True)

# ---------- DATA TABLE ----------
with st.expander("📄 Data Preview"):
    st.dataframe(filtered_df, use_container_width=True)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>🚀 Designed by Adnan | EV Analytics Dashboard</p>",
    unsafe_allow_html=True
)