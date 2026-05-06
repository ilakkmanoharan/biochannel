"""
BioChannel — unified Streamlit dashboard (spec-set-2: CSV handoff, pills, canonical loaders).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except ImportError:
    pass

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier

from src.data_loader import (
    load_cell_pca_or_demo,
    load_cell_top_features_or_demo,
    load_class_mapping_or_demo,
    load_drug_response_or_demo,
    load_edge_expression_or_demo,
    load_explain_training_or_demo,
    load_feature_importance_or_demo,
    load_info_metrics_or_none,
    load_info_timeseries_or_demo,
)
from src.gemma_explainer import ExplainContext, answer_question, explain_with_optional_gemini
from src.info_theory import (
    channel_capacity_approx,
    entropy_bits,
    information_loss_fraction,
    mutual_information_bits,
    signal_fidelity,
)
from src.prediction import drug_outcomes
from src.simulation import decision_probabilities
from src.suggestions import cards_for
from src.visualization import (
    figure_bar_probabilities,
    figure_dose_response,
    figure_feature_importance,
    figure_info_bars,
    figure_input_output_hist,
    figure_noise_curve,
    figure_pca_scatter,
    figure_survival_apoptosis,
    resistance_gauge,
)


def load_modes() -> list[dict]:
    path = ROOT / "modes_config.json"
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and data:
                return data
        except Exception:
            pass
    return [
        {
            "id": "cell_decision_simulator",
            "title": "Cell Decision Simulator",
            "description": "Simulate cellular decisions under signals and noise.",
        },
        {
            "id": "information_loss_analyzer",
            "title": "Information Loss Analyzer",
            "description": "Information flow and fidelity in noisy pathways.",
        },
        {
            "id": "drug_response_predictor",
            "title": "Drug Response Predictor",
            "description": "Dose–response and resistance-aware predictions.",
        },
        {
            "id": "explainable_cell_ai",
            "title": "Explainable Cell AI",
            "description": "Feature importance and guided explanations.",
        },
        {
            "id": "edge_biology_assistant",
            "title": "Edge Biology Assistant",
            "description": "Lightweight local / educational slice.",
        },
    ]


st.set_page_config(
    page_title="BioChannel",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .block-container { padding-top: 0.8rem; max-width: 1280px; }
    div[data-testid="stMetricValue"] { font-size: 1.25rem; }
    .bio-caption { color: #64748b; font-size: 0.95rem; }
    .modes-panel {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1rem 1.25rem 1.25rem 1.25rem;
        margin-bottom: 1rem;
    }
    .modes-title { font-size: 1.75rem; font-weight: 700; color: #0f172a; margin: 0 0 0.25rem 0; }
    .modes-sub { color: #475569; font-size: 0.95rem; margin-bottom: 0.75rem; }
</style>
""",
    unsafe_allow_html=True,
)


def top_features_from_rf(names: list[str], importances: np.ndarray, k: int = 6) -> str:
    idx = np.argsort(importances)[::-1][:k]
    parts = [f"{names[i]} ({importances[i]:.3f})" for i in idx]
    return ", ".join(parts)


def stimulus_vector(ts: pd.DataFrame, kind: str) -> np.ndarray:
    col = "input_signal" if "input_signal" in ts.columns else "stimulus"
    s = ts[col].to_numpy(dtype=float)
    if kind == "Low stimulus":
        return s * 0.35
    if kind == "Medium stimulus":
        return s * 0.65
    if kind == "High stimulus":
        return np.clip(s * 1.05, 0, 1)
    if kind == "Pulsed stimulus":
        return (np.sin(np.linspace(0, 6 * np.pi, len(s))) * 0.5 + 0.5) * float(np.mean(s) + 1e-6)
    if kind == "Gradual ramp":
        ramp = np.linspace(0.1, 1.0, len(s))
        return np.clip(s * ramp, 0, 1)
    return s


def response_base_array(ts: pd.DataFrame) -> np.ndarray:
    if "pathway_response" in ts.columns:
        return ts["pathway_response"].to_numpy(dtype=float)
    return ts["response"].to_numpy(dtype=float)


def simulation_cell_states() -> set[str]:
    return {"Normal-like", "Cancer-like", "Stressed", "Resistant", "Dormant"}


def map_cell_state(cs: str) -> str:
    if cs == "Sensitive-like profile":
        return "Normal-like"
    if cs == "Resistant-like profile":
        return "Resistant"
    return cs if cs in simulation_cell_states() else "Cancer-like"


