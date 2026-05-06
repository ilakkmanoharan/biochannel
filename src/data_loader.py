"""CSV handoff from Kaggle notebooks → Streamlit (spec-set-2). Validates columns; falls back to in-memory demos."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, List, Optional, Tuple

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
DATA_PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed"

WarnFn = Optional[Callable[[str], None]]


def _warn(warn: WarnFn, msg: str) -> None:
    if warn:
        warn(msg)


def _ensure_dir() -> None:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path, warn: WarnFn) -> Optional[pd.DataFrame]:
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception as e:
        _warn(warn, f"Could not read `{path.name}`: {e}. Using demo data.")
        return None


def _validate(df: Optional[pd.DataFrame], cols: List[str], path: str, warn: WarnFn) -> Optional[pd.DataFrame]:
    if df is None:
        return None
    missing = [c for c in cols if c not in df.columns]
    if missing:
        _warn(warn, f"`{path}` missing columns {missing}. Using demo data.")
        return None
    return df


def _synth_cell_pca() -> pd.DataFrame:
    n = 420
    coords = RNG.normal(scale=1.2, size=(n, 2))
    states = RNG.choice(["G1-like", "S-like", "Stress", "Dormant"], size=n, p=[0.35, 0.25, 0.22, 0.18])
    return pd.DataFrame({"PC1": coords[:, 0], "PC2": coords[:, 1], "cell_state": states})


def _synth_top_features() -> pd.DataFrame:
    genes = [f"gene_{i:03d}" for i in range(40)]
    v = np.sort(RNG.uniform(0.1, 3.0, size=len(genes)))[::-1]
    return pd.DataFrame({"feature": genes, "variance": v})


def _synth_info_timeseries() -> pd.DataFrame:
    t = np.linspace(0, 24, 48)
    input_signal = np.clip(np.sin(t / 4) * 0.5 + 0.5 + RNG.normal(scale=0.05, size=t.shape), 0, 1)
    lag = 2
    base = np.roll(input_signal, lag)
    pathway_response = np.clip(0.2 + 0.65 * base + RNG.normal(scale=0.12, size=t.shape), 0, 1)
    return pd.DataFrame({"time": t, "input_signal": input_signal, "pathway_response": pathway_response})


def _synth_info_metrics() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "input_entropy_bits": 2.4,
                "output_entropy_bits": 2.1,
                "mutual_information_bits": 1.15,
                "signal_fidelity": 0.48,
                "information_loss": 0.52,
            }
        ]
    )


def _synth_drug_response() -> pd.DataFrame:
    lines = ["A549", "MCF7", "HT29", "PC3"]
    drugs = ["Drug_A", "Drug_B", "Drug_C", "Combo_XY"]
    rows = []
    for line in lines:
        for drug in drugs:
            base = RNG.uniform(0.15, 0.85)
            sens = float(np.clip(1 - base + RNG.normal(scale=0.05), 0, 1))
            rows.append(
                {
                    "cell_line": line,
                    "drug": drug,
                    "sensitivity": sens,
                    "resistance_risk": float(np.clip(1 - sens + RNG.normal(scale=0.04), 0, 1)),
                    "apoptosis_proxy": float(np.clip(sens * 0.85 + RNG.normal(scale=0.06), 0, 1)),
                    "survival_proxy": float(np.clip(1 - sens * 0.7 + RNG.normal(scale=0.06), 0, 1)),
                }
            )
    return pd.DataFrame(rows)


def _synth_feature_importance() -> pd.DataFrame:
    feats = [f"feature_{i:02d}" for i in range(24)]
    imp = np.sort(RNG.uniform(0.01, 0.12, size=len(feats)))[::-1]
    return pd.DataFrame({"feature": feats, "importance": imp})


def _synth_class_mapping() -> pd.DataFrame:
    return pd.DataFrame({"class": ["class_0", "class_1"], "encoded_value": [0, 1]})


def _synth_edge_expression() -> pd.DataFrame:
    n = 80
    xy = RNG.normal(scale=1.0, size=(n, 2))
    st = RNG.choice(["edge_A", "edge_B"], size=n)
    return pd.DataFrame({"PC1": xy[:, 0], "PC2": xy[:, 1], "edge_state": st})


def load_cell_pca_or_demo(warn: WarnFn = None) -> tuple[pd.DataFrame, str]:
    """Returns (dataframe with PC1, PC2, cell_state), source label 'file'|'demo'."""
    path = DATA_PROCESSED / "cell_decision_pca.csv"
    df = _read_csv(path, warn)
    df = _validate(df, ["PC1", "PC2", "cell_state"], "cell_decision_pca.csv", warn)
    if df is not None:
        return df.copy(), "file"
    return _synth_cell_pca(), "demo"


def load_cell_top_features_or_demo(warn: WarnFn = None) -> tuple[pd.DataFrame, str]:
    path = DATA_PROCESSED / "cell_top_features.csv"
    df = _read_csv(path, warn)
    df = _validate(df, ["feature", "variance"], "cell_top_features.csv", warn)
    if df is not None:
        return df.copy(), "file"
    return _synth_top_features(), "demo"


def load_info_timeseries_or_demo(warn: WarnFn = None) -> tuple[pd.DataFrame, str]:
    path = DATA_PROCESSED / "info_timeseries.csv"
    df = _read_csv(path, warn)
    df = _validate(df, ["time", "input_signal", "pathway_response"], "info_timeseries.csv", warn)
    if df is not None:
        return df.copy(), "file"
    return _synth_info_timeseries(), "demo"


def load_info_metrics_or_none(warn: WarnFn = None) -> Tuple[Optional[pd.DataFrame], str]:
    path = DATA_PROCESSED / "info_metrics.csv"
    df = _read_csv(path, warn)
    df = _validate(
        df,
        [
            "input_entropy_bits",
            "output_entropy_bits",
            "mutual_information_bits",
            "signal_fidelity",
            "information_loss",
        ],
        "info_metrics.csv",
        warn,
    )
    if df is not None:
        return df.copy(), "file"
    return None, "missing"


def load_drug_response_or_demo(warn: WarnFn = None) -> tuple[pd.DataFrame, str]:
    path = DATA_PROCESSED / "drug_response_processed.csv"
    df = _read_csv(path, warn)
    req = [
        "cell_line",
        "drug",
        "sensitivity",
        "resistance_risk",
        "apoptosis_proxy",
        "survival_proxy",
    ]
    df = _validate(df, req, "drug_response_processed.csv", warn)
    if df is not None:
        return df.copy(), "file"
    return _synth_drug_response(), "demo"


def load_feature_importance_or_demo(warn: WarnFn = None) -> tuple[pd.DataFrame, str]:
    path = DATA_PROCESSED / "explain_feature_importance.csv"
    df = _read_csv(path, warn)
    df = _validate(df, ["feature", "importance"], "explain_feature_importance.csv", warn)
    if df is not None:
        return df.copy(), "file"
    return _synth_feature_importance(), "demo"


def load_class_mapping_or_demo(warn: WarnFn = None) -> tuple[pd.DataFrame, str]:
    path = DATA_PROCESSED / "explain_class_mapping.csv"
    df = _read_csv(path, warn)
    df = _validate(df, ["class", "encoded_value"], "explain_class_mapping.csv", warn)
    if df is not None:
        return df.copy(), "file"
    return _synth_class_mapping(), "demo"


def load_edge_expression_or_demo(warn: WarnFn = None) -> tuple[pd.DataFrame, str]:
    path = DATA_PROCESSED / "edge_small_expression.csv"
    df = _read_csv(path, warn)
    df = _validate(df, ["PC1", "PC2", "edge_state"], "edge_small_expression.csv", warn)
    if df is not None:
        return df.copy(), "file"
    return _synth_edge_expression(), "demo"


# --- Legacy matrix path (optional notebook export `cell_decision_demo.csv`) ---


def load_explain_training_or_demo(warn: WarnFn = None) -> tuple[pd.DataFrame, np.ndarray]:
    """Feature matrix + labels when app trains an on-the-fly RF (no CSV importances)."""
    n, d = 320, 24
    w = RNG.normal(size=d)
    Xn = RNG.normal(size=(n, d))
    logits = Xn @ w + RNG.normal(scale=0.5, size=n)
    y = (logits > np.median(logits)).astype(int)
    cols = [f"feature_{i:02d}" for i in range(d)]
    return pd.DataFrame(Xn, columns=cols), y


def load_cell_decision_matrix_or_demo(warn: WarnFn = None) -> tuple[pd.DataFrame, np.ndarray]:
    """Numeric gene matrix + integer labels for RF/PCA fallback when only matrix export exists."""
    path = DATA_PROCESSED / "cell_decision_demo.csv"
    df = _read_csv(path, warn)
    if df is not None and "label" in df.columns:
        y = df["label"].to_numpy()
        X = df.drop(columns=["label"])
        num = X.select_dtypes(include=[np.number])
        if len(num.columns) >= 8:
            return num, y
    n, genes = 420, 48
    centers = RNG.normal(size=(4, genes))
    labels = RNG.integers(0, 4, size=n)
    rows = centers[labels] + RNG.normal(scale=0.35, size=(n, genes))
    feat_cols = [f"gene_{i:03d}" for i in range(genes)]
    X = pd.DataFrame(rows, columns=feat_cols)
    return X, labels
