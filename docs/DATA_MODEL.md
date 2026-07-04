# DATA_MODEL — the reasoning core and the records around it

The moat: not photo logging, but mapping a finding to the regulations it engages and a
consolidated, sourced set of corrective actions. Everything here is advisory professional
judgement, never a legal guarantee, and the reasoning is deterministic — no language model decides
substance. Written out in full.

## Entity hierarchy

```
Tenant ─▶ Client ─▶ Region ─▶ Site ─▶ Inspection ─▶ Observation ─▶ Action
                                         ├─ Evidence records (documents/certificates)
                                         │
                                         └─ uses a Template (owned by the domain pack)
```

- **Tenant** — the customer organisation. Present on every record; nothing is unscopeable by it.
- **Client, Region, Site** — the access and reporting hierarchy. A Site has a persistent identity
  so visits are linkable over time (required for historical comparison).
- **Inspection** — one dated audit of one site, against one Template. Carries header and scope
  fields (site, client, inspector, date, context, scope). A report is an Inspection rendered on
  demand; it can be reopened to complete actions.
- **Observation** — a finding (below).
- **Action** — a corrective action with completion tracking (below).

## Template, Section, prompted elements (domain pack owns the layout)

The domain pack owns the **entire** template, including its grouping scheme. Occupational health
and safety groups by premises / practices / people; food safety is a separate pack with its own
scheme. The core engine only knows "a template is an ordered set of named sections, each holding
prompted elements and observations".

```json
// owned by packs/<vertical>/
{ "template_id": "ohs_v1", "grouping": ["premises", "practices", "people"],
  "sections": [
    { "section_id": "people_ppe", "group": "people", "title": "Protective equipment",
      "prompted_elements": ["pe_head", "pe_foot", "pe_eye"] } ] }

// a prompted element to look for
{ "element_id": "pe_head", "prompt": "Is head protection worn where overhead/striking risk exists?" }
```

Each addressed element resolves to an **outcome** with an optional comment in every case:

```json
{ "element_id": "pe_head", "outcome": "satisfactory|finding|not_applicable",
  "comment": "free-text, optional, positive comments allowed", "by": "user_id", "at": "iso8601" }
```
A `finding` outcome creates a full Observation. `satisfactory` and `not_applicable` are recorded
and counted (this is what enables coverage and compliance measures).

## Observation (hazard and control kept separate)

A hazard is something with potential to cause harm; a control (for example personal protective
equipment) is the mitigation. A finding names both.

```json
{ "id": "obs_001", "tenant_id": "...", "site_id": "...", "inspection_id": "...",
  "section_id": "people_ppe",
  "hazard": "head_injury_falling_object",         // the thing with potential to cause harm
  "control_at_issue": "ppe_head",                  // the missing/inadequate mitigation
  "tags": ["control.ppe.head"], "reason_codes": ["not_worn"],
  "description": "free-text; PII surface; redact before any training use",
  "recurrence_key": "site::head_injury_falling_object::ppe_head",  // links the same finding across visits
  "engages": ["ppe_reg4","ppe_reg10","mhswr_reg3","hswa_s2"],      // DERIVED from (tag x reason) mapping
  "severity": "...", "likelihood": "...",
  "priority": { "suggested": "high", "confirmed": "high", "adjusted_by_human": false },
  "ai_detections": [ /* phase 2; each carries confidence, model_version, attribution_ref */ ],
  "status": "flagged|reviewed|action_recommended|action_taken|closed|rejected",
  "audit_log": [ /* append-only */ ] }
```
- `engages` is derived from the mapping, never hand-typed.
- `priority` stores suggested, confirmed, and whether the human adjusted — the override is the
  most valuable training signal (see Prioritisation).
- `recurrence_key` is what makes repeat-finding detection and historical comparison possible; it
  must exist from the first stored audit.

## Provisions, canonical actions, mapping

