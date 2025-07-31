import os
from utils.gemini_llm import getOpenAILLM

import subprocess
import os

def get_files_to_review():
    import subprocess
    files = []
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACM", "HEAD"],
            capture_output=True, text=True, check=True
        )
        changed_files = result.stdout.strip().split('\n')

        for file in changed_files:
            if file.endswith('.py') and not file.startswith('.') and '__pycache__' not in file and os.path.exists(file):
                files.append(file)
    except subprocess.CalledProcessError as e:
        print("Error getting modified files:", e)
    return files


    


def load_prompt_template():
    try:
        with open("prompt/review_prompt.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading prompt template: {e}")
        return ""

def main():
    files = get_files_to_review()
    print("🛠️ Files being reviewed:", files) 
    prompt_template = load_prompt_template()
    if not prompt_template:
        print("Prompt template not found or empty. Exiting.")
        return

    review_input = ""
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            prompt = prompt_template.replace("{code_block}", content)
            review_input += f"### File: {file}\n\n{prompt}\n\n"
        except Exception as e:
            review_input += f"### File: {file}\nError reading file: {e}\n\n"

    llm = getOpenAILLM()
    result = ""
    try:
        for chunk in llm.stream(input=review_input):
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
