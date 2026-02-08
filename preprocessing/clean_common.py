# This file handles missing data in our tables.
import pandas as pd
import numpy as np

def fill_missing_metrics(df):
    """
    Fill missing numeric metrics with 0.
    """
    # Find all columns that have numbers
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Replace empty values (NaN) with 0 for those columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    return df

