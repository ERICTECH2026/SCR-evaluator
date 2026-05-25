import requests
import streamlit as st


FORMSPREE_ENDPOINT = "https://formspree.io/f/xeedlnrv"

st.set_page_config(
    page_title="Global SCR Catalyst Recycling & Valuation",
    page_icon="♻️",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #f7fbf8 0%, #ffffff 45%, #f3faf6 100%);
            color: #20302a;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2.5rem;
            max-width: 1180px;
        }

        h1, h2, h3 {
            color: #12372a;
        }

        .hero {
            padding: 2rem;
            border: 1px solid #dce8e1;
            border-radius: 8px;
            background: #ffffff;
            box-shadow: 0 12px 34px rgba(18, 55, 42, 0.08);
        }

        .eyebrow {
            display: inline-block;
            color: #1f7a55;
            background: #eaf7ef;
            border: 1px solid #caead8;
            padding: 0.36rem 0.68rem;
            border-radius: 999px;
            font-size: 0.86rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .hero-title {
            font-size: 2.55rem;
            line-height: 1.08;
            font-weight: 800;
            color: #12372a;
            margin: 0 0 1rem 0;
        }

        .hero-copy {
            font-size: 1.08rem;
            max-width: 760px;
            color: #65736d;
            line-height: 1.65;
        }

        .trust-row {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-top: 1.25rem;
        }

        .trust-pill {
            background: #ffffff;
            border: 1px solid #dce8e1;
            border-radius: 999px;
            color: #12372a;
            padding: 0.52rem 0.78rem;
            font-size: 0.9rem;
            font-weight: 650;
        }

        .result-card {
            background: linear-gradient(135deg, #eaf7ef 0%, #eef7fb 100%);
            border: 1px solid #cfe9d9;
            border-radius: 8px;
            padding: 1.6rem;
            height: 100%;
        }

        .result-label {
            color: #1f7a55;
            font-size: 0.86rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .result-value {
            color: #12372a;
            font-size: 2.25rem;
            line-height: 1.05;
            font-weight: 850;
            margin-bottom: 0.65rem;
        }

        .result-card p {
            color: #65736d;
            line-height: 1.6;
        }

        .mini-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin-top: 1rem;
        }

        .mini-stat {
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid rgba(31, 122, 85, 0.14);
            border-radius: 8px;
            padding: 0.85rem;
        }

        .mini-stat strong {
            display: block;
            color: #12372a;
            font-size: 1.1rem;
        }

        .mini-stat span {
            color: #65736d;
            font-size: 0.82rem;
        }

        .contact-card {
            background: #ffffff;
            border: 1px solid #dce8e1;
            border-radius: 8px;
            padding: 1rem;
            min-height: 142px;
        }

        .contact-card h4 {
            margin: 0 0 0.45rem 0;
            color: #12372a;
        }

        .contact-card strong {
            color: #1f7a55;
            font-size: 1.08rem;
        }

        .contact-card p {
            color: #65736d;
            line-height: 1.55;
        }

        .fine-print {
            color: #7f8d87;
            font-size: 0.86rem;
            text-align: center;
            margin-top: 2rem;
        }

        div[data-testid="stForm"] {
            border: 1px solid #dce8e1;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.9);
            padding: 1.15rem;
        }

        div[data-testid="stFormSubmitButton"] button {
            border-radius: 8px;
            border: 0;
            background: #1f7a55;
            color: white;
            font-weight: 750;
            min-height: 2.9rem;
        }

        div[data-testid="stFormSubmitButton"] button:hover {
            background: #12372a;
            color: white;
            border: 0;
        }

        @media (max-width: 760px) {
            .hero {
                padding: 1.35rem;
            }

            .hero-title {
                font-size: 2rem;
            }

            .mini-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def calculate_valuation(weight, wo3, v2o5, has_frame):
    base_w_factor = 65.0
    base_v_factor = 20.0
    frame_discount = 0.65 if has_frame == "With Steel Frame" else 1.0

    price_per_ton = (wo3 * base_w_factor + v2o5 * base_v_factor) * frame_discount
    price_per_ton = max(140.0, min(price_per_ton, 350.0))
    total_estimated_value = price_per_ton * weight

    return price_per_ton, total_estimated_value


st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">Global SCR Catalyst Recycling</div>
        <div class="hero-title">Estimate the recycling value of used SCR catalyst cargo.</div>
        <p class="hero-copy">
            A simple valuation and inquiry platform for power plants, cement plants, steel mills,
            glass manufacturers, chemical facilities, traders, and logistics partners handling used
            SCR denitration catalyst.
        </p>
        <div class="trust-row">
            <div class="trust-pill">Resource recovery</div>
            <div class="trust-pill">Global procurement</div>
            <div class="trust-pill">Assay-based quotation</div>
            <div class="trust-pill">Lower disposal pressure</div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.write("")

left, right = st.columns([1.08, 0.92], gap="large")

with left:
    st.markdown("### 1. Cargo & Catalyst Details")
    st.markdown(
        "Enter the basic cargo information below. The estimate is for preliminary screening only. "
        "Final pricing depends on assay, logistics, packing condition, moisture, contamination, and local compliance requirements."
    )

    c1, c2 = st.columns(2)

    with c1:
        cat_type = st.selectbox(
            "Catalyst Type",
            ["Honeycomb Catalyst", "Plate Catalyst", "Corrugated Catalyst", "Mixed / Unknown"],
        )
        weight = st.number_input(
            "Estimated Total Weight (metric tons)",
            min_value=1.0,
            max_value=5000.0,
            value=20.0,
            step=1.0,
        )
        has_frame = st.radio(
            "Steel Frame / Casing",
            ["Without Steel Frame", "With Steel Frame"],
            horizontal=True,
        )

    with c2:
        pitch_holes = st.text_input(
            "Pitch / Holes",
            placeholder="e.g., 18 holes, 20 holes, 7.4 mm pitch",
        )
        f_size = st.text_input(
            "Frame Size",
            placeholder="e.g., 1500 x 1000 x 1000 mm",
        )
        u_size = st.text_input(
            "Element Size",
            placeholder="e.g., 150 x 150 x 1000 mm",
        )

    e1, e2 = st.columns(2)

    with e1:
        wo3 = st.slider("WO3 Content (%)", 0.0, 8.0, 3.0, 0.1)

    with e2:
        v2o5 = st.slider("V2O5 Content (%)", 0.0, 5.0, 1.0, 0.1)


price_per_ton, total_estimated_value = calculate_valuation(weight, wo3, v2o5, has_frame)

with right:
    st.markdown("### 2. Instant Valuation Estimate")
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">Estimated purchase value</div>
            <div class="result-value">${total_estimated_value:,.0f} USD</div>
            <p>
                Indicative buyer-side value before final inspection, sampling, refining deduction,
                inland transport, port fees, packing, and compliance costs.
            </p>
            <div class="mini-grid">
                <div class="mini-stat">
                    <strong>${price_per_ton:,.0f}</strong>
                    <span>USD / metric ton</span>
                </div>
                <div class="mini-stat">
                    <strong>{weight:,.0f} t</strong>
                    <span>Estimated cargo</span>
                </div>
                <div class="mini-stat">
                    <strong>{wo3:.1f}% / {v2o5:.1f}%</strong>
                    <span>WO3 / V2O5</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown("### 3. Request Official Inspection & Secured Quotation")
st.markdown(
    "If you possess this cargo and are looking for an authorized refiner or buyer, "
    "please register your cargo details below. Our global procurement desk will review "
    "the logistics route and assay requirements."
)

with st.form("secure_quote_form", clear_on_submit=False):
    c5, c6 = st.columns(2)

    with c5:
        contact_name = st.text_input(
            "Contact Person Name *",
            placeholder="e.g., Mr. Eric / Procurement Manager",
        )
        phone_or_email = st.text_input(
            "Phone / WhatsApp / Email *",
            placeholder="e.g., +86 138... / info@powerplant.com",
        )

    with c6:
        cargo_location = st.text_input(
            "Cargo Location (City, Province, Port) *",
            placeholder="e.g., Shandong, China / Chittagong Port, Bangladesh",
        )
        company_name = st.text_input(
            "Company Name (Optional)",
            placeholder="e.g., Global Shipping Ltd / Energy Plant",
        )

    user_notes = st.text_area(
        "Additional Notes",
        placeholder="Poisoning status, batch size, packaging, loading port, photos or assay availability...",
    )

    submitted = st.form_submit_button(
        "Submit Cargo Details & Lock Quotation Estimate",
        type="primary",
        use_container_width=True,
    )

    if submitted:
        if not contact_name or not phone_or_email or not cargo_location:
            st.error("Please fill out all required fields marked with *.")
        else:
            payload = {
                "Contact Name": contact_name,
                "Contact Method": phone_or_email,
                "Cargo Location": cargo_location,
                "Company Name": company_name,
                "User Notes": user_notes,
                "[System] Catalyst Type": cat_type,
                "[System] Est. Total Weight": f"{weight} Tons",
                "[System] Has Frame": has_frame,
                "[System] Pitch/Holes": pitch_holes or "Not Provided",
                "[System] Frame Size": f_size or "Not Provided",
                "[System] Element Size": u_size or "Not Provided",
                "[System] WO3 %": f"{wo3}%",
                "[System] V2O5 %": f"{v2o5}%",
                "[System] Est. Price Per Ton": f"${price_per_ton:,.2f} USD",
                "[System] Est. Total Value": f"${total_estimated_value:,.2f} USD",
            }

            try:
                response = requests.post(FORMSPREE_ENDPOINT, json=payload, timeout=12)

                if response.status_code in (200, 201, 202):
                    st.success(
                        "Success. Your cargo details have been securely transmitted to our procurement desk."
                    )
                    st.info(
                        "Next step: our sourcing team will review your cargo location and technical specs, "
                        "then contact you within 24 hours."
                    )
                else:
                    st.error(
                        f"System busy. Error {response.status_code}. Please try again later or contact us directly."
                    )

            except requests.RequestException:
                st.error("Network timeout. Please check your connection or contact us directly.")

st.divider()

st.markdown("### 4. Direct Global Procurement Desk")
st.markdown("For immediate commercial consultation, contact our sourcing team directly.")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown(
        """
        <div class="contact-card">
            <h4>WhatsApp Business</h4>
            <strong>+44 7756516976</strong>
            <p>Global sourcing desk with English service.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_info2:
    st.markdown(
        """
        <div class="contact-card">
            <h4>WeChat & China Hotline</h4>
            <strong>+86 13951489801</strong>
            <p>微信同号，中文服务，国内大宗回收咨询。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_info3:
    st.markdown(
        """
        <div class="contact-card">
            <h4>Official Email</h4>
            <strong>ericshen19872025@gmail.com</strong>
            <p>Assay reports, cargo photos, and logistics documents.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <p class="fine-print">
        © 2026 SCR Catalyst Recycling & Refined Metals Processing Group.
        Preliminary estimates are not binding offers.
    </p>
    """,
    unsafe_allow_html=True,
)
