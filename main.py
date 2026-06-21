"""
Onco-Graph Researcher - Main Application
Multi-agent AI system for cancer drug repurposing
"""

import sys
import os

# Add parent directory to path so we can import agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.genomic_analyst import GenomicAnalyst
from agents.clinical_pharmacologist import ClinicalPharmacologist
from agents.moderator import LeadOncologist

def run_analysis():
    """Run the complete multi-agent analysis pipeline"""
    
    print("=" * 70)
    print("🏥 ONCO-GRAPH RESEARCHER - Multi-Agent Analysis System")
    print("=" * 70)
    print("\nStarting analysis pipeline...\n")
    
    # Sample patient data
    patient_info = """
    Patient ID: P001
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
    - Type 2 Diabetes (controlled with Metformin)
    - Hypertension (controlled with Lisinopril)
    """
    
    genomic_data = """
    Patient ID: P001
    Age: 58
    Gender: Male
    Cancer Type: Lung Adenocarcinoma
    
    Genomic Findings:
    - EGFR L858R mutation detected (exon 21)
    - TP53 R175H mutation detected (exon 5)
    - KRAS wild type (no mutation)
    - ALK negative
    - BRAF V600E negative
    """
    
    # Initialize agents
    print(" Initializing AI Agents...")
    genomic_analyst = GenomicAnalyst()
    pharmacologist = ClinicalPharmacologist()
    oncologist = LeadOncologist()
    print("✅ All agents initialized successfully!\n")
    
    # Step 1: Genomic Analysis
    print("=" * 70)
    print("🧬 STEP 1: Genomic Analyst Agent")
    print("=" * 70)
    genomic_analysis = genomic_analyst.analyze_genomic_data(genomic_data)
    print(genomic_analysis)
    print("\n")
    
    # Step 2: Pharmacology Evaluation
    print("=" * 70)
    print("💊 STEP 2: Clinical Pharmacologist Agent")
    print("=" * 70)
    pharmacology_evaluation = pharmacologist.evaluate_treatment(
        genomic_analysis, 
        patient_info
    )
    print(pharmacology_evaluation)
    print("\n")
    
    # Step 3: Final Recommendation
    print("=" * 70)
    print("‍⚕️ STEP 3: Lead Oncologist Agent - Final Recommendation")
    print("=" * 70)
    final_recommendation = oncologist.synthesize_recommendation(
        genomic_analysis,
        pharmacology_evaluation,
        patient_info
    )
    print(final_recommendation)
    print("\n")
    
    print("=" * 70)
    print("✅ Analysis Complete!")
    print("=" * 70)

if __name__ == "__main__":
    run_analysis()