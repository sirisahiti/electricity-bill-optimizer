import streamlit as st
import pandas as pd
import numpy as np

# ---------- CONFIG ----------
st.set_page_config(page_title="Voltify ⚡", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #e0f2fe, #f8fafc 70%);
}

.block-container {
    padding: 2rem 4rem;
}

.hero {
    text-align: center;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #6C63FF, #00AEEF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #475569;
}

.card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0,0,0,0.05);
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 20px;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.08);
}

.metric {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #00AEEF, #6C63FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.section-title {
    font-size: 1.2rem;
    color: #475569;
    margin-bottom: 10px;
}

.highlight {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 20px;
}

.warning-box {
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: white;
    padding: 20px;
    border-radius: 15px;
    font-weight: 600;
    margin-bottom: 20px;
}

.suggestion {
    background: rgba(0,0,0,0.03);
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
<h1>⚡ Voltify</h1>
<p>Smart energy insights to reduce your electricity bill</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#475569;'>Track. Optimize. Save ⚡</p>", unsafe_allow_html=True)

# ---------- DATA ----------
state_prices = {
    "Andhra Pradesh": 6, "Telangana": 6, "Karnataka": 7,
    "Tamil Nadu": 6, "Maharashtra": 8, "Delhi": 4
}

# ---------- INPUT ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚙️ Configure Your Usage</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    state = st.selectbox("State", list(state_prices.keys()))
    fan = st.slider("Fan (hrs)", 0, 24, 5)
    tv = st.slider("TV (hrs)", 0, 24, 3)

with c2:
    ac = st.slider("AC (hrs)", 0, 24, 2)
    light = st.slider("Lights (hrs)", 0, 24, 6)
    fridge = st.slider("Fridge (hrs)", 0, 24, 24)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- MULTIPLE APPLIANCES ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">➕ Add Appliances</div>', unsafe_allow_html=True)

if "appliances" not in st.session_state:
    st.session_state.appliances = []

col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("Appliance Name")

with col2:
    watt = st.number_input("Wattage (W)", min_value=0)

with col3:
    hours = st.slider("Hours", 0, 24, 1)

if st.button("Add Appliance"):
    if name and watt > 0:
        st.session_state.appliances.append((name, watt, hours))
        st.success(f"{name} added!")
    else:
        st.warning("Enter valid details")

total_custom_units = 0
custom_labels = []
custom_values = []

for n, w, h in st.session_state.appliances:
    units = (w * h) / 1000
    total_custom_units += units
    custom_labels.append(n)
    custom_values.append(units)
    st.markdown(f"• {n} → {units:.2f} units/day")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- CALCULATIONS ----------
cost = state_prices[state]

fan_u = (75 * fan)/1000
ac_u = (1500 * ac)/1000
light_u = (20 * light)/1000
tv_u = (100 * tv)/1000
fridge_u = (200 * fridge)/1000

labels = ["Fan", "AC", "Lights", "TV", "Fridge"] + custom_labels
values = [fan_u, ac_u, light_u, tv_u, fridge_u] + custom_values

daily_units = sum(values)
daily_bill = daily_units * cost
monthly_bill = daily_units * 30 * cost

score = max(0, 100 - (daily_units * 2))

# ---------- KPI CARDS ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ Daily Units</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric">{daily_units:.2f}</div>', unsafe_allow_html=True)
    st.caption(f"₹{daily_bill:.0f} per day")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💸 Monthly Bill</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric">₹{monthly_bill:.0f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ Energy Score</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric">{score}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- BAR CHART ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Appliance Usage Breakdown</div>', unsafe_allow_html=True)

chart_df = pd.DataFrame({
    "Appliance": labels,
    "Units": values
}).sort_values(by="Units", ascending=False)

st.bar_chart(chart_df.set_index("Appliance"))

st.caption("Higher bar = more electricity consumption")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- TOP CONSUMER FEATURE ----------
top_index = values.index(max(values))
top_appliance = labels[top_index]
top_units = values[top_index]
top_monthly_cost = top_units * 30 * cost
top_percent = (top_units / daily_units) * 100 if daily_units else 0

st.markdown(f"""
<div class="warning-box">
⚠️ <b>{top_appliance}</b> is your highest energy consumer <br><br>
Consumes <b>{top_percent:.0f}%</b> of total usage <br>
Costs approx <b>₹{int(top_monthly_cost)}</b> per month
</div>
""", unsafe_allow_html=True)

# ---------- SAVINGS ----------
potential_savings = monthly_bill * 0.2

st.markdown(f"""
<div class="highlight">
🔥 You can save ₹{int(potential_savings)} per month! <br>
Optimize usage and reduce unnecessary consumption ⚡
</div>
""", unsafe_allow_html=True)

# ---------- INSIGHTS ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🤖 Smart Insights</div>', unsafe_allow_html=True)

st.markdown(f'<div class="suggestion">Your highest consumption comes from {top_appliance}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="suggestion">Reducing its usage can save up to ₹{int(potential_savings)}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)