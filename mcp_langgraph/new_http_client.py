from langchain_mcp_adapters.client import MultiServerMCPClient

async def mcp_tools_node(state, config):
    user = config["configurable"]["langgraph_auth_user"]
         # e.g., user["github_token"], user["email"], etc.

    client = MultiServerMCPClient({
        "github": {
            "transport": "streamable_http", # 
            "url": "https://my-github-mcp-server/mcp", # 
            "headers": {
                "Authorization": f"Bearer {user['github_token']}" 
            }
        }
    })
    tools = await client.get_tools() # 

    # Your tool-calling logic here

    tool_messages = tools
    return {"messages": tool_messages}

if __name__ == "__main__":
    import asyncio
    config = {"configurable":{"langgraph_auth_user": ""}}
    asyncio.run(mcp_tools_node("CA", config))