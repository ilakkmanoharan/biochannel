"""Structured BioChannel explanations: template fallback + optional Gemini API."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExplainContext:
    module_name: str
    dataset_name: str
    signal_type: str
    signal_strength: float
    noise_level: float
    cell_state: str
    constraint: Optional[str]
    proliferation: float
    apoptosis: float
    dormancy: float
    resistance: float
    stress_adaptation: float
    mi: Optional[float]
    info_loss: Optional[float]
    signal_fidelity: Optional[float]
    top_features: str


PROMPT_TEMPLATE = """You are BioChannel, an AI biology reasoning assistant.

The user is exploring a cellular signaling simulation.

Module:
{module_name}

Dataset:
{dataset_name}

Selected inputs:
- Signal type: {signal_type}
- Signal strength: {signal_strength}
- Noise level: {noise_level}
- Cell state: {cell_state}
- Constraint: {constraint}

Computed outputs:
- Proliferation probability: {proliferation}
- Apoptosis probability: {apoptosis}
- Dormancy probability: {dormancy}
- Resistance probability: {resistance}
- Stress adaptation probability: {stress_adaptation}
- Mutual information (bits, approx.): {mi}
- Information loss: {info_loss}
- Signal fidelity: {signal_fidelity}

Top features or genes:
{top_features}

Explain:
1. What biological condition this resembles.
2. Why the output changed.
3. What the user should learn.
4. One suggested next experiment.

