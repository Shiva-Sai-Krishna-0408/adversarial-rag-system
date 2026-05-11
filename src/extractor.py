from pypdf import PdfReader


def extract_text_pypdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        text += extracted
    return text 