"""
EmbeddingPipeline - Processes PDF manuals into vector embeddings for semantic search.
Uses LangChain and Supabase for document processing and storage.
"""

from typing import Dict, List, Optional, Union
import os
from pathlib import Path
from dataclasses import dataclass
from langchain.document_loaders import PyPDFLoader, UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from dotenv import load_dotenv
import json


@dataclass
class ProcessedDocument:
    """Structured output for processed document chunks."""
    content: str
    metadata: Dict
    source: str
    page_number: int


class EmbeddingPipeline:
    """
    Processes PDF manuals into vector embeddings for semantic search.
    Handles document loading, chunking, and storage in Supabase.
    """

    def __init__(self):
        """Initialize the embedding pipeline with required components."""
        load_dotenv()
        
        # Initialize Supabase connection
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials not found in environment variables")
        
        # Initialize components
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Initialize vector store
        self.vector_store = SupabaseVectorStore(
            embedding=self.embeddings,
            supabase_url=self.supabase_url,
            supabase_key=self.supabase_key,
            table_name="document_embeddings"
        )

    def process_manual(self,
                      pdf_path: str,
                      component_type: Optional[str] = None,
                      manual_reference: Optional[str] = None) -> List[ProcessedDocument]:
        """
        Process a PDF manual into vector embeddings.
        
        Args:
            pdf_path: Path to the PDF file
            component_type: Type of component (e.g., "compressor", "valve")
            manual_reference: Reference to the manual (e.g., "Copeland AE4-1327")
        
        Returns:
            List of ProcessedDocument objects
        """
        # Load PDF
        try:
            loader = UnstructuredPDFLoader(pdf_path)
            documents = loader.load()
        except Exception as e:
            print(f"Error loading PDF with UnstructuredPDFLoader: {str(e)}")
            print("Falling back to PyPDFLoader...")
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
        
        # Split into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Process chunks
        processed_docs = []
        for chunk in chunks:
            # Extract metadata
            metadata = {
                "source": manual_reference or Path(pdf_path).stem,
                "page": chunk.metadata.get("page", 0),
                "component_type": component_type
            }
            
            # Create processed document
            processed_doc = ProcessedDocument(
                content=chunk.page_content,
                metadata=metadata,
                source=metadata["source"],
                page_number=metadata["page"]
            )
            processed_docs.append(processed_doc)
        
        return processed_docs

    def store_embeddings(self, documents: List[ProcessedDocument]):
        """
        Store document embeddings in Supabase.
        
        Args:
            documents: List of ProcessedDocument objects to store
        """
        # Convert to LangChain document format
        docs = []
        for doc in documents:
            docs.append({
                "page_content": doc.content,
                "metadata": doc.metadata
            })
        
        # Add to vector store
        self.vector_store.add_documents(docs)

    def process_directory(self,
                         input_dir: str,
                         component_mapping: Optional[Dict[str, str]] = None):
        """
        Process all PDFs in a directory.
        
        Args:
            input_dir: Directory containing PDF manuals
            component_mapping: Optional mapping of filenames to component types
        """
        # Get all PDF files
        pdf_files = list(Path(input_dir).glob("**/*.pdf"))
        
        for pdf_file in pdf_files:
            print(f"Processing {pdf_file.name}...")
            
            # Get component type from mapping
            component_type = None
            if component_mapping:
                component_type = component_mapping.get(pdf_file.stem)
            
            # Process manual
            processed_docs = self.process_manual(
                str(pdf_file),
                component_type=component_type
            )
            
            # Store embeddings
            self.store_embeddings(processed_docs)
            
            print(f"Processed {len(processed_docs)} chunks from {pdf_file.name}")

    def update_component_specs(self, specs_path: str = "component_specs.json"):
        """
        Update component specifications with processed manual references.
        
        Args:
            specs_path: Path to component_specs.json
        """
        # Load current specs
        with open(specs_path, "r") as f:
            specs = json.load(f)
        
        # Get all documents from vector store
        # TODO: Implement method to get all documents from Supabase
        
        # Update specs with manual references
        # TODO: Implement method to update specs with manual references
        
        # Save updated specs
        with open(specs_path, "w") as f:
            json.dump(specs, f, indent=4) 