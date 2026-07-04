# ROADMAP — milestone-ordered plan

Ordering rules: get the data model right first so later layers are additive, not rewrites;
build the sellable deterministic core before anything learned or vision; make each milestone
independently demonstrable; do cheap-high-value before expensive. Written out in full.

## Milestone Zero — Foundations (no application yet)
Cheapest work; prevents rework. Commit the scaffold. Lock the full data model (see DATA_MODEL.md):
the entity hierarchy, tenant and site scoping, role-to-scope grants, and every field that later
features need present — report fields, performance fields, priority fields (suggested, confirmed,
adjustment), due dates, recurrence key, token-accounting fields, explainability hooks, stable
identifiers for summary references. Draft the Data Protection Impact Assessment. Write the
regulation knowledge base design (REGULATION_KB.md). No feature is built here; the schema for
reports, access, performance, and prioritisation goes in now even though the features come later.

## Milestone One — Core audit loop (single user, one site, no authentication interface)
The sellable nucleus. Construction pack version one: hierarchical taxonomy + reason codes +
curated Open-Government-Licence regulation knowledge base (status-tagged) + the canonical
corrective-action library sourced from Approved Code of Practice and guidance. Template owned by
the pack, organised premises / practices / people, with prompted key elements per section.
Deterministic reasoning: tag-and-reason to engaged provisions to canonical actions; consolidation
with citation accumulation, general-versus-specific ordering, and gap detection. Per-element
outcomes including positive comments. Audit-comment rendering in the observation-to-outcome form.
Human-in-the-loop accept / amend / delete. Flutter screens: enter, tag, review, see the
consolidated plan. No vision, no cloud reasoning required.

## Milestone Two — Reports, action tracking, prioritisation
Inspection-as-living-report; render the report on demand; recall by site; reopen and complete
actions with what-was-done and date; overdue logic. Three-band risk-based priority suggestion
(human confirms), with suggested and confirmed bands and the adjustment recorded as training data.

## Milestone Three — Multi-site, multi-client, access
Authentication; roles; scope enforcement on every query; client and region entities.

## Milestone Four — Performance-measurement dashboard
Aggregations scoped by role: coverage, compliance rate, open versus overdue, time to close, Pareto
of categories, recurrence, inspection frequency, gaps.

## Milestone Five — Natural-language tag suggestion
Cold-start with keyword rules / zero-shot, then train the small text classifier on the
human-confirmed labels milestones one to four have been generating. Feature attribution on its
output.

## Phase Two — Vision
Licence-decided detector (see MODEL_CHOICE.md) plus on-device redaction pre-fills tags, trained on
the labels the whole of phase one produced (see DATA_STRATEGY.md). Attribution maps on detections.
Later: a learned prioritisation classifier over structured inputs, then over images, from the
priority training data captured since milestone two.

## Why this is achievable
Milestone One alone is a complete, demonstrable, sellable product with no machine learning and no
cloud-inference cost. Everything after is additive because Milestone Zero reserved the seams. The
work is never blocked waiting on data, a licence decision, or a model.
