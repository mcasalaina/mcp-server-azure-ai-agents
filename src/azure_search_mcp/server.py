from typing import Optional, List, Dict, Any, Union
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types
import mcp
import click
import asyncio
import json
import os
from .connector import AzureSearchConnector


def serve(endpoint: str, api_key: str, index_name: str) -> Server:
    """
    Create and configure the MCP server with Azure Search tools.

    Args:
        endpoint: Azure Search service endpoint
        api_key: Azure Search API key
        index_name: Default index name to use
    """
    server = Server("azure-search")
    azure_search = AzureSearchConnector(endpoint, api_key, index_name)

    @server.list_tools()
    async def list_tools() -> List[types.Tool]:
        return [
            types.Tool(
                name="azure-search-text-search",
                description="Search for documents using full text search in an Azure Search index",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query_text": {
                            "type": "string",
                            "description": "Text to search for",
                        },
                        "index_name": {
                            "type": "string",
                            "description": "Name of the index to search (optional, uses default if not specified)",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return",
                            "default": 5,
                        },
                        "output_fields": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Fields to include in results",
                        },
                        "filter_expr": {
                            "type": "string",
                            "description": "Optional filter expression",
                        },
                        "semantic_configuration": {
                            "type": "string",
                            "description": "Optional semantic configuration name to enable semantic search",
                        },
                    },
                    "required": ["query_text"],
                },
            ),
            types.Tool(
                name="azure-search-list-indexes",
                description="List all indexes in the Azure Search service",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="azure-search-index-info",
                description="Get detailed information about an Azure Search index",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "index_name": {
                            "type": "string",
                            "description": "Name of the index",
                        }
                    },
                    "required": ["index_name"],
                },
            ),
            types.Tool(
                name="azure-search-query",
                description="Query Azure Search index using filter expressions",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filter_expr": {
                            "type": "string",
                            "description": "Filter expression (e.g. 'category eq \\'documentation\\'')",
                        },
                        "index_name": {
                            "type": "string",
                            "description": "Name of the index to query (optional, uses default if not specified)",
                        },
                        "output_fields": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Fields to include in results",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results",
                            "default": 10,
                        },
                    },
                    "required": ["filter_expr"],
                },
            ),
            types.Tool(
                name="azure-search-vector-search",
                description="Perform vector similarity search on an Azure Search index",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "vector": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Query vector",
                        },
                        "vector_field": {
                            "type": "string",
                            "description": "Field containing vectors to search",
                        },
                        "index_name": {
                            "type": "string",
                            "description": "Name of the index to search (optional, uses default if not specified)",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results",
                            "default": 5,
                        },
                        "output_fields": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Fields to include in results",
                        },
                        "filter_expr": {
                            "type": "string",
                            "description": "Optional filter expression",
                        },
                        "semantic_configuration": {
                            "type": "string",
                            "description": "Optional semantic configuration name to enable semantic search",
                        },
                    },
                    "required": ["vector", "vector_field"],
                },
            ),
            types.Tool(
                name="azure-search-hybrid-search",
                description="Perform hybrid search combining text and vector similarity on an Azure Search index",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query_text": {
                            "type": "string",
                            "description": "Text to search for",
                        },
                        "vector": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Query vector",
                        },
                        "vector_field": {
                            "type": "string",
                            "description": "Field containing vectors to search",
                        },
                        "index_name": {
                            "type": "string",
                            "description": "Name of the index to search (optional, uses default if not specified)",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results",
                            "default": 5,
                        },
                        "output_fields": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Fields to include in results",
                        },
                        "filter_expr": {
                            "type": "string",
                            "description": "Optional filter expression",
                        },
                        "semantic_configuration": {
                            "type": "string",
                            "description": "Optional semantic configuration name to enable semantic search",
                        },
                    },
                    "required": ["query_text", "vector", "vector_field"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name == "azure-search-text-search":
            query_text = arguments["query_text"]
            index_name = arguments.get("index_name", azure_search.index_name)
            limit = arguments.get("limit", 5)
            output_fields = arguments.get("output_fields")
            filter_expr = arguments.get("filter_expr")
            semantic_configuration = arguments.get("semantic_configuration")

            # If index_name is different from the default, create a new connector
            if index_name != azure_search.index_name:
                connector = AzureSearchConnector(
                    endpoint=azure_search.endpoint,
                    api_key=azure_search.credential.key,
                    index_name=index_name,
                )
            else:
                connector = azure_search

            results = await connector.text_search(
                query_text=query_text,
                limit=limit,
                output_fields=output_fields,
                filter_expr=filter_expr,
                semantic_configuration=semantic_configuration,
            )

            content = [
                types.TextContent(
                    type="text",
                    text=f"Search results for '{query_text}' in index '{index_name}':",
                )
            ]

            for result in results:
                content.append(
                    types.TextContent(
                        type="text", text=f"<r>{json.dumps(result, indent=2)}<r>"
                    )
                )

            return content

        elif name == "azure-search-list-indexes":
            indexes = await azure_search.list_indexes()
            return [
                types.TextContent(
                    type="text",
                    text=f"Indexes in Azure Search service:\n{', '.join(indexes)}",
                )
            ]

        elif name == "azure-search-index-info":
            index_name = arguments["index_name"]
            info = await azure_search.get_index_info(index_name)
            return [
                types.TextContent(
                    type="text",
                    text=f"Index info for '{index_name}':\n{json.dumps(info, indent=2)}",
                )
            ]

        elif name == "azure-search-query":
            filter_expr = arguments["filter_expr"]
            index_name = arguments.get("index_name", azure_search.index_name)
            output_fields = arguments.get("output_fields")
            limit = arguments.get("limit", 10)

            # If index_name is different from the default, create a new connector
            if index_name != azure_search.index_name:
                connector = AzureSearchConnector(
                    endpoint=azure_search.endpoint,
                    api_key=azure_search.credential.key,
                    index_name=index_name,
                )
            else:
                connector = azure_search

            results = await connector.query(
                filter_expr=filter_expr, output_fields=output_fields, limit=limit
            )

            content = [
                types.TextContent(
                    type="text",
                    text=f"Query results for '{filter_expr}' in index '{index_name}':",
                )
            ]

            for result in results:
                content.append(
                    types.TextContent(
                        type="text", text=f"<r>{json.dumps(result, indent=2)}<r>"
                    )
                )

            return content

        elif name == "azure-search-vector-search":
            vector = arguments["vector"]
            vector_field = arguments["vector_field"]
            index_name = arguments.get("index_name", azure_search.index_name)
            limit = arguments.get("limit", 5)
            output_fields = arguments.get("output_fields")
            filter_expr = arguments.get("filter_expr")
            semantic_configuration = arguments.get("semantic_configuration")

            # If index_name is different from the default, create a new connector
            if index_name != azure_search.index_name:
                connector = AzureSearchConnector(
                    endpoint=azure_search.endpoint,
                    api_key=azure_search.credential.key,
                    index_name=index_name,
                )
            else:
                connector = azure_search

            results = await connector.vector_search(
                vector=vector,
                vector_field=vector_field,
                limit=limit,
                output_fields=output_fields,
                filter_expr=filter_expr,
                semantic_configuration=semantic_configuration,
            )

            content = [
                types.TextContent(
                    type="text", text=f"Vector search results in index '{index_name}':"
                )
            ]

            for result in results:
                content.append(
                    types.TextContent(
                        type="text", text=f"<r>{json.dumps(result, indent=2)}<r>"
                    )
                )

            return content

        elif name == "azure-search-hybrid-search":
            query_text = arguments["query_text"]
            vector = arguments["vector"]
            vector_field = arguments["vector_field"]
            index_name = arguments.get("index_name", azure_search.index_name)
            limit = arguments.get("limit", 5)
            output_fields = arguments.get("output_fields")
            filter_expr = arguments.get("filter_expr")
            semantic_configuration = arguments.get("semantic_configuration")

            # If index_name is different from the default, create a new connector
            if index_name != azure_search.index_name:
                connector = AzureSearchConnector(
                    endpoint=azure_search.endpoint,
                    api_key=azure_search.credential.key,
                    index_name=index_name,
                )
            else:
                connector = azure_search

            results = await connector.hybrid_search(
                query_text=query_text,
                vector=vector,
                vector_field=vector_field,
                limit=limit,
                output_fields=output_fields,
                filter_expr=filter_expr,
                semantic_configuration=semantic_configuration,
            )

            content = [
                types.TextContent(
                    type="text",
                    text=f"Hybrid search results for '{query_text}' in index '{index_name}':",
                )
            ]

            for result in results:
                content.append(
                    types.TextContent(
                        type="text", text=f"<r>{json.dumps(result, indent=2)}<r>"
                    )
                )

            return content

    return server


@click.command()
@click.option(
    "--endpoint",
    envvar="AZURE_SEARCH_ENDPOINT",
    required=True,
    help="Azure Search service endpoint",
)
@click.option(
    "--api-key",
    envvar="AZURE_SEARCH_API_KEY",
    required=True,
    help="Azure Search API key",
)
@click.option(
    "--index-name",
    envvar="AZURE_SEARCH_INDEX_NAME",
    required=True,
    help="Default Azure Search index name",
)
def main(endpoint: str, api_key: str, index_name: str):
    async def _run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            server = serve(endpoint, api_key, index_name)
            print(f"MCP server starting... Endpoint: {endpoint}, Index: {index_name}")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="azure-search",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    asyncio.run(_run())


if __name__ == "__main__":
    main()
