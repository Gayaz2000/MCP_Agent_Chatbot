from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import json
import os
# import nest_asyncio
# nest_asyncio.apply()


load_dotenv("../.env")

async def main():
    """Loads tools from MCP server and integrates them with an agent"""
    with open("D:\\My Files\\MCP_Agent_Chatbot\\mcp_client\\mcp.json", "r") as f:
        connections = json.load(f)

    client = MultiServerMCPClient(connections=connections)

    tools = await client.get_tools()
    #print("Loaded tools:", tools)

    agent = create_react_agent(
        model= ChatGroq(model="deepseek-r1-distill-llama-70b"),
        tools= tools,
    )
    math_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": }]}
    )

    print("Math response:", math_response["messages"][-1].content)

if __name__ == "__main__":
    import asyncio
    #query = input("Enter your query: ")
    asyncio.run(main())