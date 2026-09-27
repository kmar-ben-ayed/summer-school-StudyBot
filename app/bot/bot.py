"""
StudyBot: the Discord bot entry point.

This file wires together the AI service and exposes it on `bot.state` so command Cogs can use them
without global variables.
"""
from __future__ import annotations

import logging

import discord
from discord.ext import commands

from app.ai.client import AIClient
from app.ai.service import AIService
from app.config import Settings, VECTOR_STORE_DIR

logger = logging.getLogger(__name__)


class BotState:
    """Holds the shared services every command needs, built once at startup."""

    def __init__(self, settings: Settings):
        self.settings = settings

        ai_client = AIClient(settings)
        self.ai_service = AIService(ai_client)

        

class StudyBot(commands.Bot):
    def __init__(self, settings: Settings):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.state = BotState(settings)

    async def setup_hook(self) -> None:
        from app.bot.commands.basic import BasicCommands
        from app.bot.commands.ai_commands import AICommands
        
        await self.add_cog(BasicCommands(self))
        await self.add_cog(AICommands(self))
        

        synced = await self.tree.sync()
        logger.info("Synced %d slash commands", len(synced))

    async def close(self) -> None:
        await super().close()


def create_bot(settings: Settings) -> StudyBot:
    if not settings.has_discord_token:
        raise RuntimeError(
            "DISCORD_TOKEN is not set. Add it to your .env file before starting the bot."
        )
    return StudyBot(settings)
