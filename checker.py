# checker.py

from langchain.chat_models import ChatOpenAI
from langchain.core.prompts import PromptTemplate

def analyze_resume(text, skills_prompt, openai_api_key):
    try:
        llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4.1-mini",
            temperature=0
        ) prompt = PromptTemplate.from_template(
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



