"""Entropy, mutual information, fidelity, and information loss (binned)."""

from __future__ import annotations

import numpy as np
from scipy.stats import entropy as scipy_entropy
from sklearn.metrics import mutual_info_score


def _discretize(x: np.ndarray, bins: int = 16) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    # Avoid degenerate bins when signal is flat
    if np.nanstd(x) < 1e-9:
        return np.zeros_like(x, dtype=int)
    qs = np.linspace(0, 1, bins + 1)
    edges = np.quantile(x, qs)
    edges = np.unique(edges)
    if len(edges) < 2:
        return np.zeros_like(x, dtype=int)
    return np.digitize(x, edges[1:-1], right=False)


def entropy_bits(x: np.ndarray, bins: int = 16) -> float:
    disc = _discretize(x, bins=bins)
    _, counts = np.unique(disc, return_counts=True)
    p = counts / counts.sum()
    return float(scipy_entropy(p, base=2))


def mutual_information_bits(x: np.ndarray, y: np.ndarray, bins: int = 16) -> float:
    xd = _discretize(x, bins=bins)
    yd = _discretize(y, bins=bins)
    return float(mutual_info_score(xd, yd))


def signal_fidelity(x: np.ndarray, y: np.ndarray, bins: int = 16) -> float:
    h = entropy_bits(x, bins=bins)
    if h < 1e-9:
        return 0.0
    mi = mutual_information_bits(x, y, bins=bins)
    return float(np.clip(mi / h, 0.0, 1.0))


def information_loss_fraction(x: np.ndarray, y: np.ndarray, bins: int = 16) -> float:
    return float(np.clip(1.0 - signal_fidelity(x, y, bins=bins), 0.0, 1.0))


def channel_capacity_approx(mi_bits: float, noise_level: float) -> float:
    """Rough demo scalar: MI scaled down as noise increases."""
    return float(max(0.0, mi_bits * (1.0 - 0.65 * noise_level)))
