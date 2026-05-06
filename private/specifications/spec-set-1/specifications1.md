# BioChannel — Complete Build Specification

**Project tagline:**
**BioChannel: An interactive AI dashboard for exploring how cells transmit information, lose signal fidelity, and make decisions under biological noise.**

BioChannel should feel like a **scientific simulation cockpit**: users choose a biological mode, adjust inputs and constraints, see visual outputs update, and receive Gemma-powered explanations about what the selected condition resembles biologically.

This is strongly aligned with the hackathon’s **Health & Sciences** track, which rewards tools that bridge humans and data and democratize scientific knowledge . It also directly builds on your information-theoretic framing of cells as noisy communication channels .

---

# 1. Product Overview

## Product Name

**BioChannel**

## One-line description

**BioChannel lets users simulate cellular decision-making by treating biological signals as noisy communication channels.**

## Core user experience

The user can:

1. Select a module from a dropdown.
2. Select a dataset or biological condition.
3. Adjust biological inputs using sliders, dropdowns, and constraint buttons.
4. See updated plots and predicted cellular outcomes.
5. Read an AI explanation from Gemma.
6. Click suggested learning cards to explore related biological concepts.

---

# 2. Main Modules

## Module 1: Cell Decision Simulator

### Purpose

Simulate how cells respond to stress, nutrient changes, cancer state, or drug-like signals.

### Dataset

Use:

