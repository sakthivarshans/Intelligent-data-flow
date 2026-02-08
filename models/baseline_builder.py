# This file calculates the "normal" behavior (baseline) from historical data.
import pandas as pd
import numpy as np

def build_baseline(train_df):
    """
    Calculate statistical baselines from the training DataFrame.
    Metrics: Mean, Median, P75, P90, Std Dev.
    
    Args:
        train_df: DataFrame containing aggregated site-level metrics from training studies.
        
    Returns:
        dict: Baseline statistics for each metric.
    """
    # List of all the metrics we want to track
    metrics = [
        'query_count', 'query_response_days', 'missing_pages_count',
        'completeness_score', 'issue_aging_days', 
        'planned_visits', 'completed_visits', 'overdue_visits'
    ]
    
    baseline = {}
    
    for metric in metrics:
        # Check if we have data for this metric
        if metric in train_df.columns:
            # Drop any empty values
            series = train_df[metric].dropna()
            
            if series.empty:
                # If no data, set everything to 0
                baseline[metric] = {
                    'mean': 0, 'median': 0, 'p75': 0, 'p90': 0, 'std': 0
                }
            else:
                # Calculate the stats:
                # Mean: Average
                # Median: Middle value
                # P75: 75th percentile (higher than 75% of sites)
                # P90: 90th percentile (higher than 90% of sites, helps identify outliers)
                # Std: Standard Deviation (how spread out the data is)
                baseline[metric] = {
                    'mean': float(series.mean()),
                    'median': float(series.median()),
                    'p75': float(np.percentile(series, 75)),
                    'p90': float(np.percentile(series, 90)),
                    'std': float(series.std())
                }
        else:
             # If the column is missing entirely, set to 0
             baseline[metric] = {
                'mean': 0.0, 'median': 0.0, 'p75': 0.0, 'p90': 0.0, 'std': 0.0
            }
    
    return baseline

