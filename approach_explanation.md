# Round 1B: Persona-Driven Document Intelligence — Approach Explanation

## 🎯 Problem Understanding

The challenge requires building a *CPU-only, offline document intelligence system* that extracts and prioritizes the most relevant sections from a collection of PDFs. The extraction must be guided by a defined *persona* and *job need to be done*. The system must be versatile, handling diverse document types such as research papers, reports, educational content, etc., and should complete processing within 60 seconds for 3–5 PDFs, with a model size ≤ 1GB.

---

## 🛠 Solution Overview

Our solution uses a modular *offline NLP pipeline* that fulfills the required tasks through the following core stages:

1. *PDF Parsing & Chunking (PyMuPDF)*  
2. *Semantic Relevance Ranking (Sentence-Transformers)*  
3. *Structured Output Generation (as per JSON schema)*

The entire solution runs offline using lightweight models and CPU, making it suitable for low-resource environments.

---

## 📂 Step-by-Step Methodology

### 1. 🗂 Document Ingestion
The user uploads 3–10 PDFs into the `app/pdfs/` folder. The system prompts for the persona and job-to-be-done, infers titles from filenames, auto-generates metadata (including `challenge_id`, `test_case_name`, and `description`), and saves everything in `input.json` for downstream processing.

### 2. 📄 Text Extraction (Using PyMuPDF)
Each PDF is parsed page-by-page using PyMuPDF, chosen for its superior layout-aware text extraction. We extract paragraph-level text blocks while preserving page numbers and document references. This forms the raw pool of candidate sections.

### 3. 🧠 Embedding and Relevance Scoring
We embed each text block using a local pre-trained transformer (`all-MiniLM-L6-v2` from `sentence-transformers`, ~80MB) and also embed the combined persona + job-to-be-done as a query. Cosine similarity is computed to score how well each section aligns with the task.

### 4. 🧾 Output JSON Generation
The final JSON contains:
- `metadata`: documents, persona, job, timestamp
- `extracted_sections`: top 10 ranked entries with title, page number, rank
- `subsection_analysis`: cleaned and filtered refined text per section

The format strictly follows the schema in `challenge1b_output.json`.

---

## ⚙ Technical Specifications

| Component           | Tool/Method                    |
|---------------------|--------------------------------|
| PDF Parser          | PyMuPDF (`fitz`)               |
| Embedding Model     | all-MiniLM-L6-v2 (384 dims)    |
| Ranking Strategy    | Cosine Similarity              |
| Execution           | Python 3.10, CPU only          |
| Model Size          | ~80MB                          |
| Execution Time      | ≤ 60 seconds (estimated and tested) |
| Offline Capable     | Fully offline, cached models   |

---

## ✅ Why This Works Well

- Uses *semantic understanding* to detect relevant sections, not just keywords.
- Enforces *diversity* in selection to avoid overfitting to single documents.
- Fully meets the constraints: *offline*, **CPU-only**, **≤1GB model**, **<60s run time**.

---

## 🚀 Future Enhancements

- Further improving the functionality of the model
- Add GUI or web UI using Streamlit for ease of interaction

---
