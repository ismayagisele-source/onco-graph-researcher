"""
Clinical Pharmacologist Agent
Checks drug interactions, side effects, and dosage recommendations
"""

import ollama

class ClinicalPharmacologist:
    def __init__(self):
        self.name = "Clinical Pharmacologist"
        self.model = "llama3"
        self.system_prompt = """You are a Clinical Pharmacologist AI agent specialized in oncology pharmacology.
Your task is to evaluate drug recommendations from genomic analysis and provide:
1. Drug interaction checks
2. Side effect analysis
3. Dosage recommendations
4. Alternative treatments if needed
CRITICAL INSTRUCTION: You MUST provide your entire response in ENGLISH language only. Do not use any other language.
Always consider patient safety and evidence-based medicine."""
    
    def evaluate_treatment(self, genomic_analysis: str, patient_info: str) -> str:
        """Evaluate treatment recommendations based on genomic analysis"""
        
        prompt = f"""Based on the following genomic analysis and patient information, evaluate the treatment recommendations:

Patient Information:
{patient_info}

Genomic Analysis Report:
{genomic_analysis}

Please provide:
1. Drug interaction analysis (check for contraindications)
2. Common side effects of recommended drugs
3. Recommended dosage and administration
4. Alternative treatments if primary options are not suitable
5. Monitoring recommendations during treatment
6. Overall safety assessment"""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response['message']['content']


# Test the agent
if __name__ == "__main__":
    # Sample patient information
    patient_info = """
    Patient ID: P001
    Age: 58
    Gender: Male
    Weight: 70 kg
    Height: 170 cm
    Kidney Function: Normal (Creatinine 1.0 mg/dL)
    Liver Function: Normal (ALT 25 U/L, AST 22 U/L)
    Allergies: None known
    Current Medications: 
    - Metformin 500mg twice daily (for diabetes)
    - Lisinopril 10mg once daily (for hypertension)
    """
    
    # Sample genomic analysis from Agent 1
    genomic_analysis = """
    Mutations Found:
    - EGFR L858R (exon 21): Activating mutation
    - TP53 R175H (exon 5): Loss-of-function mutation
    
    Recommended Targeted Therapies:
    - Gefitinib (Iressa) 250mg once daily
    - Erlotinib (Tarceva) 150mg once daily
    
    Clinical Significance:
    - EGFR L858R predicts good response to EGFR TKIs
    - TP53 mutation indicates poor prognosis
    """
    
    # Create agent instance
    pharmacologist = ClinicalPharmacologist()
    
    # Evaluate treatment
    print("💊 Clinical Pharmacologist Agent - Treatment Evaluation\n")
    print("=" * 60)
    evaluation = pharmacologist.evaluate_treatment(genomic_analysis, patient_info)
    print(evaluation)
    print("=" * 60)