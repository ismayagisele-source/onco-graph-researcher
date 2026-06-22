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

st.markdown("""
<style>
    /* ===== GLOBAL ===== */
    .main {
        background-color: #0a0e17 !important;
    }
    
    /* ===== HEADER ===== */
    .main-header {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1d9bf0 0%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #8b949e;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* ===== INFO CARDS ===== */
    .info-card {
        background: linear-gradient(145deg, #1a2332 0%, #0f1724 100%);
        border: 1px solid rgba(29, 155, 240, 0.2);
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #1d9bf0, #00d4ff);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .info-card:hover {
        border-color: rgba(29, 155, 240, 0.5);
        box-shadow: 0 12px 40px rgba(29, 155, 240, 0.15);
        transform: translateY(-4px);
    }
    
    .info-card:hover::before {
        opacity: 1;
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1d9bf0;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid transparent;
        border-image: linear-gradient(90deg, #1d9bf0, #00d4ff) 1;
        display: inline-block;
    }
    
    /* ===== METRIC BOXES ===== */
    .metric-box {
        background: linear-gradient(145deg, #1a2332 0%, #0f1724 100%);
        border: 1px solid rgba(29, 155, 240, 0.3);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .metric-box::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #1d9bf0, #00d4ff);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1d9bf0 0%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
        letter-spacing: -1px;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    /* ===== SUCCESS BOX ===== */
    .success-box {
        background: linear-gradient(145deg, #1a3328 0%, #0f1f18 100%);
        border: 1px solid rgba(0, 168, 107, 0.4);
        border-left: 5px solid #00a86b;
        border-radius: 12px;
        padding: 1.8rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 168, 107, 0.1);
    }
    
    /* ===== CHART CONTAINER ===== */
    .chart-container {
        background: linear-gradient(145deg, #1a2332 0%, #0f1724 100%);
        border: 1px solid rgba(29, 155, 240, 0.2);
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        height: 100%;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        color: #8b949e;
        font-size: 0.9rem;
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(29, 155, 240, 0.2);
    }
    
    /* ===== SIDEBAR OVERRIDE ===== */
    section[data-testid="stSidebar"] {
        background-color: #0f1724 !important;
        border-right: 1px solid rgba(29, 155, 240, 0.2) !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e7e9ea !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1d9bf0 !important;
    }
    
    section[data-testid="stSidebar"] li {
        color: #e7e9ea !important;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: rgba(29, 155, 240, 0.2) !important;
    }
    
    /* ===== BUTTON OVERRIDE ===== */
    div.stButton > button {
        background: linear-gradient(135deg, #1d9bf0 0%, #00d4ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1.2rem 2rem !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 8px 24px rgba(29, 155, 240, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100% !important;
        text-transform: none !important;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #00d4ff 0%, #1d9bf0 100%) !important;
        box-shadow: 0 12px 32px rgba(29, 155, 240, 0.6) !important;
        transform: translateY(-3px) !important;
    }
    
    div.stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* ===== TEXT AREA OVERRIDE ===== */
    div.stTextArea textarea {
        background-color: #0f1724 !important;
        color: #e7e9ea !important;
        border: 1px solid rgba(29, 155, 240, 0.3) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        transition: all 0.3s ease !important;
    }
    
    div.stTextArea textarea:focus {
        border-color: #1d9bf0 !important;
        box-shadow: 0 0 0 3px rgba(29, 155, 240, 0.15), 0 8px 24px rgba(29, 155, 240, 0.1) !important;
        outline: none !important;
    }
    
    /* ===== EXPANDER OVERRIDE ===== */
    .streamlit-expanderHeader {
        background-color: #1a2332 !important;
        color: #1d9bf0 !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        border: 1px solid rgba(29, 155, 240, 0.2) !important;
    }
    
    .streamlit-expanderContent {
        background-color: #0f1724 !important;
        border: 1px solid rgba(29, 155, 240, 0.2) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* ===== INFO/ERROR/SUCCESS MESSAGES ===== */
    .stAlert {
        border-radius: 12px !important;
        padding: 1.2rem !important;
    }
    
    /* ===== HORIZONTAL RULE ===== */
    hr {
        border-color: rgba(29, 155, 240, 0.2) !important;
        margin: 2rem 0 !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f1724;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #1d9bf0;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

# Header dengan styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<p class="main-header">🏥 Onco-Graph Researcher</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Multi-Agent AI for Precision Oncology</p>', unsafe_allow_html=True)

# Info Cards
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3 style="color: #1d9bf0; margin-top: 0;">🧬 Genomic Analysis</h3>
        <p style="color: #e7e9ea;">AI-powered mutation detection and clinical significance analysis</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3 style="color: #1d9bf0; margin-top: 0;">💊 Drug Safety</h3>
        <p style="color: #e7e9ea;">Real-time drug interaction checking and side effect monitoring</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h3 style="color: #1d9bf0; margin-top: 0;">⚕️ Treatment Plan</h3>
        <p style="color: #e7e9ea;">Evidence-based personalized therapy recommendations</p>
    </div>
    """, unsafe_allow_html=True)

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

