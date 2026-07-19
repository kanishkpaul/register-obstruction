"""register — public interface + an illustrative pronoun-only classifier.

The validated morphological instrument (cue tables, verb-suffix rules, and
syncretism handling) is withheld pending publication. The preregistered
contextual-fraction measurement has not yet been run. See the README.
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
