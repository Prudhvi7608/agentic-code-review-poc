# tools/code_review_tool.py
from langchain.tools import tool

@tool
def review_code(code: str) -> str:
    """Reviews Python code and suggests improvements including logging, structure, error handling, and best practices."""
    return f"""
## :robot: Agent Review

Please review this code:

{code}

Your tasks:
1. Identify and explain any bugs, issues, or missing elements in the code.
2. For each issue, first highlight the mistaken part (quote the problematic line or section), then provide a suggestion, and then show the corrected code in a Python code block immediately after your suggestion.
3. Check for: Logging, structure, error handling, best practices, code readability, security issues, and performance issues.
4. At the end of your review, output the entire corrected file in a single Python code block.
5. Provide actionable suggestions for each problem found.
"""
