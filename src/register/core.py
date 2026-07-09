"""Public interface for the register classifier.

This module defines the *shape* of the instrument — the label space, the cue
record, and the classifier protocol — without the validated cue tables and
verb-morphology rules that make up the working instrument (those are withheld
pending publication). A minimal, illustrative pronoun-only classifier that
satisfies this protocol lives in `register.demo_classifier`.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol, runtime_checkable


class Register(str, Enum):
    """The honorific register label space.

    FORMAL / FAMILIAR / INTIMATE are the three grammatically-marked registers.
    NEUTRAL = no register-bearing marker present. AMBIGUOUS = markers present but
    under-determined. MIXED = markers of more than one distinct register.
    """

    FORMAL = "FORMAL"
    FAMILIAR = "FAMILIAR"
    INTIMATE = "INTIMATE"
    NEUTRAL = "NEUTRAL"
    AMBIGUOUS = "AMBIGUOUS"
    MIXED = "MIXED"


class Language(str, Enum):
    BENGALI = "bn"
    HINDI = "hi"


@dataclass(frozen=True)
class Cue:
    """One surface marker that fired, with the register it evidences and a
    coarse strength. `strong` cues (e.g. dedicated pronouns) override `weak`
    ones (e.g. syncretic suffixes) at aggregation time."""

    surface: str
    register: Register
    strength: str = "strong"  # "strong" | "weak"


@dataclass
class RegisterLabel:
    """The classifier's decision for one span of text."""

    register: Register
    language: Language
    confidence: float = 0.0
    cues: list[Cue] = field(default_factory=list)

    def is_marked(self) -> bool:
        return self.register in {
            Register.FORMAL,
            Register.FAMILIAR,
            Register.INTIMATE,
        }


@runtime_checkable
class RegisterClassifier(Protocol):
    """A register classifier reads text and returns a `RegisterLabel`.

    Implementations must be deterministic and must NOT call an LLM in the
    measurement loop (translationese bias) — the instrument is rule-based by
    design."""

    language: Language

    def classify(self, text: str) -> RegisterLabel: ...


def normalize(text: str) -> str:
    """NFC-normalize Indic text before any cue matching (project convention)."""
    return unicodedata.normalize("NFC", text)
