import streamlit as st
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import requests

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Function to download the Tesseract executable
def download_tesseract_executable():
    url = 'https://github.com/domshog/pdf-to-text/tree/main/tesseract/tesseract.exe'  # Update with your GitHub repository URL
    r = requests.get(url)
    with open('tesseract.exe', 'wb') as f:
        f.write(r.content)

# Check if the Tesseract executable exists, if not, download it
if not os.path.exists('tesseract.exe'):
    st.info("Downloading Tesseract executable...")
    download_tesseract_executable()

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = os.path.abspath('tesseract.exe')

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from PDF
def extract_text(pdf_file):
    text_output = []
    try:
        with fitz.open(pdf_file) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                image_list = page.get_pixmap(alpha=False)
                img = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)
                text = pytesseract.image_to_string(img)
                text_output.append(text)
    except Exception as e:
        st.error(f"Error extracting text: {e}")
    return '\n'.join(text_output)

# Main function
def main():
    st.title("PDF Text Extractor")
    
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if allowed_file(uploaded_file.name):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            text_output = extract_text(file_path)
            if text_output:
                st.subheader("Extracted Text:")
                st.text_area("Text Output", text_output, height=400)
            else:
                st.warning("No text found in the PDF file.")
        else:
            st.error("Please upload a PDF file.")

if __name__ == "__main__":
    main()