def apply_noise_to_response(
    stimulus: np.ndarray,
    response_base: np.ndarray,
    noise_level: float,
    noise_source: str,
) -> np.ndarray:
    rng = np.random.default_rng(7)
    y = response_base.copy()
    if noise_source == "Intrinsic molecular noise":
        y += rng.normal(scale=0.04 + 0.22 * noise_level, size=y.shape)
    elif noise_source == "Extrinsic cell-to-cell variability":
        y += rng.normal(scale=0.06 + 0.28 * noise_level, size=y.shape)
    elif noise_source == "Crosstalk":
        y += 0.15 * noise_level * np.roll(stimulus, 3)
    elif noise_source == "Feedback instability":
        y += 0.12 * noise_level * np.sin(np.linspace(0, 4 * np.pi, len(y)))
    else:
        y += rng.normal(scale=0.05 + 0.2 * noise_level, size=y.shape)
    return np.clip(y, 0, 1)


def init_session():
    if "explain_cache" not in st.session_state:
        st.session_state.explain_cache = ""


init_session()

modes = load_modes()
if "mode_id" not in st.session_state:
    st.session_state.mode_id = modes[0]["id"]

selected = next(m for m in modes if m["id"] == st.session_state.mode_id)
mode = selected["title"]

drug_df, drug_src = load_drug_response_or_demo(None)

st.title("BioChannel")
st.markdown(
    '<p class="bio-caption">Cellular signals as noisy communication channels — '
    "datasets prepared in Kaggle notebooks, interactively explored here.</p>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="modes-panel">'
    '<p class="modes-title">Modes</p>'
    "<p class=\"modes-sub\">Tap a mode to open an experiment. Processed CSVs in "
    "<code>data/processed/</code> replace demo fallbacks automatically.</p></div>",
    unsafe_allow_html=True,
)

pill_cols = st.columns(len(modes))
for i, m in enumerate(modes):
    with pill_cols[i]:
        is_sel = st.session_state.mode_id == m["id"]
        if st.button(
            m["title"],
            key=f"pill_{m['id']}",
            use_container_width=True,
            type="primary" if is_sel else "secondary",
        ):
            st.session_state.mode_id = m["id"]
            st.rerun()

st.caption(selected.get("description", ""))

# --- Defaults (sidebar may override) ---
dataset_name = "Demo fallback (place notebook CSVs in data/processed/)"
signal_type = "Growth signal"
signal_strength = 0.45
noise_level = 0.35
cell_state = "Cancer-like"
constraint = None
input_signal = "Medium stimulus"
output_marker = "Gene expression response"
noise_source = "Extrinsic cell-to-cell variability"
info_metric = "Mutual information"
cell_line = "MCF7"
drug = "Drug_B"
dose = 0.5
duration = "Medium"
resistance_pressure = 0.35
stress_level_slider = 0.35
drug_pressure_slider = 0.2

constraint_options_cell = [
    None,
    "Maximize survival",
    "Maximize apoptosis",
    "Minimize resistance",
    "Stable response",
    "Fast response",
]

constraint_options_drug = [
    None,
    "Maximize apoptosis",
    "Minimize resistance",
    "Reduce toxicity",
    "Preserve normal-like cells",
    "Maximize signal clarity",
]

constraint_options_info = [
    None,
    "Maximize information transfer",
    "Minimize noise",
    "Maximize robustness",
    "Preserve response diversity",
]

warn_fn = lambda msg: st.warning(msg, icon="⚠️")

st.sidebar.header("Controls")

if mode == "Cell Decision Simulator":
    dataset_name = st.sidebar.selectbox(
        "Dataset",
        ["Gene Expression Cancer RNA-seq (demo)", "Single-cell RNA-seq sample (demo)"],
    )
    signal_type = st.sidebar.selectbox(
        "Signal type",
        ["Nutrient stress", "Drug signal", "Growth signal", "Immune signal", "Oxidative stress"],
    )
    signal_strength = st.sidebar.slider("Signal strength", 0.0, 1.0, 0.55, 0.05)
    noise_level = st.sidebar.slider("Noise level", 0.0, 1.0, 0.38, 0.05)
    stress_level_slider = st.sidebar.slider("Stress level", 0.0, 1.0, 0.4, 0.05)
    drug_pressure_slider = st.sidebar.slider("Drug pressure", 0.0, 1.0, 0.22, 0.05)
    resistance_pressure = st.sidebar.slider("Resistance pressure", 0.0, 1.0, 0.38, 0.05)
    cell_state = st.sidebar.selectbox(
        "Cell state",
        ["Normal-like", "Cancer-like", "Stressed", "Resistant", "Dormant"],
    )
    constraint = st.sidebar.selectbox("Constraint", constraint_options_cell)

