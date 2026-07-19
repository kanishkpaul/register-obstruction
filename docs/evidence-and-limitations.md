# Evidence and limitations

## What has been measured

Two completed pieces of the study are public in aggregate:

1. A deterministic Bengali and Hindi register instrument was compared with
   LLM-produced reference labels. Precision cleared the predeclared 0.90 gate
   for `FORMAL`, `FAMILIAR`, and `INTIMATE` in both languages.
2. Five local translation systems were evaluated on 256 implicit,
   register-bearing Bengali items under direct Bengali-to-Hindi and
   Bengali-to-English-to-Hindi paths.

The aggregate tables are in [`results/`](../results/). Their private source
commit and content hashes are recorded in
[`provenance.json`](../results/provenance.json).

## What the current evidence says

| system | direct survival | pivot survival | direct minus pivot |
|---|---:|---:|---:|
| IndicTrans2 | 38.67% | 39.45% | -0.78 pp |
| NLLB | 36.72% | 34.38% | +2.34 pp |
| Gemma 3 12B | 62.50% | 40.63% | +21.88 pp |
| Llama 3.1 8B | 55.86% | 37.11% | +18.75 pp |
| Qwen3 8B | 53.91% | 37.11% | +16.80 pp |

This is more specific than the original hypothesis. Dedicated MT systems
already lose most register information on the direct path, so an English pivot
adds little consistent damage there. All three general LLM translators show a
large additional pivot penalty. The effect is model-family dependent, not a
universal fixed cost.

These are register-fidelity baselines, not contextual-fraction obstruction
scores. The contextual-fraction computation and its correlation with
downstream failure have not been run.

## Provenance

- Bengali validation: 147 labeled items.
- Hindi validation: 150 labeled items.
- Frozen evaluation set: 309 items, including 256 register items and 53
  controls; 28 candidate joins were dropped.
- All validation labels and all frozen-item verification decisions were
  produced by Claude and tagged accordingly. No independent human annotation
  has been completed.
- The frozen data comes from subtitle-domain material and should not be read as
  population-representative language use.

The private hashes commit this release to particular source artifacts, but
hashes do not make the withheld data independently reproducible. They provide
versioned provenance and make later silent substitution detectable.

## Release boundary

The release omits sentence text, per-item model outputs, cue tables,
morphological suffix rules, the planned contextual-fraction implementation,
and register-restoration system internals. Aggregate evidence is public so the
claims visible in the README can be checked without exposing those materials.
