# BioChannel Kaggle Notebooks

The `biochannel_kaggle_notebooks_v2` folder contains five Kaggle-ready notebooks for the BioChannel project.

## Notebooks

1. `01_cell_decision_simulator.ipynb`
   - Uses RNA-seq/single-cell-like expression data.
   - Exports PCA coordinates and a lightweight decision model output.

2. `02_information_loss_analyzer.ipynb`
   - Uses time-series gene-expression data.
   - Computes entropy, mutual information, signal fidelity, and information loss.

3. `03_drug_response_predictor.ipynb`
   - Uses drug-response data such as GDSC.
   - Exports cleaned drug/cell-line response summaries.

4. `04_explainable_cell_ai.ipynb`
   - Uses cancer/classification-style data.
   - Trains a simple random forest and exports feature importance for Gemma explanations.

5. `05_edge_biology_assistant.ipynb`
   - Uses a small gene-expression dataset.
   - Exports small files for local-first/edge demo mode.

## How to use on Kaggle

1. Create a new Kaggle Notebook.
2. Upload or import one of these `.ipynb` files.
3. Click **Add Data** and attach the relevant Kaggle dataset.
4. Run all cells.
5. Download files from `/kaggle/working/processed/`.
6. Copy those files into the Streamlit app under `data/processed/`.

Each notebook includes fallback synthetic/demo data so the notebook can run even before the real dataset is attached. Replace the inferred columns with exact dataset-specific column names once you inspect the attached dataset.
