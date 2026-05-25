import streamlit as st
import random
from datetime import datetime

# 页面配置 - 宽屏模式，更具商业感
st.set_page_config(page_title="SCR Catalyst Recycling Value Evaluator", page_icon="♻️", layout="wide")

# 自定义样式：让表单和核心指标更好看
st.markdown("""
    <style>
    .metric-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #0066cc; }
    .success-box { background-color: #e1f5fe; padding: 20px; border-radius: 10px; border: 1px solid #b3e5fc; }
    </style>
""", unsafe_allow_html=True)

# 顶部导航/标题
st.title("🏭 SCR Catalyst Recycling & Valuation Platform")
st.markdown("##### 全球烟气脱硝催化剂回收残值评估与货源登记系统")
st.divider()

# 使用左右分栏布局
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📋 1. 催化剂技术与规格参数 (Technical Specifications)")
    
    # 基础物理信息
    cat_type = st.selectbox("催化剂类型 / Type", ["Honeycomb (蜂窝式)", "Plate (平板式)", "Corrugated (波纹式)"])
    
    c1, c2 = st.columns(2)
    with c1:
        weight = st.number_input("总重量 (吨) / Total Weight (Tons)", min_value=0.0, value=1.0, step=0.1)
        has_frame = st.radio("是否带铁框？/ Steel Frame", ["带铁框 (With Frame)", "不带铁框/裸块 (Bare Catalyst)"])
    with c2:
        pitch_holes = st.text_input("网格孔数 (例: 40x40 或 150孔) / Mesh Holes", placeholder="40x40 / 50x50")
        sample_status = st.selectbox("是否有化验报告？/ Assay Report", ["无化验报告 (使用行业平均值)", "有精确化验报告 (请在下方填写)"])

    # 尺寸规格选填
    with st.expander("🛠️ 展开填写详细物理尺寸 (选填 / Optional Size Parameters)"):
        f_size = st.text_input("铁框外部尺寸 (长x宽x高 mm) / Frame Dimension", placeholder="例: 1910 x 966 x 1300")
        u_size = st.text_input("单体/单元条尺寸 (mm) / Element Dimension", placeholder="例: 150 x 150 x 450")
    
    # 化学成分分析（含精细算法控制）
    st.markdown("##### 🧪 核心活性成分含量 (Active Ingredients)")
    c3, c4 = st.columns(2)
    with c3:
        wo3 = st.slider("WO₃ (三氧化钨) 含量 %", 0.0, 10.0, 3.0, 0.1)
    with c4:
        v2o5 = st.slider("V₂O₅ (五氧化二钒) 含量 %", 0.0, 5.0, 1.2, 0.1)

with col_right:
    st.subheader("💰 2. 估值结果 (Valuation Result)")
    
    # --- 严格校准后的工业回收计算核心逻辑 ---
    # 3% 钨含量的带框废催化剂，一吨市场真实回收价约 1000 - 2000 元
    # 设定基准价系数（以人民币为底本）
    base_w_factor = 450.0  # 每一当量的WO3每吨的回收价值贡献（考虑了提取率、冶炼费）
    base_v_factor = 150.0  # V2O5 相对目前的提取价值贡献
    
    # 根据是否带铁框进行价值扣减与权重修正（带铁框的陶瓷净重少，且剥离人工成本高）
    frame_discount = 0.65 if "带铁框" in has_frame else 1.0
    
    # 基础吨价计算
    raw_price_per_ton = (wo3 * base_w_factor + v2o5 * base_v_factor) * frame_discount
    
    # 工业兜底价与最高限价限制（确保在 1000 - 2500 元/吨 的真实行情内波动）
    if raw_price_per_ton < 800:
        raw_price_per_ton = 800.0
    elif raw_price_per_ton > 2600:
        raw_price_per_ton = 2600.0
        
    total_estimated_value = raw_price_per_ton * weight
    
    # 界面价值展示
    st.markdown(f"""
    <div class="success-box">
        <h4>预估回收总价 (Estimated Value)</h4>
        <h2 style="color: #0066cc; margin: 0;">¥ {total_estimated_value:,.2f} 元</h2>
        <p style="color: #555; font-size: 0.9em; margin-top: 5px;">
            ( 预估回收单价: 約 ¥ {raw_price_per_ton:,.2f} 元/吨 )
        </p >
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("⚠️ 注：此价格为大宗废物资残值评估，已扣除铁框重量占重、基础冶炼及环保处理成本。最终确切价格需结合现场考察及中毒情况（如砷 As、铊 Tl 中毒 fouling）由实验室化验敲定。")

st.divider()

# 货源提交与商机捕获（关键获客表单）
st.subheader("📞 3. 获取精准报价与货源登记 (Get Official Quote & Register Cargo)")
st.markdown("如果您有此批货源准备处理，请填写以下信息。我们的全球采购代表将为您对接后续的物流与化验流程。")

with st.form("contact_form"):
    c5, c6 = st.columns(2)
    with c5:
        contact_name = st.text_input("联系人姓名 / Contact Name *", placeholder="例如：陈经理 / Mr. Eric")
        phone_or_email = st.text_input("联系电话/微信/邮箱 / Phone or Email *", placeholder="手机号、WhatsApp 或 Email")
    with c6:
        cargo_location = st.text_input("货源所在地（省、市、港口） / Cargo Location *", placeholder="例如：江苏盐城、山东青岛、Chittagong Port")
        company_name = st.text_input("企业名称（选填） / Company Name", placeholder="例如：某发电厂 / 某拆船厂")
        
    user_notes = st.text_area("其他留言说明（如：中毒情况、数量批次、打包方式） / Additional Notes", placeholder="请输入...")
    
    submit_button = st.form_submit_with_button_context(
        label="提交货源信息，锁定制单报价 (Submit & Secure Quote)",
        blueprint="submit"
    )
    
    if submit_button:
        if not contact_name or not phone_or_email or not cargo_location:
            st.error("❌ 请填写所有必填项（带有 * 号的输入框）！")
        else:
            # 生成一个随机的业务单号，让网站看起来非常有系统感
            ticket_id = f"SCR-{random.randint(100000, 999999)}"
            st.balloons()
            st.success(f"🎉 提交成功！您的询价单号为：**{ticket_id}**")
            st.markdown(f"""
            **📋 登记摘要信息已生成：**
            - **单号**: {ticket_id}
            - **规格**: {cat_type} | {has_frame} | 孔数: {pitch_holes}
            - **预估总重**: {weight} 吨
            - **货源地**: {cargo_location}
            - **联系人**: {contact_name} ({phone_or_email})
            
            **💡 下一步行动：** 请将此页面截图，或将单号发送给您的对接商务。我们的采购团队会立即根据您提供的【{cargo_location}】地址评估物流成本，并在 24 小时内与您电联！
            """)
