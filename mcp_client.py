import asyncio
from dataclasses import dataclass, field
from typing import Union, cast, List, Dict, Any
import json

import groq
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

groq_client = groq.AsyncGroq()

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["./mcp_server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

@dataclass
class Chat:
    messages: List[Dict[str, Any]] = field(default_factory=list)

    system_prompt: str = """You are a master SQLite assistant. 
    Your job is to use the tools at your disposal to execute SQL queries and provide the results to the user."""

    async def process_query(self, query: str) -> None:
        # Create a ClientSession from the read and write streams
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the connection
                await session.initialize()
                
                response = await session.list_tools()
                available_tools = [
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description or "",
                            "parameters": tool.inputSchema,
                        }
                    }
                    for tool in response.tools
                ]

                # Add the user's query to messages
                self.messages.append({"role": "user", "content": query})

                # Initial Groq API call
                res = await groq_client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "system", "content": self.system_prompt}] + self.messages,
                    tools=available_tools,
                    tool_choice="auto",
                    temperature=0.7,
                    max_tokens=8000,
                )

                assistant_message = res.choices[0].message
                if assistant_message.content:
                    print(assistant_message.content)
                    self.messages.append({
                        "role": "assistant",
                        "content": assistant_message.content
                    })

                if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = tool_call.function.arguments
                        
                        # Parse the tool_args if it's a string
                        if isinstance(tool_args, str):
                            parsed_tool_args = json.loads(tool_args)
                        else:
                            parsed_tool_args = tool_args
                            tool_args = json.dumps(tool_args)

                        # Execute tool call
                        result = await session.call_tool(tool_name, cast(dict, parsed_tool_args))

                        self.messages.append({
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [{
                                "id": tool_call.id,
                                "type": "function",
                                "function": {
                                    "name": tool_name,
                                    "arguments": tool_args
                                }
                            }]
                        })
                        
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result.content[0].text if result.content else "")
                        })

                        # Get next response from Groq
                        res = await groq_client.chat.completions.create(
                            model="llama3-70b-8192",
                            messages=self.messages,
                            tools=available_tools,
                            tool_choice="auto",
                            temperature=0.7,
                            max_tokens=8000,
                        )
                        
                        assistant_message = res.choices[0].message
                        if assistant_message.content:
                            print(assistant_message.content)
                            self.messages.append({
                                "role": "assistant",
                                "content": assistant_message.content
                            })

    async def chat_loop(self):
        while True:
            query = input("\nQuery: ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit"]:
                break
            await self.process_query(query)


async def main():
    chat = Chat()
    await chat.chat_loop()


if __name__ == "__main__":
    asyncio.run(main())
