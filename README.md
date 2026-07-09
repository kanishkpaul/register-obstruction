# register-obstruction

[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Can "untranslatability" be measured — and does it predict where machine translation quietly fails?**

> Part of a research series — see also
> [arc-agi3-world-models](https://github.com/kanishkpaul/arc-agi3-world-models) and
> [butterflygate](https://github.com/kanishkpaul/butterflygate) ·
> write-ups at [kanishkpaul.com/research](https://kanishkpaul.com/research)

A fully-local, zero-budget empirical study of a specific, hard case:
the three-way honorific **register** distinction (formal / familiar / intimate)
that Bengali and Hindi mark grammatically but English does not. When a
translation pipeline routes **Bn → English → Hi**, English acts as a
register-destroying pivot — the system has to *guess* the honorific level on the
way back out. This project quantifies how badly, per sentence, and tests whether
that quantity predicts downstream failure.

> **Status — method paper in preparation.** This is a public *showcase* of the
> engineering and the research design. The novel measurement (a
> cohomological-style *contextual-fraction* obstruction computed by linear
> programming) and the frozen evaluation dataset are **held back until
> arXiv / peer review** to preserve priority. What's here is enough to see how
> the instrument is built and how the study is run — not enough to reproduce the
> headline result ahead of the paper. See [What's public vs. withheld](#whats-public-vs-withheld).

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

**Honest methodology note.** The validation labels above were produced by an
LLM (Claude), not by independent human annotation — a deliberate project
decision, disclosed here because it changes what the numbers mean: they measure
*classifier-vs-LLM agreement*, not human-verified ground truth. The paper's
methods section states this explicitly; no claim of human validation is made.
(Human verification by a native Bengali speaker is part of the dataset-freeze
step, which is in the withheld portion.)

A second finding surfaced during validation and is worth stating because it
generalizes beyond this project: **Hindi present/progressive conjugation is
syncretic** across 2nd-person-formal, 1st-plural, and 3rd-plural
(`-ते हैं` / `-रहे हैं`), so Hindi carries structurally more register ambiguity
than Bengali. Any register classifier — rule-based or learned — inherits this.

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
advance; the paper reports the outcome regardless of direction.

## Try the interface

The label space, cue record, and classifier protocol are public
(`src/register/core.py`), plus a deliberately minimal **pronoun-only** demo
classifier — textbook honorifics (আপনি/তুমি/তুই, आप/तुम/तू), *not* the validated
morphological instrument. Pure Python, no deps to run it:

```bash
pip install -e ".[dev]"
pytest -q                  # 5 passing interface tests
python examples/demo.py
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

## What's public vs. withheld

| Public here | Withheld until publication |
|---|---|
| Research design, study spec (this README) | The contextual-fraction obstruction method (LP formulation) |
| Register-classifier **interface** + validation methodology | The classifier cue tables / internals (the working instrument) |
| Phase structure, harness shape, model list | Frozen benchmark dataset + mined triples |
| Qualitative direction of findings | Full per-path quantitative result tables + correlations |

If you're evaluating this for a role: happy to walk through the full method and
current results under a conversation / NDA — the omissions here are about
publication priority, not about hiding gaps.

## Author

Kanishk Paul — [kanishkpaul.com](https://kanishkpaul.com) ·
[github.com/kanishkpaul](https://github.com/kanishkpaul)
Write-up: kanishkpaul.com/research
