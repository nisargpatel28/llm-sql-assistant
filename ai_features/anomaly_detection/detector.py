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

    def detect_anomalies(self, data: List[Dict], threshold: float = 0.95) -> Dict:
        """
        Detect anomalies in transaction data

        Args:
            data: List of transaction dictionaries
            threshold: Confidence threshold for anomaly detection (0-1)

        Returns:
            Dictionary with anomalies and statistics
        """
        if not data:
            return {"anomalies": [], "stats": {}, "total_transactions": 0}

        try:
            # Convert to DataFrame for easier processing
            df = pd.DataFrame(data)

            # Ensure required columns exist
            required_cols = ['amount', 'date']
            if not all(col in df.columns for col in required_cols):
                return {
                    "error": f"Missing required columns: {required_cols}",
                    "anomalies": [],
                    "stats": {},
                    "total_transactions": len(data)
                }

            # Preprocess data
            processed_data = self._preprocess_data(df)

            # Detect anomalies using multiple methods
            statistical_anomalies = self._detect_statistical_anomalies(
                processed_data, threshold)
            ml_anomalies = self._detect_ml_anomalies(processed_data, threshold)

            # Combine results
            all_anomalies = self._combine_anomaly_results(
                statistical_anomalies,
                ml_anomalies,
                processed_data
            )

            # Calculate statistics
            stats = self._calculate_statistics(df)

            return {
                "anomalies": all_anomalies,
                "stats": stats,
                "total_transactions": len(data),
                "anomaly_count": len(all_anomalies)
            }

        except Exception as e:
            return {
                "error": str(e),
                "anomalies": [],
                "stats": {},
                "total_transactions": len(data)
            }

    def _preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess transaction data for anomaly detection"""
        processed = df.copy()

        # Convert date to datetime if it's not already
        if 'date' in processed.columns:
            processed['date'] = pd.to_datetime(
                processed['date'], errors='coerce')

        # Convert amount to numeric
        processed['amount'] = pd.to_numeric(
            processed['amount'], errors='coerce')

        # Fill missing values
        processed['amount'] = processed['amount'].fillna(
            processed['amount'].median())

        # Add derived features
        if 'date' in processed.columns:
            processed['hour'] = processed['date'].dt.hour
            processed['day_of_week'] = processed['date'].dt.dayofweek
            processed['month'] = processed['date'].dt.month

        # Add rolling statistics
        processed = processed.sort_values('date')
        processed['amount_rolling_mean'] = processed['amount'].rolling(
            window=10, min_periods=1).mean()
        processed['amount_rolling_std'] = processed['amount'].rolling(
            window=10, min_periods=1).std()

        return processed