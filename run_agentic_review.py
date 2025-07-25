# run_agentic_review.py
"""
This script runs the agentic code review logic directly (no Flask server).
It should be used in CI/CD pipelines to review the codebase and print the result.
"""
import os
from agent.agent_executor import execute_agent

def get_files_to_review():
    # For demo: review all .py files in the repo (customize as needed)
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
    review_input = ''
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            review_input += f"File: {file}\n{content}\n\n"
        except Exception as e:
            review_input += f"File: {file}\nError reading file: {e}\n\n"
    result = execute_agent(review_input)
    heading = "## :robot: Agent Review\n\n"
    if not result.strip().startswith("## :robot: Agent Review"):
        result = heading + result
    print(result)

if __name__ == "__main__":
    main()
