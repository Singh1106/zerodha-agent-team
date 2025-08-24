import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioConnectionParams,
    StdioServerParameters,
)

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
agent_name = os.getenv("AGENT_NAME", "root_agent_with_wcgw")
logger.info(f"Agent Name: {agent_name}")
model_name = os.getenv("MODEL_NAME", "gemini-2.5-pro")
logger.info(f"Model Name: {model_name}")

def get_wcgw_toolset() -> MCPToolset:
    """Get WCGW MCP toolset configuration"""
    logger.info("Getting WCGW toolset")

    toolset = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="uv",
                args=[
                  "tool", "run", "--python", "3.12", "wcgw@latest"
                ],
            ),
        ),
    )
    logger.info("WCGW MCP toolset created successfully.")
    return toolset

# Add WCGW toolset
tools = [get_wcgw_toolset()]
logger.debug("WCGW toolset configured.")

# Build dynamic instruction
instruction = f"""You are a helpful agent with local command execution capabilities.

Key capabilities:
- Execute commands locally on the system
- Navigate and manage files on the local system
- Install packages, configure services, and perform system administration tasks
- Monitor system resources and processes

Always be mindful of security best practices when executing commands. Use appropriate permissions and avoid potentially destructive operations without explicit confirmation."""
logger.debug("Instruction for agent created.")

root_agent = LlmAgent(
    name=agent_name,
    model=model_name,
    description="Agent with local command execution via WCGW",
    instruction=instruction,
    tools=tools,
)
logger.info(f"Agent '{agent_name}' created successfully.")

logger.info("Script finished.")
