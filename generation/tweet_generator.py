import requests
import json
import traceback
from datetime import datetime
from typing import List, Optional

from memory.models import Memory
from memory.storage import MemoryStore
from config.settings import (
    CHARACTER_NAME, COMPANY_NAME, CHARACTER_PERSONALITY,
    PROJECT_DESCRIPTION, PROJECT_STAGES, 
    LLM_API_KEY, LLM_MODEL, LLM_BASE_URL
)


class TweetGenerator:
    """Generates tweets based on character profile and memory using OpenRouter API"""
    
    def __init__(self, memory_store: MemoryStore):
        self.memory_store = memory_store
        self.llm_api_key = LLM_API_KEY
        self.llm_model = LLM_MODEL
        self.llm_url = f"{LLM_BASE_URL}/chat/completions" #will make it more dynamic in future
        self.current_stage_index = 0
    
    def get_current_project_stage(self) -> str:
        """Determine current project stage based on progression"""
        # Simple logic: advance stages based on number of memories
        total_memories = self.memory_store.get_total_memory_count()
        
        # Advance stage roughly every 3 memories
        self.current_stage_index = min(total_memories // 3, len(PROJECT_STAGES) - 1)
        return PROJECT_STAGES[self.current_stage_index]
    
    def format_memories(self, memories: List[Memory]) -> str:
        """Format memories for inclusion in prompt"""
        if not memories:
            return "No previous events yet."
            
        return "\n".join([
            f"- {m.timestamp.strftime('%Y-%m-%d')}: {m.text}" 
            for m in memories
        ])
    
    #Very important function to build the prompt
    def build_prompt(self) -> str:
        """Construct prompt for the LLM"""
        recent_memories = self.memory_store.get_recent_memories(5)
        milestone_memories = self.memory_store.get_milestone_memories()
        current_stage = self.get_current_project_stage()
        
        today = datetime.now()
        
        prompt = f"""
        You are {CHARACTER_NAME}, a junior developer working at {COMPANY_NAME}. 
        Your personality: {CHARACTER_PERSONALITY}
        
        Your current project: {PROJECT_DESCRIPTION}
        Current project stage: {current_stage}
        
        Recent events in your work life:
        {self.format_memories(recent_memories)}
        
        Important past milestones:
        {self.format_memories(milestone_memories)}
        
        Today is {today.strftime('%Y-%m-%d')}, a {today.strftime('%A')}.
        
        Write a single tweet (max 280 characters) about your work experience today. 
        Stay in character, be specific about technical details when appropriate, and maintain narrative continuity.
        Don't use hashtags unless they're meaningful to the content.
        """
        return prompt
    
    def generate_tweet(self) -> str:
        prompt = self.build_prompt()
        headers = {
            "Authorization": f"Bearer {self.llm_api_key}",
            "Content-Type": "application/json",
            # "HTTP-Referer": "http://localhost:5000" 
        }
        
        data = {
            "model": self.llm_model,
            "messages": [
                {
                "role": "user",
                "content": prompt
                }
            ],
           # "max_tokens": 300,
            "temperature": 2.0 #need to experiment with this
        }
        
        try:
            # Print debugging information
            print(f"Making request to OpenRouter API:")
            print(f"URL: {self.llm_url}")
            print(f"Model: {self.llm_model}")
           # print(f"API Key (first 4 chars): {self.llm_api_key[:4]}...")
            # print(f"Prompt: {prompt}")
            
            # Make the API request
            response = requests.post(
                self.llm_url,
                headers=headers,
                json=data
            )
            
            # Print response status and headers for debugging
            print(f"Response status code: {response.status_code}")
            
            # Try to print response content regardless of status code
            try:
                response_json = response.json()
                print(f"Response content: {json.dumps(response_json, indent=2)}")
            except:
                print(f"Raw response: {response.text[:500]}")
            
            # Now raise for status after we've logged the response
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            tweet_text = result['choices'][0]['message']['content'].strip().strip('"').strip()
            
            # Validate tweet length
            if len(tweet_text) > 280:
                tweet_text = tweet_text[:277] + "..."
                
            return tweet_text
            
        except Exception as e:
            # Print detailed error information
            print(f"Error generating tweet: {str(e)}")
            print(f"Exception type: {type(e).__name__}")
            print(f"Traceback: {traceback.format_exc()}")
            
            # Still return a fallback tweet but with more info
            return f"Technical difficulties with LLM: {type(e).__name__}. Please check logs. {datetime.now().strftime('%H:%M')}"
    
    def create_and_store_tweet(self) -> str:
        """Generate a tweet and store it in memory"""
        tweet = self.generate_tweet()
        
        # Store in memory
        memory = Memory(
            text=tweet,
            timestamp=datetime.now(),
            importance=1.0,  # Normal importance
            category="daily"
        )
        self.memory_store.save_memory(memory)
        
        return tweet