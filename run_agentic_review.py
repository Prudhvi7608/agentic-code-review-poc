import os
from utils.gemini_llm import getOpenAILLM

import subprocess
import os

import os
import json
import requests

def get_files_to_review():
    """
    Returns a list of modified .py files in the current pull request,
    using the GitHub API and the GITHUB_EVENT_PATH payload.
    """
    # Load the incoming event payload
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        print("⚠️  GITHUB_EVENT_PATH not set or file missing.")
        return []

    payload = json.load(open(event_path))
    pr = payload.get("pull_request")
    if not pr:
        print("⚠️  Not a pull_request event.")
        return []

    pr_number = pr["number"]
    repo       = os.environ["GITHUB_REPOSITORY"]  # e.g. "org/repo"
    token      = os.environ["GITHUB_TOKEN"]

    # GitHub API: list files changed in this PR
    url     = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}

    changed_py = []
    page = 1
    while True:
        resp = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        if not resp.ok:
            print(f"❌ GitHub API error: {resp.status_code} {resp.text}")
            break
        files = resp.json()
        if not files:
            break
        for f in files:
            name = f.get("filename","")
            if name.endswith(".py"):
                changed_py.append(name)
        page += 1

    return changed_py


    


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
