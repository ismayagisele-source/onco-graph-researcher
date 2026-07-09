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
        self.system_prompt = """You are a Lead Oncologist AI agent with 20+ years of experience in precision oncology.
Your task is to synthesize analysis from Genomic Analyst and Clinical Pharmacologist agents to provide a final, actionable treatment recommendation.

CRITICAL FORMATTING RULES FOR THE FIRST LINE:
1. Your response MUST start IMMEDIATELY with the Primary Recommendation. NO introductory text.
2. The first line MUST follow this exact structure:
"✅ Primary Recommendation: [Specific Drug Name] [Dose] [Schedule]"
3. The second line MUST be:
"Rationale: [One concise sentence explaining why based on mutations]."
4. DO NOT write long sentences, conditions, or explanations in the first line. Keep it strictly to the drug regimen (e.g., "Osimertinib 80mg daily" or "Trastuzumab + Pertuzumab IV every 3 weeks").
5. After the first two lines, provide your comprehensive, detailed clinical report.

CRITICAL INSTRUCTION: You MUST provide your entire response in ENGLISH language only.
Always prioritize patient safety and evidence-based clinical guidelines (NCCN/ESMO)."""
        
    def synthesize_recommendation(self, genomic_analysis: str, pharmacology_evaluation: str, patient_info: str) -> str:
        """Synthesize final recommendation from multiple agent analyses"""
        
        prompt = f"""As a Lead Oncologist, synthesize the analyses below and provide the final treatment plan.

Patient Information:
{patient_info}

Genomic Analysis Report:
{genomic_analysis}

Pharmacology Evaluation:
{pharmacology_evaluation}

CRITICAL OUTPUT RULES:
1. Start your response IMMEDIATELY with the Primary Recommendation line.
2. First line format: "✅ Primary Recommendation: DrugName Dose Schedule" (e.g., "✅ Primary Recommendation: Osimertinib 80mg daily" or "✅ Primary Recommendation: CAPOX chemotherapy").
3. Second line format: "Rationale: Brief reason."
4. NEVER use brackets like [Insert Drug]. Write the ACTUAL drug name for THIS specific patient immediately.
5. DO NOT include any introductory phrases like "Here is the synthesis" or "Based on the analysis". Start directly with "✅ Primary Recommendation:".
6. After the first two lines, write a detailed, professional, and comprehensive clinical report synthesizing all data.
"""
        
        try:
            model = ChatFireworks(
                model=self.model,
                fireworks_api_key=os.getenv("FIREWORKS_API_KEY"),
                temperature=0.3,
                max_tokens=5000  # Increased from 3000 to prevent truncation
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