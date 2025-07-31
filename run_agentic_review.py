# run_agentic_review.py
"""
This script reviews all Python files in the repo using the LLM directly (no agent).
It sends the code to the LLM and prints the result.
"""
import os
from utils.gemini_llm import get_llm_from_config

def get_files_to_review():
    # Review all .py files in the repo (customize as needed)
    files = []
    for root, dirs, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.py') and not filename.startswith('.'):
                path = os.path.join(root, filename)
                # Skip files in __pycache__
                if '__pycache__' not in path:
                    files.append(path)
    return files

def main():
    files = get_files_to_review()
    review_input = "You are an AI code reviewer. Please review the following Python files and provide feedback:\n\n"
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            review_input += f"File: {file}\n{content}\n\n"
        except Exception as e:
            review_input += f"File: {file}\nError reading file: {e}\n\n"
    llm = get_llm_from_config()
    result = ""
    try:
        for chunk in llm.stream(input=review_input):  # Directly send review_input
            result += chunk.content
    except Exception as e:
        print(f"Error during LLM call: {e}")
        return
    heading = "## :robot: LLM Review\n\n"
    if not result.strip().startswith("## :robot: LLM Review"):
        result = heading + result
    print(result)

if __name__ == "__main__":
    main()
