# tools/code_review_tool.py
from langchain.tools import tool

@tool
def review_code(code: str) -> str:
    """Reviews Python code and suggests improvements including logging, structure, error handling, and best practices."""
    return f"""
Please review this code:

{code}

Your tasks:
- Identify and explain any bugs, issues, or missing elements in the code.
- Suggest improvements and best practices.
- Check for:
  - Logging
  - Structure
  - Error handling
  - Best practices
  - Code readability
  - Security issues
  - Performance issues
- Provide actionable suggestions for each problem found.
"""