```json
// regulation provision — legal status and general/specific marking are hand-authored
{ "id": "mhswr_reg3", "instrument": "Management of Health and Safety at Work Regulations 1999",
  "section": "regulation 3", "legal_status": "law",          // law | acop | guidance
  "duty_scope": "general",                                    // general | specific
  "summary": "<own words>", "source_url": "...", "ogl": true }

// canonical corrective action — ONE action that many provisions link to
{ "id": "ca_risk_assessment", "label": "Reassess the hazard and apply the hierarchy of control",
  "discharges": ["mhswr_reg3","ppe_reg4"],
  "sourced_from": { "publication": "L25", "kind": "acop|guidance" },   // action authored from ACOP/guidance
  "acop_derived": true,                                                // stronger legal weight, surfaced
  "comment_template": "{who} observed without {control} where {hazard_context}, which could result in {outcome}; {priority_sentiment}." }
```
The mapping is keyed on **(tag x reason)** → engaged provisions → canonical actions. Because shared
obligations link to the same canonical action, consolidation is structural, not a cleanup.

## Consolidation algorithm (per inspection)

1. For each finding, gather engaged provisions and their canonical actions.
2. Union actions across the inspection; deduplicate by canonical action id.
3. For each unique action, accumulate every engaged provision it discharges, ordered
   **specific duties first, then general** (using `duty_scope`), and mark `acop_derived` actions.
4. Flag any engaged provision with no selected action as a **gap**.
Consolidation must stay transparent: the professional always sees which provision each action
discharges and can amend. Nothing legally relevant is collapsed away.

### Worked example
Finding "head protection not worn" engages the specific personal-protective-equipment duty and the
general management risk-assessment duty (and the overarching Act). Both link to the one canonical
action "reassess the hazard and apply the hierarchy of control". The plan shows that action **once**,
citing the specific duty first and the general duty as additionally engaged, marked as derived from
the L25 Approved Code of Practice / guidance. One action, full citation, correct ordering.

## Audit comment
Rendered in the form "observation of hazard leading to outcome, with priority sentiment" from the
`comment_template`, filling slots from the finding and selecting the sentiment phrase from the
confirmed priority band. The language model only fills/smooths the template; it never sets
substance or priority. A template gives a defensible phrase at zero inference cost and offline.

## Prioritisation
Three bands: high, medium, low. Computed by a transparent rule from severity and likelihood,
weighted by `legal_status`, recurrence, and people exposed. Stored as suggested + confirmed +
adjustment. The confirmed band also labels any attached image. These fields are the training set
for a later prioritisation classifier (structured inputs, then images). The rule stays the
explainable default; a learned model arrives later as a reviewed suggestion.

## Explainability
Deterministic outputs are explainable by construction (a citation points at its provision; a band
shows its rule). Learned outputs carry feature attribution: Shapley additive explanations for
structured-input classifiers, attribution maps for image models, referenced from the detection and
surfaced as the reason for a suggestion, and usable to audit a model against its training data.

## Summary references
Every Observation and Action has a stable identifier. The report summary refers to those
identifiers, so a statement in the overview links to the findings/actions it summarises. The
summary language model is held to summarising referenced, structured data — if a statement cannot
be traced to a finding or action, it does not belong in the summary.

## Evidence records (see docs/EVIDENCE.md)
A second record type alongside Observation. Generic record, `document_type` from a controlled
vocabulary, holding uploaded media, auditor tags, extracted fields with confirmation status, and
provenance. Surfaced through a management-documentation section (under "practices") whose prompted
elements are the expected documents; a missing expected document is a gap. Optical-character
extraction and expiry/validity logic are later and additive; an expired certificate becomes a
finding through the same reasoning core. Heavier personal-data surface than a site photo.

## Training units (make the label explicit)
A high-priority hazard photo with a human comment is the most valuable phase-two label, and the
rarest. Hold it as a first-class training unit: image + confirmed tags + auditor comment +
confirmed priority band + provenance. The label that trains a model is always the human-confirmed
one; the comment is redacted before any training use. Evidence documents are labelled units in the
same way (type + tags + confirmed fields).

## Access scope
`user → scope grant`, where scope is one of site | region | client | tenant. Site manager → site(s),
regional manager → region, safety manager/administrator → tenant. Modelled now; enforced on every
query once authentication lands. No organisation-administration interface in the prototype (seed
via configuration).

## Token accounting
Every language-model call records model and token count, attributed to inspection and tenant, from
the first call — for cost visibility and, later, per-customer pricing.

## Fields that must exist from the first audit (cannot be retrofitted)
Controlled `tags`/`category` and `section_id`; persistent `site_id`; `recurrence_key`; priority
`suggested`/`confirmed`/`adjusted`; `due_date`/`closed_date`; element outcomes. These power
historical comparison, performance measures, and the prioritisation flywheel.
