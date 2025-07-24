from sentence_transformers import SentenceTransformer, util

# Load sentence transformer model (offline capable)
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_candidate_sections(text_pages):
    import re
    sections = []
    for page in text_pages:
        lines = page["text"].split("\n")
        for line in lines:
            # Crude heading filter: assumes headings are capitalized and have some length
            if re.match(r"^\s*[A-Z][A-Za-z\s\-&]{5,}$", line):
                sections.append({
                    "page_number": page["page_number"],
                    "section_title": line.strip(),
                    "raw_text": page["text"]
                })
    return sections


def semantic_rank_sections(sections, job_to_be_done):
    # Encode the job/task into an embedding
    job_embedding = model.encode(job_to_be_done, convert_to_tensor=True)

    for section in sections:
        # Encode only the section title for now (you can change this to include raw_text)
        section_text = section["section_title"]
        section["embedding"] = model.encode(section_text, convert_to_tensor=True)

    # Compute cosine similarity between section and job
    for section in sections:
        section["score"] = util.cos_sim(section["embedding"], job_embedding).item()

    # Sort by similarity score
    sections.sort(key=lambda x: -x["score"])

    # Assign new importance_rank
    for i, section in enumerate(sections, 1):
        section["importance_rank"] = i
        del section["embedding"]
        del section["score"]

    return sections
