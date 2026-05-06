# Specification: Wire Kaggle Notebooks to BioChannel App

## Goal

Wire the Kaggle notebooks to the Streamlit app through a simple, reliable **CSV handoff pipeline**.

The notebooks perform:

```text
Dataset download → preprocessing → metrics/model outputs → CSV export
```

The Streamlit app performs:

```text
CSV load → interactive controls → visualization → Gemma explanation
```

---

# 1. Architecture

```text
Kaggle Notebooks
    ↓
Export processed CSV files
    ↓
Download CSVs from /kaggle/working/processed/
    ↓
Place CSVs into app/data/processed/
    ↓
Streamlit app loads CSVs
    ↓
If CSV missing, app uses demo fallback data
```

---

# 2. Required Folder Structure

```text
biochannel/
├── notebooks/
│   ├── 01_cell_decision_simulator.ipynb
│   ├── 02_information_loss_analyzer.ipynb
│   ├── 03_drug_response_predictor.ipynb
│   ├── 04_explainable_cell_ai.ipynb
│   └── 05_edge_biology_assistant.ipynb
│
└── app/
    ├── app.py
    ├── requirements.txt
    ├── src/
    │   └── data_loader.py
    │
    └── data/
        └── processed/
            ├── cell_decision_pca.csv
            ├── cell_top_features.csv
            ├── info_metrics.csv
            ├── info_timeseries.csv
            ├── drug_response_processed.csv
            ├── explain_feature_importance.csv
            ├── explain_class_mapping.csv
            └── edge_small_expression.csv
```

---

# 3. Notebook Export Contract

Each notebook must export files to:

```text
/kaggle/working/processed/
```

The exported files must use stable, predictable filenames.

---

## Notebook 1: Cell Decision Simulator

### Notebook

```text
01_cell_decision_simulator.ipynb
```

### Input Dataset

```text
Gene Expression Cancer RNA-seq
or Single-cell RNA-seq dataset
```

### Exported Files

```text
cell_decision_pca.csv
cell_top_features.csv
```

### Required Schema: `cell_decision_pca.csv`

```text
Column          Type        Description
---------------------------------------------------------
PC1             float       PCA x-coordinate
PC2             float       PCA y-coordinate
cell_state      string      Cell state / class / cluster label
```

### Required Schema: `cell_top_features.csv`

```text
Column          Type        Description
---------------------------------------------------------
feature         string      Gene or feature name
variance        float       Feature variance / ranking score
```

### Processing Steps

```text
1. Load gene-expression dataset.
2. Select numeric gene-expression columns.
3. Remove missing or invalid columns.
4. Fill missing numeric values with median.
5. Apply log1p normalization.
6. Select top variable genes/features.
7. Standardize values.
8. Run PCA to 2 dimensions.
9. Export PCA coordinates and feature rankings.
```

---

## Notebook 2: Information Loss Analyzer

### Notebook

```text
02_information_loss_analyzer.ipynb
```

### Input Dataset

```text
Time-series gene expression dataset
```

### Exported Files

```text
info_timeseries.csv
info_metrics.csv
```

### Required Schema: `info_timeseries.csv`

```text
Column              Type        Description
-------------------------------------------------------------
time                float/int   Time index or time value
input_signal        float       Input/stimulus proxy
pathway_response    float       Output/pathway response proxy
```

### Required Schema: `info_metrics.csv`

```text
Column                     Type        Description
----------------------------------------------------------------
input_entropy_bits          float       Entropy of input signal
output_entropy_bits         float       Entropy of output response
mutual_information_bits     float       MI between input and output
signal_fidelity             float       MI / input entropy
information_loss            float       1 - signal fidelity
```

### Processing Steps

```text
1. Load time-series gene-expression dataset.
2. Select numeric columns.
3. Choose input signal proxy.
4. Choose output response proxy.
5. Discretize input and output into bins.
6. Compute input entropy.
7. Compute output entropy.
8. Compute mutual information.
9. Compute signal fidelity.
10. Compute information loss.
11. Export time-series and metrics.
```

