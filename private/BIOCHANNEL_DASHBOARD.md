# BioChannel dashboard

End-to-end Streamlit dashboard: Kaggle notebooks produce CSVs; the app loads them and falls back to in-memory demo data if a file is missing or invalid (see `private/specifications/spec-set-2/`).

## What was built

A single **Streamlit** app with five **mode pills** (no dropdown), driven by `modes_config.json` at the project root.

| Piece | Role |
|--------|------|
| `app.py` | Mode pills, sidebar controls, Plotly charts, learning cards, Gemma/Gemini hook |
| `modes_config.json` | Mode `id`, `title`, `description`, `category`, `status`, `dataset` — add a mode by appending an object and restarting |
| `src/data_loader.py` | Canonical CSV loaders; validates columns; **synthetic in-memory** fallbacks (no crash) |
| `src/simulation.py` | Softmax decision model; stress / drug-pressure / resistance sliders |
| `src/info_theory.py` | Binned entropy, MI, fidelity, loss, capacity approximation |
| `src/prediction.py` | Drug outcomes; optional row blend from `drug_response_processed.csv` |
| `src/gemma_explainer.py` | Structured prompt + template text; optional **`GOOGLE_API_KEY`** → Gemini |
| `src/visualization.py` | Plotly figures (including PCA with string `cell_state` / `edge_state` labels) |
| `src/suggestions.py` | Per-module learning bullets |

## Processed data (`data/processed/`)

Place notebook exports here (from `/kaggle/working/processed/` or your local run). Use these **exact filenames**; schemas match `specifications9.md` in spec-set-2.

| File | Used for | Key columns |
|------|-----------|-------------|
| `cell_decision_pca.csv` | Cell Decision — scatter | `PC1`, `PC2`, `cell_state` |
| `cell_top_features.csv` | Cell Decision — table | `feature`, `variance` |
| `info_timeseries.csv` | Information Loss — traces | `time`, `input_signal`, `pathway_response` |
| `info_metrics.csv` | Information Loss — optional baseline row | `input_entropy_bits`, `output_entropy_bits`, `mutual_information_bits`, `signal_fidelity`, `information_loss` |
| `drug_response_processed.csv` | Drug — dropdowns + row blend | `cell_line`, `drug`, `sensitivity`, `resistance_risk`, `apoptosis_proxy`, `survival_proxy` |
| `explain_feature_importance.csv` | Explainable — bar chart | `feature`, `importance` |
| `explain_class_mapping.csv` | Explainable — expander | `class`, `encoded_value` |
| `edge_small_expression.csv` | Edge — PCA | `PC1`, `PC2`, `edge_state` |

## `modes_config.json` (project root)

Each entry is a **mode** shown as a pill. Required for display: at least `id`, `title`, and `description` (other fields are optional metadata). Example:

```json
{
  "id": "cell_decision_simulator",
  "title": "Cell Decision Simulator",
  "dataset": "gene_expression_rna_seq",
  "category": "Simulation",
  "status": "ready",
  "description": "Simulate how cells respond to stress signals and noise; explore PCA landscape and decision probabilities."
}
```

The app embeds a minimal default if the file is missing or invalid.

## Run locally

From the project root (`bio-channel`):

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

Open the URL Streamlit prints (often **http://localhost:8501**).

## Optional Gemini explanations

The app uses **Google Gemini** when `GOOGLE_API_KEY` is set and `google-generativeai` is installed (both are listed in `requirements.txt`). Otherwise it uses on-device **template** text only — no crash.

### 1. Get an API key

1. Open [Google AI Studio](https://aistudio.google.com/apikey).
2. Sign in and create an API key (store it like any secret; do not commit it to git).

### 2. Configure the key (pick one)

**A — `.env` file (recommended)**  
The app loads `.env` from the project root next to `app.py` automatically.

```bash
cd /path/to/bio-channel
cp .env.example .env
# Edit .env and set: GOOGLE_API_KEY=your_actual_key_here
```

**B — Shell for one session**

```bash
export GOOGLE_API_KEY="your_actual_key_here"
.venv/bin/streamlit run app.py
```

### 3. Install / refresh dependencies

After pulling changes:

```bash
.venv/bin/pip install -r requirements.txt
```

### 4. Optional: model name

Default model is `gemini-2.0-flash`. Override with environment variable:

```bash
export BIOCHANNEL_GEMINI_MODEL=gemini-2.0-flash
```

### 5. Use it in the UI

In the sidebar under **AI explanation (Gemini)**:

- A **status** line shows whether the key and `google-generativeai` are ready.
- **Explain with Gemini / template** runs once.
- **Auto-explain on change** refreshes the explanation whenever inputs change (can increase API usage).

The main panel heading uses **`(gemini)`** or **`(template)`**. If it’s template, a short **caption** under the heading explains why (no key, missing package, or API error).

## Kaggle / notebooks

See `biochannel_kaggle_notebooks_v2/` (or your notebook bundle). Export CSVs into **`data/processed/`** with the names above; the app prefers those files over demos.

## Related specs

- **Legacy product notes:** `private/specifications/` (`README.md`, `specifications1.md`, …).
- **CSV handoff, tabs/pills, loaders:** `private/specifications/spec-set-2/` (`specifications7.md`–`specifications11.md`, `specifications9.md` for schemas).


Restart Streamlit to pick this up:
.venv/bin/streamlit run app.py
