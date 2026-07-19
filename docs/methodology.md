# Methodology

This documents the study design and the evaluation metrics. The validated
classifier internals are withheld pending publication. The proposed
contextual-fraction linear program and correlation analysis have not yet been
run; they remain preregistered future phases rather than withheld results.

## Pipeline

```
mine aligned Bn–En–Hi dialogue triples        (OPUS OpenSubtitles, CoCoA-MT)
        │
        ▼
rule-based register labels (per language)  +  explicit/implicit context variants
        │
        ▼
translation grid:   direct Bn→Hi     vs     pivot Bn→En→Hi
   over local 4-bit models (IndicTrans2, NLLB, and general LLMs)
        │
        ▼
per-item obstruction   ─────────►   downstream register-inappropriateness
```

Everything runs on a single 16 GB machine (MLX / llama.cpp, 4-bit quants, one
model loaded at a time, checkpointed to disk). No cloud, no paid annotation.
Indic text is NFC-normalized before any regex/cue matching.

## The instrument

Register is decided by a **deterministic, rule-based** classifier per language —
never an LLM in the measurement loop, to avoid translationese bias. The public
interface (`register.core`) and a pronoun-only illustration
(`register.demo_classifier`) are in this repo; the validated instrument adds
verb-suffix morphology, syncretism resolution, and idiom handling.

## Register-fidelity metrics

For a source item with gold register *g* translated to an output with predicted
register *p*, over a set of items:

| metric | definition |
|---|---|
| **survival** | fraction where *p = g* (the register was preserved) |
| **flip rate** | fraction where *p* is a *different marked* register than *g* |
| **neutralization rate** | fraction where a marked *g* becomes NEUTRAL in *p* (register erased) |
| **hallucination rate** | fraction where a NEUTRAL source acquires a marked register |
| **chrF** | character-n-gram F-score vs the reference (adequacy control, register-blind) |

`direct` vs `pivot` paths are compared on the same items; `explicit` vs
`implicit` conditions vary whether the surrounding context disambiguates the
register. The prediction is that pivoting through English (which does not mark
register) inflates neutralization/flip on `implicit` items specifically.

## Integrity notes

- **Label provenance.** Phase-1 validation labels were produced by an LLM
  (Claude), not by independent human annotation — a deliberate project decision.
  Reported precision therefore measures classifier-vs-LLM agreement, not
  human-verified ground truth. No claim of human validation is made. Every label
  record is tagged with its annotator. The 309 frozen-item verification
  decisions were also produced by Claude rather than the originally planned
  native-speaker review.
- **Pre-registration.** Predictions (including a fixed kill criterion for the
  headline correlation) are registered before the analysis is run and reported
  regardless of outcome.
- **No tuning toward predictions.** Fixes to the instrument are validated on
  fresh, non-overlapping samples — never on the sample that motivated the fix.
