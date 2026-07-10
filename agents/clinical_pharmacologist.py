"""
Clinical Pharmacologist Agent
Checks drug interactions, side effects, and dosage recommendations
"""

import os
from dotenv import load_dotenv
from langchain_fireworks import ChatFireworks

load_dotenv()

class ClinicalPharmacologist:
    def __init__(self):
        self.name = "Clinical Pharmacologist"
        self.model = "accounts/fireworks/routers/glm-5p2-fast"
        self.system_prompt = """You are a Senior Clinical Pharmacologist AI agent with 20+ years of experience in oncology pharmacology.

YOUR TASK:
Evaluate the genomic analysis and patient data to provide a COMPREHENSIVE pharmacology evaluation report.

CRITICAL INSTRUCTIONS:
1. You MUST identify the recommended drugs from the genomic analysis (e.g., Osimertinib, Trastuzumab, T-DM1, CAPOX, Letrozole, etc.)
2. You MUST evaluate drug interactions with the patient's current medications
3. You MUST provide side effects, dosage, alternatives, and monitoring
4. You MUST NOT output any thinking process or internal reasoning
5. You MUST start your response IMMEDIATELY with "CLINICAL PHARMACOLOGY EVALUATION REPORT"
6. You MUST provide the report in ENGLISH only
7. Your response MUST be at least 500 words - be thorough and detailed

CRITICAL FORMATTING RULE:
DO NOT stop after the Patient Summary. You MUST continue and write out ALL 6 sections below in full detail. Do not summarize. Be thorough.

OUTPUT FORMAT (you MUST follow this structure exactly):

CLINICAL PHARMACOLOGY EVALUATION REPORT

[Patient ID, Age/Sex, Diagnosis, Genomic Profile, Clinical Context - keep this brief, max 5 lines]

1. DRUG INTERACTION ANALYSIS
[Detailed analysis of interactions between recommended drugs and patient's current medications. Explain the mechanism and clinical risk.]

2. SIDE EFFECT ANALYSIS
[Comprehensive list of common and serious side effects of recommended drugs. Include management strategies.]

3. DOSAGE AND ADMINISTRATION
[Specific dosage, route, frequency, and administration instructions for the primary recommended drugs.]

4. ALTERNATIVE TREATMENTS
[Alternative drugs if primary options are contraindicated or not tolerated.]

5. MONITORING RECOMMENDATIONS
[Labs, imaging, and clinical monitoring required during treatment.]

6. OVERALL SAFETY ASSESSMENT
[Final safety evaluation and risk-benefit analysis.]

Always prioritize patient safety and evidence-based medicine. Be thorough and professional."""
    
    def evaluate_treatment(self, genomic_analysis: str, patient_info: str) -> str:
        """Evaluate treatment recommendations based on genomic analysis"""
        
        prompt = f"""As a Senior Clinical Pharmacologist, provide a comprehensive pharmacology evaluation based on the data below.

PATIENT INFORMATION:
{patient_info}

GENOMIC ANALYSIS REPORT:
{genomic_analysis}

INSTRUCTIONS:
1. Identify the recommended targeted therapy/chemotherapy from the genomic analysis
2. Evaluate drug interactions with patient's current medications
3. Provide comprehensive side effect analysis
4. Specify dosage and administration
5. List alternative treatments
6. Provide monitoring recommendations
7. Give overall safety assessment

CRITICAL RULES:
- Start your response with "CLINICAL PHARMACOLOGY EVALUATION REPORT"
- Follow the 6-section format exactly
- DO NOT stop after the patient summary. You MUST write out all 6 sections
- Response must be at least 500 words
- Do NOT include any thinking process
- Provide the report in ENGLISH only
- Be thorough, detailed, and professional
"""
        
        try:
            model = ChatFireworks(
                model=self.model,
                fireworks_api_key=os.getenv("FIREWORKS_API_KEY"),
                temperature=0.3,
                max_tokens=6000  # Increased from 5000 to ensure full output
            )
            
            response = model.invoke([
                ("system", self.system_prompt),
                ("human", prompt)
            ])
            
            return response.content

        except Exception as e:
            error_msg = f"⚠️ Error during Pharmacology Evaluation: {str(e)}"
            print(error_msg)
            return error_msg