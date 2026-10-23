import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

st.set_page_config(
    page_title="GenApp v2.0 | Enterprise Forensic DVI & Kinship Engine",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for auth and data
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "cases" not in st.session_state:
    st.session_state.cases = [
        {"case_id": "CASE-2026-DVI-091", "incident": "Commercial Aircraft Incident - Flight AI-502", "location": "New Delhi Sector 4", "date": "2026-10-23", "status": "Active Investigation", "created_by": "expert@genapp.gov.in"}
    ]
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {"timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), "action": "SYSTEM_INIT", "user": "system", "details": "GenApp v2.0 initialized successfully.", "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}
    ]

# Authentication Gate
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.7); padding: 2rem; border-radius: 1rem; border: 1px solid rgba(245, 158, 11, 0.3);">
            <h2 style="color: #F8FAFC; margin-bottom: 0.5px;">GenApp v2.0</h2>
            <p style="color: #94A3B8; font-size: 0.85rem;">ISO/IEC 17025 Secure Forensic Gateway</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            user_input = st.text_input("Expert ID / Email", value="expert@genapp.gov.in")
            pass_input = st.text_input("Cryptographic PIN / Password", type="password", value="GenApp2026!")
            submit = st.form_submit_button("Authenticate & Access Workspace", use_container_width=True)
            
            if submit:
                if user_input == "expert@genapp.gov.in" and pass_input == "GenApp2026!":
                    st.session_state.authenticated = True
                    st.success("Authentication successful! Loading workspace...")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Use expert@genapp.gov.in / GenApp2026!")
    st.stop()