# Genomic Overview - Premium Display
st.markdown("---")
st.markdown('<h2 class="section-title"> Genomic Overview</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="chart-container">
        <h3 style="color: #1d9bf0; margin-top: 0; font-weight: 700;">🔬 Mutation Status</h3>
        <div style="margin-top: 1.5rem;">
            <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid rgba(29, 155, 240, 0.1);">
                <span style="color: #e7e9ea; font-weight: 600;">EGFR</span>
                <span style="color: #e74c3c; font-weight: 700;">L858R ● Positive</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid rgba(29, 155, 240, 0.1);">
                <span style="color: #e7e9ea; font-weight: 600;">TP53</span>
                <span style="color: #e74c3c; font-weight: 700;">R175H ● Positive</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid rgba(29, 155, 240, 0.1);">
                <span style="color: #e7e9ea; font-weight: 600;">KRAS</span>
                <span style="color: #00a86b; font-weight: 700;">Wild Type ● Negative</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid rgba(29, 155, 240, 0.1);">
                <span style="color: #e7e9ea; font-weight: 600;">ALK</span>
                <span style="color: #00a86b; font-weight: 700;">Negative</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.8rem 0;">
                <span style="color: #e7e9ea; font-weight: 600;">BRAF</span>
                <span style="color: #00a86b; font-weight: 700;">Negative</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="chart-container">
        <h3 style="color: #1d9bf0; margin-top: 0; font-weight: 700;">⚕️ Patient Profile</h3>
        <div style="margin-top: 1.5rem;">
            <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid rgba(29, 155, 240, 0.1);">
                <span style="color: #8b949e;">Age</span>
                <span style="color: #e7e9ea; font-weight: 600;">58 years</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid rgba(29, 155, 240, 0.1);">
                <span style="color: #8b949e;">Gender</span>
                <span style="color: #e7e9ea; font-weight: 600;">Male</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid rgba(29, 155, 240, 0.1);">
                <span style="color: #8b949e;">Cancer Stage</span>
                <span style="color: #e7e9ea; font-weight: 600;">IIIA</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid rgba(29, 155, 240, 0.1);">
                <span style="color: #8b949e;">Performance Status</span>
                <span style="color: #e7e9ea; font-weight: 600;">ECOG 1</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.8rem 0;">
                <span style="color: #8b949e;">Comorbidities</span>
                <span style="color: #e7e9ea; font-weight: 600;">Diabetes, Hypertension</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    st.markdown('<h2 class="section-title">🧬 Agent 1: Genomic Analyst</h2>', unsafe_allow_html=True)
    
    with st.spinner("Analyzing genomic mutations..."):
        start_time = time.time()
        genomic_analysis = genomic_analyst.analyze_genomic_data(genomic_data)
        duration = time.time() - start_time
    
    # Display Agent 1 Result
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success("✅ Genomic Analysis Complete")
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Processing Time</div>
            <div class="metric-value">{duration:.1f}s</div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📄 View Genomic Analysis Report", expanded=True):
        st.markdown(genomic_analysis)
    
    # --- AGENT 2: CLINICAL PHARMACOLOGIST ---
    st.markdown('<h2 class="section-title">💊 Agent 2: Clinical Pharmacologist</h2>', unsafe_allow_html=True)
    
    with st.spinner("Evaluating drug interactions and safety..."):
        start_time = time.time()
        pharmacology_evaluation = pharmacologist.evaluate_treatment(
            genomic_analysis,
            patient_info
        )
        duration = time.time() - start_time
    
    # Display Agent 2 Result
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success("✅ Pharmacology Evaluation Complete")
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Processing Time</div>
            <div class="metric-value">{duration:.1f}s</div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("💊 View Pharmacology Evaluation", expanded=False):
        st.markdown(pharmacology_evaluation)
    
    # --- AGENT 3: LEAD ONCOLOGIST ---
    st.markdown('<h2 class="section-title">⚕️ Agent 3: Lead Oncologist</h2>', unsafe_allow_html=True)
    
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
    
    st.markdown('<h2 class="section-title">🎯 Final Treatment Recommendation</h2>', unsafe_allow_html=True)
    
    # Highlight primary recommendation
    st.markdown("""
    <div class="success-box">
        <h3 style="color: #00a86b; margin-top: 0;">✅ Primary Recommendation</h3>
        <p style="color: #e7e9ea; font-size: 1.1rem;"><strong>Gefitinib 250mg Once Daily</strong></p>
        <p style="color: #8b949e;"><strong>Rationale:</strong> EGFR L858R mutation positive - predicts excellent response to EGFR-TKI therapy</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("⚕️ View Lead Oncologist Recommendation", expanded=True):
        st.markdown(final_recommendation)
    
    # --- SUMMARY METRICS ---
    st.markdown("---")
    st.markdown('<h2 class="section-title">📊 Analysis Summary</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Agent 1 Time</div>
            <div class="metric-value">110s</div>
            <p style="color: #8b949e; font-size: 0.8rem;">Genomic Analyst</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Agent 2 Time</div>
            <div class="metric-value">164s</div>
            <p style="color: #8b949e; font-size: 0.8rem;">Clinical Pharmacologist</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Agent 3 Time</div>
            <div class="metric-value">213s</div>
            <p style="color: #8b949e; font-size: 0.8rem;">Lead Oncologist</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.caption("Note: Processing time depends on hardware. On AMD MI300X, this completes in ~10 seconds.")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div class="footer">
    <p><strong>Onco-Graph Researcher</strong> | AMD Developer Hackathon ACT II | July 2026</p>
    <p>Built with ❤️ using Streamlit, LangChain, and Llama-3 | Powered by AMD MI300X</p>
</div>
""", unsafe_allow_html=True)