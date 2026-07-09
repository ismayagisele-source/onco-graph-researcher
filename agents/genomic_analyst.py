"""
Genomic Analyst Agent
Analyzes patient genomic data to identify mutations
"""

import os
from dotenv import load_dotenv
from langchain_fireworks import ChatFireworks

load_dotenv()

class GenomicAnalyst:
    def __init__(self):
        self.name = "Genomic Analyst"
        self.model = "accounts/fireworks/routers/glm-5p2-fast"
        self.system_prompt = """You are a Genomic Analyst AI agent specialized in cancer genomics.
Your task is to analyze patient genomic data and identify important mutations.
Focus on mutations related to: EGFR, KRAS, TP53, ALK, BRAF, ROS1 (but also analyze any other clinically significant mutations present in the data).

CRITICAL OUTPUT RULES:
1. You MUST NOT output your internal thinking process. Do NOT start with "Analyze the Request", "Process the Data", "Draft the Response", or similar phrases.
2. Start your response IMMEDIATELY with "1. List of Mutations Found".
3. Provide the final professional medical report in ENGLISH only.

Always cite which mutation you found and its clinical significance."""
    
    def analyze_genomic_data(self, patient_data: str) -> str:
        """Analyze genomic data and return findings"""
        
        prompt = f"""Analyze the following patient genomic data and identify mutations:

Patient Data:
{patient_data}

Please provide:
1. List of mutations found
2. Clinical significance of each mutation
3. Potential targeted therapies based on mutations
4. Confidence level of your analysis

CRITICAL OUTPUT RULES:
1. You MUST NOT output your internal thinking process. Do NOT start with "Analyze the Request" or similar phrases.
2. Start your response IMMEDIATELY with "1. List of Mutations Found".
3. Provide the final professional medical report in ENGLISH only.
"""
        
        try:
            model = ChatFireworks(
                model=self.model,
                fireworks_api_key=os.getenv("FIREWORKS_API_KEY"),
                temperature=0.3,
                max_tokens=3000
            )
            
            response = model.invoke([
                ("system", self.system_prompt),
                ("human", prompt)
            ])
            
            return response.content

        except Exception as e:
            error_msg = f"⚠️ Error during Genomic Analysis: {str(e)}"
            print(error_msg)
            return error_msg