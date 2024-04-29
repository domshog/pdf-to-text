import streamlit as st
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# Path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

st.set_page_config(page_title="PDF Text Extractor")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(pdf_file):
    pages = convert_from_path(pdf_file, 300, poppler_path="/path/to/poppler")
    text_output = []
    for page in pages:
        text = pytesseract.image_to_string(page, lang='eng')
        text_output.append(text)
    full_text = '\n'.join(text_output)
    return full_text


def main():
    st.title("PDF Text Extractor")
    
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if allowed_file(uploaded_file.name):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            text_output = extract_text(file_path)
            st.subheader("Extracted Text:")
            st.text_area("Text Output", text_output, height=400)
        else:
            st.error("Please upload a PDF file.")







if __name__ == "__main__":
    main()