elif mode == "Information Loss Analyzer":
    dataset_name = "Time-series gene expression (notebook or demo)"
    input_signal = st.sidebar.selectbox(
        "Input signal",
        ["Low stimulus", "Medium stimulus", "High stimulus", "Pulsed stimulus", "Gradual ramp"],
    )
    output_marker = st.sidebar.selectbox(
        "Output marker",
        ["Gene expression response", "Pathway activation score", "Cell state probability", "Synthetic reporter output"],
    )
    noise_source = st.sidebar.selectbox(
        "Noise source",
        [
            "Intrinsic molecular noise",
            "Extrinsic cell-to-cell variability",
            "Crosstalk",
            "Feedback instability",
        ],
    )
    noise_level = st.sidebar.slider("Noise level", 0.0, 1.0, 0.42, 0.05)
    info_metric = st.sidebar.selectbox(
        "Information metric",
        ["Entropy", "Mutual information", "Channel capacity approximation", "Signal fidelity score"],
    )
    constraint = st.sidebar.selectbox("Constraint", constraint_options_info)

elif mode == "Drug Response Predictor":
    dataset_name = "GDSC-style processed table" if drug_src == "file" else "GDSC-style demo table"
    lines = sorted(drug_df["cell_line"].astype(str).unique())
    drugs = sorted(drug_df["drug"].astype(str).unique())
    cell_line = st.sidebar.selectbox("Cell line", lines)
    drug = st.sidebar.selectbox("Drug", drugs)
    dose = st.sidebar.slider("Drug dose (relative)", 0.0, 1.0, 0.55, 0.05)
    duration = st.sidebar.selectbox("Treatment duration", ["Short", "Medium", "Long"])
    resistance_pressure = st.sidebar.slider("Resistance pressure", 0.0, 1.0, 0.4, 0.05)
    cell_state = st.sidebar.selectbox(
        "Phenotype context",
        ["Sensitive-like profile", "Resistant-like profile", "Cancer-like", "Stressed"],
    )
    constraint = st.sidebar.selectbox("Constraint", constraint_options_drug)

elif mode == "Explainable Cell AI":
    dataset_name = "Classification / feature importance (CSV or demo)"
    signal_strength = st.sidebar.slider("Pseudo stimulus scale", 0.0, 1.0, 0.5, 0.05)
    noise_level = st.sidebar.slider("Label noise injection", 0.0, 1.0, 0.12, 0.05)

elif mode == "Edge Biology Assistant":
    dataset_name = "Edge PCA subset (CSV or demo)"
    edge_mode = st.sidebar.selectbox("Mode", ["Lightweight local demo", "Small dataset mode", "Educational mode"])
    qtype = st.sidebar.selectbox(
        "Question type",
        ["Explain a gene expression pattern", "Simulate simple signal response", "Compare two biological states"],
    )
    signal_strength = st.sidebar.slider("Signal strength (demo)", 0.0, 1.0, 0.45, 0.05)
    noise_level = st.sidebar.slider("Noise level (demo)", 0.0, 1.0, 0.3, 0.05)
    st.session_state.edge_mode = edge_mode
    st.session_state.edge_qtype = qtype

st.sidebar.markdown("---")
st.sidebar.markdown("### AI explanation (Gemini)")
_genai_pkg = True
try:
    import google.generativeai  # noqa: F401
except ImportError:
    _genai_pkg = False
_key_ok = bool(os.environ.get("GOOGLE_API_KEY", "").strip())
if _key_ok and _genai_pkg:
    st.sidebar.success("Status: **ready** — key loaded; Gemini can run.")
elif _key_ok and not _genai_pkg:
    st.sidebar.warning("Key present but `google-generativeai` missing. Run `pip install -r requirements.txt`.")
else:
    st.sidebar.info("Status: **template only** — set `GOOGLE_API_KEY` in `.env` for live Gemini.")

