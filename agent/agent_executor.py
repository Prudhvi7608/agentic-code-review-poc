# agent/agent_executor.py
from langchain.agents import initialize_agent, AgentType
from utils.gemini_llm import getOpenAILLM
from tools.code_review_tool import review_code
from tools.complexity_tool import rate_complexity
import os

def getAgentExecutor():
    llm = getOpenAILLM()
    tools = [review_code, rate_complexity]
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,  # Turn off verbose output
        handle_parsing_errors=True,  # Retry or handle output parsing errors
    )
    return agent

def execute_agent(input_text: str):
    agent = getAgentExecutor()
    instructions = (
        "You are an expert Python reviewer. "
        "Use the code_review tool to analyze the code for issues and improvements. "
        "For each issue, clearly state the problem, quote the problematic code, and provide a concise suggestion. "
        "Show the corrected code in a Python code block after each suggestion. "
        "Check for logging, structure, error handling, best practices, code readability, security, and performance. "
        "At the end, output the entire corrected file in a single Python code block. "
        "Then, use the rate_complexity tool to rate its complexity from 1-5 and explain why. "
        "Keep your output structured and concise."
    )
    input_with_instructions = f"{instructions}\n\n{input_text}"
    review = agent.run(input_with_instructions)
    return review
