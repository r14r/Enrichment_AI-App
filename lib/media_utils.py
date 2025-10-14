"""Utility helpers for media-centric mini apps."""
from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Iterable, List, Mapping

__all__ = [
    "segments_to_srt",
    "segments_to_vtt",
    "slugify",
    "read_binary",
]


def _split_timestamp(seconds: float) -> tuple[int, int, int, int]:
    """Return (hours, minutes, seconds, milliseconds) for a float timestamp."""
    seconds = max(0.0, float(seconds))
    fractional, integer = math.modf(seconds)
    milliseconds = int(round(fractional * 1000))
    total_seconds = int(integer)

    # Handle rounding up to the next full second
    if milliseconds >= 1000:
        total_seconds += 1
        milliseconds = 0

    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return int(hours), int(minutes), int(secs), int(milliseconds)


def _format_srt_timestamp(seconds: float) -> str:
    h, m, s, ms = _split_timestamp(seconds)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def _format_vtt_timestamp(seconds: float) -> str:
    h, m, s, ms = _split_timestamp(seconds)
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"


def segments_to_srt(segments: Iterable[Mapping[str, float | str]]) -> str:
    """Create an SRT document from Whisper-like segments."""
    lines: List[str] = []
    for idx, seg in enumerate(segments, start=1):
        start = _format_srt_timestamp(seg.get("start", 0.0))
        end = _format_srt_timestamp(seg.get("end", 0.0))
        text = str(seg.get("text", "")).strip()
        if not text:
            continue
        lines.append(f"{idx}\n{start} --> {end}\n{text}\n")
    return "\n".join(lines).strip() + "\n"


def segments_to_vtt(segments: Iterable[Mapping[str, float | str]]) -> str:
    """Create a WebVTT document from Whisper-like segments."""
    lines: List[str] = ["WEBVTT", ""]
    for seg in segments:
        start = _format_vtt_timestamp(seg.get("start", 0.0))
        end = _format_vtt_timestamp(seg.get("end", 0.0))
        text = str(seg.get("text", "")).strip()
        if not text:
            continue
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines).strip() + "\n"


_slugify_pattern = re.compile(r"[^a-z0-9]+", re.IGNORECASE)


def slugify(value: str, fallback: str = "output") -> str:
    """Turn a string into a filesystem-friendly slug."""
    value = value.strip().lower()
    value = _slugify_pattern.sub("-", value)
    value = value.strip("-")
    return value or fallback


def read_binary(path: Path) -> bytes:
    """Read bytes from *path* and return them."""
    with path.open("rb") as f:
        return f.read()