auto_explain = st.sidebar.toggle(
    "Auto-explain on change",
    value=False,
    help="Refresh the explanation on every interaction (uses Gemini when configured).",
)
run_gemini = st.sidebar.button(
    "Explain with Gemini / template",
    help="Runs once: uses Gemini if key + package OK; otherwise built-in template.",
)
st.sidebar.caption(
    "The panel below shows **(gemini)** when the API answered, or **(template)** when falling back."
)

if st.sidebar.button("Reset session"):
    st.session_state.clear()
    st.rerun()

# --- Loaders (CSV handoff) ---
pca_df, pca_src = load_cell_pca_or_demo(warn_fn)
top_features_df, top_src = load_cell_top_features_or_demo(warn_fn)
ts, ts_src = load_info_timeseries_or_demo(warn_fn)
metrics_notebook_df, metrics_src = load_info_metrics_or_none(warn_fn)
fi_df, fi_src = load_feature_importance_or_demo(warn_fn)
cm_df, cm_src = load_class_mapping_or_demo(warn_fn)
edge_pca_df, edge_src = load_edge_expression_or_demo(warn_fn)

stim = stimulus_vector(ts, input_signal)
resp_base = response_base_array(ts)
resp = apply_noise_to_response(stim, resp_base, noise_level, noise_source)

h_in = entropy_bits(stim)
h_out = entropy_bits(resp)
mi_bits = mutual_information_bits(stim, resp)
fidelity = signal_fidelity(stim, resp)
loss = information_loss_fraction(stim, resp)
cap = channel_capacity_approx(mi_bits, noise_level)

noise_grid = np.linspace(0, 1, 25)
fidelity_curve = np.array(
    [signal_fidelity(stim, apply_noise_to_response(stim, resp_base, n, noise_source)) for n in noise_grid]
)

coords = pca_df[["PC1", "PC2"]].to_numpy(dtype=float)
rng_pca = np.random.default_rng(123)
coords_sim = coords + rng_pca.normal(
    scale=0.025 + 0.12 * noise_level,
    size=coords.shape,
) * (0.35 + 0.65 * signal_strength)

probs = decision_probabilities(
    signal_strength=signal_strength,
    noise_level=noise_level,
    cell_state=map_cell_state(cell_state),
    signal_type=signal_type,
    constraint=constraint,
    resistance_pressure=resistance_pressure,
    stress_level_slider=stress_level_slider,
    drug_pressure_slider=drug_pressure_slider,
)

X_exp, y_exp = load_explain_training_or_demo(None)
_label_noise = noise_level if mode == "Explainable Cell AI" else 0.06
rng_flip = np.random.default_rng(99)
y_noisy = y_exp.copy()
flip_mask = rng_flip.random(len(y_exp)) < _label_noise * 0.35
y_noisy[flip_mask] = 1 - y_noisy[flip_mask]
rf = RandomForestClassifier(n_estimators=120, random_state=42, max_depth=6)
rf.fit(X_exp, y_noisy)
feat_names_rf = list(X_exp.columns)

if fi_src == "file":
    feat_names = fi_df["feature"].astype(str).tolist()
    feat_imp = fi_df["importance"].to_numpy(dtype=float)
    top_feat_str = ", ".join(
        f"{a} ({b:.3f})" for a, b in zip(feat_names[:8], feat_imp[:8])
    )
else:
    feat_names = feat_names_rf
    feat_imp = rf.feature_importances_
    top_feat_str = top_features_from_rf(feat_names_rf, rf.feature_importances_)

dataset_row = None
if mode == "Drug Response Predictor":
    row = drug_df[(drug_df["cell_line"].astype(str) == str(cell_line)) & (drug_df["drug"].astype(str) == str(drug))]
    if len(row) == 1:
        dataset_row = row.iloc[0].to_dict()

if mode == "Drug Response Predictor":
    probs_drug_context = drug_outcomes(
        dose=dose,
        duration=duration,
        resistance_pressure=resistance_pressure,
        cell_state=map_cell_state(cell_state),
        constraint=constraint,
        dataset_row=dataset_row,
        stress_level_slider=stress_level_slider,
        drug_pressure_slider=drug_pressure_slider,
    )
else:
    probs_drug_context = None

explain_probs = probs
if mode == "Drug Response Predictor" and probs_drug_context is not None:
    explain_probs = {
        "proliferation": float(np.clip(probs_drug_context["survival"], 0.0, 1.0)),
        "apoptosis": float(probs_drug_context["apoptosis"]),
        "dormancy": float(probs["dormancy"]),
        "stress_adaptation": float(probs["stress_adaptation"]),
        "resistance": float(probs_drug_context["resistance"]),
    }

