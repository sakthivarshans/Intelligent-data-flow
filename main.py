# This file is the main driver of our clinical insight platform.
# It connects all the parts: data loading, baseline building, risk prediction, and evaluation.
import os
import pandas as pd
import json
import yaml
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion.load_edc_metrics import load_edc_metrics
from ingestion.load_data_quality import load_data_quality
from ingestion.load_visit_projection import load_visit_projection
from preprocessing.normalize_ids import normalize_site_ids
from preprocessing.clean_common import fill_missing_metrics
from models.baseline_builder import build_baseline
from models.risk_scoring import score_risk
from models.anomaly_detection import detect_anomalies
from evaluation.evaluate_model import generate_evaluation_report

def load_config():
    # Load our configuration file which contains file paths and thresholds
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def ingest_study_data(study_id, raw_path_base):
    # This function loads all 3 data sources for a single study folder
    study_path = os.path.join(raw_path_base, study_id)
    if not os.path.exists(study_path):
        # Graceful fallback for demo purposes if folders don't exist yet
        return pd.DataFrame()
        
    # Load each specific Excel report
    df_edc = load_edc_metrics(study_path)
    df_dq = load_data_quality(study_path)
    df_visit = load_visit_projection(study_path)
    
    # Merge on site_id to get one wide table per site
    # We use outer join to make sure we don't lose any sites
    df_merged = pd.merge(df_edc, df_dq, on='site_id', how='outer')
    df_merged = pd.merge(df_merged, df_visit, on='site_id', how='outer')
    
    df_merged['study_id'] = study_id
    return df_merged

def main():
    config = load_config()
    
    # Step 1: Ingest Training Data
    # We loop through all the train studies listed in config
    print("Step 1: Ingesting Training Data...")
    train_dfs = []
    for study in config['studies']['train_studies']:
        df = ingest_study_data(study, config['data']['raw_train'])
        if not df.empty:
            train_dfs.append(df)
    
    # Combine all training studies into one big DataFrame
    if train_dfs:
        full_train_df = pd.concat(train_dfs, ignore_index=True)
        # Clean up IDs and missing values
        full_train_df = normalize_site_ids(full_train_df)
        full_train_df = fill_missing_metrics(full_train_df)
    else:
        print("No training data found. Using empty DataFrame.")
        full_train_df = pd.DataFrame()

    # Step 2: Build Baseline
    # We calculate the statistical averages (mean, p90) from the training data
    print("Step 2: Building Baseline...")
    baseline = build_baseline(full_train_df)
    
    # Save baseline to a JSON file so we can see it or use it in the UI
    os.makedirs(config['data']['baseline'], exist_ok=True)
    baseline_path = os.path.join(config['data']['baseline'], config['data']['baseline_file'])
    with open(baseline_path, 'w') as f:
        json.dump(baseline, f, indent=4)
    print(f"Baseline saved to {baseline_path}")
    
    # Step 3: Process Test Studies & Predict Risk
    # Now we load the new studies (Study 24, 25) that we want to check
    print("Step 3: Processing Test Studies & Predicting Risk...")
    test_dfs = []
    for study in config['studies']['test_studies']:
        df = ingest_study_data(study, config['data']['raw_test'])
        if not df.empty:
            test_dfs.append(df)
            
    if test_dfs:
        full_test_df = pd.concat(test_dfs, ignore_index=True)
        full_test_df = normalize_site_ids(full_test_df)
        full_test_df = fill_missing_metrics(full_test_df)
        
        # Calculate Risk Scores using the baseline we just built
        predictions = score_risk(full_test_df, baseline, config['thresholds'])
        
        # Save Predictions to CSV
        pred_path = config['data']['predictions_file'] 
        predictions.to_csv(pred_path, index=False)
        print(f"Predictions saved to {pred_path}")
        
        # Step 4: Evaluation
        # We generate a report to see how many risks we found
        print("Step 4: Evaluation...")
        report = generate_evaluation_report(predictions, test_df=full_test_df, baseline=baseline)
        
        eval_path = config['data']['evaluation_report']
        with open(eval_path, "w") as f:
            f.write(report)
        print(f"Evaluation report saved to {eval_path}")
        
    else:
        print("No test data found. Skipping prediction.")

if __name__ == "__main__":
    main()

