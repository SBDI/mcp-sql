@echo off
echo Starting SQL Demo...

REM Start server in a new window
start "MCP SQL Server" cmd /k ".venv\Scripts\activate && python src\mcp_sql\mcp_server.py"

REM Wait a moment for the server to initialize
timeout /t 2 /nobreak > nul

REM Start client in a new window
start "MCP SQL Client" cmd /k ".venv\Scripts\activate && python src\mcp_sql\mcp_client.py"

echo Demo started in separate windows. 
