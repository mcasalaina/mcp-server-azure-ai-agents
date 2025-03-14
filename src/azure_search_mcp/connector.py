from typing import Optional, List, Dict, Any, Union
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import json

class AzureSearchConnector:
    def __init__(
        self,
        endpoint: str,
        api_key: str,
        index_name: str,
    ):
        self.endpoint = endpoint
        self.credential = AzureKeyCredential(api_key)
        self.index_name = index_name
        self.client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=self.credential
        )

    async def list_indexes(self) -> List[str]:
        """
        List all indexes in the search service.
        
        This is a simplified implementation as the SearchClient doesn't have a direct
        method to list indexes. In a full implementation, you'd use the SearchServiceClient.
        """
        # Note: In a complete implementation, you would use SearchServiceClient
        # For now, we'll return the current index
        return [self.index_name]

    async def get_index_info(self, index_name: str) -> dict:
        """Get detailed information about an index."""
        # Note: In a complete implementation, you would use SearchServiceClient to get index info
        # For now, return a simplified representation
        fields = await self._get_index_fields()
        return {
            "name": index_name,
            "fields": fields,
        }

    async def _get_index_fields(self) -> List[str]:
        """Helper method to get field names from the index."""
        # In a complete implementation, you would use SearchServiceClient
        # For now, return some common fields
        return ["id", "content", "title", "category", "url"]

    async def text_search(
        self,
        query_text: str,
        limit: int = 5,
        output_fields: Optional[List[str]] = None,
        filter_expr: Optional[str] = None,
        semantic_configuration: Optional[str] = None
    ) -> List[dict]:
        """
        Perform full text search on the index.
        
        Args:
            query_text: Text to search for
            limit: Maximum number of results (default: 5)
            output_fields: Fields to return in results (default: all)
            filter_expr: Optional filter expression
            semantic_configuration: Optional semantic configuration to use
        """
        try:
            search_options = {
                "top": limit,
                "select": ",".join(output_fields) if output_fields else None,
                "filter": filter_expr
            }
            
            # Enable semantic search if configuration is provided
            if semantic_configuration:
                search_options["semantic_configuration_name"] = semantic_configuration
                search_options["query_type"] = "semantic"
            
            results = self.client.search(
                search_text=query_text,
                **{k: v for k, v in search_options.items() if v is not None}
            )
            
            return [dict(result) for result in results]
        except Exception as e:
            raise ValueError(f"Search failed: {str(e)}")

    async def vector_search(
        self,
        vector: List[float],
        vector_field: str,
        limit: int = 5,
        output_fields: Optional[List[str]] = None,
        filter_expr: Optional[str] = None,
        semantic_configuration: Optional[str] = None
    ) -> List[dict]:
        """
        Perform vector similarity search on the index.
        
        Args:
            vector: Query vector
            vector_field: Field containing vectors to search
            limit: Maximum number of results (default: 5)
            output_fields: Fields to return in results
            filter_expr: Optional filter expression
            semantic_configuration: Optional semantic configuration to use
        """
        try:
            # Build the search options
            search_options = {
                "top": limit,
                "select": ",".join(output_fields) if output_fields else None,
                "filter": filter_expr,
                "vector_queries": [
                    {
                        "vector": vector,
                        "fields": vector_field,
                        "k": limit
                    }
                ]
            }
            
            # Enable semantic search if configuration is provided
            if semantic_configuration:
                search_options["semantic_configuration_name"] = semantic_configuration
                search_options["query_type"] = "semantic"
            
            # Note: Using vector search requires using the newer search_get_vector method
            results = self.client.search(
                search_text=None,  # For pure vector search, no text query
                **{k: v for k, v in search_options.items() if v is not None}
            )
            
            return [dict(result) for result in results]
        except Exception as e:
            raise ValueError(f"Vector search failed: {str(e)}")

    async def hybrid_search(
        self,
        query_text: str,
        vector: List[float],
        vector_field: str,
        limit: int = 5,
        output_fields: Optional[List[str]] = None,
        filter_expr: Optional[str] = None,
        semantic_configuration: Optional[str] = None
    ) -> List[dict]:
        """
        Perform hybrid search combining text and vector similarity.
        
        Args:
            query_text: Text query
            vector: Query vector
            vector_field: Field containing vectors to search
            limit: Maximum number of results (default: 5)
            output_fields: Fields to return in results
            filter_expr: Optional filter expression
            semantic_configuration: Optional semantic configuration to use
        """
        try:
            # Build the search options
            search_options = {
                "top": limit,
                "select": ",".join(output_fields) if output_fields else None,
                "filter": filter_expr,
                "vector_queries": [
                    {
                        "vector": vector,
                        "fields": vector_field,
                        "k": limit
                    }
                ]
            }
            
            # Enable semantic search if configuration is provided
            if semantic_configuration:
                search_options["semantic_configuration_name"] = semantic_configuration
                search_options["query_type"] = "semantic"
            
            results = self.client.search(
                search_text=query_text,
                **{k: v for k, v in search_options.items() if v is not None}
            )
            
            return [dict(result) for result in results]
        except Exception as e:
            raise ValueError(f"Hybrid search failed: {str(e)}")

    async def query(
        self,
        filter_expr: str,
        output_fields: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[dict]:
        """
        Query collection using filter expressions.
        
        Args:
            filter_expr: Filter expression (e.g. 'category eq 'documentation'')
            output_fields: Fields to return in results
            limit: Maximum number of results (default: 10)
        """
        try:
            search_options = {
                "top": limit,
                "select": ",".join(output_fields) if output_fields else None,
                "filter": filter_expr
            }
            
            # Setting search_text to * returns all documents that match the filter
            results = self.client.search(
                search_text="*",
                **{k: v for k, v in search_options.items() if v is not None}
            )
            
            return [dict(result) for result in results]
        except Exception as e:
            raise ValueError(f"Query failed: {str(e)}")