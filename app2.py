import streamlit as st
import os
import fitz  # PyMuPDF

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

st.set_page_config(page_title="PDF Text Extractor")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(pdf_file):
    text_output = []
    try:
        with fitz.open(pdf_file) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                text_output.append(text)
    except Exception as e:
        st.error(f"Error extracting text: {e}")
    return '\n'.join(text_output)

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
