import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from root_agent.sub_agents.zerodha_kite_agent.agent import zerodha_kite_agent
from root_agent.sub_agents.wcgw_agent.agent import wcgw_agent

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
agent_name = "root_agent"
model_name = "gemini-2.5-pro"

# Build dynamic instruction
instruction = f"""You are a root agent that orchestrates tasks between sub-agents.
You have access to the following sub-agents:
- zerodha_kite_agent: An agent with trading capabilities.
- wcgw_agent: An agent with local command execution capabilities.

Delegate tasks to the appropriate sub-agent based on the user's request."""

root_agent = LlmAgent(
    name=agent_name,
    model=model_name,
    description="Root agent for orchestrating sub-agents",
    instruction=instruction,
    sub_agents=[zerodha_kite_agent, wcgw_agent]
)