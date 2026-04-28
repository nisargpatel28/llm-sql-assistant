"""
Anomaly Detection for Transaction Data
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import statistics
from datetime import datetime, timedelta
import json


class AnomalyDetector:
    """Detects anomalies in transaction data using statistical and ML methods"""

    def __init__(self):
        self.scaler = StandardScaler()
        self.isolation_forest = IsolationForest(
            contamination=0.1,  # Expected proportion of outliers
            random_state=42,
            n_estimators=100
        )
