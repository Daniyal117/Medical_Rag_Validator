from langchain_ollama import ChatOllama
import json

llm = ChatOllama(
    model="qwen2.5:14b-instruct",
    temperature=0
)


def validate(prescription_json: str, policy_chunks):
    context = "\n\n".join([doc.page_content for doc in policy_chunks])

    prompt = f"""
You are a strict medical policy validation assistant.

Your primary task is to validate a prescription against  policy rules.Writting the missing information is complusory.

CRITICAL PRIORITY:
1. ICD code matching is mandatory and finding missing info and also write if any ICD code is missing in the policy is mandatory.decision approved if any one of the icd info matches.


---

Prescription structured data:
{prescription_json}

---

Relevant policy excerpts:
{context}


OUTPUT FORMAT (STRICT JSON ONLY):

{{
  "decision": "APPROVED | REJECTED | INSUFFICIENT_INFORMATION",
  "reasons": [
    "Clear explanation based ONLY on policy"
  ],
  "missing_information": [
    ""
  ],
  "matched_policy_points": [
    "Exact matched rules or clauses"
  ]
}}
"""
    response = llm.invoke(prompt)
    try:
        parsed_output = json.loads(response.content)
        return parsed_output
    except json.JSONDecodeError:
        return {
            "decision": "INSUFFICIENT_INFORMATION",
            "reasons": ["Validator returned invalid JSON"],
            "missing_information": ["Invalid LLM output format"],
            "matched_policy_points": []
        }
    