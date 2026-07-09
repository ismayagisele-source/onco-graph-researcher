"""
Onco-Graph Researcher - Web Application
Multi-Agent AI for Precision Oncology
Built with Streamlit
"""

import streamlit as st
import time
import os
import re
from agents.genomic_analyst import GenomicAnalyst
from agents.clinical_pharmacologist import ClinicalPharmacologist
from agents.moderator import LeadOncologist
from agents.gemma4_pathologist import Gemma4Pathologist

# ===== HELPER: Parse Genomic Data =====
def parse_genomic_data(genomic_text):
    """Parse genomic data and return dict of {gene: status}"""
    genes = {}
    lines = genomic_text.split('\n')
    in_findings = False
    for line in lines:
        line = line.strip()
        if 'Genomic Findings' in line or 'genomic findings' in line.lower():
            in_findings = True
            continue
        if in_findings and line.startswith('-'):
            line = line[1:].strip()
            # Extract gene name (first word or word before colon)
            parts = line.split(':')
            gene_name = parts[0].strip().split()[0].upper() if parts else ''
            status_text = parts[1].strip() if len(parts) > 1 else line
            
            # Determine status
            status_lower = status_text.lower()
            if any(x in status_lower for x in ['wild type', 'wildtype', 'not detected', 'negative', 'no mutation']):
                genes[gene_name] = ('Negative', '#00a86b')
            elif any(x in status_lower for x in ['detected', 'mutation', 'positive', 'pathogenic', 'missense', 'nonsense', 'frameshift']):
                genes[gene_name] = ('Positive', '#e74c3c')
            else:
                genes[gene_name] = (status_text[:30], '#f39c12')
    return genes

# ===== HELPER: Parse Clinical Data =====
def parse_clinical_data(clinical_text):
    """Parse clinical data and return dict of {field: value}"""
    fields = {}
    lines = clinical_text.split('\n')
    for line in lines:
        line = line.strip()
        if ':' in line and not line.startswith('-'):
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            fields[key] = val
    return fields

