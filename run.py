from fulfill_job import fulfill_job
from create_metadata import create_input_json

if __name__ == "__main__":
    # Step 1: Generate input JSON
    create_input_json("pdfs")

    # Step 2: Run the fulfill_job pipeline
    fulfill_job(
        input_json_path="outputs/input.json",
        pdf_dir="pdfs",
        output_path="outputs/output.json"
    )
