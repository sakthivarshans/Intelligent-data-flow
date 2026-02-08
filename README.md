# Clinical Insight-Driven Data Flow & Platform

## Problem Statement
Clinical trials generate siloed operational data using heterogeneous Excel reports. This platform integrates these datasets to detect operational bottlenecks and data quality risks using statistical baselines and rule-based risk scoring.

## Architecture
- **Ingestion**: Standardized loaders for EDC, Data Quality, and Visit Projection Excel files.
- **Preprocessing**: ID normalization, missing value handling.
- **Models**:
    - **Baseline Learning**: Statistical moments (Mean, Median, P75, P90) from 23 training studies.
    - **Risk Scoring**: Deterministic rules (e.g., Query Rate > 2x Baseline).
    - **Anomaly Detection**: Z-Score based outlier detection.
- **Evaluation**: Precision/Recall metrics calculation.
- **UI**: Streamlit-based dashboard.

### Graphs Tab
A Graphs tab was added to visualize visit delays, data completeness, site risk distribution, and baseline comparisons. A dropdown allows users to switch between daily, weekly, and monthly views.


## Train / Test Split
- **Training**: Study 01 - Study 23 (Learns the baseline)
- **Testing**: Study 24 - Study 25 (Predicts risk)

## How to Setup the datas
** Training Data **
Upload the given dataset to all the folders in data/raw/train/Study_XX. From study_01 to Study_23 needs to be uploaded by the dataset provided. For example upload the study1 dataset to data/raw/train/Study_01 folder. Note: the Study_03 and Study_12 is not there in the provided dataset so we managed with the rest of other data's.

** Testing Data **
Upload the given dataset to all the folders in data/raw/test/Study_XX. From study_24 to Study_25 needs to be uploaded by the dataset provided. For example upload the study24 dataset to data/raw/test/Study_24 folder.

## How to Run
1. **Setup Environment**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Place Data**:
   Ensure `data/raw/train/Study_XX` and `data/raw/test/Study_XX` folders exist and contain `*EDC*.xlsx`, `*DQ*.xlsx`, `*Visit*.xlsx` files.
3. **Run Pipeline**:
   ```bash
   python main.py
   ```
   This generates `baseline_metrics.json` and `predictions.csv`.
4. **Launch UI**:
   ```bash
   streamlit run app/ui.py
   ```

## Model Justification
- **Statistical Baselines**: Robust to noise and highly interpretable.
- **Rule-Based Scoring**: Compliance-friendly, explainable, and deterministic.
- **Avoidance of Black-Box**: Deep learning was explicitly excluded to ensure transparency and trust in clinical operations.

## Constraints & Reproducibility
- No synthetic data generation used.
- Fixed constraints on study splits.
- Local execution only.

## AI Layer (Optional)
- Includes `ai_layer/explainability_llm.py` structure for local LLM integration (e.g., Mistral 7B) to provide narrative explanations.

## Code Comments
Simple comments were added to the code to improve readability and understanding.

