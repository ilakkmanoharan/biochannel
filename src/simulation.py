"""Probabilistic cell-decision layer (softmax scores per specification)."""

from __future__ import annotations

from typing import Optional

import numpy as np

STATE_KEYS = ("proliferation", "apoptosis", "dormancy", "stress_adaptation", "resistance")


def softmax(scores: dict[str, float]) -> dict[str, float]:
    keys = list(scores.keys())
    v = np.array([scores[k] for k in keys], dtype=float)
    v = v - np.max(v)
    e = np.exp(v)
    p = e / e.sum()
    return {k: float(x) for k, x in zip(keys, p)}


def stress_level_from_cell_state(cell_state: str) -> float:
    return {
        "Normal-like": 0.15,
        "Cancer-like": 0.35,
        "Stressed": 0.65,
        "Resistant": 0.55,
        "Dormant": 0.45,
    }.get(cell_state, 0.35)


def drug_pressure_from_constraint(constraint: Optional[str], signal_type: str) -> float:
    if signal_type == "Drug signal":
        return 0.35
    return 0.12


def compute_decision_scores(
    *,
    signal_strength: float,
    noise_level: float,
    cell_state: str,
    signal_type: str,
    constraint: Optional[str],
    resistance_pressure: float = 0.35,
    stress_level_slider: float = 0.35,
    drug_pressure_slider: float = 0.2,
) -> dict[str, float]:
    base_stress = stress_level_from_cell_state(cell_state)
    stress_level = float(np.clip(base_stress + float(stress_level_slider) * 0.55, 0.0, 1.0))
    base_dp = drug_pressure_from_constraint(constraint, signal_type)
    drug_pressure = float(np.clip(base_dp + float(drug_pressure_slider) * 0.5, 0.0, 1.0))

    if constraint == "Fast response":
        signal_strength = min(1.0, signal_strength + 0.1)
    if constraint == "Stable response":
        noise_level = max(0.0, noise_level - 0.1)
    if constraint == "Maximize survival":
        resistance_pressure = min(1.0, resistance_pressure + 0.2)
        stress_level = max(0.0, stress_level - 0.1)
    if constraint == "Maximize apoptosis":
        drug_pressure = min(1.0, drug_pressure + 0.25)
    if constraint == "Minimize resistance":
        resistance_pressure = max(0.0, resistance_pressure - 0.18)
        drug_pressure = min(1.0, drug_pressure + 0.12)

    proliferation_score = signal_strength - stress_level - drug_pressure
    apoptosis_score = drug_pressure + stress_level - resistance_pressure
    dormancy_score = stress_level + noise_level - 0.25 * signal_strength
    stress_adaptation = stress_level + 0.35 * noise_level - 0.2 * drug_pressure
    resistance_score = resistance_pressure + noise_level + drug_pressure * 0.5

    return {
        "proliferation": proliferation_score,
        "apoptosis": apoptosis_score,
        "dormancy": dormancy_score,
        "stress_adaptation": stress_adaptation,
        "resistance": resistance_score,
    }


def decision_probabilities(**kwargs) -> dict[str, float]:
    scores = compute_decision_scores(**kwargs)
    return softmax(scores)
