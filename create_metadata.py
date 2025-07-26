from utils.json_utils import write_json
import os
import random

PDF_FOLDER = "pdfs"
OUTPUT_FILE = "outputs/input.json"

def generate_challenge_info(persona: str) -> dict:
    random_id = str(random.randint(1000, 9999))
    challenge_id = "round_1b_" + random_id
    test_case_name = persona.lower().replace(" ", "_").strip()
    description = persona.strip().capitalize()

    return {
        "challenge_id": challenge_id,
        "test_case_name": test_case_name,
        "description": description
    }

def create_input_json(pdf_folder):
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
        "challenge_info": generate_challenge_info(persona_role),
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
