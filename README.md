**Onco-Graph Researcher** is a multi-agent AI system for cancer drug repurposing using genomic analysis and medical literature synthesis on AMD MI300X 192GB.

**The Challenge:**
- Drug discovery takes 10+ years and costs $2+ billion
- Oncologists need faster ways to find personalized treatments  
- Genomic data and medical literature are too vast to analyze manually

**Our Solution:**
A multi-agent AI system that:
1. Analyzes patient genomic data (DNA sequences)
2. Cross-references with medical literature and clinical trials
3. Recommends drug repurposing opportunities
4. Provides evidence-based citations

**System Architecture:**
- **Agent 1 (Genomic Analyst):** Identifies mutations (EGFR, KRAS, TP53)
- **Agent 2 (Clinical Pharmacologist):** Checks drug interactions & safety
- **Agent 3 (Lead Oncologist):** Synthesizes recommendations

**Technology Stack:**
- LLM: Llama-3 70B (via AMD MI300X)
- Framework: LangChain, Streamlit
- Vector DB: ChromaDB/FAISS
- Hardware: AMD Instinct MI300X 192GB VRAM

**Why AMD MI300X?**
Our architecture requires 175GB+ VRAM to load multiple models and large context windows simultaneously. NVIDIA H200 (141GB) would run out of memory. AMD MI300X (192GB) is the perfect fit.

**Team:**
Levin - Solo Developer

**Hackathon:**
AMD Developer Hackathon: ACT II - Track 3 (Unicorn)  
July 6-11, 2026

**Installation:**
```bash
pip install -r requirements.txt
streamlit run app.py
