"""
Agent 0: Multimodal Digital Pathologist (Gemma 4 31B IT)
Runs on AMD MI300X GPU via vLLM API
"""

import requests
import base64
from PIL import Image
import io

class Gemma4Pathologist:
    def __init__(self, api_url="http://129.212.177.85:8000/v1/chat/completions"):
        self.api_url = api_url
        self.model = "google/gemma-4-31b-it"
    
    def analyze_image(self, image_path: str, clinical_context: str = "") -> str:
        """
        Analyze medical image using Gemma 4 vision capabilities
        Returns: Detailed pathology report in text format
        """
        try:
            # Load and encode image to base64
            with Image.open(image_path) as img:
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too large (max 1024px)
                max_size = 1024
                if max(img.size) > max_size:
                    img.thumbnail((max_size, max_size))
                
                # Convert to base64
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Build prompt
            prompt = f"""You are a senior digital pathologist specializing in oncology.

Analyze this medical image and provide a detailed pathology report.

{f'Clinical Context: {clinical_context}' if clinical_context else ''}

Provide your analysis in the following structure:

**1. Image Type & Quality:**
- Type of imaging (histopathology, CT, MRI, etc.)
- Staining method if applicable (H&E, IHC, etc.)
- Image quality assessment

**2. Morphological Findings:**
- Cellular architecture
- Nuclear features (size, shape, chromatin pattern)
- Cytoplasmic characteristics
- Tissue organization

**3. Tumor Characteristics:**
- Grade assessment (if applicable)
- Differentiation status
- Necrosis/apoptosis presence
- Mitotic activity

**4. Suspicious Features:**
- Invasive patterns
- Vascular/lymphatic invasion
- Margin status (if visible)

**5. Pathology Assessment:**
- Overall impression
- Correlation with genomic findings (if context provided)
- Recommendations for further testing

Be objective and evidence-based. Do not diagnose, only describe observed features."""

            # API call to Gemma 4
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 1024,
                "temperature": 0.3
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: API returned status {response.status_code}\n{response.text}"
        
        except Exception as e:
            return f"Error analyzing image: {str(e)}"