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
        © 2026 SCR Catalyst Recycling & Refined Metals Processing Group. Preliminary estimates are not binding offers.
    </p>
    """,
    unsafe_allow_html=True,
)
