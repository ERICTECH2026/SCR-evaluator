import streamlit as st
import random

# Page Configuration - Commercial Wide Layout
st.set_page_config(page_title="Global SCR Catalyst Valuation Platform", page_icon="♻️", layout="wide")

# Custom Professional UI Styles
st.markdown("""
    <style>
    .metric-box { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 6px solid #0066cc; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .valuation-box { background-color: #e3f2fd; padding: 25px; border-radius: 12px; border: 1px solid #90caf9; text-align: center; }
    .form-container { background-color: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("🏭 Global SCR Catalyst Recycling & Valuation Platform")
st.markdown("##### Real-time industrial de-NOx catalyst residual value estimation and cargo registration system.")
st.divider()

# Layout Split: Left for Inputs, Right for Valuation
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📋 1. Technical & Physical Specifications")
    
    # Core Specifications
    cat_type = st.selectbox("Catalyst Type", ["Honeycomb Type", "Plate Type", "Corrugated Type"])
    
    c1, c2 = st.columns(2)
    with c1:
        weight = st.number_input("Total Weight (Metric Tons)", min_value=0.0, value=1.0, step=0.1)
        has_frame = st.radio("Casing Condition", ["With Steel Frame / Module", "Bare Catalyst Blocks / Loose"])
    with c2:
        pitch_holes = st.text_input("Mesh Pitch / Number of Holes (e.g., 40x40, 50x50)", placeholder="e.g., 40x40")
        sample_status = st.selectbox("Assay Report Availability", ["No Report (Use Industry Average)", "Certified Assay Available"])

    # Physical Dimensions (Expanded Options)
    with st.expander("🛠️ Optional: Advanced Dimensions (Frame & Element Size)"):
        f_size = st.text_input("Outer Steel Frame Dimension (L x W x H mm)", placeholder="e.g., 1910 x 966 x 1300")
        u_size = st.text_input("Single Element / Pitch Size (mm)", placeholder="e.g., 150 x 150 x 450")
    
    # Chemical Composition Analysis
    st.markdown("##### 🧪 Active Chemical Ingredients (%)")
    c3, c4 = st.columns(2)
    with c3:
        wo3 = st.slider("WO₃ (Tungsten Trioxide) Content %", 0.0, 10.0, 3.0, 0.1)
    with c4:
        v2o5 = st.slider("V₂O₅ (Vanadium Pentoxide) Content %", 0.0, 5.0, 1.2, 0.1)

with col_right:
    st.subheader("💰 2. Instant Valuation Estimate")
    
    # --- Strictly Calibrated SCR Industrial Recycling Pricing Algorithm ---
    # Realistic market price for 3% WO3 with frame ranges between 1000 - 2000 RMB (~140 - 280 USD) per ton.
    # Base valuation factors per 1% content per ton (in USD equivalent)
    base_w_factor = 65.0   # Contribution of WO3 after extraction efficiency and smelting deductions
    base_v_factor = 20.0   # Contribution of V2O5 
    
    # Casings with steel frames significantly increase labor costs for stripping and reduce net catalyst weight
    frame_discount = 0.65 if "With Steel Frame" in has_frame else 1.0
    
    # Price per ton calculation
    price_per_ton = (wo3 * base_w_factor + v2o5 * base_v_factor) * frame_discount
    
    # Market price floor and ceiling safeguards (approx. $140 - $350 USD per ton)
    if price_per_ton < 140.0:
        price_per_ton = 140.0
    elif price_per_ton > 350.0:
        price_per_ton = 350.0
        
    total_estimated_value = price_per_ton * weight
    
    # UI Display for Valuation
    st.markdown(f"""
    <div class="valuation-box">
        <h4 style="color: #1565c0; margin-bottom: 5px;">Estimated Residual Value (FOB)</h4>
        <h1 style="color: #0d47a1; margin: 0;">$ {total_estimated_value:,.2f} USD</h1>
        <p style="color: #555; font-size: 0.95em; margin-top: 8px;">
            ( Estimated Unit Price: <strong>$ {price_per_ton:,.2f} USD / Ton</strong> )
        </p >
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("⚠️ **Disclaimer:** This estimation is a bulk commodity residual value asset appraisal, net of steel casing weight deductions, processing, smelting, and environmental disposal costs. Final commercial quotes depend heavily on verified lab assays and catalyst poisoning analysis (e.g., Arsenic As, Thallium Tl, Barium Ba fouling).")

st.divider()

# --- 3.0 Lead Generation & Formspree Email Integration ---
st.subheader("📞 3. Request Official Inspection & Secured Quotation")
st.markdown("If you possess this cargo and are looking for an authorized refiner/buyer, please register your cargo details below. Our global procurement desk will review the logistics and assay requirements.")

# Formspree Endpoint URL verified and integrated
FORMSPREE_ENDPOINT = "https://formspree.io/f/xeedlnrv"

# HTML Form Design embedded into Streamlit for direct email submission
form_html = f"""
<form action="{FORMSPREE_ENDPOINT}" method="POST" class="form-container">
    <input type="hidden" name="_subject" value="New Global SCR Cargo Lead!">
    <input type="hidden" name="[System] Catalyst Type" value="{cat_type}">
    <input type="hidden" name="[System] Est. Total Weight" value="{weight} Tons">
    <input type="hidden" name="[System] Has Frame" value="{has_frame}">
    <input type="hidden" name="[System] Pitch/Holes" value="{pitch_holes}">
    <input type="hidden" name="[System] Frame Size" value="{f_size}">
    <input type="hidden" name="[System] Element Size" value="{u_size}">
    <input type="hidden" name="[System] WO3 %" value="{wo3}%">
    <input type="hidden" name="[System] V2O5 %" value="{v2o5}%">
    <input type="hidden" name="[System] Est. Total Value" value="${total_estimated_value:,.2f} USD">

    <div style="display: flex; gap: 20px; margin-bottom: 15px;">
        <div style="flex: 1;">
            <label style="font-weight: bold; display:block; margin-bottom:5px;">Contact Person Name *</label>
            <input type="text" name="Contact Name" required placeholder="e.g., Mr. Eric / Procurement Manager" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
        </div>
        <div style="flex: 1;">
            <label style="font-weight: bold; display:block; margin-bottom:5px;">Phone / WhatsApp / Email *</label>
            <input type="text" name="Contact Method" required placeholder="e.g., +86 138... / info@powerplant.com" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
        </div>
    </div>

    <div style="display: flex; gap: 20px; margin-bottom: 15px;">
        <div style="flex: 1;">
            <label style="font-weight: bold; display:block; margin-bottom:5px;">Cargo Location (City, Province, Port) *</label>
            <input type="text" name="Cargo Location" required placeholder="e.g., Shandong, China / Chittagong Port, Bangladesh" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
        </div>
        <div style="flex: 1;">
            <label style="font-weight: bold; display:block; margin-bottom:5px;">Company Name (Optional)</label>
            <input type="text" name="Company Name" placeholder="e.g., Global Shipping Ltd / Energy Plant" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
        </div>
    </div>

    <div style="margin-bottom: 20px;">
        <label style="font-weight: bold; display:block; margin-bottom:5px;">Additional Notes (e.g., Poisoning status, batch size, packaging, loading port)</label>
        <textarea name="User Notes" rows="4" placeholder="Describe any known deactivation factors or logistics requirements..." style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;"></textarea>
    </div>

    <button type="submit" style="background-color: #0066cc; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%;">
        Submit Cargo Details & Lock Quotation Estimate
    </button>
</form>
"""

# Render the HTML form
st.components.v1.html(form_html, height=450, scrolling=False)
