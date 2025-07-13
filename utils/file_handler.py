import PyPDF2
import io

# extracts texts from pdf 
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file) # loads the file
    text = ''  # empty strings to add from page
    for page in pdf_reader.pages: #checks individual files
        text += page.extract_text() + '\n' # added files 
    return text 

# extracts texts from uploaded files
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == 'application/pdf': # if it's pdf
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read())) # type conversion 
    return uploaded_file.read().decode('utf-8') # if it's txt
