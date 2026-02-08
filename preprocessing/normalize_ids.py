# This file makes sure all site IDs look the same.
import pandas as pd

def normalize_site_ids(df, id_col='site_id'):
    """
    Normalize site IDs to ensure consistency.
    Converts to string and strips whitespace.
    """
    # If the column exists, we clean it up
    if id_col in df.columns:
        # Convert to text (string) and remove spaces at the beginning or end
        df[id_col] = df[id_col].astype(str).str.strip()
    return df

