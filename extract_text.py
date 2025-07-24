from PyPDF2 import PdfReader

def extract_pdf_text_and_headings(pdf_path):
    reader = PdfReader(pdf_path)
    all_text = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text:
                all_text.append({
                    "page_number": i + 1,
                    "text": text
                })
        except Exception:
            continue
    return all_text
