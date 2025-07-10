"""Azure AI Agent Service MCP Server using Bing Web Grounding Tools."""

import os
import sys
import asyncio
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Import Azure AI Agent Service modules
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import BingGroundingTool, MessageRole
from azure.identity import DefaultAzureCredential

# Add startup message
print("Starting Azure AI Agent Service MCP Server...", file=sys.stderr)

# Load environment variables
load_dotenv()
print("Environment variables loaded", file=sys.stderr)

# Create MCP server
mcp = FastMCP(
    "azure-ai-agent", 
    description="MCP server for Azure AI Agent Service integration with Bing Web Grounding tools",
    dependencies=[
        "azure-identity",
        "python-dotenv",
        "azure-ai-projects",
        "azure-ai-agents"
    ]
)
print("MCP server instance created", file=sys.stderr)

class AzureAIAgentClient:
    """Client for Azure AI Agent Service with Bing Web Grounding tools."""
    
    def __init__(self):
        """Initialize Azure AI Agent Service client with credentials from environment variables."""
        print("Initializing Azure AI Agent client...", file=sys.stderr)
        
        # Load environment variables
        self.project_endpoint = os.getenv("PROJECT_ENDPOINT")
        self.model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME")
        self.bing_connection_name = os.getenv("BING_CONNECTION_NAME")
        self.agent_id = os.getenv("AGENT_ID")
        
        # If environment variables are not found, try loading from .env file
        if not all([self.project_endpoint, self.model_deployment_name, self.bing_connection_name, self.agent_id]):
            print("Some environment variables missing, attempting to load from .env file...", file=sys.stderr)
            load_dotenv(override=True)  # Reload .env file with override
            
            # Try loading again after .env reload
            if not self.project_endpoint:
                self.project_endpoint = os.getenv("PROJECT_ENDPOINT")
            if not self.model_deployment_name:
                self.model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME")
            if not self.bing_connection_name:
                self.bing_connection_name = os.getenv("BING_CONNECTION_NAME")
            if not self.agent_id:
                self.agent_id = os.getenv("AGENT_ID")
        
        # Validate environment variables
        required_vars = {
            "PROJECT_ENDPOINT": self.project_endpoint,
            "MODEL_DEPLOYMENT_NAME": self.model_deployment_name,
            "BING_CONNECTION_NAME": self.bing_connection_name,
            "AGENT_ID": self.agent_id
        }
        
        missing = [k for k, v in required_vars.items() if not v]
        if missing:
            error_msg = f"Missing environment variables: {', '.join(missing)}"
            print(f"Error: {error_msg}", file=sys.stderr)
            raise ValueError(error_msg)
        
        # Ensure we have valid strings (not None)
        assert self.project_endpoint is not None
        assert self.model_deployment_name is not None
        assert self.bing_connection_name is not None
        assert self.agent_id is not None
        
        # Initialize AIProjectClient
        try:
            self.client = AIProjectClient(
                endpoint=self.project_endpoint,
                credential=DefaultAzureCredential()
            )
            print("AIProjectClient initialized successfully", file=sys.stderr)
        except Exception as e:
            print(f"Error initializing AIProjectClient: {str(e)}", file=sys.stderr)
            raise
        
        print(f"Azure AI Agent client initialized for Bing connection: {self.bing_connection_name}", file=sys.stderr)
    
    def web_search(self, query):
        """
        Perform a web search using Bing Web Grounding Tool.
        
        Args:
            query: The search query text
            
        Returns:
            Formatted search results from the web
        """
        print(f"Performing Bing Web search with {self.bing_connection_name} for: {query}", file=sys.stderr)
        
        try:
            bingconnection = self.bing_connection_name or "None"
            model = self.model_deployment_name or "None"
            # Initialize Bing Web Grounding Tool
            bing_tool = BingGroundingTool(bingconnection)
            
            agent = self.client.agents.create_agent(
                 model=model,
                 name="web-search-agent",
                 instructions=f"You are a helpful web search assistant. Use the Bing Web Grounding Tool to find the most current and accurate information. Provide a comprehensive answer with citations to sources. Format your response as Markdown.",
                 tools=bing_tool.definitions,
             )
            
            # Use existing agent from environment variable
            agent_id = self.agent_id
            if not agent_id:
                raise ValueError("AGENT_ID environment variable is required")
            
            # Get the existing agent
            #agent = self.client.agents.get_agent(agent_id)
            
            # Create thread for communication
            thread = self.client.agents.threads.create()
            
            # Create message to thread
            message = self.client.agents.messages.create(
                thread_id=thread.id,
                role=MessageRole.USER,
                content=query
            )
            
            # Process the run
            run = self.client.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent.id
            )
            
            if run.status == "failed":
                print(f"Run failed: {run.last_error}", file=sys.stderr)
                return f"Web search failed: {run.last_error}"
            
            # Get the agent's response
            response_message = self.client.agents.messages.get_last_message_by_role(
                thread_id=thread.id, 
                role=MessageRole.AGENT
            )
            
            result = ""
            if response_message:
                for text_message in response_message.text_messages:
                    result += text_message.text.value + "\n"
                
                # Include any citations
                for annotation in response_message.url_citation_annotations:
                    result += f"\nCitation: [{annotation.url_citation.title}]({annotation.url_citation.url})\n"
            
            self.client.agents.delete_agent(agent.id)
            
            return result
        
        except Exception as e:
            print(f"Error during web search: {str(e)}", file=sys.stderr)
            raise

# Initialize Azure AI Agent client
try:
    print("Starting initialization of agent client...", file=sys.stderr)
    agent_client = AzureAIAgentClient()
    print("Agent client initialized successfully", file=sys.stderr)
except Exception as e:
    print(f"Error initializing agent client: {str(e)}", file=sys.stderr)
    # Don't exit - we'll handle errors in the tool functions
    agent_client = None

@mcp.tool()
def web_search(query: str) -> str:
    """
    Search the web using Bing Web Grounding to find the most current information.
    
    Args:
        query: The search query text
    
    Returns:
        Formatted search results from the web with citations
    """
    print(f"Tool called: web_search({query})", file=sys.stderr)
    if agent_client is None:
        return "Error: Azure AI Agent client is not initialized. Check server logs for details."
    
    try:
        results = agent_client.web_search(query)
        return f"## Bing Web Search Results\n\n{results}"
    except Exception as e:
        error_msg = f"Error performing web search: {str(e)}"
        print(error_msg, file=sys.stderr)
        return error_msg

if __name__ == "__main__":
    # Run the server with stdio transport (default)
    print("Starting MCP server run...", file=sys.stderr)
    mcp.run()
