"""Classify a few example sentences with the illustrative pronoun-only classifier.

    python examples/demo.py
"""

from __future__ import annotations

from register import Language, PronounRegisterClassifier

EXAMPLES = {
    Language.BENGALI: [
        "আপনি কেমন আছেন?",   # formal
        "তুমি কোথায় যাচ্ছ?",   # familiar
        "তুই কী করছিস?",       # intimate
        "আজ বৃষ্টি হবে।",       # neutral (no 2nd-person pronoun)
    ],
    Language.HINDI: [
        "आप कैसे हैं?",         # formal
        "तुम कहाँ जा रहे हो?",   # familiar
        "तू क्या कर रहा है?",     # intimate
        "आज बारिश होगी।",       # neutral
    ],
}


def main() -> None:
    for lang, sentences in EXAMPLES.items():
        clf = PronounRegisterClassifier(lang)
        print(f"\n[{lang.value}]")
        for s in sentences:
            label = clf.classify(s)
            cue = label.cues[0].surface if label.cues else "—"
            print(f"  {label.register.value:<10} (cue: {cue})  {s}")


if __name__ == "__main__":
    main()
