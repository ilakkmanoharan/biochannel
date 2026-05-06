## Specification: Add Gemma into Kaggle Notebooks

### Goal

Each Kaggle notebook should include **Gemma as the AI explanation and reasoning layer** for the Decision Biology projects. The notebooks should not only train/process models, but also use Gemma to explain biological meaning, interpret results, summarize plots, and generate project-ready insights for the Streamlit app.

---

## 1. Gemma Integration Purpose

Gemma should be added to each notebook for:

```text
1. Explaining biological results in plain English
2. Interpreting model outputs
3. Summarizing UMAPs, clusters, gene-expression changes, and pathway signals
4. Generating hypotheses from the data
5. Producing app-ready explanation text
6. Supporting the Streamlit UI with AI-generated biological narratives
```

Gemma should act as the **scientific copilot** inside the notebook.

---

## 2. Required Notebook Sections

Each notebook should include the following Gemma-specific sections:

```text
1. Install and import Gemma dependencies
2. Configure Kaggle secrets / Hugging Face token
3. Load Gemma model
4. Define reusable Gemma prompt functions
5. Generate explanations from processed biological results
6. Save Gemma outputs as JSON/CSV for Streamlit
7. Optional: lightweight fallback mode if Gemma cannot run on Kaggle GPU
```

---

## 3. Gemma Model Options

Use a Kaggle-friendly Gemma model depending on available GPU:

```text
Preferred:
- google/gemma-2-2b-it
- google/gemma-2-9b-it if GPU memory allows

Fallback:
- Use small prompt templates without model execution
- Or save structured result summaries for later app-side Gemma generation
```

Recommended default:

```text
google/gemma-2-2b-it
```

Reason:

```text
- Small enough for Kaggle notebooks
- Instruction-tuned
- Good for explanations, summaries, and scientific reasoning
- Easier to run than larger models
```

---

## 4. Kaggle Setup Requirements

Each notebook should include:

```python
!pip install -q transformers accelerate bitsandbytes sentencepiece
```

Then load credentials:

```python
from kaggle_secrets import UserSecretsClient

user_secrets = UserSecretsClient()
hf_token = user_secrets.get_secret("HF_TOKEN")
```

The notebook instructions should explain:

```text
Before running:
1. Create a Hugging Face account
2. Accept the Gemma model license on Hugging Face
3. Create a Hugging Face access token
4. Add it to Kaggle Secrets as HF_TOKEN
```

---

## 5. Gemma Loading Function

Each notebook should include a reusable loading function:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def load_gemma_model(model_name="google/gemma-2-2b-it"):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        token=hf_token
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        token=hf_token,
        device_map="auto",
        torch_dtype=torch.float16
    )

    return tokenizer, model
```

---

## 6. Reusable Gemma Generation Function

Each notebook should define:

```python
def ask_gemma(prompt, tokenizer, model, max_new_tokens=350):
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    input_ids = tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        return_dict=True
    ).to(model.device)

    outputs = model.generate(
        **input_ids,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.4,
        top_p=0.9
    )

    response = tokenizer.decode(
        outputs[0][input_ids["input_ids"].shape[-1]:],
        skip_special_tokens=True
    )

    return response.strip()
```

---

## 7. Standard Prompt Template

Each notebook should use a consistent prompt structure:

```text
You are a scientific AI assistant helping interpret a Decision Biology experiment.

Project:
[Project name]

Dataset:
[Dataset name]

Inputs:
[Summary of processed data]

Results:
[Model outputs, clusters, genes, pathway scores, metrics]

Task:
Explain what these results suggest about cellular decision-making under uncertainty.

