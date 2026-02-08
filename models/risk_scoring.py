# This file decides if a site is "High Risk" or "Medium Risk".
# It compares the site's data against the baseline we calculated earlier.
import pandas as pd

def score_risk(df, baseline, thresholds):
    """
    Apply rule-based risk scoring.
    
    Rules:
    - Query rate (query_count) > 2x Baseline Mean -> High Risk
    - Visit delay (overdue_visits) > Baseline P75 -> Delay Risk
    - Missing pages (missing_pages_count) > Baseline P90 -> Data Quality Risk
    """
    
    results = []
    
    # Loop through every site in our test data
    for _, row in df.iterrows():
        site_id = row.get('site_id', 'Unknown')
        risk_level = 'Low' # Default is Low
        delay_flag = 'No'
        dq_flag = 'No'
        explanations = []
        
        # Risk Rule 1: Query Count (Too many questions?)
        metric = 'query_count'
        if metric in baseline:
            base_val = baseline[metric]['mean']
            # We check if the count is way higher than the average
            # The multiplier is read from config (e.g. 2x)
            threshold = base_val * thresholds['risk']['query_rate_multiplier']
            if base_val > 0 and row.get(metric, 0) > threshold:
                risk_level = 'High'
                explanations.append(f"Query count ({row[metric]}) > 2x Baseline Mean ({base_val:.2f})")
        
        # Risk Rule 2: Visit Delay (Are patients late?)
        metric = 'overdue_visits'
        if metric in baseline:
            # We compare against the 75th percentile of normal
            base_val = baseline[metric]['p75']
            if row.get(metric, 0) > base_val:
                delay_flag = 'Yes'
                # If it wasn't already High risk, mark it as Medium
                if risk_level != 'High': risk_level = 'Medium'
                explanations.append(f"Overdue visits ({row[metric]}) > Baseline P75 ({base_val:.2f})")

        # Risk Rule 3: Missing Pages (Data Quality issues)
        metric = 'missing_pages_count'
        if metric in baseline:
            # We compare against the 90th percentile (extreme outliers)
            base_val = baseline[metric]['p90']
            if row.get(metric, 0) > base_val:
                dq_flag = 'Yes'
                if risk_level != 'High': risk_level = 'Medium'
                explanations.append(f"Missing pages ({row[metric]}) > Baseline P90 ({base_val:.2f})")
                
        # Save the results for this site
        results.append({
            'study_id': row.get('study_id', 'Unknown'),
            'site_id': site_id,
            'risk_level': risk_level,
            'delay_flag': delay_flag,
            'data_quality_flag': dq_flag,
            'explanation': "; ".join(explanations) if explanations else "Normal operation"
        })
        
    return pd.DataFrame(results)

