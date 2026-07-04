# backend — deterministic reasoning core (Milestone One spine)

Pure standard-library Python. No runtime dependencies, no cloud, no language model — the
legally consequential reasoning is a set of lookups and set operations, so it is reproducible and
auditable.

## What is here
- `sitesentry/models.py` — domain types (provision, canonical action, finding, results).
- `sitesentry/knowledge_base.py` — loads the domain pack's authored records and builds the exact
  keyed indexes.
- `sitesentry/reasoning.py` — engages provisions and gathers actions from the (tag x reason) lookup;
  flags unmapped combinations.
- `sitesentry/consolidation.py` — one canonical action shown once, citations accumulated, specific
  duties before general, gaps surfaced.
- `sitesentry/comments.py` — renders the audit comment ("observation of hazard leading to outcome,
  with priority sentiment") deterministically from a template.
- `sitesentry/demo.py` — the head + foot worked example from the design.

The knowledge it reasons over lives in `packs/construction/knowledge_base/` (structured files,
PROVISIONAL until adjudicated).

## Run
```
cd backend
python -m sitesentry.demo     # worked example
python selfcheck.py           # standard-library checks (no dependencies)
pip install -r requirements.txt && python -m pytest   # full test suite (needs pytest)
```

## Design guarantees demonstrated
- Exact keyed recall; unmapped combinations flagged, never silently dropped.
- A shared action (risk assessment) consolidated once across several findings, citing every engaged
  instrument, specific duties first.
- Genuine gaps surfaced (an engaged provision with no authored action).
- Audit-comment priority sentiment driven by the confirmed band, not invented.