_signal_type = (
    signal_type
    if mode == "Cell Decision Simulator"
    else (f"{drug} — {cell_line}" if mode == "Drug Response Predictor" else input_signal)
)

ctx = ExplainContext(
    module_name=mode,
    dataset_name=dataset_name,
    signal_type=_signal_type,
    signal_strength=float(signal_strength),
    noise_level=float(noise_level),
    cell_state=cell_state,
    constraint=constraint,
    proliferation=float(explain_probs["proliferation"]),
    apoptosis=float(explain_probs["apoptosis"]),
    dormancy=float(explain_probs["dormancy"]),
    resistance=float(explain_probs["resistance"]),
    stress_adaptation=float(explain_probs.get("stress_adaptation", 0.0)),
    mi=float(mi_bits) if mode == "Information Loss Analyzer" else None,
    info_loss=float(loss) if mode == "Information Loss Analyzer" else None,
    signal_fidelity=float(fidelity) if mode == "Information Loss Analyzer" else None,
    top_features=top_feat_str,
)

# --- Main content ---
if mode == "Cell Decision Simulator":
    st.subheader("Simulation summary")
    st.caption(f"PCA: **{pca_src}** · Top features: **{top_src}**")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Proliferation", f"{probs['proliferation']:.2f}")
    c2.metric("Apoptosis", f"{probs['apoptosis']:.2f}")
    c3.metric("Dormancy", f"{probs['dormancy']:.2f}")
    c4.metric("Stress adaptation", f"{probs['stress_adaptation']:.2f}")
    c5.metric("Resistance", f"{probs['resistance']:.2f}")

    col_a, col_b = st.columns((2, 1))
    with col_a:
        st.plotly_chart(
            figure_pca_scatter(
                coords_sim,
                label_names=pca_df["cell_state"].astype(str).to_numpy(),
                title="Cell-state landscape (PC1 vs PC2)",
            ),
            use_container_width=True,
        )
    with col_b:
        st.plotly_chart(figure_bar_probabilities(probs), use_container_width=True)

    with st.expander("Top variable features (from notebook export)"):
        st.dataframe(top_features_df.head(25), use_container_width=True)

    st.plotly_chart(
        figure_noise_curve(noise_grid, fidelity_curve, "Noise vs signal fidelity (live MI / H(X))"),
        use_container_width=True,
    )

elif mode == "Information Loss Analyzer":
    st.subheader("Information metrics")
    st.caption(f"Time series: **{ts_src}** · Notebook metrics row: **{metrics_src}**")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("H(input)", f"{h_in:.3f} bits")
    m2.metric("H(output)", f"{h_out:.3f} bits")
    m3.metric("I(X;Y)", f"{mi_bits:.3f} bits")
    m4.metric("Information loss", f"{loss:.3f}")
    m5.metric("Fidelity", f"{fidelity:.3f}")

    if metrics_notebook_df is not None:
        with st.expander("Notebook-exported baseline metrics (`info_metrics.csv`)"):
            st.dataframe(metrics_notebook_df, use_container_width=True)

    st.plotly_chart(figure_input_output_hist(stim, resp), use_container_width=True)
    st.plotly_chart(
        figure_info_bars(
            ["Mutual information (bits)", "Channel capacity (approx)", "Information loss"],
            [mi_bits, cap, loss],
            "Information summary",
        ),
        use_container_width=True,
    )
    st.plotly_chart(
        figure_noise_curve(noise_grid, fidelity_curve, "Noise vs fidelity"),
        use_container_width=True,
    )
    st.caption(f"Metric focus: **{info_metric}** — live values use binned MI / entropy on the loaded time series.")

