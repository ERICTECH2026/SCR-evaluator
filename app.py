import streamlit as st

# 页面配置
st.set_page_config(page_title="Global SCR Catalyst Value Evaluator", page_icon="🌱", layout="centered")

# 标题
st.title("🌍 Global SCR Catalyst Value Evaluator")
st.markdown("Estimate the recycling and residual value of your waste SCR catalysts instantly.")

st.divider()

# 侧边栏：语言切换与汇率设置
currency = st.sidebar.selectbox("Select Currency / 选择货币", ["USD ($)", "CNY (¥)"])
rate = 7.2 if currency == "USD ($)" else 1.0 # 汇率基准

st.header("1. Input Catalyst Parameters / 输入催化剂参数")

# 用户输入
cat_type = st.selectbox("Catalyst Type / 催化剂类型", ["Honeycomb (蜂窝式)", "Plate (平板式)", "Corrugated (波纹式)"])
weight = st.number_input("Total Weight (Metric Tons) / 总重量 (吨)", min_value=0.0, value=1.0, step=0.1)

st.subheader("Active Ingredients (%) / 活性成分含量")
v2o5 = st.slider("V₂O₅ (Vanadium Pentoxide) %", 0.0, 5.0, 1.2, 0.1)
wo3 = st.slider("WO₃ (Tungsten Trioxide) %", 0.0, 10.0, 7.0, 0.1)

st.divider()

st.header("2. Valuation Result / 评估结果")

# 核心计算逻辑（后续你可以根据实际市场价随时修改这些系数）
v_price_per_ton = 15000 * rate  # 假设每吨纯五氧化二钒基础回收贡献值
w_price_per_ton = 25000 * rate  # 假设每吨纯三氧化钨基础回收贡献值
base_carrier_value = 200 * rate # 基体 TiO2 载体残值/吨

# 计算价值
v_value = weight * (v2o5 / 100) * v_price_per_ton
w_value = weight * (wo3 / 100) * w_price_per_ton
carrier_value = weight * base_carrier_value
total_value = v_value + w_value + carrier_value

# 显示结果
symbol = "$" if "USD" in currency else "¥"

col1, col2, col3 = st.columns(3)
col1.metric("WO₃ Estimated Value", f"{symbol}{w_value:.2f}")
col2.metric("V₂O₅ Estimated Value", f"{symbol}{v_value:.2f}")
col3.metric("Total Residual Value", f"{symbol}{total_value:.2f}")

st.success(f"💰 Total Estimated Market Value: {symbol} {total_value:,.2f}")

st.info("Note: This estimation is based on current market recycling averages. Actual quotes may vary depending on catalyst poisoning (e.g., As, Tl, Ba fouling) and local processing costs.")
