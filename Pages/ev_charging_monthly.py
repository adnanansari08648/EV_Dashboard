import streamlit as st
import pandas as pd
import plotly.express as px

# Page Title and Configuration
st.set_page_config(page_title="EV Charging Dashboard", layout="wide")

st.title("🔌 EV Charging Infrastructure Dashboard")

# Load Dataset
df = pd.read_csv("ev_charging_monthly.csv")

# Cleaning and Preprocessing

# Agar date column hai to convert karo
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month_name()
    df["year"] = df["date"].dt.year

# Month order fix (IMPORTANT 🔥)
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

if "month" in df.columns:
    df["month"] = pd.Categorical(df["month"], categories=month_order, ordered=True)

# filtering options in sidebar
st.markdown("## 🔍 Filters")

col1, col2 = st.columns(2)

with col1:
    if "year" in df.columns:
        years = st.multiselect(
            "📅 Select Year",
            options=sorted(df["year"].unique()),
            default=sorted(df["year"].unique())
        )
    else:
        years = None

with col2:
    if "state" in df.columns:
        states = st.multiselect(
            "🌍 Select State",
            options=df["state"].unique(),
            default=df["state"].unique()
        )
    else:
        states = None

        st.markdown(
    """
    <style>
    .stMultiSelect {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= APPLY FILTER =================
filtered_df = df.copy()

if years:
    filtered_df = filtered_df[filtered_df["year"].isin(years)]

if states:
    filtered_df = filtered_df[filtered_df["state"].isin(states)]

# ================= KPI SECTION =================
col1, col2, col3 = st.columns(3)

# Total chargers (latest value)
if "total_chargers_cumulative" in filtered_df.columns:
    total_chargers = int(filtered_df["total_chargers_cumulative"].max())
else:
    total_chargers = 0

# Growth (latest - first)
if "total_chargers_cumulative" in filtered_df.columns:
    growth = int(
        filtered_df["total_chargers_cumulative"].max()
        - filtered_df["total_chargers_cumulative"].min()
    )
else:
    growth = 0

col1.metric("🔌 Total Chargers (Latest)", total_chargers)
col2.metric("📈 Growth in Chargers", growth)
col3.metric("📊 Records", len(filtered_df))

# ================= CHARTS =================

# 1. Charging Growth Trend (MOST IMPORTANT 🔥)
if "month" in filtered_df.columns and "total_chargers_cumulative" in filtered_df.columns:
    trend = filtered_df.sort_values("year")

    fig1 = px.line(trend,
                   x="year",
                   y="total_chargers_cumulative",
                   title="📈 EV Charging Growth (Cumulative)",
                   markers=True)

    st.plotly_chart(fig1, use_container_width=True)

# 2. Year-wise Growth
if "year" in filtered_df.columns and "total_chargers_cumulative" in filtered_df.columns:
    yearly = filtered_df.groupby("year")["total_chargers_cumulative"].max().reset_index()

    fig2 = px.bar(yearly,
                  x="year",
                  y="total_chargers_cumulative",
                  title="📊 Year-wise Charging Growth",
                  color="year")

    st.plotly_chart(fig2, use_container_width=True)



# 3.  Top Country by Chargers
state_data = df.groupby("country")["total_chargers_cumulative"].max().reset_index()

fig = px.bar(state_data,
             x="country",
             y="total_chargers_cumulative",
             title="📍 Top Countries by EV Chargers",
             color="country")

st.plotly_chart(fig, use_container_width=True)  
  

# 4. Country-wise Charger Share (Pie Chart)
country_data = df.groupby("country")["total_chargers_cumulative"].max().reset_index()

fig = px.pie(country_data,
             names="country",
             values="total_chargers_cumulative",
             title="🥧 Country-wise Charger Share")

st.plotly_chart(fig, use_container_width=True)

# 5.    EV Charger Distribution by Country (Pie Chart with Custom Colors)
fig = px.pie(df, values = 'total_chargers_cumulative' , names= 'country', 
             title = 'EV Charger Distribution by Country',
             template='plotly_dark',
             color_discrete_sequence=px.colors.sequential.Blackbody          
             )
fig.update_traces(textposition = 'inside')      
st.plotly_chart(fig, use_container_width=True)

# ================= DATA TABLE =================
with st.expander("📄 Data Preview"):
    st.dataframe(filtered_df)



st.markdown("---")
st.markdown("<p style='text-align:center;'>🚀 Designed by Adnan | EV Analytics Dashboard</p>", unsafe_allow_html=True)