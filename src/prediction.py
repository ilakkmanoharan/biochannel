"""Drug-response style predictions from dose, duration, and resistance context."""

from __future__ import annotations

from typing import Optional

import numpy as np

from .simulation import decision_probabilities


def map_duration(duration: str) -> float:
    return {"Short": 0.25, "Medium": 0.5, "Long": 0.85}.get(duration, 0.5)


def drug_outcomes(
    *,
    dose: float,
    duration: str,
    resistance_pressure: float,
    cell_state: str,
    constraint: Optional[str],
    dataset_row: Optional[dict] = None,
    stress_level_slider: float = 0.35,
    drug_pressure_slider: float = 0.2,
) -> dict[str, float]:
    """Combine softmax decision layer with dose–response shaping."""
    dur = map_duration(duration)
    effective_signal = 0.35 + 0.55 * dose * (0.55 + 0.45 * dur)
    noise_level = 0.18 + 0.35 * resistance_pressure

    probs = decision_probabilities(
        signal_strength=effective_signal,
        noise_level=min(1.0, noise_level),
        cell_state=cell_state,
        signal_type="Drug signal",
        constraint=constraint,
        resistance_pressure=resistance_pressure,
        stress_level_slider=stress_level_slider,
        drug_pressure_slider=drug_pressure_slider,
    )

    apoptosis = probs["apoptosis"]
    survival = probs["proliferation"] + probs["dormancy"] * 0.35 + probs["stress_adaptation"] * 0.2
    sensitivity = float(
        np.clip(apoptosis * (1.1 - resistance_pressure) + dose * 0.15, 0.0, 1.0)
    )

    resistance_out = float(probs["resistance"])
    if dataset_row:
        if "sensitivity" in dataset_row and dataset_row["sensitivity"] is not None:
            sens_d = float(np.clip(dataset_row["sensitivity"], 0.0, 1.0))
            sensitivity = float(np.clip(0.4 * sensitivity + 0.6 * sens_d, 0.0, 1.0))
        if "apoptosis_proxy" in dataset_row and dataset_row["apoptosis_proxy"] is not None:
            apoptosis = float(
                np.clip(0.45 * apoptosis + 0.55 * float(dataset_row["apoptosis_proxy"]), 0.0, 1.0)
            )
        if "survival_proxy" in dataset_row and dataset_row["survival_proxy"] is not None:
            survival = float(
                np.clip(0.45 * survival + 0.55 * float(dataset_row["survival_proxy"]), 0.0, 1.0)
            )
        if "resistance_risk" in dataset_row and dataset_row["resistance_risk"] is not None:
            resistance_out = float(
                np.clip(
                    0.5 * resistance_out + 0.5 * float(dataset_row["resistance_risk"]),
                    0.0,
                    1.0,
                )
            )

    if constraint == "Maximize apoptosis":
        ranking = ["↑ dose / duration", "↓ resistance context", "consider combination"]
    elif constraint == "Minimize resistance":
        ranking = ["rotate therapy", "↑ dose gradually", "target parallel pathway"]
    elif constraint == "Reduce toxicity":
        ranking = ["↓ dose with longer duration", "pulse scheduling", "biomarker gate"]
    elif constraint == "Preserve normal-like cells":
        ranking = ["windowed dosing", "selective drug", "lower peak concentration"]
    elif constraint == "Maximize signal clarity":
        ranking = ["reduce extrinsic noise", "stagger stimuli", "feedback inhibitors"]
    else:
        ranking = ["explore dose near IC50", "extend duration", "check resistance markers"]

    return {
        "apoptosis": apoptosis,
        "survival": float(np.clip(survival, 0.0, 1.0)),
        "resistance": resistance_out,
        "sensitivity_score": sensitivity,
        "intervention_ranking": ranking,
    }
