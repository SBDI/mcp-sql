# SQL Agent with MCP and Groq

A natural language interface to query SQLite databases using Groq's LLM and MCP (Machine Communication Protocol).

## Features

- Query databases using simple English commands
- AI generates and executes SQL queries safely
- Uses MCP for structured communication between components
- Powered by Groq's LLama3-70B model

## Quick Start

1. Make sure you have Python 3.12+ installed
2. Set your Groq API key in the `.env` file:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```
   uv venv .venv312 --python=3.12
   .venv312\Scripts\activate
   uv pip install -e .
   ```
4. Run the demo:
   ```
   run_sql_demo.bat
   ```
   This will open two windows - a server and a client.

## Example Queries

In the client window, try these queries:

- "all users"
- "users older than 30"
- "average age of users"
- "emails of all users"
- "add a new user named Alice Smith with email alice@example.com and age 35"

## How It Works

1. The server (mcp_server.py) provides a tool for executing SQL queries against a SQLite database
2. The client (mcp_client.py) takes natural language input and uses Groq to translate it to SQL
3. The query is executed via MCP and results are returned to the user

## Project Structure

- `mcp_client.py`: The client application that handles user input and LLM interaction
- `mcp_server.py`: The server that provides SQL execution capabilities
- `database.db`: Sample SQLite database with user data
- `run_sql_demo.bat`: Batch file to easily run both components
- `pyproject.toml`: Python project and dependency configuration
- `.env`: Environment variables (API keys)

