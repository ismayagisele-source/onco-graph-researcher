"""
Onco-Graph Researcher - Main Application
Multi-agent AI system for precision oncology
"""

import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.gemma4_pathologist import Gemma4Pathologist
from agents.genomic_analyst import GenomicAnalyst
from agents.clinical_pharmacologist import ClinicalPharmacologist
from agents.moderator import LeadOncologist

def load_patient_data(patient_id="P001"):
    """Load patient data from JSON templates"""
    template_path = os.path.join("data", "templates", f"patient_{patient_id}.json")
    with open(template_path, 'r') as f:
        return json.load(f)

def run_analysis(patient_id="P001"):
    """Run the complete multi-agent analysis pipeline"""
    
    print("=" * 70)
    print("🏥 ONCO-GRAPH RESEARCHER - Multi-Agent Analysis System")
    print(f"📋 Analyzing Patient: {patient_id}")
    print("=" * 70)
    
    # Load patient data
    print("\n📂 Loading patient data from templates...")
    patient_data = load_patient_data(patient_id)
    print(f"✅ Loaded data for {patient_data['clinical']['diagnosis']}\n")
    
    # Initialize agents
    print("🤖 Initializing AI Agents...")
    pathologist = Gemma4Pathologist()
    genomic_analyst = GenomicAnalyst()
    pharmacologist = ClinicalPharmacologist()
    oncologist = LeadOncologist()
    print("✅ All 4 agents initialized successfully!\n")
    
    # Step 0: Pathology Analysis
    print("=" * 70)
    print("🔬 STEP 0: Multimodal Pathologist (Gemma 4 on AMD MI300X)")
    print("=" * 70)
    # Note: Replace with actual image path if running locally
    pathology_report = pathologist.analyze_image("assets/sample_pathology.png") 
    print(pathology_report)
    print("\n")
    
    # Step 1: Genomic Analysis
    print("=" * 70)
    print("🧬 STEP 1: Genomic Analyst (GLM 5.2 via Fireworks AI)")
    print("=" * 70)
    genomic_analysis = genomic_analyst.analyze_genomic_data(patient_data['genomic'])
    print(genomic_analysis)
    print("\n")
    
    # Step 2: Pharmacology Evaluation
    print("=" * 70)
    print("💊 STEP 2: Clinical Pharmacologist (GLM 5.2 via Fireworks AI)")
    print("=" * 70)
    pharmacology_evaluation = pharmacologist.evaluate_treatment(
        genomic_analysis, 
        patient_data['clinical']
    )
    print(pharmacology_evaluation)
    print("\n")
    
    # Step 3: Final Recommendation
    print("=" * 70)
    print("️ STEP 3: Lead Oncologist (GLM 5.2 via Fireworks AI)")
    print("=" * 70)
    final_recommendation = oncologist.synthesize_recommendation(
        pathology_report,
        genomic_analysis,
        pharmacology_evaluation,
        patient_data['clinical']
    )
    print(final_recommendation)
    print("\n")
    
    print("=" * 70)
    print("✅ Analysis Complete!")
    print("=" * 70)

if __name__ == "__main__":
    # Usage: python main.py P001 (or P002, P003)
    patient_id = sys.argv[1] if len(sys.argv) > 1 else "P001"
    run_analysis(patient_id)