---

## Notebook 3: Drug Response Predictor

### Notebook

```text
03_drug_response_predictor.ipynb
```

### Input Dataset

```text
GDSC drug response dataset
or other drug response prediction dataset
```

### Exported File

```text
drug_response_processed.csv
```

### Required Schema: `drug_response_processed.csv`

```text
Column              Type        Description
---------------------------------------------------------------
cell_line           string      Cell line name or ID
drug                string      Drug / compound name
sensitivity         float       Normalized sensitivity score, 0 to 1
resistance_risk     float       1 - sensitivity
apoptosis_proxy     float       Proxy probability for apoptosis
survival_proxy      float       Proxy probability for survival
```

### Processing Steps

```text
1. Load drug-response dataset.
2. Detect or manually define cell-line column.
3. Detect or manually define drug column.
4. Detect or manually define response / IC50 / AUC column.
5. Normalize response values.
6. Convert response to sensitivity score.
7. Derive resistance risk.
8. Derive apoptosis proxy.
9. Derive survival proxy.
10. Export processed drug-response table.
```

---

## Notebook 4: Explainable Cell AI

### Notebook

```text
04_explainable_cell_ai.ipynb
```

### Input Dataset

```text
Cancer classification dataset
such as Breast Cancer Wisconsin
```

### Exported Files

```text
explain_feature_importance.csv
explain_class_mapping.csv
```

### Required Schema: `explain_feature_importance.csv`

```text
Column          Type        Description
--------------------------------------------------------
feature         string      Feature name
importance      float       Model-derived importance score
```

### Required Schema: `explain_class_mapping.csv`

```text
Column          Type        Description
--------------------------------------------------------
class           string      Original class label
encoded_value   int         Encoded numeric class
```

### Processing Steps

```text
1. Load classification dataset.
2. Identify target column.
3. Select numeric features.
4. Clean missing values.
5. Train simple classifier.
6. Extract feature importances.
7. Export feature importance table.
8. Export class mapping table.
```

---

## Notebook 5: Edge Biology Assistant

### Notebook

```text
05_edge_biology_assistant.ipynb
```

### Input Dataset

```text
Small gene-expression dataset
```

### Exported File

```text
edge_small_expression.csv
```

### Required Schema: `edge_small_expression.csv`

```text
Column          Type        Description
--------------------------------------------------------
PC1             float       PCA x-coordinate
PC2             float       PCA y-coordinate
edge_state      string      Lightweight state label
```

### Processing Steps

```text
1. Load small gene-expression dataset.
2. Select numeric columns.
3. Clean missing values.
4. Apply log1p normalization.
5. Select small subset for edge demo.
6. Run PCA to 2 dimensions.
7. Assign lightweight state labels.
8. Export edge-ready dataset.
```

---

# 4. Streamlit Loader Specification

Create a shared loader file:

```text
app/src/data_loader.py
```

## Responsibilities

```text
1. Define processed data directory.
2. Check whether expected CSV exists.
3. Load CSV if present.
4. Validate minimum required columns.
5. Return fallback demo data if missing or invalid.
```

## Required Loader Functions

```text
load_cell_pca_or_demo()
load_cell_top_features_or_demo()
load_info_timeseries_or_demo()
load_info_metrics_or_none()
load_drug_response_or_demo()
load_feature_importance_or_demo()
load_edge_expression_or_demo()
```

---

## Loader Behavior

### If CSV exists

```text
Read CSV from app/data/processed/
Return real processed data
```

### If CSV is missing

```text
Generate synthetic fallback data
Return fallback data
Show app normally
```

### If CSV exists but schema is invalid

```text
Ignore invalid CSV
Use fallback demo data
Optional: show warning in Streamlit
```

---

# 5. Streamlit App Integration

## Global App Behavior

