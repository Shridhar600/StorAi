from datetime import datetime
from typing import Dict, Any, Optional

#Each tweet is a memory, and each memory has a text, timestamp, importance, category, and metadata.
class Memory:
    
    #constructor basically
    def __init__(self,text: str,timestamp: datetime,importance: float = 1.0,category: str = "daily",metadata: Optional[Dict[str, Any]] = None ):
        self.text = text
        self.timestamp = timestamp
        self.importance = importance  # 1.0 = normal, 2.0 = significant, 3.0 = milestone
        self.category = category      # dailyLog, technical, personal, milestone
        self.metadata = metadata or {}
        
#converting memory to dictionary for storage
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "timestamp": self.timestamp.isoformat(),
            "importance": self.importance,
            "category": self.category,
            "metadata": self.metadata
        }

#converting dictionary to memory      
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Memory': #type hinting for return type
        return cls(
            text=data["text"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            importance=data["importance"],
            category=data["category"],
            metadata=data.get("metadata", {})
        )