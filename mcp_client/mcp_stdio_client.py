from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import json
import os
# import nest_asyncio
# nest_asyncio.apply()


load_dotenv("../.env")

async def main(): #query
    """Loads tools from MCP server and integrates them with an agent"""
    print("Loading json file..")
    path = r"D:\My Files\MCP_Agent_Chatbot\mcp_client\mcp.json"
    try:
        if not os.path.exists(path):
            raise FileNotFoundError("mcp.json not found")
        if os.stat(path).st_size == 0:
            raise ValueError("mcp.json is empty!")

        with open(path, "r") as f:
            connections = json.load(f)

        print("Connections Retrieved")

    except Exception as e:
        return f"Error:{e}"

    # client = MultiServerMCPClient(connections)
    # print(client)
    # tools = await client.get_tools()
    # print("Loaded tools:", tools)

    # agent = create_react_agent(
    #     model= ChatGroq(model="deepseek-r1-distill-llama-70b"),
    #     tools= tools,
    # )
    # weather_response = await agent.ainvoke(
    # {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
    # )

    # print("Math response:", weather_response["messages"][-1].content)

if __name__ == "__main__":
    import asyncio
    #query = input("Enter your query: ")
    asyncio.run(main())