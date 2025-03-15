# Azure AI Search MCP Server

A Model Context Protocol (MCP) server that integrates with Azure AI Search, enabling Claude Desktop to query your search indexes using keyword, vector, or hybrid methods.

![demo](images/demo.gif)

---

## Overview

This project provides an MCP server implementation that connects Claude Desktop with Azure AI Search. The server supports three search methods:

- **Keyword Search:** Exact lexical matches.
- **Vector Search:** Semantic similarity using vector embeddings.
- **Hybrid Search:** A combination of keyword and vector searches.

---

## Features

- **Seamless Integration:** Connect Claude Desktop with Azure AI Search.
- **Multiple Search Methods:** Supports keyword, vector, and hybrid searches.
- **Customizable:** Easy to extend with additional tools or modify search logic.

---

## Requirements

- **Python:** Version 3.10 or higher
- **Azure AI Search Service:** Configured with an index containing vectorized text data
- **Claude Desktop:** Latest version
- **Operating System:** Windows or macOS (instructions provided for Windows, but adaptable)

---

## Quick Start Guide

### 1. Installation

1. **Set Up Project Directory:**

   ```bash
   mkdir mcp-server-azure-ai-search
   cd mcp-server-azure-ai-search
   ```

2. **Create a `.env` File:**

   ```bash
   echo "AZURE_SEARCH_SERVICE_ENDPOINT=https://your-service-name.search.windows.net" > .env
   echo "AZURE_SEARCH_INDEX_NAME=your-index-name" >> .env
   echo "AZURE_SEARCH_API_KEY=your-api-key" >> .env
   ```

### 2. Set Up Virtual Environment

1. **Create and Activate the Virtual Environment:**

   ```bash
   uv venv
   .venv\Scripts\activate
   ```

2. **Install Dependencies:**

   ```bash
   uv pip install "mcp[cli]" azure-search-documents==11.5.2 azure-identity python-dotenv
   ```

### 3. Server Script

Create a file named `azure_search_server.py`. This script:

- Loads configuration from the `.env` file.
- Initializes the Azure AI Search client.
- Defines search functions for keyword, vector, and hybrid searches.
- Registers these functions as MCP tools for Claude Desktop.

For detailed implementation, refer to the inline comments within the script.

---

## Configuring Claude Desktop

1. **Open Claude Desktop.**
2. **Navigate to Settings > Developer > Edit Config.**
3. **Add the following configuration (update paths and credentials):**

   ```json
   {
     "mcpServers": {
       "azure-search": {
         "command": "C:path\tomcp-server-azure-ai-search.venvScriptspython.exe",
         "args": ["C:path\tomcp-server-azure-ai-searchazure_search_server.py"],
         "env": {
           "AZURE_SEARCH_SERVICE_ENDPOINT": "https://your-service-name.search.windows.net",
           "AZURE_SEARCH_INDEX_NAME": "your-index-name",
           "AZURE_SEARCH_API_KEY": "your-api-key"
         }
       }
     }
   }
   ```

> **Note:** Replace `C:\path\to\mcp-server-azure-ai-search` with your actual project path.

---

## Testing the Server

1. **Restart Claude Desktop** to load the new configuration.
2. Look for the MCP tools icon (hammer icon) in the bottom-right of the input field.
3. Try queries such as:
   - "Can you search for information about AI in my Azure Search index?"
   - "Search for vector databases using the vector search tool."
   - "Find information about neural networks using hybrid search."

---

## Troubleshooting

- **Server Not Appearing:**
  - Check Claude Desktop logs (typically found at `%APPDATA%\Claude\logs\mcp*.log` on Windows).
  - Verify file paths and environment variables in the configuration.
  - Test running the server directly via `python azure_search_server.py`. or `uv run python azure_search_server.py `

---

## Customizing Your Server

- **Modify Search Logic:** Adjust the search methods in the `AzureSearchClient` class.
- **Add New Tools:** Use the `@mcp.tool()` decorator to integrate additional search functionalities.
- **Customize Output:** Edit the markdown formatting function for search results.

---

## License

This project is licensed under the MIT License.
