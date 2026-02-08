# This file loads the Visit Projection tracker.
# It helps us see if patient visits are happening on time.
import pandas as pd
import glob
import os

def load_visit_projection(study_path):
    """
    Load Visit Projection from Excel.
    Expected columns: 'site_id', 'planned_visits', 'completed_visits', 'overdue_visits'
    """
    # Look for the "Visit Projection" file
    files = glob.glob(os.path.join(study_path, "*Visit Projection*.xlsx"))
    
    if not files:
        files = glob.glob(os.path.join(study_path, "*Visit*.xlsx"))
        
    if not files:
        print(f"Warning: No Visit Projection file found in {study_path}")
        return pd.DataFrame(columns=['site_id', 'planned_visits', 'completed_visits', 'overdue_visits'])
    
    df = pd.read_excel(files[0])
    
    # Check if we have the right columns for the Visit Projection Tracker
    if 'Site' in df.columns and '# Days Outstanding' in df.columns:
        # Clean the site column
        df['site_id'] = df['Site'].astype(str).str.strip()
        
        # Make sure the days outstanding is a number (replace errors with 0)
        df['# Days Outstanding'] = pd.to_numeric(df['# Days Outstanding'], errors='coerce').fillna(0)
        
        # Aggregate data by site
        metrics = df.groupby('site_id').agg(
            planned_visits=('Site', 'count'), # Count total projection rows
            overdue_visits=('# Days Outstanding', lambda x: (x > 0).sum()) # Count how many are overdue (days > 0)
        ).reset_index()
        
        # Estimate completed visits.
        # Ideally, completed = total - overdue.
        metrics['completed_visits'] = metrics['planned_visits'] - metrics['overdue_visits'] 
        return metrics

    # Fallback for other formats
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    return pd.DataFrame(columns=['site_id', 'planned_visits', 'completed_visits', 'overdue_visits'])

