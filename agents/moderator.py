"""
Lead Oncologist (Moderator) Agent
Synthesizes analysis from Genomic Analyst and Clinical Pharmacologist
Provides final treatment recommendations
"""

import os
from dotenv import load_dotenv
from langchain_fireworks import ChatFireworks

load_dotenv()

class LeadOncologist:
    def __init__(self):
        self.name = "Lead Oncologist"
        self.model = "accounts/fireworks/routers/glm-5p2-fast"
        self.system_prompt = """You are a Lead Oncologist with 20+ years of experience in precision oncology.
Synthesize the genomic analysis and pharmacology evaluation to provide a final treatment recommendation.

OUTPUT FORMAT (STRICT):
Line 1: ✅ Primary Recommendation: [Drug Name] [Dose] [Schedule]
Line 2: Rationale: [One sentence explaining why based on mutations]
Lines 3+: Detailed clinical report synthesizing all data

Start IMMEDIATELY with Line 1. No introductory text. English only."""
        
    def synthesize_recommendation(self, genomic_analysis: str, pharmacology_evaluation: str, patient_info: str) -> str:
        """Synthesize final recommendation from multiple agent analyses"""
        
        prompt = f"""Patient Information:
{patient_info}

Genomic Analysis Report:
{genomic_analysis}

Pharmacology Evaluation:
{pharmacology_evaluation}

Provide final treatment recommendation following the exact format:
✅ Primary Recommendation: [Drug] [Dose] [Schedule]
Rationale: [Brief reason]
[Then detailed clinical report]

Start immediately with the recommendation line."""
        
        try:
            model = ChatFireworks(
                model=self.model,
                fireworks_api_key=os.getenv("FIREWORKS_API_KEY"),
                temperature=0.3,
                max_tokens=5000
            )
            
            response = model.invoke([
                ("system", self.system_prompt),
                ("human", prompt)
            ])
            
            return response.content

        except Exception as e:
            error_msg = f"⚠️ Error during Final Recommendation: {str(e)}"
            print(error_msg)
            return error_msg