elif mode == "Drug Response Predictor":
    assert probs_drug_context is not None
    st.subheader("Predictions")
    st.caption(f"Drug table: **{drug_src}**" + (" (row matched for blending)" if dataset_row else ""))
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Sensitivity score", f"{probs_drug_context['sensitivity_score']:.2f}")
    d2.metric("Apoptosis", f"{probs_drug_context['apoptosis']:.2f}")
    d3.metric("Survival index", f"{probs_drug_context['survival']:.2f}")
    d4.metric("Resistance", f"{probs_drug_context['resistance']:.2f}")

    doses = np.linspace(0, 1, 30)
    apop_curve = []
    surv_curve = []
    for dv in doses:
        o = drug_outcomes(
            dose=float(dv),
            duration=duration,
            resistance_pressure=resistance_pressure,
            cell_state=map_cell_state(cell_state),
            constraint=constraint,
            dataset_row=dataset_row,
            stress_level_slider=stress_level_slider,
            drug_pressure_slider=drug_pressure_slider,
        )
        apop_curve.append(o["apoptosis"])
        surv_curve.append(o["survival"])

    c_left, c_right = st.columns((1, 1))
    with c_left:
        st.plotly_chart(figure_dose_response(doses, np.array(apop_curve)), use_container_width=True)
        st.plotly_chart(
            figure_survival_apoptosis(doses, np.array(apop_curve), np.array(surv_curve)),
            use_container_width=True,
        )
    with c_right:
        st.plotly_chart(resistance_gauge(probs_drug_context["resistance"]), use_container_width=True)
        st.markdown("**Intervention ranking**")
        for step in probs_drug_context["intervention_ranking"]:
            st.markdown(f"- {step}")

elif mode == "Explainable Cell AI":
    st.subheader("Model interpretability")
    st.caption(f"Feature importance: **{fi_src}** · Class map: **{cm_src}**")
    if fi_src == "file":
        st.plotly_chart(
            figure_feature_importance(feat_names, list(feat_imp)),
            use_container_width=True,
        )
    else:
        st.plotly_chart(
            figure_feature_importance(feat_names_rf, list(rf.feature_importances_)),
            use_container_width=True,
        )
        st.caption("Demo mode trains a small random forest when `explain_feature_importance.csv` is absent.")

    with st.expander("Class mapping (`explain_class_mapping.csv`)"):
        st.dataframe(cm_df, use_container_width=True)

    question = st.text_input("Ask about the simulation or features", "Why might apoptosis increase in the drug module?")
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    with col_q1:
        if st.button("Explain simply"):
            st.session_state.q_style = "simple"
    with col_q2:
        if st.button("High school style"):
            st.session_state.q_style = "hs"
    with col_q3:
        if st.button("Researcher style"):
            st.session_state.q_style = "researcher"
    with col_q4:
        if st.button("Investor / judge"):
            st.session_state.q_style = "investor"

    for suggestion in cards_for(mode):
        if st.button(suggestion, key=f"sug_{suggestion}"):
            st.session_state.pending_q = suggestion

    pending = st.session_state.pop("pending_q", None)
    if pending:
        question = pending
    q_style = st.session_state.get("q_style", "balanced")
    if st.button("Run explanation"):
        st.session_state.explain_cache = answer_question(question, ctx, style=q_style)

    if st.session_state.explain_cache:
        st.markdown("### Answer")
        st.write(st.session_state.explain_cache)

elif mode == "Edge Biology Assistant":
    st.subheader("Local-first snapshot")
    st.caption(f"Edge PCA: **{edge_src}**")
    st.plotly_chart(
        figure_pca_scatter(
            edge_pca_df[["PC1", "PC2"]].to_numpy(),
            label_names=edge_pca_df["edge_state"].astype(str).to_numpy(),
            title="Edge dataset — PCA",
        ),
        use_container_width=True,
    )

    sim_resp = float(np.clip(0.3 + signal_strength * 0.5 - noise_level * 0.25, 0, 1))
    st.metric("Tiny signal-response readout (demo)", f"{sim_resp:.2f}")

    q_edge = st.text_input("Edge assistant prompt", "Summarize how these edge states differ.")
    if st.button("Answer locally"):
        st.session_state.explain_cache = answer_question(q_edge, ctx, style="hs")

    if st.session_state.explain_cache:
        st.markdown("### Explanation")
        st.write(st.session_state.explain_cache)

st.markdown("---")
st.markdown("### Related concepts")
cols = st.columns(3)
for i, card in enumerate(cards_for(mode)):
    cols[i % 3].markdown(f"- {card}")

explain_box = st.empty()
if run_gemini or auto_explain:
    src, text, hint = explain_with_optional_gemini(ctx)
    badge = "**(gemini)**" if src == "gemini" else "**(template)**"
    explain_box.markdown(f"### Gemma / Gemini explanation {badge}")
    if hint:
        explain_box.caption(hint)
    explain_box.write(text)
elif mode not in ("Explainable Cell AI", "Edge Biology Assistant"):
    st.caption(
        "Sidebar → **Explain with Gemini / template** (one shot) or **Auto-explain on change**. "
        "Look for **(gemini)** vs **(template)** in the heading above."
    )
