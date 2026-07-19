# register-obstruction

[![tests](https://github.com/kanishkpaul/register-obstruction/actions/workflows/ci.yml/badge.svg)](https://github.com/kanishkpaul/register-obstruction/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Can "untranslatability" be measured — and does it predict where machine translation quietly fails?**

> Part of a research series — see also
> [arc-agi3-world-models](https://github.com/kanishkpaul/arc-agi3-world-models) and
> [butterflygate](https://github.com/kanishkpaul/butterflygate) ·
> write-ups at [kanishkpaul.com/research](https://kanishkpaul.com/research)

A fully-local, zero-budget empirical study of a specific, hard case:
the three-way honorific **register** distinction (formal / familiar / intimate)
that Bengali and Hindi mark grammatically but English does not. When a
translation pipeline routes **Bn → English → Hi**, the English intermediate
removes the overt grammatical signal and the system has to *guess* the
honorific level on the way back out. Whether that causes additional loss beyond
direct Bn → Hi translation is an empirical, model-dependent question.

> **Status — active research preview.** Classifier validation and aggregate
> direct-vs-pivot register-fidelity baselines are complete and public here. The
> proposed cohomological-style *contextual-fraction* obstruction, its linear
> program, and the correlation analysis have **not yet been run**. The central
> obstruction hypothesis remains preregistered and untested. The frozen
> sentences and instrument internals remain private pending a write-up. See
> [What's public vs. not public](#whats-public-vs-not-public).

---

## Why this is interesting

Register is not decoration. In Bengali and Hindi the pronoun and verb
morphology *force* a choice — you cannot address someone without encoding
formal / familiar / intimate. English has no grammatical equivalent, so any
translation that passes through English loses the marking and has to
re-hallucinate it. The hypothesis under test:

> Cross-lingual untranslatability of a feature can be quantified as a
> **contextual obstruction**, and that obstruction predicts where
> translate-through-English pipelines produce register-inappropriate output.

This is a clean, falsifiable instance of a general question about what pivot
languages destroy — with a pre-registered kill criterion (below).

## The instrument (this is the part you can inspect here)

The measurement depends on a **rule-based register classifier** for each
language — deliberately *not* an LLM, to avoid translationese bias in the
ground truth. The classifier reads pronouns and verb-suffix morphology and
emits `FORMAL / FAMILIAR / INTIMATE / NEUTRAL` with a cue-level audit trail.

Validation gate (precision ≥ 0.90 on all three register classes, both
languages) — **passed**:

| language | FORMAL | FAMILIAR | INTIMATE |
|---|---|---|---|
| Bengali | 1.00 | 1.00 | 0.92 |
| Hindi   | 1.00 | 0.96 | 1.00 |

**Honest methodology note.** The validation labels above were produced by
Claude, not by independent human annotation. The 309 frozen-item verification
decisions were also produced by Claude, contrary to the original plan for a
native-speaker review. The numbers measure *classifier-vs-LLM agreement*, not
human-verified ground truth. Every private record is tagged with that
provenance; no claim of human validation is made.

A second finding surfaced during validation and is worth stating because it
generalizes beyond this project: **Hindi present/progressive conjugation is
syncretic** across 2nd-person-formal, 1st-plural, and 3rd-plural
(`-ते हैं` / `-रहे हैं`), so Hindi carries structurally more register ambiguity
than Bengali. Any register classifier — rule-based or learned — inherits this.

## Aggregate direct-vs-pivot evidence

Register survival on 256 implicit, register-bearing items:

| system | direct Bn→Hi | pivot Bn→En→Hi | direct minus pivot |
|---|---:|---:|---:|
| IndicTrans2 | 38.67% | 39.45% | -0.78 pp |
| NLLB | 36.72% | 34.38% | +2.34 pp |
| Gemma 3 12B | 62.50% | 40.63% | +21.88 pp |
| Llama 3.1 8B | 55.86% | 37.11% | +18.75 pp |
| Qwen3 8B | 53.91% | 37.11% | +16.80 pp |

Dedicated MT already loses most register information on the direct path; the
English pivot adds little consistent damage for those two systems. All three
general LLM translators show a large additional pivot penalty. The detailed
aggregate CSVs, validation confusion counts, hashes, and limitations are in
[`results/`](results/) and
[`docs/evidence-and-limitations.md`](docs/evidence-and-limitations.md).

These are register-fidelity baselines, **not obstruction scores**.

## Study design

```
mine aligned Bn–En–Hi dialogue triples  (OPUS OpenSubtitles, CoCoA-MT)
        │
        ▼
rule-based register labels + explicit/implicit context variants
        │
        ▼
run translation grid:  direct Bn→Hi   vs   pivot Bn→En→Hi
   across local 4-bit models (IndicTrans2, NLLB, general LLMs)
        │
        ▼
per-item obstruction  ⟶  correlate with downstream register-inappropriateness
```

Everything runs on a single 16 GB Mac (MLX / llama.cpp, 4-bit quants,
one model at a time, checkpointed to disk). No cloud, no paid annotation.

## Pre-registered predictions

Registered *before* running the analysis, reported either way:

1. Obstruction ≈ 0 for direct Bn→Hi on register-neutral controls and
   explicit-context items.
2. Obstruction significantly positive for implicit-register items on pivot
   (Bn→En→Hi) paths.
3. Item-level obstruction correlates (Spearman ρ > 0.3, p < 0.01) with
   downstream register-inappropriateness of final outputs.

**Failure of prediction 3 kills the theory.** That criterion is fixed in
advance; the analysis has not yet been run.

## Try the interface

The label space, cue record, and classifier protocol are public
(`src/register/core.py`), plus a deliberately minimal **pronoun-only** demo
classifier — textbook honorifics (আপনি/তুমি/তুই, आप/तुम/तू), *not* the validated
morphological instrument. Pure Python, no deps to run it:

```bash
pip install -e ".[dev]"
pytest -q                  # 6 passing tests
python examples/demo.py
python scripts/check_public_results.py
```

```
[hi]
  FORMAL     (cue: आप)   आप कैसे हैं?
  FAMILIAR   (cue: तुम)   तुम कहाँ जा रहे हो?
  INTIMATE   (cue: तू)    तू क्या कर रहा है?
  NEUTRAL    (cue: —)     आज बारिश होगी।
```

The demo returns NEUTRAL when register lives only in the verb, not the pronoun —
which is exactly what the withheld morphological instrument exists to catch. See
[`docs/methodology.md`](docs/methodology.md) for the study design and metric
definitions.

## What's public vs. not public

| Public here | Not public here |
|---|---|
| Research design and preregistered predictions | The planned contextual-fraction LP implementation |
| Register-classifier interface, aggregate validation metrics, and confusion counts | Classifier cue tables and morphological internals |
| Aggregate direct-vs-pivot register-fidelity results | Frozen sentences, mined triples, and per-item outputs |
| Private source commit and artifact hashes | Register-restoration system internals |
| Explicit current phase status and limitations | Contextual-fraction scores and correlations, which have not yet been produced |

If you're evaluating this for a role: happy to walk through the private
instrument and current results directly. Dataset and instrument omissions
protect publication priority; unfinished analysis is labeled unfinished above.

## Author

Kanishk Paul — [kanishkpaul.com](https://kanishkpaul.com) ·
[github.com/kanishkpaul](https://github.com/kanishkpaul)
Write-up: kanishkpaul.com/research
