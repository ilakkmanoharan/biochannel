# BioChannel Specification

## Product

**BioChannel** is a Gemma-powered scientific dashboard that models cells as noisy communication channels.

It lets users explore:

```text
Signal input → noisy biological pathway → cellular response → decision outcome
```

The product is built as one unified app with **separate top-level tabs**, not a mode dropdown.

---

## Core Architecture

```text
Kaggle Notebooks
    ↓
Download public datasets
    ↓
Preprocess + compute metrics
    ↓
Export CSV files
    ↓
Streamlit App
    ↓
Interactive simulation + visualization
    ↓
Gemma explanation layer
```

---

## Main App Tabs

```text
Tab 1: Cell Decision Simulator
Tab 2: Information Loss Analyzer
Tab 3: Drug Response Predictor
Tab 4: Explainable Cell AI
Tab 5: Edge Biology Assistant
```

---

## Folder Structure

```text
BioChannel/
│
├── notebooks/
│   ├── 01_cell_decision_simulator.ipynb
│   ├── 02_information_loss_analyzer.ipynb
│   ├── 03_drug_response_predictor.ipynb
│   ├── 04_explainable_cell_ai.ipynb
│   └── 05_edge_biology_assistant.ipynb
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── src/
│   │   └── data_loader.py
│   │
│   └── data/
│       └── processed/
│           ├── cell_decision_pca.csv
│           ├── cell_top_features.csv
│           ├── info_metrics.csv
│           ├── info_timeseries.csv
│           ├── drug_response_processed.csv
│           ├── explain_feature_importance.csv
│           ├── explain_class_mapping.csv
│           └── edge_small_expression.csv
│
└── README.md
```

---

# 1. Kaggle Notebook Layer

Each notebook is responsible for one BioChannel module.

## Notebook Responsibilities

```text
- Download or load public dataset
- Clean dataset
- Preprocess biological features
- Compute module-specific outputs
- Export processed CSV files
```

The notebooks export files to:

```text
/kaggle/working/processed/
```

Then the user downloads the CSV files and places them in:

```text
app/data/processed/
```

---

# 2. Streamlit App Layer

The Streamlit app loads processed CSV files from:

```text
app/data/processed/
```

If a file is missing, the app uses demo fallback data.
This ensures the app always runs.

---

# 3. Module Specifications

## Tab 1: Cell Decision Simulator

### Goal

Simulate how cells respond to biological signals, stress, drugs, and noise.

### Dataset

Gene expression / RNA-seq dataset.

### Notebook

```text
01_cell_decision_simulator.ipynb
```

### Exported Files

```text
cell_decision_pca.csv
cell_top_features.csv
```

### Processing

```text
- Load gene expression data
- Select numeric gene-expression columns
- Clean missing values
- Apply log1p normalization
- Select top variable genes
- Run PCA
- Export PC1, PC2, and cell state labels
```

### App Inputs

```text
Signal type:
- Nutrient stress
- Drug signal
- Growth signal
- Immune signal
- Oxidative stress

Sliders:
- Signal strength
- Noise level
- Stress level
- Drug pressure
- Resistance pressure

Constraints:
- None
- Maximize survival
- Maximize apoptosis
- Minimize resistance
- Stable response
- Fast response
```

### App Outputs

```text
- PCA cell-state landscape
- Proliferation probability
- Apoptosis probability
- Dormancy probability
- Resistance probability
- Top dataset features
- Gemma explanation
```

---

## Tab 2: Information Loss Analyzer

### Goal

Measure how much biological signal information survives noisy signal transduction.

### Dataset

Time-series gene expression dataset.

### Notebook

```text
02_information_loss_analyzer.ipynb
```

### Exported Files

```text
info_metrics.csv
info_timeseries.csv
```

### Processing

```text
- Load time-series expression data
- Identify input signal proxy
- Identify pathway response proxy
- Discretize input and output
- Compute entropy
- Compute mutual information
- Compute signal fidelity
- Compute information loss
```

