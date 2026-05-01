import streamlit as st

# Title and Page Configuration
st.set_page_config(
    page_title="EV Dashboard",
    page_icon="⚡",
    layout="wide"
)

# Design and Styling 
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #0f172a, #1e293b);
        color: white;
    }

    .title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        margin-top: 20px;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 40px;
    }

    .card {
        background: #1e293b;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        transition: 0.3s;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    .card:hover {
        transform: scale(1.05);
        background: #334155;
    }

    .btn {
        display: inline-block;
        padding: 12px 25px;
        border-radius: 10px;
        text-decoration: none;
        color: white;
        font-weight: bold;
        margin: 10px;
    }

    .green {
        background-color: #22c55e;
    }

    .blue {
        background-color: #0ea5e9;
    }
    </style>
""", unsafe_allow_html=True)

# Header and Subheader
st.markdown('<div class="title">⚡ EV Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart Insights | Clean Energy | Future Mobility</div>', unsafe_allow_html=True)

# Columns for Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="card">🚗<br><br>EV Sales Insights</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">⛽<br><br>Fuel Price Trends</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">🔌<br><br>Charging Stations</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card">🏭<br><br>Brand Performance</div>', unsafe_allow_html=True)

# Call to Action Buttons
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown("""
<style>
.btn {
    padding: 12px 25px;
    text-decoration: none;
    border-radius: 10px;
    font-weight: bold;
    color: white;
    margin: 10px;
    display: inline-block;
    transition: 0.3s;
}
.btn.purple { background: linear-gradient(to right, #6366f1, #8b5cf6); color: white; text-decoration: none; }
.btn.purple { background: linear-gradient(to right, #6366f1, #8b5cf6); color: white; }

.btn:hover {
    transform: scale(1.05);
    opacity: 0.9;
}
</style>

<div style="text-align:center;">
    <a href="/ev_sales_brands" target="_self" class="btn purple">🚀 Explore Dashboard</a>
    <a href="/reports" target="_self" class="btn purple">📊 View Reports</a>
</div>
""", unsafe_allow_html=True)
    

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center; color:#64748b;">© 2026 EV Dashboard | Designed by You 🚀</div>',
    unsafe_allow_html=True
)



st.markdown("---")
st.markdown("<p style='text-align:center;'>🚀 Designed by Adnan | EV Analytics Dashboard</p>", unsafe_allow_html=True)