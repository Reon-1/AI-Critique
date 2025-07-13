import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  ## load the environment variable from env file

# import GEMINI key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Calling the GEMINI model   
def analyze_resume_with_gemini(prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text
