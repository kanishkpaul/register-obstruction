"""register — public interface + an illustrative pronoun-only classifier.

The validated morphological instrument (cue tables, verb-suffix rules, syncretism
handling) and the contextual-fraction obstruction measurement are withheld
pending publication. See the README.
"""

from .core import (
    Cue,
    Language,
    Register,
    RegisterClassifier,
    RegisterLabel,
    normalize,
)
from .demo_classifier import PronounRegisterClassifier

__all__ = [
    "Cue",
    "Language",
    "Register",
    "RegisterClassifier",
    "RegisterLabel",
    "PronounRegisterClassifier",
    "normalize",
]
