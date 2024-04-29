import streamlit as st
import os

import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# Path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from PDF
def extract_text(pdf_file):
    pages = convert_from_path(pdf_file, 300)
    text_output = []
    for page in pages:
        text = pytesseract.image_to_string(page, lang='eng')
        text_output.append(text)
    full_text = '\n'.join(text_output)
    return full_text

# Main function to run the Streamlit app
def main():
    st.title("PDF Text Extractor")
    
    # Upload PDF file
    uploaded_file = st.file_uploader("Choose a PDF file", type='pdf')
    
    if uploaded_file is not None:
        # Check if file extension is allowed
        if allowed_file(uploaded_file.name):
            # Display file details
            st.write('File uploaded:', uploaded_file.name)
            
            # Save the uploaded file temporarily
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getvalue())
                
            # Extract text from the PDF file
            text_output = extract_text(file_path)
            
            # Display extracted text
            st.header("Extracted Text:")
            st.write(text_output)
        else:
            st.error("File type not supported. Please upload a PDF file.")

# Run the main function
if __name__ == '__main__':
    main()
