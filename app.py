"""
Onco-Graph Researcher - Web Application
Multi-Agent AI for Precision Oncology
Built with Streamlit
"""

import streamlit as st
import time
from agents.genomic_analyst import GenomicAnalyst
from agents.clinical_pharmacologist import ClinicalPharmacologist
from agents.moderator import LeadOncologist

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Onco-Graph Researcher",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="main-header">🏥 Onco-Graph Researcher</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Multi-Agent AI System for Precision Oncology & Drug Repurposing</p>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **Onco-Graph Researcher** is a multi-agent AI system that:
    
    1. 🧬 Analyzes genomic data
    2. 💊 Evaluates drug interactions
    3. ⚕️ Provides treatment recommendations
    
    **Powered by:**
    - Llama-3 (Local Testing)
    - AMD MI300X 192GB (Production)
    """)
    
    st.markdown("---")
    st.markdown("**Hackathon:** AMD Developer Hackathon ACT II")
    st.markdown("**Track:** Unicorn (Healthcare)")
    st.markdown("**Developer:** Levin")

# --- SAMPLE DATA ---
default_patient_info = """Patient ID: P001
Age: 58
Gender: Male
Weight: 70 kg
Height: 170 cm
Cancer Type: Lung Adenocarcinoma (Stage IIIA)
Performance Status: ECOG 1
Kidney Function: Normal (Creatinine 1.0 mg/dL)
Liver Function: Normal (ALT 25 U/L, AST 22 U/L)
Allergies: None known
Comorbidities: 
- Type 2 Diabetes (controlled with Metformin 500mg BID)
- Hypertension (controlled with Lisinopril 10mg QD)"""

default_genomic_data = """Patient ID: P001
Cancer Type: Lung Adenocarcinoma

Genomic Findings:
- EGFR L858R mutation detected (exon 21)
- TP53 R175H mutation detected (exon 5)
- KRAS wild type (no mutation)
- ALK negative
- BRAF V600E negative
- ROS1 negative"""

# --- INPUT SECTION ---
st.markdown("---")
st.header("📋 Patient Data Input")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Clinical Information")
    patient_info = st.text_area(
        "Patient Clinical Data",
        value=default_patient_info,
        height=250,
        help="Enter patient demographics, comorbidities, and current medications"
    )

with col2:
    st.subheader("Genomic Data")
    genomic_data = st.text_area(
        "Genomic Sequencing Results",
        value=default_genomic_data,
        height=250,
        help="Enter genomic findings including mutations and biomarkers"
    )

# --- ANALYSIS BUTTON ---
st.markdown("---")
analyze_button = st.button(
    "🚀 Run Multi-Agent Analysis",
    type="primary",
    use_container_width=True
)

# --- ANALYSIS PIPELINE ---
if analyze_button:
    st.info("⏳ Initializing AI Agents... This may take several minutes on local hardware.")
    
    # Initialize agents
    genomic_analyst = GenomicAnalyst()
    pharmacologist = ClinicalPharmacologist()
    oncologist = LeadOncologist()
    
    # --- AGENT 1: GENOMIC ANALYST ---
    st.markdown("### 🧬 Agent 1: Genomic Analyst")
    with st.spinner("Analyzing genomic mutations..."):
        start_time = time.time()
        genomic_analysis = genomic_analyst.analyze_genomic_data(genomic_data)
        duration = time.time() - start_time
    
    with st.expander(f"📄 View Genomic Analysis Report ({duration:.1f}s)", expanded=True):
        st.markdown(genomic_analysis)
    
    # --- AGENT 2: CLINICAL PHARMACOLOGIST ---
    st.markdown("### 💊 Agent 2: Clinical Pharmacologist")
    with st.spinner("Evaluating drug interactions and safety..."):
        start_time = time.time()
        pharmacology_evaluation = pharmacologist.evaluate_treatment(
            genomic_analysis,
            patient_info
        )
        duration = time.time() - start_time
    
    with st.expander(f"💊 View Pharmacology Evaluation ({duration:.1f}s)", expanded=False):
        st.markdown(pharmacology_evaluation)
    
    # --- AGENT 3: LEAD ONCOLOGIST ---
    st.markdown("### ⚕️ Agent 3: Lead Oncologist")
    with st.spinner("Synthesizing final treatment recommendation..."):
        start_time = time.time()
        final_recommendation = oncologist.synthesize_recommendation(
            genomic_analysis,
            pharmacology_evaluation,
            patient_info
        )
        duration = time.time() - start_time
    
    # --- FINAL RESULT ---
    st.markdown("---")
    st.success("✅ Analysis Complete!")
    
    st.markdown("### 🎯 Final Treatment Recommendation")
    with st.expander("⚕️ View Lead Oncologist Recommendation", expanded=True):
        st.markdown(final_recommendation)
    
    # --- SUMMARY ---
    st.markdown("---")
    st.markdown("### 📊 Analysis Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Agent 1 Time", f"{duration:.1f}s", help="Genomic Analyst")
    
    with col2:
        st.metric("Agent 2 Time", f"{duration:.1f}s", help="Clinical Pharmacologist")
    
    with col3:
        st.metric("Agent 3 Time", f"{duration:.1f}s", help="Lead Oncologist")
    
    st.caption("Note: Processing time depends on hardware. On AMD MI300X, this completes in ~10 seconds.")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>Onco-Graph Researcher | AMD Developer Hackathon ACT II | July 2026</p>
        <p>Built with ❤️ using Streamlit, LangChain, and Llama-3</p>
    </div>
    """,
    unsafe_allow_html=True
)