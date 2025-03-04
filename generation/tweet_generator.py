import json
import traceback
from datetime import datetime
from typing import List, Optional

from memory.models import Memory
from memory.storage import MemoryStore
from config.settings import (
    CHARACTER_NAME, COMPANY_NAME, CHARACTER_PERSONALITY,
    PROJECT_DESCRIPTION, PROJECT_STAGES
)
from .llm_clients import LLMClient, LLMError, TweetGenerationError


class TweetGenerator:
    """Generates tweets based on character profile and memory."""

    def __init__(self, memory_store: MemoryStore, llm_client: LLMClient):
        self.memory_store = memory_store
        self.llm_client = llm_client
        self.current_stage_index = 0

    def get_current_project_stage(self) -> str:
        """Determine current project stage based on progression"""
        # Simple logic: advance stages based on number of memories
        total_memories = self.memory_store.get_total_memory_count()

        # Advance stage roughly every 3 memories
        self.current_stage_index = min(total_memories // 3, len(PROJECT_STAGES) - 1)
        return PROJECT_STAGES[self.current_stage_index]

    def _format_recent_memories(self) -> str:
        """Format recent memories for inclusion in prompt."""
        recent_memories = self.memory_store.get_recent_memories(5)
        if not recent_memories:
            return "No previous events yet."

        return "\n".join([
            f"- {m.timestamp.strftime('%Y-%m-%d')}: {m.text}"
            for m in recent_memories
        ])

    def _format_milestone_memories(self) -> str:
        """Format milestone memories for inclusion in prompt."""
        milestone_memories = self.memory_store.get_milestone_memories()
        if not milestone_memories:
            return "No significant milestones yet."

        return "\n".join([
            f"- {m.timestamp.strftime('%Y-%m-%d')}: {m.text}"
            for m in milestone_memories
        ])

    def _format_character_profile(self) -> str:
        """Format the character's profile information."""
        return f"You are {CHARACTER_NAME}, a junior developer working at {COMPANY_NAME}. \nYour personality: {CHARACTER_PERSONALITY}"

    def _format_project_details(self) -> str:
        """Format the project description and current stage."""
        current_stage = self.get_current_project_stage()
        return f"Your current project: {PROJECT_DESCRIPTION}\nCurrent project stage: {current_stage}"

    def _format_current_date(self) -> str:
        """Format the current date."""
        today = datetime.now()
        return f"Today is {today.strftime('%Y-%m-%d')}, a {today.strftime('%A')}."

    def build_prompt(self) -> str:
        """Construct prompt for the LLM."""
        prompt = f"""
{self._format_character_profile()}

{self._format_project_details()}

Recent events in your work life:
{self._format_recent_memories()}

Important past milestones:
{self._format_milestone_memories()}

{self._format_current_date()}

Write a single tweet (max 280 characters) about your work experience today. 
Stay in character, be specific about technical details when appropriate, and maintain narrative continuity.
Don't use hashtags unless they're meaningful to the content.
        """
        return prompt

    def generate_tweet(self) -> str:
        """Generates a tweet using the configured LLM client."""
        prompt = self.build_prompt()
        try:
            tweet_text = self.llm_client.generate_text(prompt)
            if not tweet_text:
                raise TweetGenerationError("Generated tweet is empty.")
            return tweet_text
        except LLMError as e:
            raise TweetGenerationError(f"Error generating tweet: {e}") from e

#call this to set memories.
    # def create_and_store_tweet(self) -> str:
    #     """Generate a tweet and store it in memory"""
    #     try:
    #         tweet = self.generate_tweet()
    #          # Store in memory
    #         memory = Memory(
    #             text=tweet,
    #             timestamp=datetime.now(),
    #             importance=1.0,  # Normal importance
    #             category="daily"
    #         )
    #         self.memory_store.save_memory(memory)

    #         return tweet
    #     except TweetGenerationError as e:
    #         print(f"Error creating and storing tweet: {e}")
    #         # Handle the error as appropriate, e.g., return a fallback tweet or re-raise
    #         return "Fallback tweet due to generation error."
