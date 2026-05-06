"""Normalization and dimensionality reduction helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def scale_expression(X: pd.DataFrame) -> np.ndarray:
    x = np.log1p(np.maximum(X.to_numpy(dtype=float), 0))
    return StandardScaler().fit_transform(x)


def pca_2d(X_scaled: np.ndarray) -> tuple[np.ndarray, PCA]:
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X_scaled)
    return coords, pca


def perturb_expression(X_scaled: np.ndarray, signal_strength: float, noise_level: float) -> np.ndarray:
    """Scale signal and add Gaussian noise in scaled feature space."""
    scaled = X_scaled * (0.55 + 0.9 * signal_strength)
    noise = np.random.default_rng(123).normal(scale=0.08 + 0.55 * noise_level, size=scaled.shape)
    return scaled + noise
