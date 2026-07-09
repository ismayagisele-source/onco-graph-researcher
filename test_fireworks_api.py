import os
import time
from dotenv import load_dotenv
from langchain_fireworks import ChatFireworks

load_dotenv()

print("=" * 60)
print("GLM 5.2 API TEST")
print("=" * 60)

# TEST: GLM 5.2 Clinical Reasoning
print("\n[TEST] GLM 5.2 - Clinical Reasoning")
print("-" * 60)
try:
    glm_model = ChatFireworks(
        model="accounts/fireworks/models/glm-5p2",
        fireworks_api_key=os.getenv("FIREWORKS_API_KEY"),
        temperature=0.3,
        max_tokens=500
    )
    
    start_time = time.time()
    response = glm_model.invoke("""
You are a clinical oncologist. A patient has EGFR T790M mutation.
What targeted therapy do you recommend and why?
Answer in 2-3 sentences.
""")
    elapsed = time.time() - start_time
    
    print(f"✅ SUCCESS | Time: {elapsed:.2f}s")
    print(f"Response:\n{response.content}")
except Exception as e:
    print(f"❌ FAILED: {str(e)}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)