#!/usr/bin/env python3
"""
BioChannel promo video builder.

1. Calls Gemini (GOOGLE_API_KEY in repo-root .env) to generate a scientific narration.
2. macOS: Text-to-speech via `say`.
3. Muxes narration with images in private/marketing/images/ using ffmpeg from imageio-ffmpeg.

Usage (from repo root):
  python private/marketing/build_promo_video.py

Requires: network for Gemini on first run.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

MARKETING = Path(__file__).resolve().parent
ROOT = MARKETING.parent.parent  # bio-channel/
IMAGES = MARKETING / "images"
VIDEOS = MARKETING / "videos"

REFERENCE_SNIPPETS = """
BioChannel is a Streamlit scientific dashboard that models cells as noisy communication channels:
signal → pathway → gene expression → decisions (proliferation, apoptosis, dormancy, resistance).
Modules: Cell Decision Simulator (PCA landscape + softmax decisions), Information Loss Analyzer
(entropy, mutual information, fidelity), Drug Response Predictor (dose–response, resistance),
Explainable Cell AI (feature importance + Gemini explanations), Edge Biology Assistant (lightweight PCA).
Kaggle notebooks export CSVs to data/processed/; the app loads real outputs or demo fallbacks.
The UI shows a principal-component scatter plot of cell states and a bar chart of decision probabilities.
"""


def load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env")
    except ImportError:
        pass


def gemini_narration(api_key: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model_name = os.environ.get("BIOCHANNEL_GEMINI_MODEL", "gemini-2.0-flash")
    model = genai.GenerativeModel(model_name)

    prompt = f"""You are writing voice-over narration for a short (~45–75 second) promo video about BioChannel.

Context:
{REFERENCE_SNIPPETS}

