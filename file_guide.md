# Clinical Insight Platform - Project File Guide

This document provides a detailed overview of the project structure and the purpose of each file within the Clinical Insight-Driven Data Flow & Platform.

## Root Directory

### `main.py`
The **main entry point** and driver of the application. It orchestrates the entire pipeline:
1.  **Ingestion**: Loads training data (Studies 1-23).
2.  **Training**: Builds statistical baselines from training data.
3.  **Inference**: Loads test data (Studies 24-25) and scores risk.
4.  **Evaluation**: Compares predictions against ground truth and generates `evaluation_report.md`.

### `config.yaml`
Central configuration file containing:
-   **File Paths**: Locations for raw data, processed data, and outputs.
-   **Study Configuration**: Lists of specific studies used for Training vs. Testing.
-   **Thresholds**: Risk parameters (e.g., Query Rate Multiplier = 2.0).
-   **App Settings**: UI titles and defaults.

### `requirements.txt`
Lists all Python dependencies required to run the project (e.g., `pandas`, `streamlit`, `pyyaml`, `openpyxl`).

### `README.md`
The high-level project documentation explaining the problem statement, architecture, setup instructions, and how to run the pipeline.

### `walkthrough.md`
A guide/walkthrough artifact describing recent changes or usage of the system.

### `predictions.csv`
(Generated Output) A CSV file containing the final risk assessment for each site in the test studies. Columns usually include `site_id`, `risk_level` (High/Medium/Low), and explanation flags.

### `evaluation_report.md`
(Generated Output) A Markdown report summarizing model performance metrics (Precision, Recall, F1-Score) and Data Quality statistics.

---

## 2. Ingestion Layer (`ingestion/`)
*Responsible for loading raw data from heterogeneous Excel reports.*

-   **`load_edc_metrics.py`**: Loads **EDC (Electronic Data Capture)** reports. Extracts query counts and response times. Handles file name variations (e.g., `*Compiled EDRR*` vs `*EDC*`).
-   **`load_data_quality.py`**: Loads **Data Quality** reports. specifically tracking "Missing Pages" issues to identify sites with poor data entry practices.
-   **`load_visit_projection.py`**: Loads **Visit Projection** reports. Extracts "Projected Date" and "# Days Outstanding" to calculate visit delays.

## 3. Preprocessing Layer (`preprocessing/`)
*Handles data cleaning, normalization, and preparation.*

-   **`normalize_ids.py`**: Standardizes `site_id` formats. It handles complex strings like "Site1-Subject100" to extract the clean Site ID for merging.
-   **`clean_common.py`**: specific logic to fill missing values (NaN) with defaults (e.g., 0 for counts) to ensure downstream math works correctly.
-   **`align_time.py`**: (If present) Utilities for aligning time-series data or handling date formats across different Excel files.

## 4. Modeling Layer (`models/`)
*Contains the core logic for statistical learning and risk assessment.*

-   **`baseline_builder.py`**: Calculates the **Statistical Baselines** from the training studies. Computes Mean, Median, P75 (75th percentile), and P90 for key metrics (Query Count, Delay, Missing Pages).
-   **`risk_scoring.py`**: The **Deterministic Inference Engine**. Compares new data (Test Studies) against the baselines using rules defined in `config.yaml`:
    -   *High Risk*: Query Rate > 2x Baseline.
    -   *Medium Risk*: Delays > P75 or Missing Pages > P90.
-   **`anomaly_detection.py`**: Contains fallback or complementary logic for outlier detection, potentially using Z-Scores to find sites that deviate significantly from the norm.

## 5. Evaluation Layer (`evaluation/`)
*Assesses the accuracy and quality of the risk predictions.*

-   **`evaluate_model.py`**: Calculates performance (Precision, Recall, F1) by comparing the system's "Risk Level" against a ground truth (derived from strict percentiles). Generates the text for `evaluation_report.md`.
-   **`metrics.py`**: Helper functions for specific mathematical metric calculations (MAE, RMSE, etc.).

## 6. Application Layer (`app/`)
*The User Interface for interacting with the platform.*

-   **`ui.py`**: A **Streamlit** application that provides:
    -   **Overview**: Project context and study splits.
    -   **Baselines**: Visualization of the learned training stats.
    -   **Predictions**: Interactive table of risk scores for Test sites (Color-coded).
    -   **Evaluation**: Displays the generated evaluation report.
    -   **Graphs**: Visualizes trends like Visit Delays and Data Completeness over time.

## 7. AI Layer (`ai_layer/`)
*Optional layer for GenAI integration.*

-   **`explainability_llm.py`**: A wrapper structure for integrating a Local LLM (like Mistral or Llama). It is designed to take the structured risk data and generate a natural language narrative explaining *why* a site is high risk. (Currently uses a rule-based fallback if no model is loaded).

## 8. Root Utilities
*Helper scripts for debugging and data inspection.*

-   **`columns_dump.txt` / `dump_columns.py`**: Utilities likely used during development to inspect the column names of raw Excel files to handle schema variations.
-   **`inspect_headers_clean.py`**: Script to verify header consistency across dataset files.
