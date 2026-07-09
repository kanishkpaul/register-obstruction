"""Illustrative, PRONOUN-ONLY register classifier.

This is a teaching example, not the research instrument. It keys only on the
second-person honorific *pronouns*, which are dictionary-level common knowledge:

    Bengali:  আপনি (formal) · তুমি (familiar) · তুই (intimate)
    Hindi:    आप   (formal) · तुम  (familiar) · तू   (intimate)

The validated instrument used for the study additionally reads verb-suffix
morphology, resolves syncretic forms (e.g. Hindi `-ते हैं` across
formal/1pl/3pl), and handles idiomatic exceptions — none of which is included
here. Expect this demo to return NEUTRAL on register-bearing sentences that
carry the register only in the verb, not the pronoun.
"""

from __future__ import annotations

from .core import Cue, Language, Register, RegisterClassifier, RegisterLabel, normalize

# Dictionary-level honorific pronoun sets (surface variants included).
_PRONOUNS: dict[Language, dict[Register, tuple[str, ...]]] = {
    Language.BENGALI: {
        Register.FORMAL: ("আপনি", "আপনারা", "আপনার", "আপনাকে"),
        Register.FAMILIAR: ("তুমি", "তোমরা", "তোমার", "তোমাকে"),
        Register.INTIMATE: ("তুই", "তোরা", "তোর", "তোকে"),
    },
    Language.HINDI: {
        Register.FORMAL: ("आप", "आपको", "आपका", "आपके"),
        Register.FAMILIAR: ("तुम", "तुम्हें", "तुम्हारा", "तुम्हारे"),
        Register.INTIMATE: ("तू", "तुझे", "तेरा", "तेरे"),
    },
}


class PronounRegisterClassifier(RegisterClassifier):
    """Minimal classifier satisfying the `RegisterClassifier` protocol."""

    def __init__(self, language: Language) -> None:
        self.language = language
        self._table = _PRONOUNS[language]

    def classify(self, text: str) -> RegisterLabel:
        tokens = set(normalize(text).replace("?", " ").replace("।", " ").split())
        cues: list[Cue] = []
        for register, forms in self._table.items():
            for form in forms:
                if form in tokens:
                    cues.append(Cue(surface=form, register=register, strength="strong"))

        found = {c.register for c in cues}
        if not found:
            return RegisterLabel(Register.NEUTRAL, self.language, 0.0, cues)
        if len(found) > 1:
            return RegisterLabel(Register.MIXED, self.language, 0.5, cues)
        (register,) = found
        return RegisterLabel(register, self.language, 1.0, cues)
