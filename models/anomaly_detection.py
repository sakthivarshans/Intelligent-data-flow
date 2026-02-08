# This file uses statistics to find weird data points (anomalies).
import pandas as pd
import numpy as np

def detect_anomalies(df, baseline):
    """
    Detect anomalies using Z-Score based on baseline mean and std.
    """
    anomalies = []
    
    # Define metrics to check for anomalies
    metrics = ['query_count', 'missing_pages_count', 'overdue_visits']
    
    for _, row in df.iterrows():
        site_anomalies = []
        for metric in metrics:
            # We need standard deviation to calculate Z-Score
            if metric in baseline and baseline[metric]['std'] > 0:
                mean = baseline[metric]['mean']
                std = baseline[metric]['std']
                val = row.get(metric, 0)
                
                # Formula for Z-Score: (Value - Mean) / Standard Deviation
                # It tells us how many "standard deviations" away this value is.
                z_score = (val - mean) / std
                
                # If Z-Score is > 3 (or < -3), it's very unusual.
                if abs(z_score) > 3: # Standard threshold for anomaly
                    site_anomalies.append(f"{metric} Z-Score: {z_score:.2f}")
        
        if site_anomalies:
            anomalies.append({
                'site_id': row.get('site_id'),
                'anomalies': "; ".join(site_anomalies)
            })
            
    return pd.DataFrame(anomalies)

