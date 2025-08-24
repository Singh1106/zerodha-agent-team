import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioConnectionParams,
    StdioServerParameters,
)

# Configure logging
script_dir = Path(__file__).parent
log_file_path = script_dir / 'zerodha_kite_agent.log'

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
agent_name = os.getenv("AGENT_NAME", "zerodha_kite_agent")
logger.info(f"Agent Name: {agent_name}")
model_name = os.getenv("MODEL_NAME", "gemini-2.5-pro")
logger.info(f"Model Name: {model_name}")

def get_kite_toolset() -> MCPToolset:
    """Get Kite MCP toolset configuration"""
    logger.info("Getting Kite toolset")

    toolset = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=[
                  "mcp-remote", "https://mcp.kite.trade/mcp"
                ],
            ),
        ),
    )
    logger.info("Kite MCP toolset created successfully.")
    return toolset

# Add toolsets
tools = [get_kite_toolset()]
logger.debug("Toolsets configured.")

# Build dynamic instruction
instruction = f"""You are a helpful agent with trading capabilities.

Key capabilities:
- Retrieve market data, manage portfolios, and execute trades using the Kite Connect API.

Always be mindful of security best practices when executing commands. Use appropriate permissions and avoid potentially destructive operations without explicit confirmation."""
logger.debug("Instruction for agent created.")

zerodha_kite_agent = Agent(
    name=agent_name,
    model=model_name,
    description="""Agent with trading capabilities via Kite Connect API.
Available tools:
- Authentication: login
- Market Data: get_quotes, get_ltp, get_ohlc, get_historical_data, search_instruments
- Portfolio & Account: get_profile, get_margins, get_holdings, get_positions, get_mf_holdings
- Orders & Trading: place_order, modify_order, cancel_order, get_orders, get_trades, get_order_history, get_order_trades
- GTT Orders: get_gtts, place_gtt_order, modify_gtt_order, delete_gtt_order""",
    instruction=instruction,
    tools=tools,
)
logger.info(f"Agent '{agent_name}' created successfully.")

logger.info("Script finished.")
