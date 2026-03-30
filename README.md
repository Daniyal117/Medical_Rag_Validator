
# 🧠 Medical Document Decision Engine

An AI system that converts unstructured medical prescriptions into **policy-validated decisions** using a local Retrieval-Augmented Generation (RAG) pipeline.

---

## 🚀 Overview

Validating prescriptions against policy documents is typically a manual process involving unstructured PDFs, domain knowledge, and complex rules.

This system automates that workflow by:

- Parsing prescription PDFs (text + layout-aware extraction)
- Structuring clinical information using a local LLM
- Retrieving relevant policy rules from a vector database
- Performing **evidence-based validation**

---

## 🎯 Problem

- Prescriptions are unstructured and inconsistent  
- Policy documents contain dense text and tables  
- Manual validation is slow, error-prone, and not scalable  

---

## 💡 Approach


---

## ⚙️ Tech Stack

- **Docling** — OCR + layout-aware PDF parsing  
- **LangChain** — pipeline orchestration  
- **FAISS** — local vector database  
- **Ollama (Qwen2.5 14B)** — local LLM inference  
- **FastAPI** — API layer  

> Runs fully locally with GPU acceleration (RTX 5090)

---

## 🧠 Key Features

- End-to-end RAG pipeline for document validation  
- Handles **complex PDFs (tables + text)**  
- Evidence-based decision logic (no blind inference)  
- Missing information detection  
- Fully offline (no external API dependency)  

---

## 📡 API

### POST `/validate-prescription`

Upload a prescription PDF.

#### Request
- `multipart/form-data`
- field name: `file`

#### Response

```json
{
  "decision": "APPROVED | REJECTED | INSUFFICIENT_INFORMATION",
  "reasons": [],
  "missing_information": [],
  "matched_policy_points": []
}
```
## ▶️ Run Locally

### 1. Install Ollama (Local LLM Runtime)

Download and install Ollama:


```bash
irm https://ollama.com/install.ps1 | iex
```
### Verify installation:
```
ollama run qwen2.5:14b-instruct
ollama --version
ollama ps

Pull Required Models (GPU Accelerated)
```


### 3. Install Python Dependencies
```
pip install -r requirements.txt
```
### 4. Build Policy Vector Database
```
. Build Policy Vector Database
```

### 5. Start the API Server
```
uvicorn api:app --reload
```