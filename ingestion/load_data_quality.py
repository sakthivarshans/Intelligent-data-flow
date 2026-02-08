# This file loads the Data Quality reports.
# These reports tell us if any pages are missing in the clinical data.
import pandas as pd
import glob
import os

def load_data_quality(study_path):
    """
    Load Data Quality metrics from Excel files in the study directory.
    Expected columns: 'site_id', 'completeness_score', 'issue_aging_days'
    """
    # Look for files with "Missing" and "Page" in the name (e.g., Global Missing Pages)
    # We use * wildcards because the names might change a bit
    files = glob.glob(os.path.join(study_path, "*Missing*Page*.xlsx"))
    
    # If we didn't find the Missing Pages file, try looking for a generic DQ file
    if not files:
        files = glob.glob(os.path.join(study_path, "*DQ*.xlsx"))

    # If still no file, print a warning and return empty data
    if not files:
        print(f"Warning: No Data Quality file found in {study_path}")
        return pd.DataFrame(columns=['site_id', 'completeness_score', 'issue_aging_days', 'missing_pages_count'])
    
    # Load the first file we found
    df = pd.read_excel(files[0])
    
    # Logic for Global Missing Pages Report
    # We check if the 'SiteNumber' column exists to know if it's the right file format
    if 'SiteNumber' in df.columns:
        # Convert site number to string to match other files
        df['site_id'] = df['SiteNumber'].astype(str).str.strip()
        
        # Count how many rows (missing pages) there are for each site
        metrics = df.groupby('site_id').size().reset_index(name='missing_pages_count')
        
        # Calculate a simple completeness score.
        # We start with 100% and subtract the number of missing pages.
        # We make sure it doesn't go below 0 using max(0, ...).
        metrics['completeness_score'] = metrics['missing_pages_count'].apply(lambda x: max(0, 100 - x))
        metrics['issue_aging_days'] = 0 # We don't have aging data in this file, so set to 0
        
        return metrics

    # Fallback if the file format is different than expected
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    return pd.DataFrame(columns=['site_id', 'completeness_score', 'issue_aging_days', 'missing_pages_count'])

