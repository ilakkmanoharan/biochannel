"""Plotly figures for BioChannel."""

from __future__ import annotations

from typing import Iterable, List, Optional, Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def figure_pca_scatter(
    coords: np.ndarray,
    labels: Optional[np.ndarray] = None,
    *,
    label_names: Union[List[str], np.ndarray, None] = None,
    title: str = "PCA embedding (demo)",
) -> go.Figure:
    if label_names is not None:
        codes = pd.Categorical(np.asarray(label_names).astype(str)).codes
        fig = go.Figure(
            data=go.Scatter(
                x=coords[:, 0],
                y=coords[:, 1],
                mode="markers",
                marker=dict(size=8, opacity=0.75, color=codes, colorscale="Viridis", showscale=False),
                text=[str(x) for x in np.asarray(label_names).astype(str)],
                hovertemplate="%{text}<extra></extra>",
            )
        )
    elif labels is not None:
        fig = go.Figure(
            data=go.Scatter(
                x=coords[:, 0],
                y=coords[:, 1],
                mode="markers",
                marker=dict(size=8, opacity=0.75, color=labels.astype(int), colorscale="Viridis"),
                text=[f"cell {i}" for i in range(len(coords))],
            )
        )
    else:
        fig = go.Figure(
            data=go.Scatter(
                x=coords[:, 0],
                y=coords[:, 1],
                mode="markers",
                marker=dict(size=8, opacity=0.75, color="#3b82f6"),
            )
        )
    fig.update_layout(
        title=title,
        xaxis_title="PC1",
        yaxis_title="PC2",
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#111827",
        font=dict(color="#e5e7eb"),
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


def figure_bar_probabilities(probs: dict[str, float], title: str = "Predicted cell decisions") -> go.Figure:
    keys = list(probs.keys())
    vals = [probs[k] for k in keys]
    fig = go.Figure(
        data=go.Bar(
            x=keys,
            y=vals,
            marker_color="#22c55e",
            text=[f"{v:.2f}" for v in vals],
            textposition="auto",
        )
    )
    fig.update_layout(
        title=title,
        yaxis_title="Probability",
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#111827",
        font=dict(color="#e5e7eb"),
        margin=dict(l=40, r=20, t=50, b=80),
        xaxis_tickangle=-25,
    )
    fig.update_yaxes(range=[0, 1])
    return fig


def figure_noise_curve(noise_grid: np.ndarray, metric: np.ndarray, title: str) -> go.Figure:
    fig = go.Figure(
        data=go.Scatter(x=noise_grid, y=metric, mode="lines+markers", line=dict(color="#38bdf8"))
    )
    fig.update_layout(
        title=title,
        xaxis_title="Noise level",
        yaxis_title="Value",
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#111827",
        font=dict(color="#e5e7eb"),
    )
    return fig


def figure_input_output_hist(stimulus: np.ndarray, response: np.ndarray) -> go.Figure:
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Input (stimulus)", "Output (response)"))
    fig.add_trace(go.Histogram(x=stimulus, nbinsx=20, marker_color="#a78bfa", name="stimulus"), row=1, col=1)
    fig.add_trace(go.Histogram(x=response, nbinsx=20, marker_color="#34d399", name="response"), row=1, col=2)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#111827",
        font=dict(color="#e5e7eb"),
        showlegend=False,
        title_text="Input vs output distributions",
    )
    return fig


def figure_info_bars(
    labels: Iterable[str],
    values: Iterable[float],
    title: str,
) -> go.Figure:
    lab = list(labels)
    val = list(values)
    fig = go.Figure(
        data=go.Bar(
            x=lab,
            y=val,
            marker_color=["#f97316" if "loss" in x.lower() else "#60a5fa" for x in lab],
        )
    )
    fig.update_layout(
        title=title,
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#111827",
        font=dict(color="#e5e7eb"),
    )
    return fig


def figure_dose_response(doses: np.ndarray, response: np.ndarray, title: str = "Dose–response (demo)") -> go.Figure:
    fig = go.Figure(
        data=go.Scatter(
            x=doses,
            y=response,
            mode="lines+markers",
            fill="tozeroy",
            line=dict(color="#f472b6"),
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Relative dose",
        yaxis_title="Predicted apoptotic pressure",
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#111827",
        font=dict(color="#e5e7eb"),
    )
    return fig


def figure_survival_apoptosis(doses: np.ndarray, apoptosis: np.ndarray, survival: np.ndarray) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=doses, y=apoptosis, name="Apoptosis", mode="lines+markers", line=dict(color="#fb7185"))
    )
    fig.add_trace(
        go.Scatter(x=doses, y=survival, name="Survival index", mode="lines+markers", line=dict(color="#4ade80"))
    )
    fig.update_layout(
        title="Survival vs apoptosis across dose",
        xaxis_title="Dose",
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#111827",
        font=dict(color="#e5e7eb"),
    )
    return fig


def figure_feature_importance(names: list[str], scores: list[float]) -> go.Figure:
    order = np.argsort(scores)[::-1][:15]
    n = [names[i] for i in order]
    s = [scores[i] for i in order]
    fig = go.Figure(
        data=go.Bar(
            x=s[::-1],
            y=n[::-1],
            orientation="h",
            marker_color="#93c5fd",
        )
    )
    fig.update_layout(
        title="Top feature importance (random forest)",
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#111827",
        font=dict(color="#e5e7eb"),
        margin=dict(l=120, r=20, t=50, b=40),
    )
    return fig


def resistance_gauge(value: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=float(np.clip(value, 0, 1)) * 100,
            title={"text": "Resistance risk (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#f43f5e"},
                "steps": [
                    {"range": [0, 40], "color": "#14532d"},
                    {"range": [40, 70], "color": "#854d0e"},
                    {"range": [70, 100], "color": "#7f1d1d"},
                ],
            },
        )
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        font=dict(color="#e5e7eb"),
        height=320,
    )
    return fig
