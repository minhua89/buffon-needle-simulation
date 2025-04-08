import streamlit as st
import numpy as np
import plotly.graph_objs as go
import math

st.set_page_config(layout="wide")
st.title("🎯 布豐投針模擬 - Buffon's Needle Simulation (Tabs 版)")

st.markdown("""
這是一個結合數學、模擬與視覺化的經典問題。  
你將看到紅針模擬、π 估算變化，並理解大數法則的威力 📉
""")

# -------------------------------
# 🎛️ 側邊欄參數：分開控制兩個 Tabs 的試驗次數
# -------------------------------
st.sidebar.header("模擬參數")

# Tab1 的針數（動畫限制最多 500）
trials_tab1 = st.sidebar.slider("Tab1：紅針模擬針數", 10, 500, 100, step=10)

# Tab2 的總模擬次數（估算折線圖）
trials_tab2 = st.sidebar.slider("Tab2：π估算模擬次數", 1000, 100000, 10000, step=1000)

# 共用參數
needle_length = st.sidebar.slider("針長 (l)", 0.1, 2.0, 1.0, 0.1)
line_distance = st.sidebar.slider("線距 (d)", 0.2, 3.0, 2.0, 0.1)

# -------------------------------
# Tabs 區域
# -------------------------------
tab1, tab2 = st.tabs(["🔴 紅針模擬圖", "📈 π估算折線圖"])

# -------------------------------
# 🔴 Tab1：紅針與平行線模擬圖
# -------------------------------
with tab1:
    st.subheader("🔴 模擬紅針與黑色平行線的視覺圖")

    center_y = np.random.uniform(0, line_distance, trials_tab1)
    center_x = np.random.uniform(0, 10, trials_tab1)
    angles = np.random.uniform(0, np.pi, trials_tab1)

    x0 = center_x - (needle_length / 2) * np.cos(angles)
    x1 = center_x + (needle_length / 2) * np.cos(angles)
    y0 = center_y - (needle_length / 2) * np.sin(angles)
    y1 = center_y + (needle_length / 2) * np.sin(angles)

    hits = np.sum((y0 // line_distance) != (y1 // line_distance))
    pi_estimate = (2 * needle_length * trials_tab1) / (line_distance * hits) if hits > 0 else 0

    fig1 = go.Figure()
    fig1.add_shape(type="line", x0=0, x1=12, y0=0, y1=0, line=dict(color="black", width=2))
    fig1.add_shape(type="line", x0=0, x1=12, y0=line_distance, y1=line_distance, line=dict(color="black", width=2))

    for i in range(trials_tab1):
        fig1.add_shape(type="line",
                       x0=x0[i], y0=y0[i],
                       x1=x1[i], y1=y1[i],
                       line=dict(color="red", width=2))

    fig1.update_layout(title=f"模擬丟針 {trials_tab1} 次 - 估算 π ≈ {pi_estimate:.5f}",
                       xaxis=dict(range=[0, 12]),
                       yaxis=dict(range=[-1, line_distance + 1]),
                       height=500)
    st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 📈 Tab2：π估算折線圖（每1000次一次估算）
# -------------------------------
with tab2:
    st.subheader("📈 每 1000 次模擬估算一次 π")

    y_dist = np.random.uniform(0, line_distance / 2, trials_tab2)
    angs = np.random.uniform(0, math.pi / 2, trials_tab2)

    trial_steps = np.arange(1000, trials_tab2 + 1, 1000)
    est_pis = []

    for n in trial_steps:
        y_part = y_dist[:n]
        angle_part = angs[:n]
        hits_temp = np.sum(y_part <= (needle_length / 2) * np.sin(angle_part))
        pi_est = (2 * needle_length * n) / (line_distance * hits_temp) if hits_temp > 0 else 0
        est_pis.append(pi_est)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=trial_steps, y=est_pis, mode='lines+markers', name='Estimated π'))
    fig2.add_trace(go.Scatter(x=trial_steps, y=[math.pi]*len(trial_steps),
                              mode='lines', name='True π ≈ 3.1416',
                              line=dict(dash='dash', color='red')))
    fig2.update_layout(title="π 估算值隨試驗進行變化",
                       xaxis_title="試驗次數",
                       yaxis_title="估算 π",
                       height=500)
    st.plotly_chart(fig2, use_container_width=True)
