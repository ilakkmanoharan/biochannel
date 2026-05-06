## Revised Specification: Mode Tabs Page as Tag-Style Scientific Workspace

### Goal

Create one complete **Mode Tabs page** where every mode appears as a large rounded pill, similar to the TagScribe tags screen.

This page should allow Decision Biology to keep growing as we add:

```text
- new datasets
- new analysis modes
- new notebook outputs
- new Gemma explanations
- new ways to explore the same dataset
```

---

# 1. Page Concept

The Mode Tabs page should feel like a **scientific mode launcher**.

Instead of using a dropdown or narrow horizontal tabs, every mode is shown as a **rounded chip / pill button** on one page.

Users can tap a mode to open that experiment.

---

# 2. Visual Style

Use the TagScribe-style layout:

```text
Large title at top
Short explanatory subtitle
Rounded mode pills arranged in flexible rows
Clean white background
Soft gray pill backgrounds
Selected mode highlighted
Settings / configuration icon in top-right
Bottom navigation optional
```

Example page title:

```text
Modes
```

Example subtitle:

```text
Explore Decision Biology through datasets, simulations, information-flow models, perturbations, and Gemma-powered biological interpretations. Tap a mode to open an experiment.
```

---

# 3. Page Layout

```text
--------------------------------------------------
Top Bar
    - Optional settings/config icon

Main Header
    - "Modes"
    - Short description

Mode Pill Grid
    - Cell Decision Simulator
    - Cancer Expression
    - Information Flow
    - Perturbation Layer
    - CRISPR Designer
    - Trajectory Analysis
    - Pathway Explorer
    - Noise Simulator
    - Drug Response
    - Future modes...

Selected Mode Detail Panel
    - Dataset overview
    - Notebook status
    - Visualizations
    - Metrics
    - Gemma explanation
    - Open / Run / Download actions
--------------------------------------------------
```

---

# 4. Mode Pills

Each mode should appear as a rounded pill:

```text
Cell Decision Simulator
Cancer Expression
Information Flow
Perturbation Layer
CRISPR Designer
```

Pill behavior:

```text
Default state:
- light gray background
- black text

Selected state:
- blue or darker highlighted pill
- white text

Disabled / unavailable state:
- lighter gray
- muted text
- optional "coming soon" label
```

---

# 5. No Dropdowns

Important requirement:

```text
Modes must NOT be shown in a dropdown.
Modes must NOT be hidden behind a small tab bar.
Modes must be visible as tappable pills on one page.
```

Reason:

```text
The app should support discovery.
Users should see all available scientific modes at once.
As we add more datasets and experiments, the page should grow naturally like a tag library.
```

---

# 6. Config-Driven Mode System

Modes should be generated from a configuration file.

### `modes_config.json`

```json
[
  {
    "id": "cell_decision_simulator",
    "title": "Cell Decision Simulator",
    "dataset": "single_cell_rna_seq",
    "category": "Single-cell",
    "status": "ready",
    "notebook_output": "outputs/gemma_cell_decision_summary.json",
    "description": "Simulate how cells respond to stress signals and choose survival, dormancy, proliferation, or apoptosis."
  },
  {
    "id": "cancer_expression",
    "title": "Cancer Expression",
    "dataset": "cancer_rna_seq",
    "category": "Cancer",
    "status": "ready",
    "notebook_output": "outputs/gemma_cancer_expression_summary.json",
    "description": "Compare normal and cancer expression profiles to understand altered cellular decision logic."
  },
  {
    "id": "information_flow",
    "title": "Information Flow",
    "dataset": "single_cell_rna_seq",
    "category": "Information Theory",
    "status": "ready",
    "notebook_output": "outputs/gemma_signaling_information_summary.json",
    "description": "Measure how much biological signal is preserved through noisy cellular pathways."
  }
]
```

---

# 7. Dynamic Rendering

The UI should read `modes_config.json` and render all modes automatically.

Adding a new mode should only require:

```text
1. Add a new notebook or analysis output
2. Add one object to modes_config.json
3. Restart the app
4. New pill appears automatically
```