Keep the answer clear, grounded, and avoid medical advice."""


def _fmt(v: Optional[float], digits: int = 3) -> str:
    if v is None:
        return "n/a"
    return f"{v:.{digits}f}"


def build_prompt(ctx: ExplainContext) -> str:
    return PROMPT_TEMPLATE.format(
        module_name=ctx.module_name,
        dataset_name=ctx.dataset_name,
        signal_type=ctx.signal_type,
        signal_strength=ctx.signal_strength,
        noise_level=ctx.noise_level,
        cell_state=ctx.cell_state,
        constraint=ctx.constraint or "(none)",
        proliferation=_fmt(ctx.proliferation),
        apoptosis=_fmt(ctx.apoptosis),
        dormancy=_fmt(ctx.dormancy),
        resistance=_fmt(ctx.resistance),
        stress_adaptation=_fmt(ctx.stress_adaptation),
        mi=_fmt(ctx.mi) if ctx.mi is not None else "n/a",
        info_loss=_fmt(ctx.info_loss) if ctx.info_loss is not None else "n/a",
        signal_fidelity=_fmt(ctx.signal_fidelity) if ctx.signal_fidelity is not None else "n/a",
        top_features=ctx.top_features,
    )


def template_explanation(ctx: ExplainContext) -> str:
    """Heuristic explanation when no LLM is configured."""
    parts = []
    parts.append(
        f"This setup ({ctx.module_name} on **{ctx.dataset_name}**) resembles a "
        f"{ctx.cell_state.lower()} context with **{ctx.signal_type.lower()}** at strength {_fmt(ctx.signal_strength)} "
        f"and noise {_fmt(ctx.noise_level)}."
    )
    if ctx.noise_level > 0.55:
        parts.append(
            "Higher noise tends to **blur** input–output mapping, favoring cautious states such as dormancy or adaptation."
        )
    elif ctx.noise_level < 0.25:
        parts.append("Low noise supports **clearer** signaling, so proliferation can dominate when growth cues are present.")

    parts.append(
        f"Model probabilities: proliferation {_fmt(ctx.proliferation)}, apoptosis {_fmt(ctx.apoptosis)}, "
        f"dormancy {_fmt(ctx.dormancy)}, resistance {_fmt(ctx.resistance)}."
    )

    if ctx.signal_fidelity is not None and ctx.info_loss is not None:
        parts.append(
            f"Information view: fidelity ≈ {_fmt(ctx.signal_fidelity)} with loss ≈ {_fmt(ctx.info_loss)} "
            "(binned MI vs input entropy — illustrative for the demo)."
        )

    if ctx.constraint:
        parts.append(f"Active constraint **{ctx.constraint}** steers the scoring rules toward that optimization goal.")

    parts.append(
        f"Evidence hooks: {ctx.top_features}. "
        "Try varying noise and signal strength together to see trade-offs between growth and safety states."
    )
    parts.append(
        "**Next experiment (conceptual):** perturb one pathway readout while holding stimulus fixed to test whether fidelity drops."
    )
    return "\n\n".join(parts)


def explain_with_optional_gemini(ctx: ExplainContext) -> tuple[str, str, str]:
    """
    Returns (source, text, hint).

    source is 'gemini' or 'template'. hint is empty when Gemini succeeds; otherwise a short reason
    (no API key, import error, API error, empty model response).
    """
    api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not api_key:
        return (
            "template",
            template_explanation(ctx),
            "No `GOOGLE_API_KEY` in the environment. Add it to `.env` or export it before `streamlit run`.",
        )

    try:
        import google.generativeai as genai  # type: ignore
    except ImportError:
        return (
            "template",
            template_explanation(ctx),
            "Package `google-generativeai` not installed. Run: `pip install -r requirements.txt`",
        )

    try:
        genai.configure(api_key=api_key)
        model_name = os.environ.get("BIOCHANNEL_GEMINI_MODEL", "gemini-2.0-flash")
        model = genai.GenerativeModel(model_name)
        prompt = build_prompt(ctx)
        resp = model.generate_content(prompt)
        text = (resp.text or "").strip()
        if not text:
            return (
                "template",
                template_explanation(ctx),
                "Gemini returned empty text — using template. Try another model via `BIOCHANNEL_GEMINI_MODEL`.",
            )
        return "gemini", text, ""
    except Exception as e:
        err = str(e).strip().split("\n")[0][:200]
        return (
            "template",
            template_explanation(ctx),
            f"Gemini API error — using template. ({err})",
        )


def answer_question(
    question: str,
    ctx: ExplainContext,
    style: str = "balanced",
) -> str:
    """Short Q&A using template logic; Gemini optional via GOOGLE_API_KEY."""
    q = question.strip().lower()

    style_hint = {
        "simple": "Use short sentences and analogies (water pipe / noisy radio).",
        "researcher": "Use precise terms: pathway, variability, trade-offs, distributions.",
        "hs": "Explain like a curious high school student: plain language, one analogy.",
        "investor": "Executive summary: impact, risk, what was learned, one next step — no jargon wall.",
    }.get(style, "")

    extra = ""
    if "apoptosis" in q:
        extra = "Apoptosis probability rises when drug or stress pressure dominates over survival cues in the demo scoring model."
    elif "information loss" in q or "lose information" in q:
        extra = "Information loss here means output bins carry less predictable information about the input bins (1 − normalized MI)."
    elif "noise" in q:
        extra = "Noise inflates dormancy/adaptation scores and erodes fidelity between stimulus and response traces."
    elif "gene" in q or "feature" in q:
        extra = f"Top discriminating features in the explainable module: {ctx.top_features}."

    api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if api_key:
        try:
            import google.generativeai as genai  # type: ignore

            genai.configure(api_key=api_key)
            model_name = os.environ.get("BIOCHANNEL_GEMINI_MODEL", "gemini-2.0-flash")
            model = genai.GenerativeModel(model_name)
            prompt = (
                build_prompt(ctx)
                + f"\n\nUser question: {question}\nAnswer style: {style_hint or 'clear and concise'}.\n"
                "Answer in 2–4 short paragraphs. Avoid medical advice."
            )
            resp = model.generate_content(prompt)
            text = (resp.text or "").strip()
            if text:
                return text
        except Exception:
            pass

    base = template_explanation(ctx)
    return (extra + "\n\n" if extra else "") + base
