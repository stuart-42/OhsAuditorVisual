# PROGRESS — build log

Running record so any session can pick up the thread. Append new stages to the top.

**Project:** SiteSentry (working title) — advisory occupational health and safety inspection tool.
Professional aid, not a definitive determination.

## Where we are
Design phase complete; the deterministic reasoning core is now implemented and tested in `backend/`. The full agreed basis is `docs/FUNDAMENTALS.md`; the build sequence is
`docs/ROADMAP.md`. Next action on desktop: commit this bundle, then begin Milestone Zero, then
adjudicate the first knowledge-base batch.

## Roadmap (summary — full version in docs/ROADMAP.md)
- **Milestone Zero** — foundations: commit scaffold, lock the data model, draft the Data Protection
  Impact Assessment, regulation knowledge base design.
- **Milestone One** — core audit loop (single user, one site): construction pack, deterministic
  reasoning, consolidation, prompted elements, audit comments. Sellable, no vision, no cloud
  inference.
- **Milestone Two** — reports, action tracking, three-band prioritisation.
- **Milestone Three** — multi-site / multi-client / access.
- **Milestone Four** — performance-measurement dashboard.
- **Milestone Five** — natural-language tag suggestion (trained on confirmed labels).
- **Phase Two** — vision (licence-decided detector, on-device redaction); later, learned
  prioritisation.

## Stages
### Stage 11 — Reasoning core in code (tested)  ·  2026-06-20
- `backend/sitesentry/`: the deterministic Milestone One spine in pure standard-library Python —
  knowledge base loader + exact (tag x reason) lookup, consolidation with citation accumulation,
  specific-before-general ordering, gap detection, and audit-comment rendering.
- `packs/construction/knowledge_base/`: provisional structured knowledge (provisions, actions,
  mapping, vocabulary) derived from the draft findings.
- Verified: `selfcheck.py` (all pass) and `sitesentry.demo` reproduce the head + foot worked
  example with one consolidated risk-assessment action across both findings and a surfaced gap.

### Stage 10 — Evidence & documents  ·  2026-06-20
- `docs/EVIDENCE.md`: generic evidence record + controlled document-type vocabulary, surfaced via a
  management-documentation section; optical-character extraction and expiry logic later; auditor tags
  as training data.
- `docs/DATA_MODEL.md`: Evidence record type added; high-priority hazard-photo-plus-comment made an
  explicit first-class training unit.

### Stage 9 — Capture interface  ·  2026-06-20
- `docs/CAPTURE_INTERFACE.md`: section-scoped tap capture, prompted elements as targets, recents,
  type-ahead into the full vocabulary, camera-first, and unmapped-capture-and-triage. Milestone One.

### Stage 8 — Design consolidation  ·  2026-06-20
- Added `docs/FUNDAMENTALS.md`, `docs/ROADMAP.md`, `docs/REGULATION_KB.md`.
- Rewrote `docs/DATA_MODEL.md` and `CLAUDE.md` for the full deepened design: client/site/inspection
  entities, template-per-domain with prompted elements and positive outcomes, hazard-vs-control
  findings, canonical actions with citation accumulation, general/specific marking, actions sourced
  from Approved Code of Practice and guidance, audit-comment rendering, three-band prioritisation
  with training capture, explainability, summary references, access scopes, performance fields,
  token accounting.
- Started `packs/construction/knowledge_base/` with the first protective-equipment findings as a
  DRAFT awaiting adjudication.

### Stage 7 — Tagging & reason-code model  ·  2026-06-20
- Hierarchical multi-label tags + reason codes; mapping keyed on (tag x reason); NLP suggestion loop.

### Stages 0-6  ·  2026-06-20
- Scaffold, skills, secrets hygiene, vision prototype (phase two), model critique, data strategy,
  audit-first reorder + initial data model. (See git history / earlier docs.)

## Next up (Milestone Zero, on desktop)
- [ ] Commit this bundle; protect main; confirm checks run.
- [ ] Implement the data model from `docs/DATA_MODEL.md` (entities, scopes, all required fields).
- [ ] Draft `docs/DPIA.md` (Data Protection Impact Assessment) — required before any real-site use.
- [ ] Adjudicate `packs/construction/knowledge_base/findings_ppe_DRAFT.md`; record settled versions.
- [ ] Then Milestone One: deterministic reasoning + consolidation + audit screens.
