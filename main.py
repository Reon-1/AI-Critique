import streamlit as st
from utils.file_handler import extract_text_from_file
from utils.gemini_model import analyze_resume_with_gemini
from utils.pdf_generator import generate_feedback_pdf

st.set_page_config(page_title='AI Critiquer', page_icon='📄', layout='centered')
st.title("AI Critiquer")
st.markdown('Upload the PDF and get AI-Powered feedback as per the needs!')

# Upload file
uploaded_file = st.file_uploader('Upload your PDF or TXT', type=['pdf', 'txt'])
job_role = st.text_input("Enter the Job role you're targeting (optional)")
analyze = st.button('Analyze File')

if analyze and uploaded_file:
    try:
        # Extract text content from uploaded file
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error('File has no contents...')
            st.stop()

        # Prepare prompt for AI
        prompt = f"""
Please analyze this resume and provide constructive feedback.
Focus on the following aspects:

1. Content clarity and impact
2. Skills Presentation
3. Experience Descriptions
4. Specific improvements for {job_role if job_role else 'General job applications'}
5. Unique features and strengths

content:
{file_content}

Please provide your analysis in a clear, structured format.
"""

        # Call Gemini AI
        response_text = analyze_resume_with_gemini(prompt)

        st.markdown("### Analysis Results")
        st.markdown(response_text)

        # Check AI feedback
        if not response_text.strip():
            st.error("The AI did not generate any feedback. Please try again.")
        else:
            # Generate PDF bytes only if valid response
            pdf_bytes = generate_feedback_pdf(response_text)

            # Show download button INSIDE else block
            st.download_button(
                label="📥 Download Feedback",
                data=pdf_bytes,
                file_name="resume_feedback.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error Occurred: {str(e)}")
