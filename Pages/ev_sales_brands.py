import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EV Sales by Brand Dashboard", layout="wide")
st.title("🚗 EV Sales by Brand Dashboard")

# ---- LOAD DATA ----
df = pd.read_csv("ev_sales_brands.csv")

# ---- CLEANING ----
df = df.dropna(subset=["brand", "units_sold"])

# ---- SIDEBAR FILTERS ----
st.sidebar.header("Filters")

# Year filter
years = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

# Country filter
countries = st.sidebar.multiselect(
    "Select Country",
    options=df["country"].unique(),
    default=df["country"].unique()
)

# Apply filters
filtered_df = df[
    (df["year"].isin(years)) &
    (df["country"].isin(countries))
]

# ---- BRAND SALES AGGREGATION ----
brand_sales = filtered_df.groupby("brand")["units_sold"].sum().reset_index()
brand_sales = brand_sales.sort_values(by="units_sold", ascending=False)

# ---- KPI SECTION ----
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Units Sold", int(brand_sales["units_sold"].sum()))
col2.metric("Top Brand", brand_sales.iloc[0]["brand"])
col3.metric("Units Sold (Top Brand)", int(brand_sales.iloc[0]["units_sold"]))
col4.metric("Average Units Sold per Brand", int(brand_sales["units_sold"].mean()))

st.divider()
#  ROW 1
#  TOP 10 BAR CHART 

c1, c2 =st.columns(2)
 
st.subheader("📊 Top 10 EV Brands")

fig_bar = px.bar(
    brand_sales.head(10),
    x="brand",
    y="units_sold",
    color="brand",
    text="units_sold",
    template="plotly_dark"
)

st.plotly_chart(fig_bar, use_container_width=True)

#  MARKET SHARE PIE CHART
st.subheader("🥧 Market Share by Brand")

fig_pie = px.pie(
    brand_sales,
    names="brand",
    values="units_sold",
    template="plotly_dark"
)

st.plotly_chart(fig_pie, use_container_width=True)
#  ROW 2 
# 3. HORIZONTAL COMPARISON

c1, c2 =st.columns(2)

st.subheader("📈 Brand Comparison")

fig_hbar = px.bar(
    brand_sales,
    x="units_sold",
    y="brand",
    orientation="h",
    color="units_sold",
    template="plotly_dark"
)

st.plotly_chart(fig_hbar, use_container_width=True)

# 4. SUNBURST CHART
st.subheader("🌳 Brand Distribution")

fig_tree = px.sunburst(
    brand_sales,
    path=["brand"],
    values="units_sold",
    template="plotly_dark"
)

st.plotly_chart(fig_tree, use_container_width=True)

# 5. YEARLY TREND
st.subheader("📅 Brand Sales Trend Over Time")

trend = filtered_df.groupby(["year", "brand"])["units_sold"].sum().reset_index()

fig_line = px.line(
    trend,
    x="year",
    y="units_sold",
    color="brand",
    markers=True,
    template="plotly_dark"
)

st.plotly_chart(fig_line, use_container_width=True)

# 6. GROWTH RATE CALCULATION
df_year = df.groupby(["brand", "year"])["units_sold"].sum().reset_index()

# sort for correct growth calc
df_year = df_year.sort_values(["brand", "year"])

# growth calculation
df_year["growth_rate"] = df_year.groupby("brand")["units_sold"].pct_change() * 100

df_year = df_year.dropna()

fig = px.sunburst(
    df_year,
    path=['year', 'brand'],
    values='growth_rate',
    title="📈 Yearly Sales Trend by Brand",
    color='growth_rate',
    template='plotly_dark',
    color_continuous_scale='RdYlGn'   # green = growth, red = decline
)

fig.update_traces(textinfo='label+percent entry')

st.plotly_chart(fig, use_container_width=True)

# --- Data Preview ---
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)

st.markdown("---")
st.markdown("<p style='text-align:center;'>🚀 Designed by Adnan | EV Analytics Dashboard</p>", unsafe_allow_html=True)