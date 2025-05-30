# app.py
import os
import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from checker import analyze_resume

# Set OpenAI API key
openai_api_key = st.secrets.get("OPENAI_API_KEY")
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
else:
    raise ValueError("OPENAI_API_KEY not found in Streamlit secrets.")

st.set_page_config(page_title="Resume Skill Score Checker", layout="wide")
st.title("📄 Resume Skill Score Checker")

st.markdown("Upload a resume and get a skill match **(Score out of 100)** based on the required skills you provide.")

skills_required = st.text_area("🧠 Enter Required Skills (comma-separated or list format)")

uploaded_files = st.file_uploader(
    "📂 Upload Resume(s) - PDF or DOCX only", type=["pdf", "docx"], accept_multiple_files=True
)

if st.button("🚀 Analyze Resume(s)"):
    if not openai_api_key:
        st.error("❌ OpenAI API key is missing. Please set it as an environment variable.")
    elif not skills_required.strip():
        st.error("❌ Please enter required skills.")
    elif not uploaded_files:
        st.error("❌ Please upload at least one resume file.")
    else:
        with st.spinner("Analyzing..."):
            for file in uploaded_files:
                if file.name.lower().endswith(".pdf"):
                    text = extract_text_from_pdf(file)
                elif file.name.lower().endswith(".docx"):
                    text = extract_text_from_docx(file)
                else:
                    st.warning(f"❌ Unsupported file type: {file.name}")
                    continue

                result = analyze_resume(text, skills_required, openai_api_key)

                st.subheader(f"📄 {file.name}")
                st.markdown(f"```\n{result}\n```")
