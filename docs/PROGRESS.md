# PROGRESS — build log

Running record so any session can pick up the thread. Append new stages to the top.

**Project:** SiteSentry (working title) — advisory occupational health and safety inspection tool.
Professional aid, not a definitive determination.

## Where we are

Milestone Zero is partially complete. The deterministic reasoning core is implemented, tested,
and expanded to full protective-equipment coverage. The data model now carries all
"cannot-be-retrofitted" fields (tenant_id, site_id, inspection_id, section_id, recurrence_key,
priority triple, status, audit_log). A FastAPI test harness enables manual browser testing. A
strategy audit identified the remaining gaps. A DPIA skeleton has been drafted.

Remaining Milestone Zero work before Milestone One features: persistence layer, knowledge-base
adjudication, template JSON, DPIA sign-off by the data controller. See `docs/AUDIT_2026-07-04.md`
for the full gap analysis and `docs/DEVELOPMENT.md` for the current issue list.

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

### Stage 14 — Strategy audit; Milestone Zero data model; pipeline fixes  ·  2026-07-04
- `docs/AUDIT_2026-07-04.md`: full gap analysis comparing strategy documents against working code.
  Ten gaps identified; ordered by severity. Serves as the reference for the next build sessions.
- `docs/DPIA.md`: Data Protection Impact Assessment skeleton drafted (required before real-site
  use). Six sections: description of processing, necessity/proportionality, personal data
  inventory, risks, mitigations, residual risk and sign-off. Marked DRAFT pending data-controller
  review and sign-off.
- `backend/sitesentry/models.py`: Milestone Zero fields added to `Finding` — `tenant_id`,
  `site_id`, `inspection_id`, `section_id`, `recurrence_key`, `priority_suggested`,
  `priority_confirmed`, `priority_adjusted_by_human`, `status` (ObservationStatus enum),
  `audit_log` (append-only). New dataclasses: `ObservationStatus`, `ElementOutcome`,
  `ElementResult`, `TemplateElement`, `TemplateSection`, `InspectionTemplate`. All existing
  tests pass unchanged (new fields default to empty/neutral values).
- `backend/pyproject.toml`: ruff and mypy configuration committed; tool behaviour consistent
  across machines.
- CI fixed: `api_requirements.txt` now installed in the backend job so FastAPI imports resolve;
  mypy scoped to `sitesentry/` and `tests/` (api.py checked separately as it has its own deps);
  all enums upgraded to `StrEnum`; deprecated `typing.List`/`Optional` replaced throughout.
- `docs/DEVELOPMENT.md`: stale vision-first "first issues" list replaced with the current
  Milestone Zero completion checklist.
- `docs/PROGRESS.md` (this file): "Where we are" updated to reflect current state.
- Verified: lint clean, format clean, mypy clean, 8/8 pytest, 10/10 selfcheck.

### Stage 13 — PPE knowledge base expanded; FastAPI test harness  ·  2026-07-04
- `packs/construction/knowledge_base/`: actions 3→7 (ca_maintain_ppe, ca_provide_eye,
  ca_provide_gloves, ca_provide_hiviz); mapping 2→13 (full PPE coverage for head/foot/eye/
  hand/hiviz across all three reason codes); vocabulary 3→5 tags (hand, hiviz added).
- `backend/api.py`: FastAPI app with embedded HTML test harness at GET /; `/vocabulary` and
  `/consolidate` endpoints; advisory banner on every response.
- Tests updated: `test_gap_detection` uses a synthetic in-memory KB; two new tests for
  ca_maintain_ppe and eye protection mapping; sentinel changed to hiviz × doesnt_fit.
- Verified: 8/8 pytest, 10/10 selfcheck.

### Stage 12 — Knowledge base scaffold + reasoning core verified  ·  2026-07-04
- Zip scaffold applied to branch; reasoning core in sitesentry/; provisional KB from Stage 11.
- Initial selfcheck and pytest verified.

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
