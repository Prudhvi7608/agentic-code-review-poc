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
    )
    return agent

def execute_agent(input_text: str):
    agent = getAgentExecutor()
    instructions = (
        "You are an expert Python reviewer. "
        "First, use the code_review tool to analyze the code for issues and improvements. "
        "For each issue you find, provide a suggestion and then show the corrected code in a Python code block immediately after your suggestion. "
        "Check that logging is present, structure is good, error handling is robust, and best practices are followed. "
        "At the end of your review, output the entire corrected file in a single Python code block. "
        "Then, use the rate_complexity tool to rate its complexity from 1-5 and explain why. "
        "Do NOT repeat the original code in your output except in corrected code blocks. Only output your final review, suggestions, corrected code, and complexity rating."
    )
    input_with_instructions = f"{instructions}\n\n{input_text}"
    review = agent.run(input_with_instructions)
    return review