[https://www.kaggle.com/datasets/uciml/gene-expression-cancer-rna-seq](https://www.kaggle.com/datasets/uciml/gene-expression-cancer-rna-seq)

or single-cell RNA-seq if easier to preprocess:

[https://www.kaggle.com/datasets/allen-institute-for-cell-science/single-cell-rna-seq-data](https://www.kaggle.com/datasets/allen-institute-for-cell-science/single-cell-rna-seq-data)

### Inputs shown in frontend

```text
Dataset selector:
- Gene Expression Cancer RNA-seq
- Single-cell RNA-seq sample

Signal type:
- Nutrient stress
- Drug signal
- Growth signal
- Immune signal
- Oxidative stress

Signal strength:
- Slider: 0.0 to 1.0

Noise level:
- Slider: 0.0 to 1.0

Cell state:
- Normal-like
- Cancer-like
- Stressed
- Resistant
- Dormant

Constraint buttons:
- High noise
- Low energy
- Drug pressure
- Fast response
- Stable response
- Maximize survival
- Maximize apoptosis
```

### Outputs

```text
Visual outputs:
- PCA or UMAP-style cluster plot
- Predicted decision probability chart
- Signal-to-response curve
- Noise impact plot

Predicted cell decisions:
- Proliferation probability
- Apoptosis probability
- Dormancy probability
- Stress adaptation probability
- Resistance probability
```

### Gemma explanation

Every time values change, Gemma explains:

```text
- What the selected condition resembles biologically
- Why the predicted decision changed
- Whether the result suggests signal preservation or signal loss
- What biological interpretation the user should take away
```

Example:

> This input resembles a high-stress, high-noise cellular environment. The model predicts increased dormancy because strong noise reduces the reliability of the growth signal, making the cell more likely to enter a protective state rather than commit to proliferation.

---

## Module 2: Information Loss Analyzer

### Purpose

Quantify how much information is preserved or lost between input signal and output response.

This directly matches your research objective: measuring how effectively cellular signaling pathways transmit information under biological noise .

### Dataset

Use:

[https://www.kaggle.com/datasets/soham1024/gene-expression-time-series](https://www.kaggle.com/datasets/soham1024/gene-expression-time-series)

Alternative:

[https://www.ncbi.nlm.nih.gov/geo/](https://www.ncbi.nlm.nih.gov/geo/)

### Inputs shown in frontend

```text
Input signal:
- Low stimulus
- Medium stimulus
- High stimulus
- Pulsed stimulus
- Gradual ramp

Output marker:
- Gene expression response
- Pathway activation score
- Cell state probability
- Synthetic reporter output

Noise source:
- Intrinsic molecular noise
- Extrinsic cell-to-cell variability
- Crosstalk
- Feedback instability

Noise level:
- Slider: 0.0 to 1.0

Information metric:
- Entropy
- Mutual information
- Channel capacity approximation
- Signal fidelity score

Constraint:
- Maximize information transfer
- Minimize noise
- Maximize robustness
- Preserve response diversity
```

### Outputs

```text
Metrics:
- Input entropy
- Output entropy
- Approximate mutual information
- Information loss percentage
- Signal fidelity score

Visuals:
- Input vs output distribution
- Information loss bar chart
- Noise vs fidelity curve
- Channel capacity approximation
```

### Gemma explanation

Gemma explains:

```text
- Whether information is preserved or lost
- Which noise source is most damaging
- What the result means biologically
- How the user could improve signal fidelity
```

Example:

> This setup resembles a pathway where the input signal is strong but the output remains uncertain. The likely cause is extrinsic variability, meaning different cells respond differently even under the same stimulus. The information loss is high because the output no longer reliably identifies the original input.

---

## Module 3: Drug Response Predictor

### Purpose

Predict how cells respond to drug-like interventions and explain whether the intervention improves or disrupts cellular decision-making.

### Dataset

Use:

[https://www.kaggle.com/datasets/ghazaleh/gdsc-drug-response](https://www.kaggle.com/datasets/ghazaleh/gdsc-drug-response)

Alternative:

[https://www.kaggle.com/datasets/cdc/drug-response-prediction](https://www.kaggle.com/datasets/cdc/drug-response-prediction)

### Inputs shown in frontend

```text
Cell line selector:
- Cancer cell line A
- Cancer cell line B
- Resistant-like profile
- Sensitive-like profile

Drug selector:
- Drug 1
- Drug 2
- Drug 3
- Combination therapy

Drug dose:
- Slider: 0.0 to 1.0

Treatment duration:
- Short
- Medium
- Long

Resistance pressure:
- Slider: 0.0 to 1.0

Constraint:
- Maximize apoptosis
- Minimize resistance
- Reduce toxicity
- Preserve normal-like cells
- Maximize signal clarity
```

### Outputs

```text
Predictions:
- Drug sensitivity score
- Resistance probability
- Apoptosis probability
- Survival probability
- Recommended intervention direction

Visuals:
- Dose-response curve
- Predicted survival chart
- Resistance risk meter
- Intervention ranking
```

### Gemma explanation

Gemma explains:

```text
- Why the selected drug condition produces the predicted outcome
- Whether the cell appears sensitive or resistant
- How noise may affect drug response
- What alternative intervention may improve the outcome
```

Example:

> This condition resembles partial drug resistance. The drug signal is strong, but the response remains weak, suggesting the pathway may be losing information downstream. A combination strategy or longer treatment window may improve decision pressure toward apoptosis.

---

## Module 4: Explainable Cell AI

### Purpose

Let users ask questions about the simulation, dataset, or biological interpretation.

### Dataset

Use the same dataset currently active in the selected module.

### Frontend inputs

```text
Question box:
- Why did apoptosis increase?
- Why did information loss rise?
- What does high noise mean?
- Which genes are driving this state?
- What condition is this similar to?

Suggested question buttons:
- Explain this result simply
- Explain like I am a high school student
- Explain like a biology researcher
- What changed from the previous input?
- What should I try next?
```

### Outputs

```text
AI explanation:
- Short answer
- Biological interpretation
- Data-based evidence
- Suggested next experiment
```

---

## Module 5: Edge Biology Assistant

### Purpose

Show that BioChannel can run locally or in low-resource settings.

This helps position the project for the hackathon’s local-first / edge-AI technology tracks.

### Dataset

Use a small subset from:

[https://www.kaggle.com/datasets/mehranksingh/gene-expression](https://www.kaggle.com/datasets/mehranksingh/gene-expression)

### Frontend inputs

```text
Mode:
- Lightweight local demo
- Small dataset mode
- Educational mode

Question type:
- Explain a gene expression pattern
- Simulate simple signal response
- Compare two biological states
```

### Outputs

```text
- Small simulation result
- Lightweight explanation
- Offline-friendly learning summary
```

---

# 3. Recommended Final App Structure

```text
BioChannel/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── simulation.py
│   ├── info_theory.py
│   ├── prediction.py
│   ├── gemma_explainer.py
│   ├── suggestions.py
│   └── visualization.py
│
├── pages/
│   ├── 1_Cell_Decision_Simulator.py
│   ├── 2_Information_Loss_Analyzer.py
│   ├── 3_Drug_Response_Predictor.py
│   ├── 4_Explainable_Cell_AI.py
│   └── 5_Edge_Biology_Assistant.py
│
└── assets/
    ├── logo.png
    ├── cover.png
    └── demo_images/
```

---

# 4. Tech Stack

```text
Frontend:
- Streamlit
- streamlit-option-menu
- Plotly
- Altair or Matplotlib

Backend / Modeling:
- Python
- Pandas
- NumPy
- SciPy
- scikit-learn

Dimensionality Reduction:
- PCA from scikit-learn
- UMAP optional using umap-learn

Information Theory:
- scipy.stats
- sklearn.metrics.mutual_info_score
- custom entropy functions
- optional: npeet or kNN-based MI estimator

AI Layer:
- Gemma 4 through Kaggle / Google AI Studio / local Ollama depending on setup
- Prompt templates for biological explanation
- Structured JSON responses from Gemma

Deployment:
- Streamlit Community Cloud
- Hugging Face Spaces
- Kaggle Notebook demo
- Optional Docker deployment

Repository:
- GitHub public repo
```

---

# 5. Core Data Processing Pipeline

## Step 1: Load dataset

```text
Input:
- Gene expression matrix
- Labels if available
- Drug response values if available
- Time-series conditions if available

Output:
- Clean dataframe
- Feature matrix X
- Labels y
- Metadata
```

## Step 2: Normalize

```text
Methods:
- log1p transform
- StandardScaler
- remove missing values
- optional top variable gene selection
```

## Step 3: Reduce dimensions

```text
Use:
- PCA for fast build
- UMAP if time permits

Output:
- 2D coordinates for visualization
```

## Step 4: Build simulation layer

```text
Inputs:
- signal_strength
- noise_level
- cell_state
- constraint

Simulation:
- create probabilistic cell decision model
- perturb expression scores based on noise
- compute decision probabilities
```

## Step 5: Compute information metrics

```text
Metrics:
- entropy(input)
- entropy(output)
- mutual_information(input, output)
- information_loss = 1 - MI / entropy(input)
- signal_fidelity = MI / entropy(input)
```

## Step 6: Generate Gemma explanation

```text
Inputs sent to Gemma:
- selected module
- selected dataset
- signal type
- signal strength
- noise level
- constraint
- model output
- top changed genes/features
- information metrics

Output:
- explanation
- biological analogy
- next suggestions
- safety caveat
```

---

# 6. Frontend Layout

## Main landing page

```text
Header:
BioChannel
Cellular signals as noisy communication channels

Subtitle:
Explore how cells process signals, lose information, and make decisions under uncertainty.

Main dropdown:
Select Mode:
- Cell Decision Simulator
- Information Loss Analyzer
- Drug Response Predictor
- Explainable Cell AI
- Edge Biology Assistant

Sidebar:
- Dataset selector
- Module-specific controls
- Constraint buttons
- Reset button
- Run simulation button

Main Panel:
- Simulation summary card
- Plots
- Prediction outputs
- Gemma explanation
- Suggested next actions
```

---

# 7. UI Interaction Behavior

Every time the user changes:

```text
- mode
- dataset
- signal type
- signal strength
- noise level
- cell state
- constraint
- drug dose
- treatment duration
```

The app should update:

```text
1. Computed model output
2. Visualization
3. Information metrics
4. Gemma explanation
5. Clickable suggestions
```

To avoid slow response:

```text
- update plots instantly
- call Gemma only when user clicks “Explain with Gemma”
- optionally add “Auto-explain” toggle
```

---

# 8. Suggested Learning Cards

Each module should show related clickable suggestions.

## Cell Decision Simulator suggestions

```text
- What does dormancy mean?
- Why do cells choose apoptosis?
- What is cellular noise?
- What is signal transduction?
- Why do cancer cells resist signals?
```

## Information Loss suggestions

```text
- What is mutual information?
- What is channel capacity?
- Why does noise reduce fidelity?
- What is intrinsic vs extrinsic noise?
- How do feedback loops affect information flow?
```

## Drug Response suggestions

```text
- Why do cells become drug resistant?
- What is a dose-response curve?
- What does apoptosis probability mean?
- How can combination therapy improve response?
```

## Edge Assistant suggestions

```text
- How can biology AI run locally?
- Why does offline AI matter for science education?
- How can students use gene expression data?
```

---

# 9. Gemma Prompt Template

Use structured prompting.

```text
You are BioChannel, an AI biology reasoning assistant.

The user is exploring a cellular signaling simulation.

Module:
{module_name}

Dataset:
{dataset_name}

Selected inputs:
- Signal type: {signal_type}
- Signal strength: {signal_strength}
- Noise level: {noise_level}
- Cell state: {cell_state}
- Constraint: {constraint}

Computed outputs:
- Proliferation probability: {proliferation}
- Apoptosis probability: {apoptosis}
- Dormancy probability: {dormancy}
- Resistance probability: {resistance}
- Mutual information: {mi}
- Information loss: {info_loss}
- Signal fidelity: {signal_fidelity}

Top features or genes:
{top_features}

Explain:
1. What biological condition this resembles.
2. Why the output changed.
3. What the user should learn.
4. One suggested next experiment.

Keep the answer clear, grounded, and avoid medical advice.
```

---

# 10. Modeling Specification

## Simple probabilistic model

For fast implementation, use a softmax-style scoring model.

```text
Inputs:
signal_strength = 0 to 1
noise_level = 0 to 1
drug_pressure = 0 to 1
stress_level = 0 to 1
resistance_pressure = 0 to 1

Scores:
proliferation_score = signal_strength - stress_level - drug_pressure
apoptosis_score = drug_pressure + stress_level - resistance_pressure
dormancy_score = stress_level + noise_level
resistance_score = resistance_pressure + noise_level + drug_pressure * 0.5

Apply softmax to convert scores into probabilities.
```

This is enough for a working demo.

Later, connect scores to real dataset clusters or labels.

---

# 11. Information Theory Specification

Implement:

```text
entropy(values):
    Discretize values into bins
    Compute probability distribution
    Return -sum(p * log2(p))

mutual_information(x, y):
    Discretize x and y
    Use sklearn.metrics.mutual_info_score
    Normalize by entropy(x)

information_loss:
    1 - normalized_mutual_information

signal_fidelity:
    normalized_mutual_information
```

---

# 12. Visualizations

Minimum required visuals:

```text
Cell Decision Simulator:
- PCA/UMAP scatter plot
- Decision probability bar chart
- Noise vs decision curve

Information Loss Analyzer:
- Input-output distribution plot
- Mutual information gauge
- Information loss chart

Drug Response Predictor:
- Dose-response curve
- Survival vs apoptosis chart
- Resistance risk meter

Explainable Cell AI:
- Explanation panel
- Suggested questions
- Top gene/feature importance chart
```

---

# 13. Kaggle Hackathon Positioning

## Track

**Health & Sciences**

## Optional special track

**Ollama** or **LiteRT**, if you run Gemma locally.

## Submission angle

BioChannel is not just a chatbot. It is:

```text
- an interactive simulation system
- a biological reasoning dashboard
- an information-theoretic learning tool
- a Gemma-powered scientific explainer
```

The competition requires a Kaggle writeup, public video, public code repository, live demo, and media gallery .

---

# 14. MVP Build Order

Build in this exact order:

```text
Day 1:
- Streamlit shell
- Mode dropdown
- Sidebar inputs
- Load one gene expression dataset

Day 2:
- PCA plot
- Cell decision probability model
- Decision probability chart

Day 3:
- Entropy + mutual information functions
- Information loss analyzer page

Day 4:
- Drug response page
- Dose-response curve
- Resistance probability

Day 5:
- Gemma explanation layer
- Suggested learning cards

Day 6:
- Polish UI
- Add README
- Record demo video
- Write Kaggle submission
```

---

# 15. Final Product Story

Use this as the core pitch:

> BioChannel turns cellular signaling into an interactive communication-channel dashboard. Users can explore how biological signals pass through noisy cellular systems, how much information is preserved or lost, and how those changes influence cell decisions such as proliferation, apoptosis, dormancy, or resistance. Gemma acts as the scientific reasoning layer, translating simulations and biological data into clear explanations and suggested next experiments.

This is the right scope: ambitious enough to feel original, but small enough to build fast.
