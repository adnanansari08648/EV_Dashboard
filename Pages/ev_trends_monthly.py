import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="EV Trends Dashboard", layout="wide")

# ---------- LOAD DATA ----------
df = pd.read_csv("ev_trends_monthly.csv")
df.columns = df.columns.str.lower()

# ---------- FIX MONTH ----------
if "month" in df.columns:
    df["month"] = pd.to_numeric(df["month"], errors="coerce")
    df = df.sort_values("month")

numeric_cols = df.select_dtypes(include='number').columns.tolist()
# Exclude 'month' from numeric_cols so it's not treated as a metric
metric_cols = [c for c in numeric_cols if c not in ("month", "year")]
non_numeric_cols = df.select_dtypes(exclude='number').columns.tolist()
cols = df.columns.tolist()

# ---------- SIDEBAR FILTER ----------
st.sidebar.header("🔍 Filters")

if "month" in df.columns:
    selected_month = st.sidebar.multiselect(
        "Select Month",
        options=sorted(df["month"].dropna().unique()),
        default=sorted(df["month"].dropna().unique())
    )
    df = df[df["month"].isin(selected_month)]

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align:center; color:#00FFFF;'>⚡ EV Trends Dashboard</h1>
<p style='text-align:center; color:gray;'>Smart Insights • Clean Design • Powerful Visuals</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- KPI ROW ----------
col1, col2, col3, col4 = st.columns(4)

total_records = len(df)
total_value = df[metric_cols[0]].sum() if metric_cols else 0
avg_value   = df[metric_cols[0]].mean() if metric_cols else 0
max_value   = df[metric_cols[0]].max()  if metric_cols else 0

col1.metric("📊 Records", total_records)
col2.metric("⚡ Total",   f"{total_value:,.0f}")
col3.metric("📈 Avg",     f"{avg_value:,.2f}")
col4.metric("🔥 Peak",    f"{max_value:,.0f}")

st.markdown("---")

# ---------- ROW 1: Line Chart vs Area Chart (different metrics) ----------
c1, c2 = st.columns(2)

if "month" in df.columns and len(metric_cols) > 0:
    # LINE CHART — first metric
    trend = df.groupby("month")[metric_cols[0]].sum().reset_index()
    trend["month"] = trend["month"].astype(str)          # readable x-axis labels

    fig1 = px.line(
        trend,
        x="month",
        y=metric_cols[0],
        markers=True,
        title=f"📈 Monthly Trend — {metric_cols[0].title()}"
    )
    fig1.update_layout(
        template="plotly_dark",
        title_x=0.5,
        xaxis_title="Month",
        yaxis_title=metric_cols[0].title(),
        xaxis=dict(type="category"),   # keep months in order, not as numbers
    )
    c1.plotly_chart(fig1, use_container_width=True)

    # AREA CHART — second metric (or same if only one exists)
    area_col = metric_cols[1] if len(metric_cols) > 1 else metric_cols[0]
    area = df.groupby("month")[area_col].sum().reset_index()
    area["month"] = area["month"].astype(str)

    fig2 = px.area(
        area,
        x="month",
        y=area_col,
        title=f"🌊 Growth Area — {area_col.title()}"
    )
    fig2.update_layout(
        template="plotly_dark",
        title_x=0.5,
        xaxis_title="Month",
        yaxis_title=area_col.title(),
        xaxis=dict(type="category"),
    )
    c2.plotly_chart(fig2, use_container_width=True)

# ---------- ROW 2: Bar Chart + Donut ----------
c3, c4 = st.columns(2)

if metric_cols:
    # BAR CHART — use a categorical column for x-axis instead of the first column
    # Pick the best label column: prefer non-numeric, fall back to 'month'
    if non_numeric_cols:
        bar_x = non_numeric_cols[0]
        bar_df = (
            df.groupby(bar_x)[metric_cols[0]].sum()
              .reset_index()
              .nlargest(10, metric_cols[0])
        )
    elif "month" in df.columns:
        bar_x = "month"
        bar_df = (
            df.groupby("month")[metric_cols[0]].sum()
              .reset_index()
              .nlargest(10, metric_cols[0])
        )
        bar_df["month"] = bar_df["month"].astype(str)
    else:
        bar_x = cols[0]
        bar_df = df.nlargest(10, metric_cols[0])

    fig3 = px.bar(
        bar_df,
        x=bar_x,
        y=metric_cols[0],
        color=metric_cols[0],
        title="🔥 Top Performance",
        text_auto=True,
        color_continuous_scale="Teal",
    )
    fig3.update_layout(
        template="plotly_dark",
        title_x=0.5,
        xaxis_title=bar_x.title(),
        yaxis_title=metric_cols[0].title(),
    )
    fig3.update_xaxes(tickangle=-35)
    c3.plotly_chart(fig3, use_container_width=True)

# Donut Chart — unchanged (as requested)
if len(df.columns) > 1 and metric_cols:
    fig4 = px.pie(
        df,
        names=df.columns[0],
        values=metric_cols[0],
        hole=0.5,
        title="🍩 Distribution"
    )
    fig4.update_layout(template="plotly_dark", title_x=0.5)
    c4.plotly_chart(fig4, use_container_width=True)

# ---------- ROW 3: Sunburst (unchanged) ----------
st.markdown("### 🌞 Hierarchical Insights")

if len(cols) >= 2 and metric_cols:
    fig5 = px.sunburst(
        df,
        path=[cols[0], cols[1]],
        values=metric_cols[0],
        color=cols[0],
        color_discrete_sequence=px.colors.qualitative.Bold_r
    )
    fig5.update_layout(template="plotly_dark", title_x=0.4)
    fig5.update_traces(
        textinfo="label+value",
        insidetextorientation="radial"
    )
    st.plotly_chart(fig5, use_container_width=True)

# ---------- DATA TABLE ----------
with st.expander("📄 View Raw Data"):
    st.dataframe(df)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>🚀 Designed by Adnan | Premium EV Dashboard</p>",
    unsafe_allow_html=True
)