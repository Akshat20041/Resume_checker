# resume_parser.py

import fitz  # PyMuPDF
import docx
import io

def extract_text_from_pdf(uploaded_file):
    try:
        file_bytes = uploaded_file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_docx(uploaded_file):
    try:
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error reading DOCX: {e}"

# checker.py

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def analyze_resume(text, skills_prompt, openai_api_key):
    try:
        llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0, model="gpt-4o")
        prompt = PromptTemplate.from_template(
            """You are a resume screening assistant.
Given the following resume and a list of required skills, evaluate how well the resume matches the skills.
Give the percentage of match (0-100%) for each skill and a brief explanation.
Resume:
{text}
Required Skills:
{skills}
Your Output: It should contain the name of the resume and then it's skills and % matched.
"""
        )
        formatted_prompt = prompt.format(text=text, skills=skills_prompt)
        return llm.predict(formatted_prompt)
    except Exception as e:
        return f"Error analyzing resume: {e}"
# app.py
import os
import streamlit as st
# from resume_parser import extract_text_from_pdf, extract_text_from_docx
# from checker import analyze_resume

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
else:
    st.error("OPENAI_API_KEY not found. Please set it in the environment variables.")
    st.stop()


st.set_page_config(page_title="Resume Skill Score Checker", layout="wide")
st.title("📄 Resume Skill Score Checker")

st.markdown("Upload a resume and get a skill match **score out of 10** based on the required skills you provide.")

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
