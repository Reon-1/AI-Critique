import streamlit as st
import PyPDF2
import io
import os
import google.generativeai as genai
from dotenv import load_dotenv  

load_dotenv() ## load the environment variable from env file

## webpage configs 
st.set_page_config(page_title='AI Critiquer', page_icon='📄', layout='centered')
st.title("AI Critiquer")
st.markdown('Upload the PDF and get AI-Powered feedback as per the needs!')

## import GEMINI key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

## upload file
uploaded_file = st.file_uploader('Upload your PDF or TXT', type=['pdf','txt'])
job_role = st.text_input("Enter the Job role you're targerrting (optional)")
analyze = st.button('Analyze File')

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
    
if analyze and uploaded_file:  
    try:
        file_content = extract_text_from_file(uploaded_file) # check if the file has contents or not

        if not file_content.strip():  # remove any blank. empty characters and all
            st.error('File has no contets...')
            st.stop() # stop the program

        # prompt for GEMINI model to check the file contents & give feedback (can be any prompt)
        prompt = f"""
        Please analyze this resume and provide constructive feedback.
        Focus on the following aspects:
        
        1. Content clarity and impact
        2. Skills Presentation
        3. Experience Descriptions
        4. Specefic improvements for {job_role if job_role else 'General job applications'}
        5. Unique General and uniuqe features it has.
        
        content:
        {file_content}
        
        Please provide your analysis in a clear, structured format."""
     
        # Calling the GEMINI model   
        model =  genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(prompt)
        
        st.markdown("### Analysis Results")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"Error Occurred: {str(e)}")
