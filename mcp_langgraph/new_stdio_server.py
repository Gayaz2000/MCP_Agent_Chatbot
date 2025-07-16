from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent