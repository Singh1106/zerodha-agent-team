# Project Overview

This is a Python project that implements a Gemini agent with local command execution capabilities. The agent is built using the `google-adk` library and is configured to use a toolset called "WCGW" for interacting with the local system.

**Key Technologies:**

*   **Python:** The core programming language.
*   **Poetry:** For dependency management.
*   **google-adk:** The library used to build the Gemini agent.
*   **python-dotenv:** For managing environment variables.

**Architecture:**

The project consists of a single agent defined in `root_agent/agent.py`. The agent is configured with a specific model and a set of tools. The "WCGW" toolset is used to provide the agent with local command execution capabilities.

# Building and Running

**1. Install Dependencies:**

```bash
poetry install
```

**2. Configure Environment Variables:**

Create a `.env` file in the `root_agent` directory with the following content:

```
AGENT_NAME=root_agent_with_wcgw
MODEL_NAME=gemini-1.5-pro-latest
```

**3. Run the Agent:**

```bash
poetry run python root_agent/agent.py
```

# Development Conventions

*   **Dependency Management:** Dependencies are managed using Poetry. Add any new dependencies to the `pyproject.toml` file.
*   **Environment Variables:** All configuration should be managed through environment variables. Use the `.env` file for local development.
*   **Logging:** The agent uses the `logging` module to log information to `root_agent/root_agent.log`.
