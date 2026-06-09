"""YT Auto AI Client."""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import logging

from config.settings import AIProvider, get_settings
from utils.logger import get_logger


logger = get_logger(__name__)


class AIClientBase(ABC):
    """Abstract base class for AI clients."""
    
    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate text from a prompt.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate structured output.
        
        Args:
            prompt: User prompt
            schema: Output schema
            system_prompt: Optional system prompt
            
        Returns:
            Structured output as dictionary
        """
        pass


class MockAIClient(AIClientBase):
    """Mock AI client for testing and development."""
    
    def __init__(self):
        self.name = "mock"
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate mock text response."""
        logger.info(f"[MOCK] Generating text for prompt: {prompt[:50]}...")
        
        # TODO: Replace with actual AI integration
        return f"[MOCK RESPONSE] This is a simulated response for: {prompt[:100]}"
    
    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate mock structured response."""
        logger.info(f"[MOCK] Generating structured output for: {prompt[:50]}...")
        
        # TODO: Replace with actual AI integration
        return {"mock": True, "prompt": prompt[:100]}


class OpenAIClient(AIClientBase):
    """OpenAI API client."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.name = "openai"
        self._client = None
        
        if not api_key:
            logger.warning("OpenAI API key not provided, falling back to mock")
    
    def _get_client(self):
        """Lazy load OpenAI client."""
        if self._client is None and self.api_key:
            try:
                from openai import AsyncOpenAI
                self._client = AsyncOpenAI(api_key=self.api_key)
            except ImportError:
                logger.warning("OpenAI library not installed, using mock")
                return MockAIClient()
        return self._client
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate text using OpenAI."""
        client = self._get_client()
        
        if client is None:
            mock_client = MockAIClient()
            return await mock_client.generate_text(prompt, system_prompt, max_tokens, temperature)
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            mock_client = MockAIClient()
            return await mock_client.generate_text(prompt, system_prompt, max_tokens, temperature)
    
    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate structured output using OpenAI."""
        # TODO: Implement structured output with OpenAI function calling
        text = await self.generate_text(
            f"{prompt}\n\nReturn valid JSON matching this schema: {schema}",
            system_prompt,
        )
        import json
        try:
            return json.loads(text)
        except:
            return {"error": "Failed to parse JSON", "raw": text}


class AnthropicClient(AIClientBase):
    """Anthropic Claude API client."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.name = "anthropic"
        self._client = None
        
        if not api_key:
            logger.warning("Anthropic API key not provided, falling back to mock")
    
    def _get_client(self):
        """Lazy load Anthropic client."""
        if self._client is None and self.api_key:
            try:
                from anthropic import AsyncAnthropic
                self._client = AsyncAnthropic(api_key=self.api_key)
            except ImportError:
                logger.warning("Anthropic library not installed, using mock")
                return MockAIClient()
        return self._client
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate text using Anthropic."""
        client = self._get_client()
        
        if client is None:
            mock_client = MockAIClient()
            return await mock_client.generate_text(prompt, system_prompt, max_tokens, temperature)
        
        try:
            response = await client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=max_tokens,
                system=system_prompt or "You are a helpful assistant.",
                messages=[{"role": "user", "content": prompt}],
            )
            
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            mock_client = MockAIClient()
            return await mock_client.generate_text(prompt, system_prompt, max_tokens, temperature)
    
    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate structured output using Anthropic."""
        text = await self.generate_text(
            f"{prompt}\n\nReturn valid JSON matching this schema: {schema}",
            system_prompt,
        )
        import json
        try:
            return json.loads(text)
        except:
            return {"error": "Failed to parse JSON", "raw": text}


class GoogleClient(AIClientBase):
    """Google Generative AI client."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.name = "google"
        self._client = None
        
        if not api_key:
            logger.warning("Google API key not provided, falling back to mock")
    
    def _get_client(self):
        """Lazy load Google client."""
        if self._client is None and self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai.GenerativeModel("gemini-pro")
            except ImportError:
                logger.warning("Google AI library not installed, using mock")
                return MockAIClient()
        return self._client
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate text using Google."""
        client = self._get_client()
        
        if client is None:
            mock_client = MockAIClient()
            return await mock_client.generate_text(prompt, system_prompt, max_tokens, temperature)
        
        try:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = client.generate_content(full_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Google API error: {e}")
            mock_client = MockAIClient()
            return await mock_client.generate_text(prompt, system_prompt, max_tokens, temperature)
    
    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate structured output using Google."""
        text = await self.generate_text(
            f"{prompt}\n\nReturn valid JSON matching this schema: {schema}",
            system_prompt,
        )
        import json
        try:
            return json.loads(text)
        except:
            return {"error": "Failed to parse JSON", "raw": text}


class AIClient:
    """Unified AI client that delegates to provider-specific clients."""
    
    def __init__(self, provider: AIProvider = AIProvider.MOCK):
        self.provider = provider
        self._client = self._create_client(provider)
    
    def _create_client(self, provider: AIProvider) -> AIClientBase:
        """Create appropriate client based on provider."""
        settings = get_settings()
        
        if provider == AIProvider.OPENAI:
            return OpenAIClient(settings.openai_api_key)
        elif provider == AIProvider.ANTHROPIC:
            return AnthropicClient(settings.anthropic_api_key)
        elif provider == AIProvider.GOOGLE:
            return GoogleClient(settings.google_api_key)
        else:
            return MockAIClient()
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate text from prompt."""
        return await self._client.generate_text(
            prompt, system_prompt, max_tokens, temperature
        )
    
    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate structured output."""
        return await self._client.generate_structured(prompt, schema, system_prompt)


# Global client instance
_ai_client: Optional[AIClient] = None


def get_ai_client(provider: Optional[AIProvider] = None) -> AIClient:
    """Get or create global AI client instance.
    
    Args:
        provider: Optional provider override
        
    Returns:
        AI client instance
    """
    global _ai_client
    if _ai_client is None:
        settings = get_settings()
        _ai_client = AIClient(provider or settings.ai_provider)
    return _ai_client