Requirements:
- Pleasant, relaxed, conversational tone—warm and easy to listen to, not stiff or lecture-heavy.
- Keep it brief: focus only on why it is useful and how someone uses the app (sidebar, sliders, switching modes).
- Do NOT include stage directions, brackets, timestamps, or bullet lists.
- Plain prose only, two short paragraphs maximum.
- Approximately 90 to 140 words total."""

    resp = model.generate_content(prompt)
    text = (resp.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned empty narration.")
    return text


def strip_for_say(text: str) -> str:
    """Remove markdown artifacts and extra whitespace for macOS say."""
    t = re.sub(r"[`*_#]", "", text)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def synthesize_audio_macos(text: str, out_aiff: Path) -> None:
    txt = out_aiff.with_suffix(".txt")
    txt.write_text(text, encoding="utf-8")
    # Default: Karen (pleasant, relaxed AU English). Override with BIOCHANNEL_VIDEO_VOICE.
    voice = os.environ.get("BIOCHANNEL_VIDEO_VOICE", "Karen")
    rate = os.environ.get("BIOCHANNEL_VIDEO_SPEAKING_RATE", "152").strip()
    cmd = ["say", "-v", voice]
    if rate:
        cmd.extend(["-r", rate])
    cmd.extend(["-f", str(txt), "-o", str(out_aiff)])
    subprocess.run(cmd, check=True, cwd=str(out_aiff.parent))


def wav_duration_seconds(wav_path: Path) -> float:
    import wave

    with wave.open(str(wav_path), "rb") as w:
        return w.getnframes() / float(w.getframerate())


def build_video(ffmpeg_exe: str, narration_audio: Path, out_mp4: Path) -> None:
    imgs = sorted(IMAGES.glob("*.png"))
    if len(imgs) < 1:
        raise FileNotFoundError(f"No PNG images in {IMAGES}")

    dur = wav_duration_seconds(narration_audio)
    # setsar=1 so concat accepts mixed upstream SAR from scale+pad
    vf_scale = (
        "scale=1280:720:force_original_aspect_ratio=decrease,"
        "pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"
    )

    if len(imgs) == 1:
        cmd = [
            ffmpeg_exe,
            "-y",
            "-loop",
            "1",
            "-i",
            str(imgs[0]),
            "-i",
            str(narration_audio),
            "-vf",
            vf_scale,
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-t",
            str(dur),
            str(out_mp4),
        ]
        subprocess.run(cmd, check=True)
        return

    n = len(imgs)
    seg = dur / n
    cmd = [ffmpeg_exe, "-y"]
    for img in imgs:
        cmd += ["-loop", "1", "-t", str(seg), "-i", str(img)]
    audio_ix = n
    cmd += ["-i", str(narration_audio)]
    fc_parts = [
        f"[{i}:v]{vf_scale},setpts=PTS-STARTPTS[v{i}]" for i in range(n)
    ]
    concat_ins = "".join(f"[v{i}]" for i in range(n))
    fc_parts.append(f"{concat_ins}concat=n={n}:v=1:a=0[v]")
    cmd += [
        "-filter_complex",
        ";".join(fc_parts),
        "-map",
        "[v]",
        "-map",
        f"{audio_ix}:a",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True)


def load_narration(api_key: str) -> tuple[str, str]:
    """Returns (narration_text, source_label)."""
    bundled = MARKETING / "narration_biochannel_promo.txt"
    fallback = """BioChannel helps you explore how cells might behave under stress and drugs, without getting lost in spreadsheets. Use the sidebar to pick your scenario and tune the sliders. The maps and probabilities refresh as you go. Switch modes when you want cell decisions, information metrics, drug response, or explainable views. It is a calm way to teach, run quick what-ifs, and walk teammates through your thinking."""

    skip_gemini = os.environ.get("BIOCHANNEL_VIDEO_SKIP_GEMINI", "").strip() in ("1", "true", "yes")

    if bundled.exists() and (skip_gemini or not api_key):
        text = bundled.read_text(encoding="utf-8").strip()
        return text, "bundled_script"

    if api_key and not skip_gemini:
        print("Generating narration with Gemini…")
        try:
            text = gemini_narration(api_key)
            return text, "gemini"
        except Exception as e:
            print(f"Gemini narration failed ({e}); falling back to bundled script.", file=sys.stderr)
            if bundled.exists():
                return bundled.read_text(encoding="utf-8").strip(), "bundled_after_gemini_error"
            return fallback, "inline_fallback"

    if bundled.exists():
        return bundled.read_text(encoding="utf-8").strip(), "bundled_script"

    return fallback, "inline_fallback"


def main() -> int:
    load_env()
    api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    VIDEOS.mkdir(parents=True, exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)

    narration_path = VIDEOS / "biochannel_promo_narration.txt"
    narration, src = load_narration(api_key)
    narration_path.write_text(narration + f"\n\n--- source: {src} ---\n", encoding="utf-8")
    print(f"Narration source: {src}")

    clean = strip_for_say(narration)
    aiff = VIDEOS / "biochannel_promo_voice.aiff"
    wav = VIDEOS / "biochannel_promo_voice.wav"

    print("Synthesizing voice with macOS `say`…")
    try:
        synthesize_audio_macos(clean, aiff)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"ERROR: `say` failed ({e}). Install macOS or set up manual VO.", file=sys.stderr)
        narration_path.write_text(narration + "\n\n", encoding="utf-8")
        return 1

    # Prefer WAV for broader ffmpeg compatibility
    try:
        import imageio_ffmpeg

        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg_exe = "ffmpeg"

    subprocess.run(
        [ffmpeg_exe, "-y", "-i", str(aiff), str(wav)],
        check=True,
        capture_output=True,
    )

    out_mp4 = VIDEOS / "BioChannel_promo.mp4"
    print(f"Assembling video → {out_mp4}")
    try:
        build_video(ffmpeg_exe, wav, out_mp4)
    except Exception as e:
        print(f"ffmpeg assembly failed: {e}", file=sys.stderr)
        print(f"Narration and audio saved under {VIDEOS}. Install imageio-ffmpeg: pip install imageio-ffmpeg", file=sys.stderr)
        return 1

    print(f"Done: {out_mp4}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
