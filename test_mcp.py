"""
Simple test script to connect to a running Azure AI Agent MCP Server and perform a web search.

Make sure to start the MCP server first:
python azure_agent_with_bing.py
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent

async def test_web_search():
    """Connect to the running MCP server and test web search."""
    
    print("Connecting to MCP server...")
    
    # Connect to the running MCP server via stdio
    server_params = StdioServerParameters(
        command="python",
        args=["azure_agent_with_bing.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize the session
            await session.initialize()
            print("✅ Connected to MCP server successfully!")
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools.tools]}")
            
            # Find the web_search tool
            web_search_tool = None
            for tool in tools.tools:
                if tool.name == "web_search":
                    web_search_tool = tool
                    break
            
            if not web_search_tool:
                print("❌ web_search tool not found!")
                return
            
            print(f"Found web_search tool: {web_search_tool.description}")
            
            # Call the web_search tool
            print("Calling web_search tool...")
            result = await session.call_tool(
                "web_search",
                {"query": "latest AI news 2025"}
            )
            
            print("✅ Web search completed!")
            if result.content:
                for content in result.content:
                    if isinstance(content, TextContent):
                        print(f"Result: {content.text[:300]}...")
                        break
                else:
                    print(f"Result: {str(result.content[0])[:300]}...")
            else:
                print("No content returned")

def main():
    """Run the test."""
    print("Azure AI Agent MCP Server Test")
    print("=" * 40)
    print("Note: Make sure the MCP server is running first!")
    print("Start it with: python azure_agent_with_bing.py")
    print()
    
    try:
        asyncio.run(test_web_search())
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Make sure the MCP server is running and accessible.")

if __name__ == "__main__":
    main()