# ===== HELPER: Clean AI Output =====
def clean_ai_output(text, max_chars=None):
    """Remove AI thinking/verbose parts, NO truncation"""
    # Remove common thinking patterns
    thinking_patterns = [
        "Wait,", "Actually,", "Let me think", "Let's double check",
        "Let's refine", "Wait, the prompt", "Let me structure",
        "Let's draft", "Let me refine", "I must point out",
        "So the pharmacology", "Let's structure", "Let me check",
        "The user wants", "Since we don't know", "I need to frame"
    ]
    
    for pattern in thinking_patterns:
        idx = text.find(pattern)
        if idx > 200:  # Don't cut at beginning
            text = text[:idx]
            break
    
    # Remove lines that are clearly AI thinking
    lines = text.split('\n')
    cleaned_lines = []
    skip_block = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(('Wait,', 'Actually,', 'Let me ', "Let's ", "The user wants", "Since we don't", "I need to")):
            skip_block = True
            continue
        if skip_block and stripped == '':
            skip_block = False
            continue
        if not skip_block:
            cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # NO TRUNCATION - return full text
    return text

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
    
    /* ===== EXPANDER OVERRIDE - FIX LENGKAP ===== */
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
        width: 100% !important;
        max-width: 100% !important;
    }
    
    .streamlit-expanderContent p {
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        margin-bottom: 0.8rem !important;
        color: #e7e9ea !important;
        width: 100% !important;
        max-width: 100% !important;
        word-wrap: break-word !important;
    }
    
    .streamlit-expanderContent ul,
    .streamlit-expanderContent ol {
        margin-left: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    .streamlit-expanderContent li {
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        margin-bottom: 0.5rem !important;
        color: #e7e9ea !important;
    }
    
    .streamlit-expanderContent strong,
    .streamlit-expanderContent b {
        color: #1d9bf0 !important;
        font-weight: 600 !important;
    }
    
    /* ===== INFO/ERROR/SUCCESS MESSAGES ===== */
    .stAlert {
        border-radius: 12px !important;
        padding: 1.2rem !important;
    }
    
    /* ===== EQUAL HEIGHT TEXT AREAS ===== */
    div[data-testid="stTextArea"] {
        height: 280px !important;
    }
    
    div[data-testid="stTextArea"] textarea {
        height: 250px !important;
        min-height: 250px !important;
        max-height: 250px !important;
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
    - GLM 5.2 (Clinical Reasoning)
    - Gemma 4 31B IT (Multimodal Analysis)
    - AMD MI300X 192GB (Production)
    - Fireworks AI API (Deployment)
    """)
    
    st.markdown("---")
    st.markdown("**Hackathon:** AMD Developer Hackathon ACT II")
    st.markdown("**Track:** Unicorn (Healthcare)")
    st.markdown("**Developer:** Levin")
    st.markdown("---")
    st.markdown("### 📋 How to Use")
    st.info(
        "1. **Input Data:** Fill in the Clinical Profile and Genomic Mutations.\n"
        "2. **Run Analysis:** Click the button to start the multi-agent AI.\n"
        "3. **Review Results:** Check the final treatment recommendations."
    )
    
    st.markdown("---")
    st.warning(
        "⚠️ **DEMO PURPOSES ONLY**\n\n"
        "This system is for educational and research demonstration only.\n\n"
        "- NOT for clinical use or medical diagnosis\n"
        "- All patient data is fictional or from public sources\n"
        "- No real patient information is used\n"
        "- Complies with HIPAA regulations"
    )

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

# DISCLAIMER
st.warning(
    "⚠️ **DISCLAIMER:** This is a research prototype for hackathon demonstration only. "
    "NOT intended for clinical use or medical diagnosis. "
    "All patient data shown is fictional or from public domain sources. "
    "Complies with HIPAA regulations."
)

st.markdown("---")

# Medical Image Upload (Gemma 4)
st.subheader("🔬 Medical Image (Optional - Powered by Gemma 4 on AMD MI300X)")
uploaded_image = st.file_uploader("Upload Histopathology / CT Scan / MRI (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded Medical Image", width=300)

st.markdown("---")

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

# Genomic Overview - PROFESSIONAL DASHBOARD
st.markdown("---")
st.markdown('<h2 class="section-title">🧬 Genomic Overview</h2>', unsafe_allow_html=True)

# ===== Parse Clinical Data (FIXED: Support Bullet Points) =====
clinical_dict = {}
current_key = None
for line in patient_info.split('\n'):
    line_stripped = line.strip()
    # Jika baris memiliki titik dua dan bukan bullet point
    if ':' in line_stripped and not line_stripped.startswith('-'):
        key, value = line_stripped.split(':', 1)
        key = key.strip()
        value = value.strip()
        clinical_dict[key] = value
        current_key = key
    # Jika baris adalah bullet point, gabungkan ke key sebelumnya
    elif line_stripped.startswith('-') and current_key:
        clinical_dict[current_key] += " " + line_stripped[1:].strip()

# ===== Parse Genomic Data =====
mutations = {}
in_findings = False
for line in genomic_data.split('\n'):
    line = line.strip()
    if 'genomic findings' in line.lower():
        in_findings = True
        continue
    if in_findings and line.startswith('-'):
        line = line[1:].strip()
        if ':' in line:
            parts = line.split(':', 1)
            gene = parts[0].strip().upper()
            status_text = parts[1].strip().lower()
        else:
            parts = line.split()
            gene = parts[0].upper() if parts else ''
            status_text = ' '.join(parts[1:]).lower()
        
        negative_keywords = ['wildtype', 'wild type', 'not detected', 'negative', 'no mutation']
        positive_keywords = ['mutation', 'detected', 'positive', 'pathogenic', 'missense', 'nonsense', 'frameshift']
        
        is_negative = any(kw in status_text for kw in negative_keywords)
        is_positive = any(kw in status_text for kw in positive_keywords) and not is_negative
        
        mutations[gene] = {
            'status': 'Negative' if is_negative else ('Positive' if is_positive else 'Unknown'),
            'color': '#00a86b' if is_negative else ('#e74c3c' if is_positive else '#f39c12')
        }

# Smart Clinical Fields
priority_fields = [
    ('Cancer Type', 'Cancer Type'),
    ('Stage', 'Stage'),
    ('Performance Status', 'Performance'),
    ('Tumor Grade', 'Tumor Grade'),
    ('ER Status', 'ER Status'),
    ('PR Status', 'PR Status'),
    ('HER2 Status', 'HER2 Status'),
    ('Ki67 Index', 'Ki67 Index'),
    ('Menopausal Status', 'Menopausal'),
    ('MSI Status', 'MSI Status'),
    ('BRAF V600E', 'BRAF V600E'),
    ('Lymphovascular Invasion', 'LVI'),
    ('Margin Status', 'Margin Status'),
    ('Kidney Function', 'Kidney Function'),
    ('Liver Function', 'Liver Function'),
    ('Previous Treatment', 'Prior Treatment'),
    ('Surgery', 'Surgery Plan'),
    ('Adjuvant Therapy', 'Adjuvant Plan'),
    ('Current Medications', 'Current Meds'),
    ('Comorbidities', 'Comorbidities'),
]

right_items = []
for key, label in priority_fields:
    if key in clinical_dict and clinical_dict[key]: # Pastikan value tidak kosong
        right_items.append((label, clinical_dict[key]))

# HAPUS LOGIKA max_items YANG MEMOTONG FIELD PENTING!
# Biarkan semua field yang relevan muncul.

# ===== Layout: Independent Columns =====
col1, col2 = st.columns([4, 6])

# KOLOM KIRI: Mutation Status
with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#1d9bf0;margin-top:0;font-weight:700;font-size:1.1rem;">🔬 Mutation Status</h3>', unsafe_allow_html=True)
    if mutations:
        for gene, info in mutations.items():
            icon = "🟢" if info['status'] == 'Positive' else "⚪"
            st.markdown(f'<div style="display:flex;justify-content:space-between;padding:0.6rem 0;border-bottom:1px solid rgba(29,155,240,0.1);"><span style="color:#e7e9ea;font-weight:600;">{gene}</span><span style="color:{info["color"]};font-weight:700;">{icon} {info["status"]}</span></div>', unsafe_allow_html=True)
    else:
        st.info("No mutation data")
    st.markdown('</div>', unsafe_allow_html=True)

# KOLOM KANAN: Treatment Context
with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#1d9bf0;margin-top:0;font-weight:700;font-size:1.1rem;">⚕️ Treatment Context</h3>', unsafe_allow_html=True)
    if right_items:
        for label, value in right_items:
            st.markdown(f'<div style="display:flex;justify-content:space-between;padding:0.6rem 0;border-bottom:1px solid rgba(29,155,240,0.1);"><span style="color:#8b949e;">{label}</span><span style="color:#e7e9ea;font-weight:600;text-align:right;max-width:60%;">{value}</span></div>', unsafe_allow_html=True)
    else:
        st.info("No clinical context data found")
    st.markdown('</div>', unsafe_allow_html=True)


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
    
    # --- AGENT 0: MULTIMODAL PATHOLOGIST (GEMMA 4) ---
    pathology_report = ""
    time_agent0 = 0.0
    
    if uploaded_image is not None:
        st.markdown('<h2 class="section-title">🔬 Agent 0: Multimodal Pathologist (Gemma 4)</h2>', unsafe_allow_html=True)
        
        with st.spinner("Analyzing medical image on AMD MI300X (Gemma 4 31B)..."):
            temp_image_path = "temp_uploaded_image.jpg"
            with open(temp_image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
            
            start_time = time.time()
            pathologist = Gemma4Pathologist()
            pathology_report = pathologist.analyze_image(temp_image_path, clinical_context=patient_info)
            time_agent0 = time.time() - start_time
            
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success("✅ Multimodal Pathology Analysis Complete (AMD MI300X)")
        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Processing Time</div>
                <div class="metric-value">{time_agent0:.1f}s</div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("📄 View Pathology Report (Gemma 4)", expanded=True):
            st.markdown(pathology_report)
            
        st.markdown("---")

    # --- AGENT 1: GENOMIC ANALYST ---
    st.markdown('<h2 class="section-title">🧬 Agent 1: Genomic Analyst</h2>', unsafe_allow_html=True)
    
    with st.spinner("Analyzing genomic mutations..."):
        start_time = time.time()
        genomic_analysis = genomic_analyst.analyze_genomic_data(genomic_data)
        time_agent1 = time.time() - start_time
    
    # Display Agent 1 Result
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success("✅ Genomic Analysis Complete")
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Processing Time</div>
            <div class="metric-value">{time_agent1:.1f}s</div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📄 View Genomic Analysis Report", expanded=True):
        st.markdown(clean_ai_output(genomic_analysis))  # HAPUS , 2000
    
    # Gabungkan Laporan Genomik + Patologi (jika ada gambar)
    if pathology_report:
        combined_genomic_data = f"{genomic_analysis}\n\n--- MULTIMODAL PATHOLOGY REPORT (Gemma 4) ---\n{pathology_report}"
    else:
        combined_genomic_data = genomic_analysis
    
    # --- AGENT 2: CLINICAL PHARMACOLOGIST ---
    st.markdown('<h2 class="section-title">💊 Agent 2: Clinical Pharmacologist</h2>', unsafe_allow_html=True)
    
    with st.spinner("Evaluating drug interactions and safety..."):
        start_time = time.time()
        pharmacology_evaluation = pharmacologist.evaluate_treatment(
            combined_genomic_data,
            patient_info
        )
        time_agent2 = time.time() - start_time
    
    # Display Agent 2 Result
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success("✅ Pharmacology Evaluation Complete")
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Processing Time</div>
            <div class="metric-value">{time_agent2:.1f}s</div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("💊 View Pharmacology Evaluation", expanded=False):
        st.markdown(clean_ai_output(pharmacology_evaluation))  # HAPUS , 2000
    
    # --- AGENT 3: LEAD ONCOLOGIST ---
    st.markdown('<h2 class="section-title">⚕️ Agent 3: Lead Oncologist</h2>', unsafe_allow_html=True)
    
    with st.spinner("Synthesizing final treatment recommendation..."):
        start_time = time.time()
        final_recommendation = oncologist.synthesize_recommendation(
            combined_genomic_data,
            pharmacology_evaluation,
            patient_info
        )
        time_agent3 = time.time() - start_time
    
    # --- FINAL RESULT ---
    st.markdown("---")
    st.success("✅ Analysis Complete!")
    st.markdown('<h2 class="section-title">🎯 Final Treatment Recommendation</h2>', unsafe_allow_html=True)

    # Highlight primary recommendation
    primary_rec_text = "Consult Multidisciplinary Tumor Board"
    rationale_text = "Based on comprehensive genomic and clinical analysis."

    # Clean text first
    clean_rec = clean_ai_output(final_recommendation)

    # Pattern 1: Direct extraction after "Primary Recommendation"
    patterns = [
        r'(?:Primary Recommendation|✅ Primary Recommendation)[:\s]+([^\n]+)',
        r'(?:My )?(?:primary )?recommendation (?:is|should be)[:\s]+([^\n]+)',
        r'(?:Recommended (?:Treatment|Therapy))[:\s]+([^\n]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, clean_rec, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            # Skip if it looks like AI thinking
            if any(x in candidate.lower() for x in ['wait', 'actually', 'let me', 'i need', 'should address']):
                continue
            # Accept if it contains drug-related keywords
            if any(x in candidate.lower() for x in ['mg', 'daily', 'therapy', 'inhibitor', 'chemotherapy', 'treatment', 'trastuzumab', 'osimertinib', 'capox', 'folfox', 'tdm1', 'pertuzumab']):
                primary_rec_text = candidate
                break

    # Pattern 2: Fallback - search for specific drug names
    if primary_rec_text == "Consult Multidisciplinary Tumor Board":
        drug_patterns = [
            r'(Osimertinib \d+mg[^\n]*)',
            r'(Trastuzumab[^\n]*(?:\+ [^\n]+)?)',
            r'(T-DM1[^\n]*)',
            r'(CAPOX[^\n]*)',
            r'(FOLFOX[^\n]*)',
        ]
        for pattern in drug_patterns:
            match = re.search(pattern, clean_rec, re.IGNORECASE)
            if match:
                primary_rec_text = match.group(1).strip()
                break

    # Extract rationale
    rationale_match = re.search(r'Rationale:\s*([^\n]+)', clean_rec, re.IGNORECASE)
    if rationale_match:
        rationale_text = rationale_match.group(1).strip()
        if len(rationale_text) < 20 or any(x in rationale_text.lower() for x in ['insert', 'drug name']):
            rationale_text = "Based on comprehensive genomic and clinical analysis."

    # Display Primary Recommendation Card
    st.markdown(f"""
    <div class="success-box">
    <h3 style="color: #00a86b; margin-top: 0;">✅ Primary Recommendation</h3>
    <p style="color: #e7e9ea; font-size: 1.1rem;"><strong>{primary_rec_text}</strong></p>
    <p style="color: #8b949e;"><strong>Rationale:</strong> {rationale_text}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- NUCLEAR OPTION: Remove AI internal monologue ---
    clean_recommendation = final_recommendation
    cutoff_phrases = ["Wait,", "Actually,", "Let me think", "Let's double check", "Let's refine", "Wait, the prompt"]
    for phrase in cutoff_phrases:
        if phrase in clean_recommendation:
            idx = clean_recommendation.find(phrase)
            if idx > 100:
                clean_recommendation = clean_recommendation[:idx]
                break

    # Display full recommendation in expander
    with st.expander("⚕️ View Lead Oncologist Recommendation", expanded=True):
        st.markdown(clean_ai_output(clean_recommendation))

    # --- SUMMARY METRICS ---
    st.markdown("---")
    st.markdown('<h2 class="section-title">📊 Analysis Summary</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
        <div class="metric-label">Agent 1 Time</div>
        <div class="metric-value">{time_agent1:.1f}s</div>
        <p style="color: #8b949e; font-size: 0.8rem;">Genomic Analyst</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
        <div class="metric-label">Agent 2 Time</div>
        <div class="metric-value">{time_agent2:.1f}s</div>
        <p style="color: #8b949e; font-size: 0.8rem;">Clinical Pharmacologist</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-box">
        <div class="metric-label">Agent 3 Time</div>
        <div class="metric-value">{time_agent3:.1f}s</div>
        <p style="color: #8b949e; font-size: 0.8rem;">Lead Oncologist</p>
        </div>
        """, unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown("---")
    st.markdown("""
    <div class="footer">
    <p><strong>Onco-Graph Researcher</strong> | AMD Developer Hackathon ACT II | July 2026</p>
    <p>Built with ❤️ using Streamlit, LangChain, GLM 5.2 & Gemma 4 31B | Powered by AMD MI300X & Fireworks AI</p>
    </div>
    """, unsafe_allow_html=True)