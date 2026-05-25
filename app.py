import streamlit as st
import requests

# Page Configuration - Commercial Wide Layout
st.set_page_config(page_title="Global SCR Catalyst Valuation Platform", page_icon="♻️", layout="wide")

# Custom Professional UI Styles
st.markdown("""
    <style>
    .metric-box { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 6px solid #0066cc; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .valuation-box { background-color: #e3f2fd; padding: 25px; border-radius: 12px; border: 1px solid #90caf9; text-align: center; }
    .form-container { background-color: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #e0e0e0; }
    .contact-card { background-color: #f1f8e9; padding: 20px; border-radius: 10px; border: 1px solid #c5e1a5; margin-top: 15px; }
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
    base_w_factor = 65.0   # Contribution of WO3 after extraction efficiency and smelting deductions
    base_v_factor = 20.0   # Contribution of V2O5 
    
    frame_discount = 0.65 if "With Steel Frame" in has_frame else 1.0
    price_per_ton = (wo3 * base_w_factor + v2o5 * base_v_factor) * frame_discount
    
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

# --- 3.1 Streamlit Native Form with Backend Requests Integration ---
st.subheader("📞 3. Request Official Inspection & Secured Quotation")
st.markdown("If you possess this cargo and are looking for an authorized refiner/buyer, please register your cargo details below.")

# Use Streamlit's native form component for rock-solid stability
with st.form("secure_quote_form", clear_on_submit=False):
    c5, c6 = st.columns(2)
    with c5:
        contact_name = st.text_input("Contact Person Name *", placeholder="e.g., Mr. Eric / Procurement Manager")
        phone_or_email = st.text_input("Phone / WhatsApp / Email *", placeholder="e.g., +86 138... / info@powerplant.com")
    with c6:
        cargo_location = st.text_input("Cargo Location (City, Province, Port) *", placeholder="e.g., Shandong, China / Chittagong Port, Bangladesh")
        company_name = st.text_input("Company Name (Optional)", placeholder="e.g., Global Shipping Ltd / Energy Plant")
        
    user_notes = st.text_area("Additional Notes (e.g., Poisoning status, batch size, packaging, loading port)", placeholder="Describe any known deactivation factors...")
    
    # Submit Button
    submitted = st.form_submit_button("Submit Cargo Details & Lock Quotation Estimate", type="primary")

    if submitted:
        if not contact_name or not phone_or_email or not cargo_location:
            st.error("❌ Please fill out all required fields marked with *")
        else:
            # Prepare data payload for Formspree
            payload = {
                "Contact Name": contact_name,
                "Contact Method": phone_or_email,
                "Cargo Location": cargo_location,
                "Company Name": company_name,
                "User Notes": user_notes,
                "[System] Catalyst Type": cat_type,
                "[System] Est. Total Weight": f"{weight} Tons",
                "[System] Has Frame": has_frame,
                "[System] Pitch/Holes": pitch_holes,
                "[System] Frame Size": f_size if f_size else "Not Provided",
                "[System] Element Size": u_size if u_size else "Not Provided",
                "[System] WO3 %": f"{wo3}%",
                "[System] V2O5 %": f"{v2o5}%",
                "[System] Est. Total Value": f"${total_estimated_value:,.2f} USD"
            }
            
            # Formspree Endpoint URL
            FORMSPREE_ENDPOINT = "https://formspree.io/f/xeedlnrv"
            
            # Send the request directly from server side
            try:
                response = requests.post(FORMSPREE_ENDPOINT, json=payload)
                if response.status_code == 200:
                    st.balloons()
                    st.success("🎉 Success! Your cargo details have been securely transmitted to our procurement desk.")
                    st.markdown("""
                    **Next Steps:**
                    Our global sourcing team will review your cargo location and technical specs to estimate logistics costs. We will contact you via your provided details within 24 hours.
                    """)
                else:
                    st.error(f"⚠️ System busy (Error {response.status_code}). Please try again later or contact us directly.")
            except Exception as e:
                st.error("📡 Network timeout. Please check your network or try again.")

st.divider()

# --- 4.0 Official Contact Directory (Footer Component) ---
st.subheader("🏢 4. Direct Global Procurement Desk")
st.markdown("You can also contact our head office directly via the hotlines below for immediate commercial consultations.")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown("""
    <div style="background-color: #f4f6f9; padding: 15px; border-radius: 8px; border-top: 4px solid #25d366;">
        <h5 style="color: #128c7e; margin-top:0;">🟢 WhatsApp Business</h5>
        <p style="font-size: 1.1em; margin-bottom:5px;"><strong>+44 7756516976</strong></p >
        <span style="color: #666; font-size: 0.85em;">Global Sourcing (English Service)</span>
    </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown("""
    <div style="background-color: #f4f6f9; padding: 15px; border-radius: 8px; border-top: 4px solid #07c160;">
        <h5 style="color: #07c160; margin-top:0;">🟢 WeChat & China Hotline</h5>
        <p style="font-size: 1.1em; margin-bottom:5px;"><strong>+86 13951489801</strong></p >
        <span style="color: #666; font-size: 0.85em;">微信同号 (中文服务/国内大宗回收)</span>
    </div>
    """, unsafe_allow_html=True)

with col_info3:
    st.markdown("""
    <div style="background-color: #f4f6f9; padding: 15px; border-radius: 8px; border-top: 4px solid #ea4335;">
        <h5 style="color: #ea4335; margin-top:0;">🔴 Official Email</h5>
        <p style="font-size: 1.1em; margin-bottom:5px;"><strong>ericshen19872025@gmail.com</strong></p >
        <span style="color: #666; font-size: 0.85em;">Assay Reports & Logistics Documents</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #999; font-size: 0.85em;'>© 2026 SCR Catalyst Recycling & Refined Metals Processing Group. All Rights Reserved.</p >", unsafe_allow_html=True)