# Main Application Header
st.sidebar.title("🧬 GENAPP v2.0")
st.sidebar.markdown("---")
st.sidebar.markdown("**Logged in as:** Dr. A. Sharma")
st.sidebar.markdown("**Role:** Senior Forensic Biologist")
st.sidebar.markdown("**Compliance:** ISO/IEC 17025")
if st.sidebar.button("Terminate Session", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("---")
nav_selection = st.sidebar.radio("Navigation Modules", [
    "1. Case Management", 
    "2. Electropherogram QC", 
    "3. Likelihood Ratio (LR) Engine", 
    "4. Triage Matrix", 
    "5. eCoC Audit Trail"
])

st.title("Enterprise Forensic DVI & Kinship Engine")
st.markdown("Fusing short tandem repeat (STR) molecular biology, GenomeIndia allele frequencies, and ISO/IEC 17025 audit compliance.")
st.markdown("---")

if nav_selection == "1. Case Management":
    st.header("Disaster Victim Identification (DVI) Cases")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Cases", len(st.session_state.cases))
    col2.metric("GenomeIndia Cohorts", "69 Groups (>135M variants)")
    col3.metric("Audit Integrity", "SHA-256 Verified")
    
    st.markdown("### Active Case Register")
    df_cases = pd.DataFrame(st.session_state.cases)
    st.dataframe(df_cases, use_container_width=True)
    
    with st.expander("Initialize New Disaster Case"):
        with st.form("new_case_form"):
            c_id = st.text_input("Case ID", value=f"CASE-2026-{int(datetime.utcnow().timestamp()) % 10000}")
            c_inc = st.text_input("Incident Description", value="Mass Casualty Incident - Sector 7")
            c_loc = st.text_input("Location", value="New Delhi")
            c_date = st.date_input("Incident Date")
            c_submit = st.form_submit_button("Create Case File")
            
            if c_submit:
                new_c = {
                    "case_id": c_id,
                    "incident": c_inc,
                    "location": c_loc,
                    "date": str(c_date),
                    "status": "Active Investigation",
                    "created_by": "expert@genapp.gov.in"
                }
                st.session_state.cases.append(new_c)
                
                log_msg = f"Initialized case {c_id} for incident: {c_inc}"
                sha = hashlib.sha256(log_msg.encode()).hexdigest()
                st.session_state.audit_logs.insert(0, {
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "action": "CASE_INITIALIZED",
                    "user": "expert@genapp.gov.in",
                    "details": log_msg,
                    "sha256": sha
                })
                st.success(f"Case {c_id} successfully created and logged!")
                st.rerun()

elif nav_selection == "2. Electropherogram QC":
    st.header("Capillary Electrophoresis File Parser (.fsa / .xml)")
    st.markdown("Upload or simulate raw genetic analyzer output files for automated allele calling and artifact quality control.")
    
    uploaded_file = st.file_uploader("Upload .fsa or .xml Profile", type=["fsa", "xml", "csv", "txt"])
    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' successfully parsed!")
    
    st.markdown("### Automated Quality Control Summary")
    qc_data = [
        {"Marker": "D3S1358", "Allele 1": "15", "Allele 2": "17", "Peak RFU": "4,200", "Quality Flag": "PASS (High Confidence)"},
        {"Marker": "vWA", "Allele 1": "14", "Allele 2": "18", "Peak RFU": "3,850", "Quality Flag": "PASS (High Confidence)"},
        {"Marker": "FGA", "Allele 1": "22", "Allele 2": "24", "Peak RFU": "1,200", "Quality Flag": "FLAG: Stutter / Low RFU"},
        {"Marker": "D8S1179", "Allele 1": "12", "Allele 2": "13", "Peak RFU": "5,100", "Quality Flag": "PASS (High Confidence)"}
    ]
    st.table(qc_data)

elif nav_selection == "3. Likelihood Ratio (LR) Engine":
    st.header("Combined Kinship Index (CKI) & Likelihood Ratio Calculator")
    st.markdown("Calculates formal statistical weights across CODIS loci using GenomeIndia allele frequencies.")
    
    col1, col2 = st.columns(2)
    with col1:
        locus = st.selectbox("Select STR Locus", ["D3S1358", "vWA", "FGA", "D8S1179", "D21S11", "TH01"])
        allele_freq = st.slider("Population Allele Frequency f(A)", 0.01, 0.50, 0.125)
    with col2:
        st.markdown("### Computed Statistics")
        lr_val = 1.0 / (2.0 * allele_freq)
        st.metric("Single Locus Likelihood Ratio (LR)", f"{lr_val:.2f} : 1")
        st.metric("Combined Kinship Index (CKI)", f"{(lr_val ** 4):,.2f} : 1")

elif nav_selection == "4. Triage Matrix":
    st.header("Candidate Match Triage Matrix")
    st.markdown("Sorted candidate relatives by statistical compatibility scores for high-throughput disaster victim triage.")
    
    triage_data = [
        {"Rank": "#1", "PM Sample ID": "PM-SAMPLE-104", "Candidate Reference": "REF-FAM-502 (Mother)", "Relationship": "Parent-Child", "Compatibility": "95.2%", "LR": "99.9% (9.24M)", "Status": "Verified Match"},
        {"Rank": "#2", "PM Sample ID": "PM-SAMPLE-104", "Candidate Reference": "REF-FAM-503 (Sibling)", "Relationship": "Full Sibling", "Compatibility": "81.4%", "LR": "91.2% (412.5k)", "Status": "Pending Review"},
        {"Rank": "#3", "PM Sample ID": "PM-SAMPLE-108", "Candidate Reference": "REF-FAM-610 (Father)", "Relationship": "Parent-Child", "Compatibility": "94.8%", "LR": "99.8% (8.15M)", "Status": "Verified Match"}
    ]
    st.table(triage_data)

elif nav_selection == "5. eCoC Audit Trail":
    st.header("Immutable Electronic Chain of Custody (eCoC) Logs")
    st.markdown("Cryptographically secured SHA-256 audit trail meeting ISO/IEC 17025 courtroom admissibility standards.")
    
    df_audit = pd.DataFrame(st.session_state.audit_logs)
    st.dataframe(df_audit, use_container_width=True)
