
import sys

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("No PDF library found")
        sys.exit(1)

try:
    reader = PdfReader("d:/Study materials/Portugal/P2/SIBD/Project/second part/SIBD 2526  - Project Assignment - Part 2.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    with open("pdf_content.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("PDF content written to pdf_content.txt")
except Exception as e:
    print(f"Error reading PDF: {e}")
