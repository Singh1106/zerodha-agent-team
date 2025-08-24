import os
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioConnectionParams,
    StdioServerParameters,
)

# Get configuration from environment variables
agent_name = os.getenv("AGENT_NAME", "zerodha_kite_agent")
model_name = os.getenv("MODEL_NAME", "gemini-2.5-pro")

def get_kite_toolset() -> MCPToolset:
    """Get Kite MCP toolset configuration"""
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
    return toolset

# Add toolsets
tools = [get_kite_toolset()]

# Build dynamic instruction
instruction = f"""You are a helpful agent with trading capabilities.

Key capabilities:
- Retrieve market data, manage portfolios, and execute trades using the Kite Connect API.

Always be mindful of security best practices when executing commands. Use appropriate permissions and avoid potentially destructive operations without explicit confirmation."""

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