No page redesign should be needed.

---

# 8. Streamlit UI Skeleton

```python
import streamlit as st
import json

st.set_page_config(
    page_title="Decision Biology Modes",
    layout="wide"
)

def load_modes():
    with open("modes_config.json", "r") as f:
        return json.load(f)

modes = load_modes()

st.markdown("# Modes")
st.markdown(
    "Explore Decision Biology through datasets, simulations, information-flow models, "
    "perturbations, and Gemma-powered biological interpretations. Tap a mode to open an experiment."
)

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = modes[0]["id"]

st.markdown("### Explore Modes")

cols = st.columns(4)

for index, mode in enumerate(modes):
    col = cols[index % 4]

    with col:
        is_selected = st.session_state.selected_mode == mode["id"]

        button_label = mode["title"]

        if st.button(button_label, key=mode["id"]):
            st.session_state.selected_mode = mode["id"]

selected_mode = next(
    mode for mode in modes
    if mode["id"] == st.session_state.selected_mode
)

st.divider()

st.subheader(selected_mode["title"])
st.write(selected_mode["description"])
```

---

# 9. Custom Pill Styling Requirement

The implementation should include custom CSS so Streamlit buttons look like TagScribe pills:

```text
- rounded corners
- soft gray background
- large readable text
- generous horizontal padding
- flexible wrapping
- mobile-friendly spacing
```

Desired look:

```text
[ Cell Decision Simulator ] [ Cancer Expression ] [ Information Flow ]
[ Perturbation Layer ] [ CRISPR Designer ] [ Pathway Explorer ]
```

---

# 10. Selected Mode Detail Area

When a user taps a mode pill, the lower part of the page should update.

Each selected mode detail section should include:

```text
1. Mode title
2. Dataset overview
3. Science explanation
4. Notebook output status
5. Visualization placeholder
6. Metrics / results
7. Gemma interpretation
8. Export buttons
```

---

# 11. Gemma Explanation Panel

Each selected mode should show Gemma output if available.

```python
def render_gemma_panel(mode):
    st.subheader("Gemma Interpretation")

    try:
        with open(mode["notebook_output"], "r") as f:
            data = json.load(f)

        st.write(data.get("gemma_response", "No Gemma response found."))

    except FileNotFoundError:
        st.warning("Gemma explanation is not available yet for this mode.")
```

---

# 12. Mode Growth Strategy

The page should support many future modes, for example:

```text
Cell Decision Simulator
Cancer Expression
Information Flow
Perturbation Layer
CRISPR Designer
Trajectory Analysis
Pathway Explorer
Noise Simulator
Drug Response
Stress Response
Single-Cell Clustering
Gene Module Discovery
Pseudotime Explorer
Cell Fate Predictor
Synthetic Circuit Builder
OmniPath Explorer
LINCS Perturbation Explorer
```

The layout should wrap naturally like a tag cloud.

---

# 13. Optional Search

Because the number of modes may grow, add a search field later:

```text
Search modes by:
- title
- dataset
- category
- biological process
- analysis type
```

Example:

```python
search = st.text_input("Search modes")

filtered_modes = [
    mode for mode in modes
    if search.lower() in mode["title"].lower()
    or search.lower() in mode["category"].lower()
]
```

---

# 14. Optional Category Filters

Later, add category chips:

```text
All
Single-cell
Cancer
Information Theory
Perturbation
CRISPR
Pathways
Simulation
```

This should also use pill-style buttons, not dropdowns.

---

# 15. Bottom Navigation

Optional bottom navigation can include:

```text
Workspace
Datasets
Modes
Notebooks
More
```

For Streamlit, this can be approximated with sidebar navigation or page links.

---

# 16. Final Positioning

This page should be designed as:

```text
A TagScribe-style mode library for Decision Biology.
```

It should make the app feel expandable, visual, and exploratory.

The user should immediately understand:

```text
Each pill is a scientific experiment.
Each experiment is powered by a dataset.
Each dataset can generate multiple modes.
Each mode can connect to notebook outputs and Gemma explanations.
```
