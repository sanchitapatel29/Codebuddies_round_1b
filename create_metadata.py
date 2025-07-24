from utils.json_utils import write_json
import os

PDF_FOLDER = "pdfs"
OUTPUT_FILE = "outputs/input.json"

def create_input_json(pdf_folder):
    challenge_id = input("Enter Challenge ID: ")
    test_case_name = input("Enter Test Case Name: ")
    description = input("Enter Challenge Description: ")
    persona_role = input("Enter Persona Role: ")
    job_task = input("Enter the Job To Be Done: ")

    documents = []

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            title = os.path.splitext(filename)[0]
            documents.append({
                "filename": filename,
                "title": title
            })

    structured_data = {
        "challenge_info": {
            "challenge_id": challenge_id,
            "test_case_name": test_case_name,
            "description": description
        },
        "documents": documents,
        "persona": {
            "role": persona_role
        },
        "job_to_be_done": {
            "task": job_task
        }
    }

    write_json(OUTPUT_FILE, structured_data)
    print(f"[✓]  Input JSON saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    create_input_json(PDF_FOLDER)
