# agent/reviewer.py

import google.generativeai as genai
import os

# Load your Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini 1.5 Pro model
model = genai.GenerativeModel("gemini-2.0-flash")

def reviewCode(code: str) -> str:
    prompt = f"""You are a code reviewer bot. Review the following Python code and provide suggestions for improvement, bug fixes, and missing elements like logging or exception handling:\n\n{code}"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
