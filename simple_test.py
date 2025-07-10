"""Simple test of web search functionality."""

from dotenv import load_dotenv
import os
import sys
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import BingGroundingTool, MessageRole
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables
load_dotenv()

print("🔍 Testing Azure AI Agent Web Search", file=sys.stderr)
print(f"Query: 'which county in TX was affected by the floods'", file=sys.stderr)

# credential = DefaultAzureCredential()
# project_client = AIProjectClient(
#     credential=DefaultAzureCredential(),
#     endpoint="https://aipmaker-project-resource.services.ai.azure.com/api/projects/aipmaker-project"  # Ensure this is set in your environment variables
# )
# connections = project_client.connections.list()
# for conn in connections:
#     print(f"Connection ID: {conn.id}")
#     print(f"  • Type:       {conn.type}")
#     print("---")

try:
    from azure_agent_with_bing import AzureAIAgentClient
    
    print("Initializing client...", file=sys.stderr)
    client = AzureAIAgentClient()
    
    print("Performing web search...", file=sys.stderr)
    query = "which county in TX was affected by the floods"
    results = client.web_search(query)
    
    print("\n" + "="*60)
    print("SEARCH RESULTS:")
    print("="*60)
    print(results)
    print("="*60)
    
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    import traceback
    traceback.print_exc()
