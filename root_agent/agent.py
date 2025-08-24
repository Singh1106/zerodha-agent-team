import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from root_agent.sub_agents.zerodha_kite_agent.agent import zerodha_kite_agent
from root_agent.sub_agents.wcgw_agent.agent import wcgw_agent

# Configure logging
script_dir = Path(__file__).parent
log_file_path = script_dir / 'root_agent.log'

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler(log_file_path, mode='w')
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

logger.info("Starting agent script...")

# Load environment variables from .env file
load_dotenv()
logger.info("Loaded environment variables.")

# Get configuration from environment variables
agent_name = os.getenv("AGENT_NAME", "root_agent")
logger.info(f"Agent Name: {agent_name}")
model_name = os.getenv("MODEL_NAME", "gemini-2.5-pro")
logger.info(f"Model Name: {model_name}")

# Build dynamic instruction
instruction = f"""You are a root agent that orchestrates tasks between sub-agents.
You have access to the following sub-agents:
- zerodha_kite_agent: An agent with trading capabilities.
- wcgw_agent: An agent with local command execution capabilities.

Delegate tasks to the appropriate sub-agent based on the user's request."""
logger.debug("Instruction for agent created.")

root_agent = LlmAgent(
    name=agent_name,
    model=model_name,
    description="Root agent for orchestrating sub-agents",
    instruction=instruction,
    sub_agents=[zerodha_kite_agent, wcgw_agent]
)
logger.info(f"Agent '{agent_name}' created successfully.")

logger.info("Script finished.")
