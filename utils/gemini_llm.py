# # utils/gemini_llm.py
# from langchain_google_genai import ChatGoogleGenerativeAI
import os

# def getGeminiLLM():
#     return ChatGoogleGenerativeAI(
#         model="gemini-2.0-flash",
#         temperature=0.4,
#         google_api_key=os.getenv("GEMINI_API_KEY")
#     )
from langchain_openai import ChatOpenAI

def getOpenAILLM():
    # Prefer environment variable, fallback to Streamlit secrets if available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets["OPENAI_API_KEY"]
        except Exception:
            api_key = None
    if not api_key:
        raise Exception("OpenAI API key not found in environment or Streamlit secrets.")
    return ChatOpenAI(
        model="gpt-4.1-mini",  # or "gpt-4" if you have access
        temperature=0.4,
        api_key=api_key
    )