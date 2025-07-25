# app.py
import streamlit as st
import requests
import openai

st.set_page_config(page_title="LangChain Code Reviewer & Chatbot", layout="centered")
st.title("🧠 LangChain Agentic Code Reviewer & Code Chatbot")

# PR Review
st.markdown("## PR Review")
repo = st.text_input("GitHub Repository (e.g. user/repo):")
pr_number = st.text_input("PR Number:")
webhook_url = st.text_input("Webhook URL (e.g. http://localhost:5000/webhook):", value="http://localhost:5000/webhook")

if st.button("Fetch & Review PR Code"):
    if repo.strip() and pr_number.strip():
        payload = {
            "action": "opened",
            "repository": {"full_name": repo},
            "pull_request": {"number": int(pr_number)}
        }
        with st.spinner("Fetching and reviewing PR code..."):
            try:
                response = requests.post(webhook_url, json=payload)
                response.raise_for_status()
                result = response.json()
                st.success("✅ Review Complete!")
                st.markdown("### 🔍 Agentic Workflow Response")
                st.json(result)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter both repository and PR number.")

st.markdown("---")

# Codebase Chatbot
st.markdown("## Codebase Chatbot")
import os
from dotenv import load_dotenv
load_dotenv()

chat_history = st.session_state.get("chat_history", [])
user_input = st.text_input("Ask a question about the codebase:")

def fetch_github_file(repo, filename, github_token):
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
    contents_url = f"https://api.github.com/repos/{repo}/contents/{filename}"
    try:
        resp = requests.get(contents_url, headers=headers)
        resp.raise_for_status()
        file_json = resp.json()
        if "content" in file_json and file_json["encoding"] == "base64":
            import base64
            content = base64.b64decode(file_json["content"]).decode("utf-8", errors="ignore")
        else:
            content = file_json.get("content", "")
        return f"File: {filename}\n{content}"
    except Exception as api_error:
        return f"Error fetching {filename} from GitHub: {api_error}"

def list_github_files(repo, github_token):
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
    contents_url = f"https://api.github.com/repos/{repo}/contents"
    try:
        resp = requests.get(contents_url, headers=headers)
        resp.raise_for_status()
        items = resp.json()
        return [item["name"] for item in items if item["type"] == "file"]
    except Exception as api_error:
        return []

if st.button("Ask Chatbot"):
    if user_input.strip():
        openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else ""
        github_token = os.getenv("GITHUB_TOKEN")
        repo_for_search = repo if repo else ""
        code_context = ""
        if repo_for_search and github_token:
            with st.spinner("Searching GitHub repo for relevant code..."):
                import re
                filename_match = re.search(r"([\w\-]+\.py)", user_input)
                if filename_match:
                    filename = filename_match.group(1)
                    code_context = fetch_github_file(repo_for_search, filename, github_token)
                else:
                    files = list_github_files(repo_for_search, github_token)
                    if files:
                        code_context = fetch_github_file(repo_for_search, files[0], github_token)
                    else:
                        code_context = "No files found in the GitHub repository."
        prompt = f"You are a helpful codebase assistant. Answer based on the following codebase context.\n\nCodebase context:{code_context}\n\nQuestion: {user_input}"
        try:
            response = openai.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "system", "content": "You are a codebase expert."}, {"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            chat_history.append((user_input, answer))
            st.session_state["chat_history"] = chat_history
        except Exception as e:
            answer = f"Error: {e}"
            chat_history.append((user_input, answer))
            st.session_state["chat_history"] = chat_history
    else:
        st.warning("Please enter a question.")

if chat_history:
    st.markdown("### Chat History")
    if st.button("Clear Chat History"):
        st.session_state["chat_history"] = []
        chat_history = []
        # st.experimental_rerun()
    for q, a in chat_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Bot:** {a}")
