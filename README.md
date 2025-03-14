# MCP Server for Azure AI Search

> The Model Context Protocol (MCP) is an open protocol that enables seamless integration between LLM applications and external data sources and tools. This repository contains a MCP server that provides access to [Azure AI Search](https://azure.microsoft.com/en-us/products/ai-services/ai-search) functionality.

## Prerequisites

Before using this MCP server, ensure you have:

- Python 3.8 or higher
- An Azure AI Search service set up
- An index created in your Azure AI Search service

## Installation

Install the package using pip:

```bash
pip install azure-search-mcp
```

Alternatively, you can install directly from the repository:

```bash
pip install git+https://github.com/your-username/azure-search-mcp.git
```

## Usage

The server can be run directly from the command line:

```bash
azure-search-mcp --endpoint "https://<your-search-service>.search.windows.net" --api-key "<your-api-key>" --index-name "<your-index-name>"
```

You can also set environment variables instead of using command-line options:

```bash
export AZURE_SEARCH_ENDPOINT="https://<your-search-service>.search.windows.net"
export AZURE_SEARCH_API_KEY="<your-api-key>"
export AZURE_SEARCH_INDEX_NAME="<your-index-name>"
azure-search-mcp
```

## Supported Applications

This MCP server can be used with various LLM applications that support the Model Context Protocol:

- **Claude Desktop**: Anthropic's desktop application for Claude
- **Cursor**: AI-powered code editor with MCP support in its Composer feature
- **Custom MCP clients**: Any application implementing the MCP client specification

## Usage with Claude Desktop

1. Install Claude Desktop from https://claude.ai/download
2. Open your Claude Desktop configuration:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

3. Add the following configuration (modify paths as needed):
```json
{
  "mcpServers": {
    "azure-search": {
      "command": "/PATH/TO/python",
      "args": [
        "-m",
        "azure_search_mcp.server",
        "--endpoint", "https://<your-search-service>.search.windows.net",
        "--api-key", "<your-api-key>",
        "--index-name", "<your-index-name>"
      ]
    }
  }
}
```

4. Restart Claude Desktop

## Usage with Cursor

[Cursor also supports MCP](https://docs.cursor.com/context/model-context-protocol) tools through its Agent feature in Composer.

Create a `.cursor/mcp.json` file in your project root:

1. Create the `.cursor` directory in your project root:
   ```bash
   mkdir -p /path/to/your/project/.cursor
   ```

2. Create a `mcp.json` file with the following content:
   ```json
   {
     "mcpServers": {
       "azure-search": {
         "command": "/PATH/TO/python",
         "args": [
           "-m",
           "azure_search_mcp.server",
           "--endpoint", "https://<your-search-service>.search.windows.net",
           "--api-key", "<your-api-key>",
           "--index-name", "<your-index-name>"
         ]
       }
     }
   }
   ```

3. Restart Cursor or reload the window

## Available Tools

The server provides the following tools:

### Search Operations

- `azure-search-text-search`: Perform full-text search on an index
  - Parameters:
    - `query_text`: Text to search for
    - `index_name`: Name of the index (optional, uses default if not specified)
    - `limit`: Maximum results (default: 5)
    - `output_fields`: Fields to include in results
    - `filter_expr`: Optional filter expression
    - `semantic_configuration`: Optional semantic configuration name to enable semantic search

- `azure-search-vector-search`: Perform vector similarity search
  - Parameters:
    - `vector`: Query vector
    - `vector_field`: Field containing vectors to search
    - `index_name`: Name of the index (optional, uses default if not specified)
    - `limit`: Maximum results (default: 5)
    - `output_fields`: Fields to include in results
    - `filter_expr`: Optional filter expression
    - `semantic_configuration`: Optional semantic configuration name to enable semantic search

- `azure-search-hybrid-search`: Perform hybrid search combining text and vector similarity
  - Parameters:
    - `query_text`: Text to search for
    - `vector`: Query vector
    - `vector_field`: Field containing vectors to search
    - `index_name`: Name of the index (optional, uses default if not specified)
    - `limit`: Maximum results (default: 5)
    - `output_fields`: Fields to include in results
    - `filter_expr`: Optional filter expression
    - `semantic_configuration`: Optional semantic configuration name to enable semantic search

### Index Management

- `azure-search-list-indexes`: List all indexes in the search service

- `azure-search-index-info`: Get detailed information about an index
  - Parameters:
    - `index_name`: Name of the index

### Query Operations

- `azure-search-query`: Query an index using filter expressions
  - Parameters:
    - `filter_expr`: Filter expression (e.g. 'category eq 'documentation'')
    - `index_name`: Name of the index (optional, uses default if not specified)
    - `output_fields`: Fields to include in results
    - `limit`: Maximum results (default: 10)

## Semantic Search Support

For `azure-search-text-search`, `azure-search-vector-search`, and `azure-search-hybrid-search`, you can enable semantic ranking by providing a `semantic_configuration` parameter with the name of a semantic configuration defined in your Azure Search index.

Example:
```json
{
  "query_text": "What is Azure AI Search?",
  "semantic_configuration": "my-semantic-config"
}
```

Semantic search capabilities must be [configured in your Azure Search index](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview) before using this feature.

## Environment Variables

- `AZURE_SEARCH_ENDPOINT`: Azure Search service endpoint
- `AZURE_SEARCH_API_KEY`: Azure Search API key
- `AZURE_SEARCH_INDEX_NAME`: Default Azure Search index name

## Examples

### Using Claude Desktop 

#### Example 1: Basic Text Search

```
Search my knowledge base for information about Azure AI Search features.
```

Claude will use MCP to search your Azure index:

```
I'll search for information about Azure AI Search features.

> View result from azure-search-text-search from azure-search (local)

Here are the search results for 'Azure AI Search features' in your knowledge base:
[Results will appear here based on your actual data]
```

#### Example 2: Filtering Results

```
Find documents about vector search that were published after January 2023.
```

Claude will use filter expressions to refine the search:

```
I'll search for documents about vector search with the specified filter.

> View result from azure-search-text-search from azure-search (local)

Here are the filtered search results:
[Filtered results will appear here based on your actual data]
```

## Troubleshooting

### Common Issues

#### Connection Errors

If you see errors like "Failed to connect to Azure Search service":

1. Verify your Azure Search endpoint is correct
2. Ensure your API key has the correct permissions
3. Check if there are any network restrictions or firewalls

#### Authentication Issues

If you see authentication errors:

1. Verify your API key is correct
2. Ensure you're using a valid API key with appropriate permissions

#### Tool Not Found

If the MCP tools don't appear in Claude Desktop or Cursor:

1. Restart the application
2. Check the server logs for any errors
3. Verify the MCP server is running correctly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.