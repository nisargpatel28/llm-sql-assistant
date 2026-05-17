"""
Automated Report Generation for Transaction Data
"""

import pandas as pd
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class ReportGenerator:
    """Generates automated reports from transaction data"""

    def __init__(self):
        self.templates = self._load_templates()
