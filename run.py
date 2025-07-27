from fulfill_job import fulfill_job
from create_metadata import create_input_json
import os

def wait_for_pdf_upload(pdf_dir):
    print("📂 Please upload your PDF files into the 'app/pdfs/' folder.")
    input("✅ Press Enter once you have finished uploading the PDFs...")

    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    if not any(fname.endswith('.pdf') for fname in os.listdir(pdf_dir)):
        print("⚠️ No PDFs found in the folder! Please add at least one PDF and rerun the script.")
        exit(1)

if __name__ == "__main__":
    PDF_DIR = "app/pdfs"
    wait_for_pdf_upload(PDF_DIR)

    # Step 1: Generating input JSON from metadata
    create_input_json(PDF_DIR)

    # Step 2: Running the fulfill_job pipeline
    fulfill_job(
        input_json_path="/app/outputs/input.json",
        pdf_dir=PDF_DIR,
        output_path="/app/outputs/output.json"
    )
