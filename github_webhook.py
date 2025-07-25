from flask import Flask, request, jsonify
import json
import os
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook received!")
    try:
        # Log raw request data for debugging
        print(f"Raw data: {request.data}")
        try:
            payload = request.get_json(force=True)
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return jsonify({"status": "error", "details": "Invalid JSON payload"}), 400
        print(json.dumps(payload, indent=2))  # Pretty print payload for debugging

        # Extract key info safely
        action = payload.get('action', None)
        pull_request = payload.get('pull_request', {})
        repo = payload.get('repository', {}).get('full_name', None)
        sender = payload.get('sender', {}).get('login', None)

        print(f"Action: {action}, Repo: {repo}, Sender: {sender}")

        # Get PR number
        pr_number = pull_request.get('number', None)
        if not pr_number:
            pr_number = payload.get('number', None)
        if not pr_number or not repo:
            return jsonify({"status": "error", "details": "Missing PR number or repo"}), 400

        # Get GitHub token from environment
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            raise Exception('GITHUB_TOKEN environment variable not set')

        # Fetch changed files from GitHub API
        headers = {'Authorization': f'token {github_token}', 'Accept': 'application/vnd.github.v3+json'}
        files_url = f'https://api.github.com/repos/{repo}/pulls/{pr_number}/files'
        files_resp = requests.get(files_url, headers=headers)
        files_resp.raise_for_status()
        files = files_resp.json()

        # Fetch full file contents for review
        changed_files_content = []
        for file in files:
            filename = file.get('filename')
            raw_url = file.get('raw_url')
            file_content = ''
            if raw_url:
                try:
                    raw_resp = requests.get(raw_url, headers=headers)
                    raw_resp.raise_for_status()
                    file_content = raw_resp.text
                except Exception as fetch_err:
                    print(f"Error fetching raw file {filename}: {fetch_err}")
                    file_content = f"Error fetching raw file: {fetch_err}"
            else:
                file_content = f"Raw URL not available for {filename}"
            changed_files_content.append({'filename': filename, 'content': file_content})

        # Combine all full file contents for agentic review
        review_input = '\n\n'.join([f"File: {f['filename']}\n{f['content']}" for f in changed_files_content])

        # Import agent_executor and run agentic workflow
        from agent.agent_executor import execute_agent
        try:
            agent_result = execute_agent(review_input)
            status = "processed"
        except Exception as agent_error:
            print(f"Agentic workflow error: {agent_error}")
            agent_result = f"Agentic workflow failed: {agent_error}"
            status = "error"
        print(f"Agentic workflow result: {agent_result}")

        # Always return 200 OK to GitHub to prevent delivery failure
        return jsonify({"status": status, "agent_result": agent_result}), 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "details": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000)
