"""
High-level AI service used by bot commands.

This is the layer that bot command handlers talk to. It knows nothing about
Discord and nothing about vector stores directly, it just turns
(question, optional context) into text answers using an AIClient and the
prompt templates. This separation makes each piece independently testable.
"""
from __future__ import annotations

from typing import List, Optional

from app.ai.client import AIClient
from app.ai import prompts
from app.config import ConfigError


class AIService:
    def __init__(self, client: AIClient):
        self._client = client

    @property
    def is_ready(self) -> bool:
        return self._client.is_configured

    def answer_general(self, question: str) -> str:
        if not self._client.is_configured:
            raise ConfigError(
                "AI is not configured yet. Ask the bot owner to set HF_API_KEY."
            )
        return self._client.chat(prompts.build_general_prompt(question))

    