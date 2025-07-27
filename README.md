# Round 1B: Persona-Driven Document Intelligence

> Theme: “Connect What Matters — For the User Who Matters”

This project is an offline, CPU-only **intelligent document analyst** that extracts and prioritizes the most relevant sections from a collection of PDFs — based on a specific **persona** and their **job-to-be-done**.

The pipeline is designed to handle various types of documents (e.g., research papers, financial reports, textbooks) and adapts to diverse personas and related goals.

---

## 🚀 Features

- ✅ **Offline & CPU-Only** (no internet required at runtime)
- 📄 **PDF Parsing & Chunking** using `PyMuPDF`
- 🧠 **Semantic Similarity Scoring** using `sentence-transformers`
- 🧾 **Structured Output** in the required `challenge1b_output.json` format
- ⚡ Fast & Lightweight (≤ 1GB model, ≤ 60 sec for 3–5 documents)
- 🧑‍💼 Persona-aware & job-guided content filtering

---

## 🧰 Tech Stack

| Component         | Tool / Library                  |
|-------------------|----------------------------------|
| PDF Parser        | `PyMuPDF` (fitz)                 |
| Embedding Model   | `all-MiniLM-L6-v2` (80MB)        |
| NLP Libraries     | `sentence-transformers`, `transformers` |
| Language          | Python 3.10                      |
| Runtime           | CPU only                         |

---

## 📁 Project Structure

```bash
project-root/
│
├── app/
│   ├── pdfs/                 # Input folder for uploaded PDFs
│   ├── outputs/              # Auto-generated input/output JSONs
│       ├── input.json
│       └── output.json
│   
├── utils/
│   ├── __init__.py
    └── json_utils.py
│   
├── create_metadata.py   # Input gathering + metadata generation
├── extract_text.py      # PDF parsing with PyMuPDF
├── fulfill_job.py       # Core logic: ranking + output generation
├── rank_sections.py     # Embedding + semantic scoring
├── run.py               # End-to-end pipeline launcher
├── requirements.txt     # Python dependencies
└── approach_explanation.md
```

## ⚙️ Setup Instructions

Follow these steps to set up and run the project locally in an isolated environment.

---

### 1. Prerequisite: Install Python 3.10

Make sure Python 3.10 is installed on your machine.

- 🔗 [Download Python 3.10](https://www.python.org/downloads/release/python-3100/)
- Confirm installation:
```bash
python3.10 --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/persona-doc-intelligence.git
cd persona-doc-intelligence
```

### 3. Create a Virtual Environment

On Windows: 
```bash
py -3.10 -m venv .venv
.venv\Scripts\activate
```
On macOS/Linux: 
```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```
⚠️ If tokenizers fails, try:
```bash
pip install tokenizers==0.13.2 --prefer-binary
```

### 5. Add Input PDFs

Place your .pdf files inside the following folder:
```bash
app/pdfs/
```
If it doesn’t exist, create it manually.

### 6. Run the Project

Place your .pdf files inside the following folder:
```bash
python run.py
```
This script will:
- Prompt for persona and job-to-be-done
- Generate:
    - app/outputs/input.json
    - app/outputs/output.json



🎉 You're Ready to Go!
Your offline, CPU-friendly NLP pipeline will extract, rank, and refine the most relevant sections based on your specified persona and task.
