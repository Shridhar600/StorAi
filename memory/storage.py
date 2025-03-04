import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from .models import Memory
from config.settings import MEMORY_FILE


class MemoryStore:
    """Manages storage and retrieval of the bot's memories"""
    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or MEMORY_FILE
        self.memories = self._load_memories()
        
    def _load_memories(self) -> List[Memory]: #returns a list of memories from disk.
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f: #Automatically closes the file.
                try:
                    data = json.load(f)
                    return [Memory.from_dict(item) for item in data] #iterating over the data and converting it to a list of memory objects.
                except json.JSONDecodeError:
                    print(f"Warning: Memory file corrupted. Starting with empty memories.") #error case if the file is corrupted
                    return []
        return [] #returning an empty list if the file does not exist. Same for above if the file is corrupted.
    
    def save_memory(self, memory: Memory) -> None: #void function
        self.memories.append(memory)
        self._save_to_disk()
        
    def _save_to_disk(self) -> None:
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        with open(self.file_path, 'w') as f:
            json.dump([m.to_dict() for m in self.memories], f, indent=2)
    
    def get_recent_memories(self, count: int = 5) -> List[Memory]:
        """Get most recent memories"""
        return sorted(self.memories, key=lambda x: x.timestamp, reverse=True)[:count]
    
    def get_milestone_memories(self) -> List[Memory]:
        """Get important milestone memories"""
        return [m for m in self.memories if m.importance >= 2.5]
    
    def get_memories_by_category(self, category: str) -> List[Memory]:
        """Get memories filtered by category"""
        return [m for m in self.memories if m.category == category]
    
    def get_total_memory_count(self) -> int:
        """Get total number of memories"""
        return len(self.memories)