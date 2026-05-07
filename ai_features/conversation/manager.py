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