### App Inputs

```text
Input signal:
- Low stimulus
- Medium stimulus
- High stimulus
- Pulsed stimulus
- Gradual ramp

Noise source:
- Intrinsic molecular noise
- Extrinsic cell-to-cell variability
- Crosstalk
- Feedback instability

Slider:
- Noise level

Constraints:
- Maximize information transfer
- Minimize noise
- Maximize robustness
- Preserve response diversity
```

### App Outputs

```text
- Input entropy
- Mutual information
- Signal fidelity
- Information loss
- Input vs pathway response chart
- Information preservation chart
- Gemma explanation
```

---

## Tab 3: Drug Response Predictor

### Goal

Predict how drug-like interventions shift cells toward survival, apoptosis, or resistance.

### Dataset

GDSC / drug response dataset.

### Notebook

```text
03_drug_response_predictor.ipynb
```

### Exported File

```text
drug_response_processed.csv
```

### Processing

```text
- Load drug response dataset
- Detect cell line column
- Detect drug column
- Detect response / IC50 / sensitivity column
- Normalize response
- Convert response into sensitivity score
- Derive resistance risk
- Derive apoptosis proxy
- Derive survival proxy
```

### App Inputs

```text
Dropdowns:
- Cell line
- Drug
- Treatment duration

Sliders:
- Drug dose
- Resistance pressure

Constraints:
- Maximize apoptosis
- Minimize resistance
- Reduce toxicity
- Preserve normal-like cells
- Maximize signal clarity
```

### App Outputs

```text
- Dataset sensitivity score
- Predicted apoptosis
- Resistance risk
- Dose-response curve
- Gemma explanation
```

---

## Tab 4: Explainable Cell AI

### Goal

Use dataset-derived features and Gemma explanations to explain cellular variability and decision pathways.

### Dataset

Breast cancer / classification dataset.

### Notebook

```text
04_explainable_cell_ai.ipynb
```

### Exported Files

```text
explain_feature_importance.csv
explain_class_mapping.csv
```

### Processing

```text
- Load classification dataset
- Identify target label
- Train Random Forest classifier
- Extract feature importances
- Export top explanatory features
- Export class mapping
```

### App Inputs

```text
Active dataset context:
- Gene Expression Cancer RNA-seq
- Single-cell RNA-seq
- Time-series gene expression
- Drug response dataset
- Small edge dataset

Explanation level:
- High school student
- Biology researcher
- Investor / judge
- Software engineer

User question:
- Free-text question box
```

### App Outputs

```text
- Top feature importance chart
- Gemma explanation
- Suggested learning prompts
```

---

## Tab 5: Edge Biology Assistant

### Goal

Show a lightweight, local-first version of BioChannel for education and low-resource settings.

### Dataset

Small gene expression dataset.

### Notebook

```text
05_edge_biology_assistant.ipynb
```

### Exported File

```text
edge_small_expression.csv
```

### Processing

```text
- Load small gene expression dataset
- Select numeric columns
- Clean and normalize
- Create smaller subset
- Run PCA
- Export lightweight cell-state landscape
```

### App Inputs

```text
Edge mode:
- Small dataset mode
- Educational mode
- Offline simulation mode

Local model target:
- Gemma via Ollama
- Gemma via LiteRT
- Small fallback explainer

Sliders:
- Signal strength
- Noise level
```

### App Outputs

```text
- Small edge dataset PCA landscape
- Lightweight decision probabilities
- Local-first explanation placeholder
- Suggested learning prompts
```

---

# 4. Data Handoff Specification

## Notebook Output Location

```text
/kaggle/working/processed/
```

## App Input Location

```text
app/data/processed/
```

## Required CSVs

```text
cell_decision_pca.csv
cell_top_features.csv
info_metrics.csv
info_timeseries.csv
drug_response_processed.csv
explain_feature_importance.csv
explain_class_mapping.csv
edge_small_expression.csv
```

