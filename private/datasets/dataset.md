Perfect — now you are looking at the correct datasets.

For your Decision Biology hackathon/demo, I recommend these:

# BEST PICKS

## 1. Cancer RNA-Seq Dataset

Use:

```text id="4fjlwm"
Gene Expression Cancer RNA-Seq
```

(Alban NYANTUDRE)

Why:

* Clean
* Easy CSV loading
* Good for clustering/PCA/UMAP
* Great for ML demos
* Lightweight

Click the `+` button to add it.

---

# 2. Single-Cell Dataset

Use:

```text id="a5q5vi"
scRNA-seq breast cancer cell lines
```

Why:

* TRUE single-cell data
* Excellent for:

  * UMAP
  * t-SNE
  * clustering
  * cellular heterogeneity
  * noisy biological decisions

This is VERY aligned with Decision Biology.

Add this too.

---

# Recommended Mapping to Your 5 Notebooks

```text id="gqdzcw"
Notebook 1 → Gene Expression Cancer RNA-Seq
Notebook 2 → scRNA-seq breast cancer cell lines
Notebook 3 → same scRNA-seq dataset
Notebook 4 → same scRNA-seq dataset
Notebook 5 → same scRNA-seq dataset + synthetic perturbation
```

You do NOT need 5 separate datasets initially.

Using:

* one bulk RNA-seq dataset
* one single-cell dataset

is enough for a strong demo.

---

# After Clicking +

Run this:

```python id="eglnm0"
import os

for root, dirs, files in os.walk('/kaggle/input'):
    print(root)
    for f in files[:10]:
        print("   ", f)
```

This will show paths like:

```text id="q65rf9"
/kaggle/input/gene-expression-cancer-rna-seq
/kaggle/input/scrna-seq-breast-cancer-cell-lines
```

---

# Then Load Dataset

Example:

```python id="ffejqy"
import pandas as pd

df = pd.read_csv(
    '/kaggle/input/gene-expression-cancer-rna-seq/data.csv'
)

df.head()
```

For the scRNA dataset:

```python id="nry0uo"
import pandas as pd

df = pd.read_csv(
    '/kaggle/input/scrna-seq-breast-cancer-cell-lines/FILENAME.csv'
)

df.head()
```

Use the exact filename from the os.walk output.

---

# Recommendation

For the hackathon:

## Focus on:

* UMAP/t-SNE
* clustering
* noisy cell states
* pathway visualization
* entropy / mutual information
* Gemma biological explanations

NOT:

* heavy wet-lab biological accuracy
* giant genomics preprocessing pipelines

The judges will care more about:

* insight
* clarity
* interactivity
* novelty
* biological framing
* polished UX/UI

than massive preprocessing complexity.
