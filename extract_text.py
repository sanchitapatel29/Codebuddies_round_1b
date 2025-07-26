import fitz 

def extract_pdf_text_and_headings(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        try:
            # Extract text blocks (with coordinates and font sizes)
            blocks = page.get_text("dict")["blocks"]
            page_text = ""

            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        line_text = " ".join([span["text"] for span in line["spans"]])
                        page_text += line_text + "\n"

            if page_text.strip():
                all_text.append({
                    "page_number": page_num + 1,
                    "text": page_text.strip()
                })
        except Exception as e:
            print(f"Error on page {page_num + 1}: {e}")
            continue

    return all_text