## Fallback Behavior

If any CSV is missing:

```text
- App does not crash
- App loads synthetic demo data
- User can still test UI and demo flow
```

---

# 5. Gemma Layer Specification

## Current Implementation

The current app includes a placeholder function:

```text
gemma_placeholder()
```

## Final Implementation

Replace placeholder with Gemma 4 inference.

### Gemma Input

```text
- Active tab/module
- Selected dataset
- User-selected biological inputs
- Constraint selection
- Computed model outputs
- Dataset-derived features
- Information metrics
```

### Gemma Output

```text
- Biological explanation
- What the condition resembles
- Why the output changed
- What the user should learn
- Suggested next experiment
```

### Example Prompt Shape

```text
You are BioChannel, a scientific reasoning assistant.

Explain the current simulation using:
- module
- signal type
- signal strength
- noise level
- constraint
- computed probabilities
- mutual information metrics
- top dataset features

Avoid medical advice. Keep the explanation grounded in the data.
```

---

# 6. Core Scientific Model

BioChannel uses the idea:

```text
External biological signal = input
Cellular pathway = noisy communication channel
Gene expression / drug response = output
Cell fate = decision
```

## Information Metrics

```text
Entropy:
Measures uncertainty in the input or output.

Mutual information:
Measures how much information about the input is preserved in the output.

Signal fidelity:
mutual information / input entropy

Information loss:
1 - signal fidelity
```

## Cell Decision Model

The Streamlit app uses a lightweight softmax decision model:

```text
Inputs:
- signal strength
- noise level
- stress level
- drug pressure
- resistance pressure

Outputs:
- proliferation
- apoptosis
- dormancy
- resistance
```

---

# 7. UI Specification

## Global UI

```text
Title:
BioChannel

Subtitle:
Cells as noisy communication channels: signals in, biological decisions out.

Navigation:
Top-level tabs, not dropdowns
```

## Each Tab Contains

```text
Left panel:
- dataset / biological inputs
- sliders
- constraints
- local controls

Right panel:
- metrics
- plots
- Gemma explanation button
- learning cards
```

## Learning Cards

Each tab has clickable educational prompts such as:

```text
- What is mutual information?
- Why does noise change cell fate?
- What is a dose-response curve?
- Why do cells become drug resistant?
- What can run on a small device?
```

---

# 8. Tech Stack

```text
Frontend:
- Streamlit

Visualization:
- Plotly

Data:
- Kaggle public datasets
- CSV handoff

Modeling:
- Python
- Pandas
- NumPy
- scikit-learn

Information Theory:
- sklearn.metrics.mutual_info_score
- custom entropy calculations

AI Explanation:
- Gemma 4
- Optional local deployment via Ollama / LiteRT

Deployment:
- Streamlit Community Cloud
- Hugging Face Spaces
- Kaggle Notebook demo
- GitHub public repository
```

---

# 9. How to Run

## Run Notebooks

Upload notebooks to Kaggle and run them.

Outputs are saved to:

```text
/kaggle/working/processed/
```

Download those files.

## Run App

Place downloaded CSVs into:

```text
app/data/processed/
```

Then:

```bash
cd app
pip install -r requirements.txt
streamlit run app.py
```

---

# 10. Hackathon Positioning

BioChannel should be submitted as:

```text
Track:
Health & Sciences

Optional Special Track:
Ollama or LiteRT, if Gemma runs locally
```

## Submission Story

> BioChannel is a Gemma-powered biology dashboard that helps users understand how cells process signals, lose information under noise, and make decisions such as proliferation, apoptosis, dormancy, or resistance.

## Why It Is Strong

```text
- Uses real public biological datasets
- Has reproducible Kaggle notebooks
- Provides interactive scientific simulation
- Uses information theory as a unique scientific foundation
- Uses Gemma as the explanation and reasoning layer
- Demonstrates real-world value in biology education, drug response, and systems biology
```