The app must not call Kaggle notebooks directly.

Instead:

```text
Notebooks produce files.
App consumes files.
```

This keeps the app simple, stable, and deployable.

---

## Tab 1 Integration

### Load

```text
cell_decision_pca.csv
cell_top_features.csv
```

### Use

```text
- Plot PC1 vs PC2 as cell-state landscape
- Color points by cell_state
- Display top features table
- Use sliders to modify simulated decision probabilities
```

---

## Tab 2 Integration

### Load

```text
info_timeseries.csv
info_metrics.csv
```

### Use

```text
- Plot input_signal vs pathway_response over time
- Recompute metrics when user changes noise level
- Display notebook-exported baseline metrics in expandable section
```

---

## Tab 3 Integration

### Load

```text
drug_response_processed.csv
```

### Use

```text
- Populate cell line dropdown from cell_line column
- Populate drug dropdown from drug column
- Use sensitivity score to compute dose-response curve
- Use resistance_risk to inform resistance metric
```

---

## Tab 4 Integration

### Load

```text
explain_feature_importance.csv
explain_class_mapping.csv
```

### Use

```text
- Show feature importance chart
- Send top features into Gemma prompt
- Use class mapping for explanation context
```

---

## Tab 5 Integration

### Load

```text
edge_small_expression.csv
```

### Use

```text
- Plot lightweight PCA landscape
- Color by edge_state
- Use local controls for simple signal/noise simulation
```

---

# 6. CSV Handoff Workflow

## Step 1: Run Kaggle Notebooks

Each notebook creates:

```text
/kaggle/working/processed/*.csv
```

## Step 2: Download Outputs

Download all generated CSV files.

## Step 3: Place in App

Move CSVs into:

```text
app/data/processed/
```

## Step 4: Run Streamlit

```bash
cd app
pip install -r requirements.txt
streamlit run app.py
```

---

# 7. Dataset Download Specification

Each notebook should include two dataset loading paths.

## Option A: Kaggle UI Add Data

Recommended for Kaggle notebooks.

```text
1. Open notebook on Kaggle.
2. Click Add Data.
3. Search dataset.
4. Attach dataset.
5. Load from /kaggle/input/...
```

## Option B: Kaggle API Download

Optional.

Each notebook includes:

```python
!pip install -q kaggle

import os
os.environ["KAGGLE_CONFIG_DIR"] = "/kaggle/working"

# After adding kaggle.json:
# !kaggle datasets download -d DATASET_SLUG -p /kaggle/working/raw --unzip
```

---

# 8. Gemma Wiring Specification

The notebooks do **not** need to call Gemma.

Gemma should be called from the Streamlit app because that is where the user interaction happens.

## Gemma Input

Each tab sends:

```text
- tab name
- dataset name
- selected user inputs
- selected constraints
- visible metrics
- top features
- predicted probabilities
```

## Gemma Output

```text
- biological interpretation
- what the condition resembles
- why output changed
- information-theoretic interpretation
- suggested next experiment
```

---

# 9. Validation Requirements

Before final demo, verify:

```text
- Each notebook runs independently
- Each notebook exports expected CSV names
- Each CSV has required columns
- Streamlit app runs without CSVs
- Streamlit app runs with real CSVs
- All five tabs render correctly
- Gemma placeholder can be replaced cleanly
```

---

# 10. Why This Wiring Approach Is Best

This avoids over-engineering.

```text
Bad approach:
Streamlit calls notebooks directly

Good approach:
Notebooks export CSVs; Streamlit consumes CSVs
```

Benefits:

```text
- Easy to debug
- Easy to explain to judges
- Reproducible
- Works on Kaggle
- Works locally
- App remains deployable
- Stronger technical credibility
```

Final system story:

> BioChannel uses reproducible Kaggle notebooks for biological data preparation and information-theoretic analysis, then exposes those processed outputs through an interactive Streamlit dashboard powered by Gemma explanations.
