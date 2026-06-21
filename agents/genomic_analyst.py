"""
Genomic Analyst Agent
Analyzes patient genomic data to identify mutations
"""

import ollama

class GenomicAnalyst:
    def __init__(self):
        self.name = "Genomic Analyst"
        self.model = "llama3"
        self.system_prompt = """You are a Genomic Analyst AI agent specialized in cancer genomics.
Your task is to analyze patient genomic data and identify important mutations.
Focus on mutations related to: EGFR, KRAS, TP53, ALK, BRAF, ROS1.
CRITICAL INSTRUCTION: You MUST provide your entire response in ENGLISH language only. Do not use any other language.
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
4. Confidence level of your analysis"""
        
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
    # Sample patient genomic data
    sample_data = """
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
    
    # Create agent instance
    analyst = GenomicAnalyst()
    
    # Analyze data
    print("🧬 Genomic Analyst Agent - Analysis Report\n")
    print("=" * 60)
    analysis = analyst.analyze_genomic_data(sample_data)
    print(analysis)
    print("=" * 60)