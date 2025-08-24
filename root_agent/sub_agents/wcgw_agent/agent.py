import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioConnectionParams,
    StdioServerParameters,
)

# Get configuration from environment variables
agent_name = os.getenv("AGENT_NAME", "wcgw_agent")
model_name = os.getenv("MODEL_NAME", "gemini-2.5-pro")

def get_wcgw_toolset() -> MCPToolset:
    """Get WCGW MCP toolset configuration"""
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
    return toolset

# Add WCGW toolset
tools = [get_wcgw_toolset()]

# Build dynamic instruction
instruction = f"""You are a helpful agent with local command execution capabilities.

Key capabilities:
- Execute commands locally on the system
- Navigate and manage files on the local system
- Install packages, configure services, and perform system administration tasks
- Monitor system resources and processes

Always be mindful of security best practices when executing commands. Use appropriate permissions and avoid potentially destructive operations without explicit confirmation."""

wcgw_agent = LlmAgent(
    name=agent_name,
    model=model_name,
    description="Agent with local command execution via WCGW",
    instruction=instruction,
    tools=tools,
)