Write:
1. Plain-English explanation
2. Biological interpretation
3. Decision Biology interpretation
4. Possible hypothesis
5. What should be shown in the Streamlit app
```

---

## 8. Notebook-Specific Gemma Usage

### Notebook 1: Cell Decision Simulator

Gemma should explain:

```text
- What stress condition was simulated
- Which genes/pathways changed
- What decision state the cell appears to enter
- Whether the cell response looks like survival, stress adaptation, proliferation, apoptosis, or dormancy
```

Output file:

```text
outputs/gemma_cell_decision_summary.json
```

---

### Notebook 2: Gene Expression Cancer RNA-seq

Gemma should explain:

```text
- Differences between normal and cancer gene-expression profiles
- Key genes contributing to classification
- What cellular decision logic may be altered in cancer
- How noise and pathway dysregulation affect decision-making
```

Output file:

```text
outputs/gemma_cancer_expression_summary.json
```

---

### Notebook 3: Signaling Pathway Information Flow

Gemma should explain:

```text
- Mutual information results
- Which signaling pathways preserve or lose information
- How biological noise affects signal reliability
- What this means for cellular decision-making
```

Output file:

```text
outputs/gemma_signaling_information_summary.json
```

---

### Notebook 4: Perturbation / Drug Response Layer

Gemma should explain:

```text
- How perturbations shift gene-expression states
- Which drug or CRISPR perturbation appears most meaningful
- How the intervention may redirect cellular decisions
- Potential biological mechanism
```

Output file:

```text
outputs/gemma_perturbation_summary.json
```

---

### Notebook 5: CRISPR Circuit Designer

Gemma should explain:

```text
- Candidate genes for control
- Possible synthetic circuit logic
- Risk of noisy or unstable decisions
- Recommended circuit strategy
- Why the selected targets may influence cell fate
```

Output file:

```text
outputs/gemma_crispr_design_summary.json
```

---

## 9. Save Gemma Outputs for App

Each notebook should save Gemma outputs in a common format:

```python
import json
from pathlib import Path

def save_gemma_output(project_name, dataset_name, prompt, response, output_path):
    output = {
        "project_name": project_name,
        "dataset_name": dataset_name,
        "prompt": prompt,
        "gemma_response": response
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
```

Example:

```python
save_gemma_output(
    project_name="Cell Decision Simulator",
    dataset_name="Single-cell RNA-seq",
    prompt=prompt,
    response=response,
    output_path="outputs/gemma_cell_decision_summary.json"
)
```

---

## 10. Streamlit App Connection

The Streamlit app should read Gemma-generated JSON files from the notebook outputs.

App behavior:

```text
Each tab should show:
1. Dataset summary
2. Model result
3. Visualization
4. Gemma explanation panel
5. Downloadable Gemma summary
```

Example app section:

```python
import json
import streamlit as st

def load_gemma_summary(path):
    with open(path, "r") as f:
        return json.load(f)

summary = load_gemma_summary("outputs/gemma_cell_decision_summary.json")

st.subheader("Gemma Biological Interpretation")
st.write(summary["gemma_response"])
```

---

## 11. UI Requirement

The Streamlit UI should not use a dropdown for project modes.

Use separate tabs:

```python
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Cell Decision Simulator",
    "Cancer Expression",
    "Information Flow",
    "Perturbation Layer",
    "CRISPR Designer"
])
```

Each tab should have its own Gemma explanation section.

---

## 12. Fallback Mode

If Gemma cannot run on Kaggle due to GPU/memory limits, the notebook should still work.

Fallback behavior:

```text
1. Process dataset normally
2. Train or run analysis normally
3. Save structured result summary
4. Mark Gemma output as pending
5. Allow Streamlit app to load the structured summary
```

Example fallback output:

```json
{
  "project_name": "Cell Decision Simulator",
  "dataset_name": "Single-cell RNA-seq",
  "gemma_status": "not_run",
  "reason": "Gemma model could not be loaded in Kaggle environment",
  "structured_results": {}
}
```

---

## 13. Deliverables

```text
1. Five Kaggle-ready notebooks
2. Each notebook includes dataset download code
3. Each notebook includes preprocessing code
4. Each notebook includes modeling / analysis code
5. Each notebook includes Gemma loading code
6. Each notebook includes Gemma prompt templates
7. Each notebook saves Gemma summaries as JSON
8. Streamlit app reads notebook outputs
9. UI uses separate tabs, not dropdown modes
10. App displays Gemma explanations per project
```

---

## 14. Final Positioning

Gemma should be described as:

```text
Gemma is the scientific explanation layer of the Decision Biology stack.

The notebooks produce data, metrics, models, and plots.
Gemma turns those outputs into biological insight, hypotheses, and app-ready explanations.
```

This makes the project stronger because it shows both:

```text
1. Real computational biology pipeline
2. AI-powered scientific interpretation layer
```
