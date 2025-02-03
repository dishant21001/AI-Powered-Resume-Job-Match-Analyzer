import pdfplumber

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.

    Args:
        pdf_file (file): PDF file uploaded by the user

    Returns:
        str: Extracted text content
    """
    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    return text.strip() if text else "No text found in PDF."
