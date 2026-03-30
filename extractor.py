from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:14b-instruct",
    temperature=0
)


def extract_prescription_data(text: str):
    prompt = f"""
You are extracting structured information from a medical prescription/referral document.

Return strict JSON only with this structure:
{{
  "diagnoses": [],
  "medications": [],
  "requested_items": [],
  "clinician_info": {{}},
  "important_notes": []
}}

Document:
{text}
"""
    response = llm.invoke(prompt)
    return response.content