import streamlit as st
import pandas as pd
import plotly.express as px

# Title and Page Configuration
st.set_page_config(page_title="EV Market Dashboard", layout="wide")

st.title("⚡ EV Market Dashboard")

# Load Dataset
df = pd.read_csv("ev_market_master.csv")

# Applying Sidebar Filters
st.sidebar.header("🔍 Filters")

# Brand Filter
if "brand" in df.columns:
    brands = st.sidebar.multiselect(
        "Select Brand",
        options=df["brand"].unique(),
        default=df["brand"].unique()
    )
else:
    brands = None

# Year Filter
if "year" in df.columns:
    years = st.sidebar.multiselect(
        "Select Year",
        options=sorted(df["year"].unique()),
        default=sorted(df["year"].unique())
    )
else:
    years = None

# Country Filter
if "country" in df.columns:
    countries = st.sidebar.multiselect(
        "Select Country",
        options=sorted(df["country"].unique()),
        default=sorted(df["country"].unique())
    )
else:
    countries = None    

# Main DataFrame after applying filters
filtered_df = df.copy()

if brands is not None:
    filtered_df = filtered_df[filtered_df["brand"].isin(brands)]

if years is not None:
    filtered_df = filtered_df[filtered_df["year"].isin(years)]

# ================= KPI SECTION =================
col1, col2, col3 = st.columns(3)

if "units_sold" in filtered_df.columns:
    total_sales = int(filtered_df["units_sold"].sum())
else:
    total_sales = 0

if "brand" in filtered_df.columns and "units_sold" in filtered_df.columns:
    top_brand = filtered_df.groupby("brand")["units_sold"].sum().idxmax()
else:
    top_brand = "N/A"

col1.metric("🚗 Total Sales", total_sales)
col2.metric("🏆 Top Brand", top_brand)
col3.metric("📊 Records", len(filtered_df))

# Charts and Visualizations

# 1. Sales Trend (Line Chart)
if "year" in filtered_df.columns and "units_sold" in filtered_df.columns:
    trend = filtered_df.groupby("year")["units_sold"].sum().reset_index()

    fig1 = px.line(trend, x="year", y="units_sold",
                   title="📈 Sales Trend",
                   markers=True)

    st.plotly_chart(fig1, use_container_width=True)

# 2. Brand Performance (Bar Chart)
if "brand" in filtered_df.columns and "units_sold" in filtered_df.columns:
    brand_perf = filtered_df.groupby("brand")["units_sold"].sum().reset_index()

    fig2 = px.bar(brand_perf, x="brand", y="units_sold",
                  title="🏭 Brand Performance",
                  color="brand")

    st.plotly_chart(fig2, use_container_width=True)

# 3. Market Share (Pie Chart)
if "brand" in filtered_df.columns and "units_sold" in filtered_df.columns:
    fig3 = px.pie(filtered_df,
                  names="brand",
                  values="units_sold",
                  title="🥧 Market Share")

    st.plotly_chart(fig3, use_container_width=True)



# 4. EV Sales Growth Over Time (Line Chart)
trend = df.groupby("year")["units_sold"].sum().reset_index()

fig = px.line(trend, x="year", y="units_sold",
              title="📈 EV Sales Growth Over Time",
              markers=True)

st.plotly_chart(fig, use_container_width=True)

# 5. Brand-wise Growth (Line Chart)

fig = px.line(df, x="year", y="units_sold",
              color="brand",
              title="📊 Brand-wise Growth",
              markers=True)

st.plotly_chart(fig, use_container_width=True)

# ================= TABLE =================
with st.expander("📄 Data Preview"):
    st.dataframe(filtered_df)


st.markdown("---")
st.markdown("<p style='text-align:center;'>🚀 Designed by Adnan | EV Analytics Dashboard</p>", unsafe_allow_html=True)