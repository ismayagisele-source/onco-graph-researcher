"""
Lead Oncologist (Moderator) Agent
Synthesizes analysis from Genomic Analyst and Clinical Pharmacologist
Provides final treatment recommendations
"""

import ollama

class LeadOncologist:
    def __init__(self):
        self.name = "Lead Oncologist"
        self.model = "llama3"
        self.system_prompt = """You are a Lead Oncologist AI agent with 20+ years of experience in precision oncology.
Your task is to synthesize analysis from Genomic Analyst and Clinical Pharmacologist agents.
Provide final, actionable treatment recommendations for cancer patients.
Consider:
1. Genomic mutations and their clinical significance
2. Drug interactions and safety
3. Patient-specific factors (age, comorbidities, organ function)
4. Evidence-based treatment guidelines
5. Quality of life considerations
CRITICAL INSTRUCTION: You MUST provide your entire response in ENGLISH language only. Do not use any other language.
Always prioritize patient safety and efficacy."""
    
    def synthesize_recommendation(self, genomic_analysis: str, pharmacology_evaluation: str, patient_info: str) -> str:
        """Synthesize final recommendation from multiple agent analyses"""
        
        prompt = f"""As a Lead Oncologist, please synthesize the following analyses and provide a final treatment recommendation:

Patient Information:
{patient_info}

Genomic Analysis Report (from Genomic Analyst Agent):
{genomic_analysis}

Pharmacology Evaluation (from Clinical Pharmacologist Agent):
{pharmacology_evaluation}

Please provide a comprehensive final recommendation including:
1. Primary treatment recommendation (drug, dose, schedule)
2. Rationale for this recommendation (based on genomic profile)
3. Safety considerations and monitoring plan
4. Expected outcomes and prognosis
5. Alternative options if primary treatment fails
6. Multidisciplinary team coordination needs
7. Patient counseling points"""
        
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
    Cancer Type: Lung Adenocarcinoma (Stage IIIA)
    Performance Status: ECOG 1
    Kidney Function: Normal (Creatinine 1.0 mg/dL)
    Liver Function: Normal (ALT 25 U/L, AST 22 U/L)
    Allergies: None known
    Comorbidities: 
    - Type 2 Diabetes (controlled with Metformin)
    - Hypertension (controlled with Lisinopril)
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
    
    # Sample pharmacology evaluation from Agent 2
    pharmacology_evaluation = """
    Drug Interaction Analysis:
    - Gefitinib may inhibit metformin metabolism (dose reduction needed)
    - Erlotinib has no contraindication with lisinopril
    
    Side Effects:
    - Gefitinib: Pneumonia, skin rash, diarrhea, fatigue
    - Erlotinib: Acne-like rash, diarrhea, nausea, fatigue
    
    Recommended Dosage:
    - Gefitinib: 250mg once daily with food
    - Erlotinib: 150mg once daily with or without food
    
    Alternatives:
    - Afatinib (Gilotrif)
    - Alectinib (Alecenza)
    
    Monitoring:
    - Regular kidney and liver function tests
    - Monitor for side effects and contraindications
    - Tumor response and disease progression
    
    Safety Assessment:
    - TP53 mutation indicates poor prognosis
    - Close monitoring required for side effects
    """
    
    # Create agent instance
    oncologist = LeadOncologist()
    
    # Synthesize final recommendation
    print("‍⚕️ Lead Oncologist Agent - Final Treatment Recommendation\n")
    print("=" * 70)
    recommendation = oncologist.synthesize_recommendation(
        genomic_analysis, 
        pharmacology_evaluation, 
        patient_info
    )
    print(recommendation)
    print("=" * 70)