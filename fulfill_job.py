import os
import json
import datetime
from extract_text import extract_pdf_text_and_headings
from rank_sections import get_candidate_sections, semantic_rank_sections
from sentence_transformers import SentenceTransformer, util
import unicodedata
import re

os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

model = SentenceTransformer("/app/models/all-MiniLM-L6-v2")


def filter_relevant_paragraphs(text: str, task: str, threshold: float = 0.2) -> str:
    import re

    # Split text into logical paragraphs (allow both bullet points and blocks)
    blocks = re.split(r'\n\s*\n', text.strip())
    blocks = [block.strip() for block in blocks if block.strip()]

    task_embedding = model.encode(task, convert_to_tensor=True)
    relevant_blocks = []

    for block in blocks:
        block_embedding = model.encode(block, convert_to_tensor=True)
        similarity = util.cos_sim(task_embedding, block_embedding).item()
        
        if similarity >= threshold:
            relevant_blocks.append((similarity, block))

    # Sort by similarity, highest first
    relevant_blocks.sort(reverse=True)

    # Return top 3 most relevant blocks if any, else fallback to longest 2 blocks
    if relevant_blocks:
        return "\n\n".join(block for _, block in relevant_blocks[:3])
    else:
        blocks.sort(key=len, reverse=True)
        return "\n\n".join(blocks[:2])


def remove_headings(text: str) -> str:
    import re
    lines = text.splitlines()
    content_lines = []

    for line in lines:
        stripped = line.strip()
        if (
            len(stripped) < 60 and
            not stripped.startswith("•") and
            not re.search(r'[.!?]', stripped) and
            not re.match(r'^[\s\-–—]*$', stripped)
        ):
            continue
        content_lines.append(line)

    return "\n".join(content_lines)

def clean_text(text: str) -> str:
    import re
    import unicodedata

    # Normalize weird unicode characters (e.g., \ufb00, \u00e9, etc.)
    text = unicodedata.normalize("NFKD", text)

    # Fix common split-word artifacts like "space -themed", "pr ehistoric"
    text = re.sub(r'(\w+)\s*-\s*(\w+)', r'\1-\2', text) 
    text = re.sub(r'(\w+)\s+([a-z])', lambda m: m.group(1) + m.group(2) if len(m.group(1)) <= 2 else m.group(0), text)

    # Replace • or \u2022 with hyphen bullets
    text = text.replace("\u2022", "")

    # Replace multiple newlines with one
    text = re.sub(r'\n{2,}', '\n', text)

    # Fix multiple spaces
    text = re.sub(r' {2,}', ' ', text)

    # Remove any lingering non-printable characters
    text = ''.join(ch for ch in text if ch.isprintable())

    # Clean lines and re-join
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def fulfill_job(input_json_path, pdf_dir, output_path):
    with open(input_json_path, 'r') as f:
        input_data = json.load(f)

    metadata = {
        "input_documents": [doc["filename"] for doc in input_data["documents"]],
        "persona": input_data["persona"]["role"],
        "job_to_be_done": input_data["job_to_be_done"]["task"],
        "processing_timestamp": datetime.datetime.now().isoformat()
    }

    extracted_sections = []
    subsection_analysis = []
    all_sections = []

    for doc in input_data["documents"]:
        pdf_path = os.path.join(pdf_dir, doc["filename"])
        text_pages = extract_pdf_text_and_headings(pdf_path)
        candidate_sections = get_candidate_sections(text_pages)

        for section in candidate_sections:
            section["document"] = doc["filename"]

        all_sections.extend(candidate_sections)

    ranked_sections = semantic_rank_sections(all_sections, input_data["job_to_be_done"]["task"])

    for section in ranked_sections[:10]:
        extracted_sections.append({
            "document": section["document"],
            "section_title": section["section_title"],
            "importance_rank": section["importance_rank"],
            "page_number": section["page_number"]
        })

        subsection_analysis.append({
            "document": section["document"],
            "refined_text": clean_text(
                remove_headings(
                    filter_relevant_paragraphs(section["raw_text"], input_data["job_to_be_done"]["task"])
                )
            ),

            "page_number": section["page_number"]
        })



    output_data = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=4)

    print(f"[✓] Output written to: {output_path}")
