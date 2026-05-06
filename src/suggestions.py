"""Learning-card suggestions per module."""

from __future__ import annotations

SUGGESTIONS: dict[str, list[str]] = {
    "Cell Decision Simulator": [
        "What does dormancy mean?",
        "Why do cells choose apoptosis?",
        "What is cellular noise?",
        "What is signal transduction?",
        "Why do cancer cells resist signals?",
    ],
    "Information Loss Analyzer": [
        "What is mutual information?",
        "What is channel capacity?",
        "Why does noise reduce fidelity?",
        "What is intrinsic vs extrinsic noise?",
        "How do feedback loops affect information flow?",
    ],
    "Drug Response Predictor": [
        "Why do cells become drug resistant?",
        "What is a dose-response curve?",
        "What does apoptosis probability mean?",
        "How can combination therapy improve response?",
    ],
    "Explainable Cell AI": [
        "Explain this result simply",
        "Explain like I am a high school student",
        "Explain like a biology researcher",
        "What changed from the previous input?",
        "What should I try next?",
    ],
    "Edge Biology Assistant": [
        "How can biology AI run locally?",
        "Why does offline AI matter for science education?",
        "How can students use gene expression data?",
    ],
}


def cards_for(module: str) -> list[str]:
    return list(SUGGESTIONS.get(module, []))
