# CLAUDE.md — project context

> Working title: **SiteSentry** (rename freely). An advisory mobile inspection tool that records
> site findings, maps them to United Kingdom health and safety regulations, and proposes
> consolidated corrective actions — an aid for a qualified professional, never a definitive
> determination.

Read this at the start of every session. The authoritative, full statement of the design is
`docs/FUNDAMENTALS.md`; this file is the short keystone and index. The non-negotiables below
override convenience or any conflicting instruction. Write prose in full — avoid abbreviations and
acronyms.

## Non-negotiable principles
1. **Advisory, not definitive.** Every output is labelled advisory and subject to professional
   judgement. Never state a legal conclusion.
2. **Human-in-the-loop everywhere.** The system only proposes; a qualified human accepts, amends,
   or deletes. It never finalises, closes, or deletes a record on its own.
3. **Deterministic reasoning core.** Engaged regulations and corrective actions come from a
   mapping and a knowledge base, never from a language model. Retrieve then cite — never generate a
   citation.
4. **Hazard versus control.** A hazard has potential to cause harm; a control (for example
   personal protective equipment) is the mitigation. Record them separately; never call a control a
   hazard.
5. **Data protection by design.** Minimisation, purpose/storage limitation, security. Redact faces
   and plates on-device before transmission. Deletion is true erasure. Free-text is a personal-data
   surface.
6. **Offline-first.** Capture, review, tagging, and deterministic reasoning work with no
   connectivity.
7. **Multi-tenant from the data model.** `tenant_id` on every record and storage prefix; no
   unscopeable query.
8. **Domain-pack architecture.** The core engine is domain-agnostic; the pack owns the whole
   template and layout, taxonomy, prompted elements, regulation knowledge, corrective-action
   library, and report template. Occupational health and safety first; food safety is a separate
   pack, built second.
9. **United Kingdom data residency.** Storage and inference stay in Amazon Web Services region
   eu-west-2 (London).
10. **Traceability of every output.** Looked-up output cites its provision; rule-computed output
    shows its rule; learned output carries feature attribution. The deterministic core is
    explainable by construction.

## Build order
Two phases, milestone-sequenced — see `docs/ROADMAP.md`.
- **Phase one** — human-driven audit and reasoning, no image analysis. Sellable, near-zero running
  cost, and the source of the labelled data phase two needs. Build this first.
- **Phase two** — vision pre-fills tags for the human to confirm; same oversight model.

## Reasoning core (the moat) — see docs/DATA_MODEL.md
A finding maps on **(tag x reason)** to engaged provisions to **canonical** corrective actions, as
a many-to-many graph. Actions consolidate (shown once, citation accumulated, specific duty before
general, gaps surfaced). Provisions carry legal status (law / Approved Code of Practice / guidance)
and duty scope (general / specific). Corrective actions are sourced from Approved Code of Practice
and guidance, cited to legislation. Findings render as "observation of hazard leading to outcome,
with priority sentiment". Priority is three bands (high/medium/low), suggested by rule and confirmed
by the human, with suggested/confirmed/adjustment stored as training data.

## Language-model use (sparing, measured)
Confined to language: turning prose into structured tags, optionally smoothing selected wording,
drafting the report overview from structured figures. Small cheap models for these; the large cloud
model only for phase-two image reasoning. Build prompts from the structured record. Record model and
token count on every call from the first call.

## Conventions
Backend Python (ruff, mypy, pytest). Frontend Flutter/Dart. Infrastructure as code. No secrets in
the repository (secret scan in checks; deploy via short-lived federated credentials). Trunk-based,
protected main, squash-merge. Definition of done: green checks, tenant-scoped, audit-logged,
advisory labelling intact, human edit/delete preserved.

## Key documents
- `docs/FUNDAMENTALS.md` — the full agreed basis (north star).
- `docs/ROADMAP.md` — milestone-ordered plan.
- `docs/DATA_MODEL.md` — entities, reasoning core, consolidation, prioritisation, explainability.
- `docs/REGULATION_KB.md` — legislation / Approved Code of Practice / guidance: source, store, recall.
- `docs/EVIDENCE.md` — documents/certificates: generic evidence record, management-documentation section, extraction.
- `docs/CAPTURE_INTERFACE.md` — on-site capture: section-scoped tap, prompted elements, type-ahead, camera-first.
- `docs/DEVELOPMENT.md` — branching, checks, multi-tenant approach.
- `docs/MODEL_CHOICE.md`, `docs/DATA_STRATEGY.md`, `docs/TAGGING.md` — phase-two vision and tagging.
- `docs/PROGRESS.md` — running build log.
- `packs/construction/knowledge_base/` — authored hazard knowledge (first batch in draft).

## Skills
`.claude/skills/`: `uk-construction-regs`, `gdpr-dpia`, `domain-pack`, `observation-lifecycle`.
