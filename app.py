import pandas as pd
import streamlit as st

import compliance

# Page Config
st.set_page_config(page_title="DocuVerify | SpecGuard", layout="wide")

st.title("DocuVerify: Vendor Spec & Compliance Copilot")
st.caption(
    "Automated unstructured document extraction & compliance validation engine."
)
st.divider()

# Sidebar Ingestion Controls
st.sidebar.header("Document Ingestion")
uploaded_file = st.sidebar.file_uploader(
    "Upload Vendor Spec PDF", type=["pdf"]
)

st.sidebar.subheader("Or Select Demo Sample")
demo_choice = st.sidebar.selectbox(
    "Choose pre-loaded sample:",
    ["None", "compliant_sample.pdf", "non_compliant_sample.pdf"],
)

target_file = None

if uploaded_file is not None:
    target_file = uploaded_file
elif demo_choice != "None":
    target_file = demo_choice

if target_file:
    # Run Extraction & Rules Engine
    raw_text = compliance.extract_text_from_pdf(target_file)
    extracted_data = compliance.parse_spec_data(raw_text)
    compliance_results = compliance.check_compliance(extracted_data)

    # 2-Column Split Screen
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📄 Source Document Content")
        st.text_area(
            "Extracted Raw PDF Text",
            raw_text,
            height=380,
            disabled=True,
        )

    with col2:
        st.subheader("⚡ Human-in-the-Loop Verification")
        st.caption("Review extracted fields before committing to Dataverse.")

        with st.form("verification_form"):
            prod_name = st.text_input(
                "Product Name", value=extracted_data["product_name"]
            )
            abv_val = st.text_input(
                "Alcohol By Volume (ABV)", value=extracted_data["abv"]
            )
            net_vol = st.text_input(
                "Net Volume", value=extracted_data["net_volume"]
            )
            french_txt = st.text_input(
                "French Label Text", value=extracted_data["french_label"]
            )

            st.write("---")
            st.write("### Policy Checklist")

            df_compliance = pd.DataFrame(compliance_results)
            st.dataframe(df_compliance, use_container_width=True)

            submit_btn = st.form_submit_button(
                "Approve & Export Record to Dataverse"
            )

        if submit_btn:
            st.success(
                f"✅ Record for '{prod_name}' successfully validated and staged for Dataverse ingestion!"
            )
            st.json(
                {
                    "Product": prod_name,
                    "ABV": abv_val,
                    "Volume": net_vol,
                    "Status": "Approved",
                    "Target_System": "D365 / Dataverse Product Catalog",
                }
            )
else:
    st.info(
        "👈 Please upload a vendor spec PDF or select a demo sample from the sidebar to begin."
    )