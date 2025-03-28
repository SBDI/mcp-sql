# Hands-on Model Context Protocol (MCP)

This project demonstrates how to use the Model Context Protocol (MCP) to create a natural language interface to SQLite databases. It's a practical introduction to building AI systems that can interact with external tools.

## What is MCP?

MCP is designed as a universal protocol that connects AI systems with data sources and tools using a standardized communication layer. As described by Anthropic:
> "The Model Context Protocol is an open standard that enables developers to build secure, two-way connections between their data sources and AI-powered tools." anthropic.com
It functions somewhat like an "Internet for Agents," providing a standardized way for AI systems to access external tools without needing custom integrations for each one.

This demo shows how an LLM (Groq's Llama3-70B) can execute SQL queries through MCP, without directly accessing the database.

## Getting Started

1. Make sure you have Python 3.12+ installed
2. Set your Groq API key in the `.env` file:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```
   uv venv .venv --python=3.12
   .venv\Scripts\activate
   uv pip install -e .
   ```
4. Run the demo:
   ```
   run_sql_demo.bat
   ```
   This will open two windows - an MCP server and an MCP client.

## Hands-on with MCP

In the client window, try natural language queries like:

- "all users" - The LLM converts this to a SQL query using MCP's tool interface
- "users older than 30" - Watch how complex queries get properly translated
- "average age of users" - See aggregation functions at work
- "add a new user named Alice Smith with email alice@example.com and age 35" - Try data manipulation

Each query demonstrates how MCP enables an LLM to use external tools (SQL queries) safely and effectively.

## How MCP Works in This Project

1. **MCP Server (mcp_server.py)**: 
   - Defines tools (like `query_data`) with schemas
   - Handles execution of SQL queries against a database
   - Returns results in a structured format

2. **MCP Client (mcp_client.py)**:
   - Takes natural language input from users
   - Uses Groq's LLM to generate tool calls via MCP
   - Handles the communication protocol with the server

The magic happens through MCP's standardized communication, allowing LLMs to use tools without accessing the underlying code.

## Project Structure

- `mcp_server.py`: MCP server with SQL execution capabilities
- `mcp_client.py`: MCP client for LLM-driven tool calling
- `database.db`: Sample SQLite database with user data
- `run_sql_demo.bat`: Script to run both MCP components
- `pyproject.toml`: Python project configuration
- `.env`: Environment variables (API keys)

