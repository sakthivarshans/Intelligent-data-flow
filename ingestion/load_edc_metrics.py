# This file loads EDC (Electronic Data Capture) metrics.
# It tracks issues like open queries (questions about data) for each site.
import pandas as pd
import glob
import os

def load_edc_metrics(study_path):
    """
    Load EDC metrics from Excel files in the study directory.
    Expected columns in Excel: 'site_id', 'query_count', 'query_response_days', 'missing_pages_count'
    """
    # Look for the "Compiled EDRR" file which has the query data
    files = glob.glob(os.path.join(study_path, "*Compiled EDRR*.xlsx"))
    
    if not files:
        # If not found, try a generic "EDC" file name
        files = glob.glob(os.path.join(study_path, "*EDC*.xlsx"))
    
    if not files:
        print(f"Warning: No EDC metrics file found in {study_path}")
        return pd.DataFrame(columns=['site_id', 'query_count', 'query_response_days'])
    
    df = pd.read_excel(files[0])
    
    # Check if this is the "Compiled EDRR" format we expect
    if 'Total Open issue Count per subject' in df.columns and 'Subject' in df.columns:
        # The site ID isn't in its own column, it's inside the Subject ID (e.g. "Site1-Subject100")
        # So we need to splitting the Subject string to get the Site.
        
        def extract_site(subj):
            s = str(subj)
            if '-' in s:
                return s.split('-')[0].strip() # Take the part before the dash
            return s # If no dash, just use the whole thing
            
        df['site_id'] = df['Subject'].apply(extract_site)
        
        # Group by site and sum up all the open issues (queries)
        metrics = df.groupby('site_id')['Total Open issue Count per subject'].sum().reset_index()
        metrics.rename(columns={'Total Open issue Count per subject': 'query_count'}, inplace=True)
        
        # We don't have response days in this file, so we set it to 0
        metrics['query_response_days'] = 0
        
        return metrics

    # Fallback if the file format is completely different
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    metrics = pd.DataFrame()
    metrics['site_id'] = df.get('site_id', df.get('site', []))
    metrics['query_count'] = 0
    metrics['query_response_days'] = 0
    return metrics

