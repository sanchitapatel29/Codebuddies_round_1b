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
├── Dockerfile
├── README.md
└── approach_explanation.md
```

## ⚙️ Setup Instructions

Follow these steps to set up and run the project locally in an isolated environment.

---

### 1. Prerequisite: Install Docker
Ensure Docker is installed and running on your system.

- 🔗 [Download Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
- Verify Installation:
```bash
docker --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/sanchitapatel29/Codebuddies_round_1b.git
cd Codebuddies_round_1b
```

### 3. Build the Docker Image
```bash
docker build -t codebuddies2 .
```
This will take several minutes on the first build (approx 50 - 60 minutes)

### 4. Add Input PDFs

Place your .pdf files inside the following folder:
```bash
app/pdfs/
```
If it doesn’t exist, create it manually.

### 5. Run the container
```bash
docker run --rm -it `
  -v "${PWD}\app\pdfs:/app/pdfs" `
  -v "${PWD}\app\outputs:/app/outputs" `
  --network none `
  codebuddies2
```

This script will:
- Prompt for persona and job-to-be-done
- Generate:
    - app/outputs/input.json
    - app/outputs/output.json



🎉 You're Ready to Go!

Your offline, CPU-friendly NLP pipeline will extract, rank, and refine the most relevant sections based on your specified persona and task.
