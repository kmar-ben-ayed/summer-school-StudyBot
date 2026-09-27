"""
Prompt templates used across the bot.

"""
from __future__ import annotations

from typing import List

SYSTEM_GENERAL = (
    "You are StudyBot, a friendly and concise AI study assistant for "
    "university students. Answer clearly and keep responses focused. "
    "If you are unsure, say so instead of making things up."
)


def build_general_prompt(question: str) -> List[dict]:
    return [
        {"role": "system", "content": SYSTEM_GENERAL},
        {"role": "user", "content": question},
    ]


