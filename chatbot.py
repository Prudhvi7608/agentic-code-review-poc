
# chatbot.py
import os
import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import openai

st.title("GitHub Repo Chatbot")

github_token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {github_token}"}

chat_input = st.text_area("Chat with your GitHub assistant (ask anything, e.g. 'Hi', 'Where is agent_executor.py?', 'What does main.py do in owner/repo?'):")

def extract_repo_and_file(message):
    import re
    repo_match = re.search(r'([\w.-]+/[\w.-]+)', message)
    file_match = re.search(r'([\w./\\-]+\.py)', message)
    repo = repo_match.group(1) if repo_match else None
    filepath = file_match.group(1) if file_match else None
    return repo, filepath

def ask_llm(messages, api_key):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.1-mini", # or "gpt-4o" or your preferred model
        messages=messages,
        temperature=0.2
    )
    return response.choices[0].message.content

if st.button("Ask Agent"):
    openai_api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("OpenAI API key not found. Please add it to .streamlit/secrets.toml or .env.")
    elif not github_token:
        st.error("GITHUB_TOKEN is not loaded. Please check your .env file and environment setup.")
    elif not chat_input:
        st.warning("Please enter your question.")
    else:
        repo, filepath = extract_repo_and_file(chat_input)
        system_prompt = "You are a helpful assistant with access to the user's GitHub repositories. Answer general questions conversationally. If the user asks about a specific file, fetch its content and use it to answer. If the repo or file is not found, reply conversationally and ask the user to clarify or provide more details."
        user_message = chat_input
        file_fetched = False
        if repo and filepath:
            branch = os.getenv("CURRENT_BRANCH", "main")
            url = f"https://api.github.com/repos/{repo}/contents/{filepath}?ref={branch}"
            st.info(f"Fetching from URL: {url}")
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                content = resp.json().get("content", "")
                import base64
                try:
                    file_text = base64.b64decode(content).decode("utf-8")
                except Exception:
                    file_text = "Could not decode file content."
                user_message += f"\n\nFile: {filepath}\n\n{file_text}"
                file_fetched = True
            else:
                user_message += f"\n\n(File {filepath} in {repo} could not be fetched. Please check the repo and file name.)"
        elif filepath:
            user_message += f"\n\n(File {filepath} could not be fetched. Please specify the repo name as well.)"
        elif repo:
            user_message += f"\n\n(Repo {repo} specified, but no file name found. Please specify the file name.)"
        else:
            user_message += "\n\n(I couldn't detect a repo or file name. Please clarify your question or provide more details.)"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        with st.spinner("Agent is thinking..."):
            try:
                answer = ask_llm(messages, openai_api_key)
                st.markdown(answer)
            except Exception as e:
                st.error(f"LLM error: {e}")
