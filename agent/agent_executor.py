# agent/agent_executor.py
from langchain.agents import initialize_agent, AgentType
from utils.gemini_llm import getOpenAILLM
from tools.code_review_tool import review_code
from tools.complexity_tool import rate_complexity
import os

def getAgentExecutor():
    llm = llm = getOpenAILLM()
    tools = [review_code, rate_complexity]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    return agent

def execute_agent(input_text: str):
    agent = getAgentExecutor()
    instructions = (
        "You are an expert Python reviewer. "
        "First, use the code_review tool to analyze the code for issues and improvements. "
        "Then, use the rate_complexity tool to rate its complexity from 1-5 and explain why."
    )
    input_with_instructions = f"{instructions}\n\n{input_text}"
    review = agent.run(input_with_instructions)  # Use agent.run to get the LLM's review output
    complexity = agent.tools[1](input_with_instructions)  # rate_complexity
    return f"Review:\n{review}\n\nComplexity Rating:\n{complexity}"
