# 🧬 Onco-Graph Researcher

### Multi-Agent AI System for Precision Oncology  
**Powered by AMD Instinct MI300X • Gemma 4 31B • GLM 5.2 Fast via Fireworks AI**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![AMD](https://img.shields.io/badge/Hardware-AMD_MI300X_192GB-ED1C24?logo=amd)](https://www.amd.com/)
[![Fireworks AI](https://img.shields.io/badge/Inference-Fireworks_AI-FF6B35)](https://fireworks.ai/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?logo=chainlink)](https://langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **Onco-Graph Researcher** delivers **clinical-grade precision oncology recommendations** in under 60 seconds by analyzing histopathology images, genomic profiles, and patient clinical data. Built for the **AMD Developer Hackathon ACT II 2026**.

---

##  Problem Statement

Precision oncology requires synthesizing complex multimodal data (pathology images, genomic sequencing, clinical history) — a task that traditionally demands a multidisciplinary tumor board of 4-6 specialists and hours of analysis. This creates:
- **Delayed treatment decisions** (days to weeks)
- **Inconsistent recommendations** across institutions
- **Limited access** to expert-level precision medicine in resource-constrained settings

## 💡 Solution

Onco-Graph Researcher deploys **4 specialized AI agents** working in a coordinated pipeline:

| Agent | Role | Model | Infrastructure |
|-------|------|-------|----------------|
| **Agent 0** | Multimodal Pathologist | Gemma 4 31B IT | 🟢 AMD MI300X (Local) |
| **Agent 1** | Genomic Analyst | GLM 5.2 Fast | ⚡ Fireworks AI |
| **Agent 2** | Clinical Pharmacologist | GLM 5.2 Fast | ⚡ Fireworks AI |
| **Agent 3** | Lead Oncologist | GLM 5.2 Fast | ⚡ Fireworks AI |

---

## 🏗️ System Architecture

Patient Image → [Agent 0: Gemma 4 on AMD MI300X] → Pathology Report
↓
Genomic Data → [Agent 1: GLM 5.2] → Genomic Analysis
↓
Clinical Data → [Agent 2: GLM 5.2] → Pharmacology Evaluation
↓
[Agent 3: GLM 5.2] → Final Treatment Recommendation + Primary Drug Card


### 🔒 Hybrid Deployment Strategy

**Local (Privacy & Vision):**
- **Hardware:** AMD Instinct MI300X (192GB HBM3)
- **Model:** Google Gemma 4 31B IT
- **Purpose:** Processes sensitive histopathology images locally (HIPAA-compliant)

**Cloud (Reasoning & Scale):**
- **Provider:** Fireworks AI
- **Model:** GLM 5.2 Fast (1M Context Window)
- **Purpose:** Powers clinical reasoning agents with massive context

---

## 🚀 Features

- **🔬 Multimodal Pathology Analysis** — Gemma 4 analyzes H&E and IHC stained slides
- **🧬 Genomic Interpretation** — Identifies actionable mutations (EGFR, KRAS, BRCA1, PIK3CA, TP53)
- **💊 Pharmacology Evaluation** — Drug interaction analysis with patient's current medications
- **⚕️ Evidence-Based Recommendations** — Aligned with NCCN/ESMO guidelines
- **🎯 Smart Primary Recommendation Card** — Auto-extracted drug regimen displayed prominently
- **⚡ Sub-60-Second Analysis** — Full pipeline completes in under 1 minute
- **🌐 Multi-Cancer Support** — Validated on Lung, Breast, and Colon adenocarcinoma

---

## 📊 Validated Clinical Cases

| Patient | Cancer Type | Key Mutations | Primary Recommendation |
|---------|-------------|---------------|------------------------|
| **P001** | Lung Adenocarcinoma (Stage IIIA) | EGFR L858R, TP53 R175H | **Osimertinib 80mg daily** |
| **P002** | Breast IDC (Stage IIIA, HER2+) | BRCA1, PIK3CA, TP53 | **T-DM1 3.6mg/kg q3w** |
| **P003** | Colon Adenocarcinoma (Stage IIB) | KRAS G12V, APC, TP53 | **CAPOX × 8 cycles** |

---

## 🛠️ Tech Stack

### Core
- **Python 3.10+**
- **Streamlit 1.35+**
- **LangChain 0.2+**

### AI Models
- **Gemma 4 31B IT** — Multimodal vision-language model (Google)
- **GLM 5.2 Fast** — Long-context reasoning model (Zhipu AI)

### Infrastructure
- **AMD Instinct MI300X** — 192GB HBM3 GPU for local inference
- **Fireworks AI** — Cloud inference with 1M context window
- **vLLM + ROCm** — High-performance serving stack

---

## 📦 Installation

### Prerequisites
- Python 3.10+
- Fireworks AI API key ([get one here](https://fireworks.ai))
- (Optional) AMD MI300X GPU server with ROCm

### Setup

```bash
# Clone repository
git clone https://github.com/ismayagisele-source/onco-graph-researcher.git
cd onco-graph-researcher

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your FIREWORKS_API_KEY

Running

streamlit run app.py

Open http://localhost:8501

📁 Project Structure

onco-graph-researcher/
├── app.py                          # Main Streamlit application
├── agents/
│   ├── gemma4_pathologist.py       # Agent 0
│   ├── genomic_analyst.py          # Agent 1
│   ├── clinical_pharmacologist.py  # Agent 2
│   └── moderator.py                # Agent 3
├── requirements.txt
├── .env.example
└── README.md

🎬 Demo Video
Watch the full system demo:
🔗 [Video Link] (update after submission)

📄 Documentation
Full technical report (PDF) available in repository:
📑 [Technical Report PDF]

🏆 Hackathon Submission
AMD Developer Hackathon ACT II 2026 on lablab.ai
Category: AI for Healthcare / Precision Medicine
Track: Unicorn Track
Description: Production-grade multi-agent AI for precision oncology using AMD MI300X GPU and Fireworks AI API.

👥 Team
Levin — Lead Developer & AI Architect

📜 License
MIT License — see LICENSE file.

⚠️ Disclaimer
Onco-Graph Researcher is a research prototype for hackathon demonstration. NOT intended for clinical use. All outputs should be reviewed by qualified oncology professionals.

<div align="center">

Built with ❤️ for precision oncology
Powered by AMD Instinct MI300X • Gemma 4 • GLM 5.2 • Fireworks AI
</div>