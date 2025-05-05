"""
LLMInterface - Unified interface for interacting with different LLM providers.
Supports Gemini (default), OpenAI, and Claude with consistent prompt formatting.
"""

from typing import Dict, List, Optional, Union
import os
from dataclasses import dataclass
import google.generativeai as genai
from dotenv import load_dotenv


@dataclass
class LLMResponse:
    """Structured response from LLM following MCP format."""
    text: str
    confidence: float
    source_references: List[str]


class LLMInterface:
    """
    Unified interface for interacting with different LLM providers.
    Handles prompt formatting, context management, and response parsing.
    """

    def __init__(self, provider: str = "gemini"):
        """
        Initialize the LLM interface with specified provider.
        
        Args:
            provider: LLM provider to use ("gemini", "openai", or "claude")
        """
        load_dotenv()  # Load API keys from .env file
        
        self.provider = provider.lower()
        self._initialize_provider()
        
        # Default prompt template following MCP format
        self.prompt_template = """
        You are a refrigeration system diagnostic assistant. Use the following context
        to help diagnose the issue:

        System State:
        {system_state}

        Relevant Manual Sections:
        {manual_context}

        Please provide:
        1. Diagnosis
        2. Confidence level (0-1.0)
        3. Next steps
        4. Safety warnings
        5. Manual references

        Format your response in a clear, structured way suitable for apprentice technicians.
        """

    def _initialize_provider(self):
        """Initialize the selected LLM provider with API keys."""
        if self.provider == "gemini":
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        elif self.provider == "openai":
            # TODO: Implement OpenAI initialization
            pass
        elif self.provider == "claude":
            # TODO: Implement Claude initialization
            pass
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def ask_llm(self, 
                system_state: Dict[str, Union[float, List[str]]],
                manual_context: List[str]) -> LLMResponse:
        """
        Send a diagnostic query to the LLM with system state and manual context.
        
        Args:
            system_state: Current system sensor values and alarms
            manual_context: Relevant sections from service manuals
        
        Returns:
            LLMResponse with diagnosis, confidence, and references
        """
        # Format the prompt with system state and manual context
        prompt = self.prompt_template.format(
            system_state=self._format_system_state(system_state),
            manual_context="\n".join(manual_context)
        )
        
        # Get response from selected provider
        if self.provider == "gemini":
            response = self._get_gemini_response(prompt)
        elif self.provider == "openai":
            response = self._get_openai_response(prompt)
        elif self.provider == "claude":
            response = self._get_claude_response(prompt)
        
        return response

    def _format_system_state(self, state: Dict) -> str:
        """Format system state into a readable string."""
        formatted = []
        for key, value in state.items():
            if isinstance(value, list):
                formatted.append(f"{key}: {', '.join(value)}")
            else:
                formatted.append(f"{key}: {value}")
        return "\n".join(formatted)

    def _get_gemini_response(self, prompt: str) -> LLMResponse:
        """Get response from Gemini model."""
        try:
            response = self.model.generate_content(prompt)
            # TODO: Parse response into structured format
            return LLMResponse(
                text=response.text,
                confidence=0.85,  # Placeholder
                source_references=["Copeland AE4-1327"]  # Placeholder
            )
        except Exception as e:
            raise RuntimeError(f"Error getting response from Gemini: {str(e)}")

    def _get_openai_response(self, prompt: str) -> LLMResponse:
        """Get response from OpenAI model."""
        # TODO: Implement OpenAI response handling
        raise NotImplementedError("OpenAI integration not yet implemented")

    def _get_claude_response(self, prompt: str) -> LLMResponse:
        """Get response from Claude model."""
        # TODO: Implement Claude response handling
        raise NotImplementedError("Claude integration not yet implemented") 