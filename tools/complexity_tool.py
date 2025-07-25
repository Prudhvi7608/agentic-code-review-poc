from langchain.tools import tool

@tool
def rate_complexity(code: str) -> str:
    """Rates the complexity of a given Python code snippet from 1 (simple) to 5 (complex) with justification."""
    return f"""
Analyze this code:

{code}

Then give a complexity score from 1 (simple) to 5 (very complex), and explain why.
"""
