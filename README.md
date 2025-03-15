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

# Azure AI Agent Service MCP Server

A Model Context Protocol (MCP) server that integrates with Azure AI Agent Service, enabling Claude Desktop to query your Azure AI Search indexes and the web using Bing Web Grounding.

---

## Overview

This project provides an MCP server implementation that connects Claude Desktop with Azure AI Agent Service, offering two powerful search tools:

- **Azure AI Search Tool:** Search through your indexed documents using the best retrieval method automatically.
- **Bing Web Grounding Tool:** Search the web for current information with source citations.

This implementation leverages Azure AI Agent Service to provide intelligent search capabilities across both your private data and the public web.

---

## Features

- **AI-Enhanced Search:** Utilizes Azure AI Agent Service for intelligent search capabilities.
- **Dual Search Sources:** Search both your private Azure AI Search index and the public web.
- **Best Retrieval Method:** Automatically uses the optimal search method for your Azure AI Search index.
- **Web Grounding:** Get up-to-date information from the web with source citations.
- **Seamless Integration:** Connect Claude Desktop with Azure AI tools and services.

---

## Requirements

- **Python:** Version 3.10 or higher
- **Azure AI Project:** Set up with both Azure AI Search and Bing connections
- **Azure AI Search Service:** Configured with an index containing vectorized text data
- **Bing Search API:** Connected to your Azure AI Project
- **Claude Desktop:** Latest version
- **Operating System:** Windows or macOS (instructions provided for Windows, but adaptable)

---

## Quick Start Guide

### 1. Installation

1. **Set Up Project Directory:**

   ```bash
   mkdir mcp-server-azure-ai-agent
   cd mcp-server-azure-ai-agent
   ```

2. **Create a `.env` File:**

   ```bash
   echo "PROJECT_CONNECTION_STRING=your-project-connection-string" > .env
   echo "MODEL_DEPLOYMENT_NAME=your-model-deployment-name" >> .env
   echo "AI_SEARCH_CONNECTION_NAME=your-search-connection-name" >> .env
   echo "BING_CONNECTION_NAME=your-bing-connection-name" >> .env
   echo "AI_SEARCH_INDEX_NAME=your-index-name" >> .env
   ```

### 2. Set Up Virtual Environment

1. **Create and Activate the Virtual Environment:**

   ```bash
   uv venv
   .venv\Scripts\activate
   ```

2. **Install Dependencies:**

   ```bash
   uv pip install "mcp[cli]" azure-identity python-dotenv azure-ai-projects
   ```

### 3. Server Script

Use the `azure_ai_agent_service.py` script for integration with Azure AI Agent Service. This implementation provides two powerful tools:

1. **Azure AI Search Tool:** For searching your private indexed documents
2. **Bing Web Grounding Tool:** For searching the web for current information

The script connects to your Azure AI Project and utilizes both tools through the Azure AI Agent Service. For detailed implementation, refer to the inline comments within the script.

---

## Configuring Claude Desktop

1. **Open Claude Desktop.**
2. **Navigate to Settings > Developer > Edit Config.**
3. **Add the following configuration (update paths and credentials):**

   ```json
   {
     "mcpServers": {
       "azure-ai-agent": {
         "command": "C:\\path\\to\\mcp-server-azure-ai-agent\\.venv\\Scripts\\python.exe",
         "args": ["C:\\path\\to\\mcp-server-azure-ai-agent\\azure_ai_agent_service.py"],
         "env": {
           "PROJECT_CONNECTION_STRING": "your-project-connection-string",
           "MODEL_DEPLOYMENT_NAME": "your-model-deployment-name",
           "AI_SEARCH_CONNECTION_NAME": "your-search-connection-name",
           "BING_CONNECTION_NAME": "your-bing-connection-name",
           "AI_SEARCH_INDEX_NAME": "your-index-name"
         }
       }
     }
   }
   ```

> **Note:** Replace `C:\path\to\mcp-server-azure-ai-agent` with your actual project path.

---

## Azure AI Agent Service Setup

Before using the Azure AI Agent Service implementation, you need to:

1. **Create an Azure AI Project:**
   - Go to the Azure Portal and create a new Azure AI Project.
   - Note your project's connection string for the `PROJECT_CONNECTION_STRING` environment variable.
   - Note your model deployment name for the `MODEL_DEPLOYMENT_NAME` environment variable.

2. **Create an Azure AI Search Connection:**
   - In your Azure AI Project, add a connection to your Azure AI Search service.
   - Note the connection name for the `AI_SEARCH_CONNECTION_NAME` environment variable.
   - Note the index name for the `AI_SEARCH_INDEX_NAME` environment variable.

3. **Create a Bing Web Search Connection:**
   - In your Azure AI Project, add a connection to Bing Search service.
   - Note the connection name for the `BING_CONNECTION_NAME` environment variable.

4. **Configure Azure Credentials:**
   - The implementation uses `DefaultAzureCredential`, so ensure you're authenticated:
   ```bash
   az login
   ```

---

## Testing the Server

1. **Restart Claude Desktop** to load the new configuration.
2. Look for the MCP tools icon (hammer icon) in the bottom-right of the input field.
3. Try queries such as:
   - "Can you search for information about AI in my Azure Search index?"
   - "Search the web for the latest developments in LLMs."
   - "Find information about neural networks in my index and then get recent updates from the web."

---

## Troubleshooting

- **Server Not Appearing:**
  - Check Claude Desktop logs (typically found at `%APPDATA%\Claude\logs\mcp*.log` on Windows).
  - Verify file paths and environment variables in the configuration.
  - Test running the server directly via `python azure_ai_agent_service.py` or `uv run python azure_ai_agent_service.py`.

- **Azure AI Agent Service Issues:**
  - Ensure your Azure AI Project is correctly set up.
  - Verify that the Azure AI Search connection exists and is properly configured.
  - Check that you're logged in with Azure CLI (`az login`).

---

## Implementation Benefits

### Azure AI Agent Service with Dual Search Tools

- **Comprehensive Search Capability:**
  - Search both private data (Azure AI Search) and public web (Bing).
  - Get the most relevant and up-to-date information from multiple sources.

- **Intelligent Processing:**
  - AI-enhanced search results with better context understanding.
  - Automatic selection of the best retrieval method for your index.
  - Natural language understanding for better query interpretation.

- **Source Citations:**
  - Web search results include citations to the original sources.
  - Improved trustworthiness and ability to verify information.

- **Single Interface:**
  - Both tools are accessible through the same Claude Desktop interface.
  - Unified experience for searching across different data sources.

---

## Customizing Your Server

- **Modify Tool Instructions:** Adjust the instructions provided to each agent to change how they process queries.
- **Add New Tools:** Use the `@mcp.tool()` decorator to integrate additional Azure AI Agent tools.
- **Customize Response Formatting:** Edit how responses are formatted and returned to Claude Desktop.
- **Adjust Web Search Parameters:** Modify the web search tool to focus on specific domains or types of content.

---

## License

This project is licensed under the MIT License.