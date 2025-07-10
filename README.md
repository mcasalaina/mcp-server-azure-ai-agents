# Azure AI Agent Service + Bing Web Search MCP Server

A Model Context Protocol (MCP) server that enables MCP Consumers to search web content using Azure AI services.

![demo](images/demo.gif)

---

## Overview

This project provides an MCP server implementation to connect MCP consumers with Azure search capabilities:

1. **Azure AI Agent Service Implementation (Recommended)** - Uses the powerful Azure AI Agent Service to provide:
   - **Bing Web Grounding Tool** - Search the web with source citations

---

## Features

- **AI-Enhanced Bing Search** - Azure AI Agent Service optimizes search results with intelligent processing
- **Source Citations** - Web search results include citations to original sources
- **Customizable** - Easy to extend or modify search behavior

---

## Quick Links

- [Azure AI Agent Service Quickstart](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/agent-quickstart)

---

## Requirements

- **Python:** Version 3.13 or higher
- **Azure Resources:** 
  - Azure AI Project with Bing connection
- **Operating System:** Windows or macOS (instructions provided for Windows, but adaptable)

---

## Azure AI Agent Service Implementation (Recommended)

### Setup Guide

1. **Project Directory:**

   ```bash
   mkdir mcp-server-azure-ai-search
   cd mcp-server-azure-ai-search
   ```

2. **Create a `.env` File:**

   ```bash
   echo "PROJECT_ENDPOINT=your-project-endpoint" > .env
   echo "MODEL_DEPLOYMENT_NAME=your-model-deployment-name" >> .env
   echo "BING_CONNECTION_NAME=your-bing-connection-name" >> .env
   ```

   Note that the Bing Connection name is actually the _id_ of the Bing Connection, not its name. So it should look like /subscriptions/<your subscription ID>/resourceGroups/<your resource group name>/providers/Microsoft.CognitiveServices/accounts/<your Foundry project resource name>/projects/<your Foundry project name>/connections/<your Bing connection name>.

3. **Set Up Virtual Environment:**

   ```bash
   uv venv
   .venv\Scripts\activate
   uv pip install "mcp[cli]" azure-identity python-dotenv azure-ai-projects
   ```

4. **Use the `azure_agent_with_bing.py` script** for integration with Azure AI Agent Service and Bing Web Grounding.

### Azure AI Agent Service Setup

Before using the implementation, you need to:

1. **Create an Azure AI Project:**
   - Go to the Azure Portal and create a new Azure AI Project
   - Note the project endpoint (not connection string)

2. **Deploy a Model:**
   - In your Azure AI Project, deploy a model (e.g., GPT-4o)
   - Note the deployment name

3. **Create a Bing Web Search Connection:**
   - In your Azure AI Project, add a connection to Bing Search service
   - Note the connection name

4. **Authenticate with Azure:**
   ```bash
   az login
   ```

### Configuring MCP Consumer

This works for MCP consumers such as Claude Desktop and VS Code.

```json
{
  "mcpServers": {
    "azure-ai-agent": {
      "command": "C:\\path\\to\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\azure_agent_with_bing.py"],
      "env": {
        "PROJECT_ENDPOINT": "https://your-project-name.cognitiveservices.azure.com/",
        "MODEL_DEPLOYMENT_NAME": "your-model-deployment-name",
        "BING_CONNECTION_NAME": "your-bing-connection-name"
      }
    }
  }
}
```

> **Note:** Replace path placeholders with your actual project paths.

---

---

## Troubleshooting

- **Server Not Appearing:**
  - Check Claude Desktop logs (located at `%APPDATA%\Claude\logs\mcp*.log` on Windows)
  - Verify file paths and environment variables in the configuration
  - Test running the server directly: `python azure_ai_agent_service_server.py` or `uv run python azure_ai_agent_service_server.py`

- **Azure AI Agent Service Issues:**
  - Ensure your Azure AI Project is correctly configured
  - Verify that connections exist and are properly configured
  - Check your Azure authentication status

---

## Customizing Your Server

- **Modify Tool Instructions:** Adjust the instructions provided to each agent to change how they process queries
- **Add New Tools:** Use the `@mcp.tool()` decorator to integrate additional tools
- **Customize Response Formatting:** Edit how responses are formatted and returned to Claude Desktop
- **Adjust Web Search Parameters:** Modify the web search tool to focus on specific domains

---

## License

This project is licensed under the MIT License.