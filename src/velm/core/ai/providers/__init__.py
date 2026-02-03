# Path: scaffold/core/ai/providers/__init__.py
# --------------------------------------------
from typing import Dict, Type
from .base import BaseProvider
from .openai import OpenAIProvider
from .anthropic import AnthropicProvider
from .google import GoogleProvider
from .local import LocalAIProvider

# The Pantheon
PROVIDER_REGISTRY: Dict[str, BaseProvider] = {
    "openai": OpenAIProvider(),
    "anthropic": AnthropicProvider(),
    "google": GoogleProvider(),
    "local": LocalAIProvider(),
    "ollama": LocalAIProvider(),
    "lm_studio": LocalAIProvider(),
}

def get_provider(key: str) -> BaseProvider:
    return PROVIDER_REGISTRY.get(key.lower())