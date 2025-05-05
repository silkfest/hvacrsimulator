"""
VectorSearch - Handles document retrieval from Supabase vector store.
Uses LangChain for embedding and similarity search of refrigeration manuals.
"""

from typing import Dict, List, Optional, Union
import os
from dataclasses import dataclass
from langchain.vectorstores import SupabaseVectorStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import json


@dataclass
class SearchResult:
    """Structured output for vector search results."""
    content: str
    metadata: Dict
    similarity_score: float
    source_reference: str


class VectorSearch:
    """
    Handles document retrieval from Supabase vector store.
    Provides semantic search capabilities for refrigeration manuals.
    """

    def __init__(self):
        """Initialize vector search with Supabase connection."""
        load_dotenv()
        
        # Initialize Supabase connection
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials not found in environment variables")
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings()
        
        # Initialize vector store
        self.vector_store = SupabaseVectorStore(
            embedding=self.embeddings,
            supabase_url=self.supabase_url,
            supabase_key=self.supabase_key,
            table_name="document_embeddings"
        )
        
        # Initialize text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    def search_manuals(self, 
                      query: str,
                      component_type: Optional[str] = None,
                      max_results: int = 5) -> List[SearchResult]:
        """
        Search refrigeration manuals for relevant information.
        
        Args:
            query: Search query (e.g., "high discharge temperature")
            component_type: Optional component type to filter results
            max_results: Maximum number of results to return
        
        Returns:
            List of SearchResult objects with content and metadata
        """
        # Prepare metadata filter if component type is specified
        filter_dict = None
        if component_type:
            filter_dict = {"component_type": component_type}
        
        # Perform similarity search
        results = self.vector_store.similarity_search_with_score(
            query,
            k=max_results,
            filter=filter_dict
        )
        
        # Convert to SearchResult objects
        search_results = []
        for doc, score in results:
            search_results.append(SearchResult(
                content=doc.page_content,
                metadata=doc.metadata,
                similarity_score=score,
                source_reference=doc.metadata.get("source", "Unknown")
            ))
        
        return search_results

    def get_component_manuals(self, 
                            component_name: str,
                            max_results: int = 3) -> List[SearchResult]:
        """
        Get relevant manual sections for a specific component.
        
        Args:
            component_name: Name of the component (e.g., "ZB58KCE-TFD")
            max_results: Maximum number of results to return
        
        Returns:
            List of SearchResult objects with component-specific information
        """
        # Load component specs to get manual references
        with open("component_specs.json", "r") as f:
            specs = json.load(f)
        
        # Find component in specs
        component_ref = None
        for category in specs["components"].values():
            if component_name in category:
                component_ref = category[component_name]["manual_reference"]
                break
        
        if not component_ref:
            raise ValueError(f"Component {component_name} not found in specifications")
        
        # Search for component-specific information
        return self.search_manuals(
            query=f"{component_name} {component_ref}",
            component_type=component_name,
            max_results=max_results
        )

    def get_diagnostic_context(self,
                             diagnosis: str,
                             symptoms: List[str],
                             max_results: int = 5) -> List[SearchResult]:
        """
        Get relevant manual sections for a specific diagnosis.
        
        Args:
            diagnosis: The diagnosis to search for
            symptoms: List of observed symptoms
            max_results: Maximum number of results to return
        
        Returns:
            List of SearchResult objects with diagnostic information
        """
        # Construct search query from diagnosis and symptoms
        query = f"{diagnosis} {' '.join(symptoms)}"
        
        return self.search_manuals(
            query=query,
            max_results=max_results
        ) 