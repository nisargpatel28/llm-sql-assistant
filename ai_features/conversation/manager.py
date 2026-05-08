"""
Conversation Manager for Multi-turn Conversations with Context Retention
"""

import json
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class Message:
    """Represents a single message in the conversation"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    metadata: Optional[Dict] = None


class ConversationManager:
    """Manages conversation context and history for multi-turn interactions"""

    def __init__(self, db_path: str = "conversation.db", max_context_length: int = 50):
        self.db_path = db_path
        self.max_context_length = max_context_length
        self._init_database()