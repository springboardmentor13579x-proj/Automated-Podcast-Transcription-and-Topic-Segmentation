from PyPDF2 import PdfReader
from fuzzywuzzy import fuzz

def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def read_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.read()

def compare_files(pdf_path, txt_path):
    pdf_text = extract_pdf_text(pdf_path)
    txt_text = read_txt(txt_path)

    match_percent = fuzz.token_set_ratio(pdf_text, txt_text)

    print(f"Matching Percentage: {match_percent}%")


pdf_file = ".24-1056.mp3.pdf"
txt_file = ".24-1056.mp3_transcript.txt"

compare_files(pdf_file, txt_file)
