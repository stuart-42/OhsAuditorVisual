---
name: uk-construction-regs
description: Occupational health and safety regulatory knowledge for the construction domain pack — the hazard-to-regulation-to-corrective-action mapping, the general/specific marking, and the legal-status tagging. Use this skill whenever the work involves construction hazard findings, classifying an observation, referencing United Kingdom health and safety law (Construction Design and Management Regulations 2015, Work at Height Regulations 2005, Provision and Use of Work Equipment Regulations 1998, Personal Protective Equipment at Work Regulations 1992, Management of Health and Safety at Work Regulations 1999, the Health and Safety at Work etc. Act 1974), authoring or editing the construction knowledge base, mapping findings to provisions, or drafting corrective actions. Trigger it even if the user only says hazards, compliance, regulations, site inspection, or names a regulation, and even if they do not name this skill.
---

# United Kingdom construction regulatory knowledge (construction domain pack)

Domain knowledge for the construction vertical, not core-engine logic. The full data model is in
`docs/DATA_MODEL.md`; the sourcing/storage/recall rules are in `docs/REGULATION_KB.md`. This skill
is the standing set of rules for authoring and using that knowledge.

## Hard rules
- Output is advisory. Always cite the provision; never assert a definitive legal breach. The
  qualified human decides.
- A hazard is something with potential to cause harm. A control (for example personal protective
  equipment) is the mitigation. Record the hazard and the control-at-issue separately. Never call a
  control a hazard.
- Reasoning is deterministic. Engaged provisions and corrective actions come from the mapping and
  the knowledge base, never from a language model. Retrieve then cite — never generate a citation.
- Scope: United Kingdom Legislation, Guidance, and Approved Codes of Practice only — all Open
  Government Licence. Carry the attribution line. Never reproduce British Standards Institution or
  International Organization for Standardization standard text (copyright).

## Authoring each finding
Map on **(tag x reason)** → engaged provisions → canonical corrective action. For each:
- Mark every provision's `legal_status` (law | acop | guidance) and `duty_scope`
  (general | specific). Output leads with the specific duty and notes the general one.
- Link shared obligations to a single **canonical** corrective action so consolidation is structural.
- Source the corrective action from the Approved Code of Practice / guidance, cite it to the
  legislation, and set `acop_derived` where its basis is an Approved Code of Practice (stronger
  weight, surfaced).
- Give the finding a comment template in the form "observation of hazard leading to outcome, with
  priority sentiment".

## Consolidation
One canonical action shown once, accumulating every engaged provision it discharges (specific
first, then general), Approved-Code-of-Practice-derived actions marked, and any uncovered engaged
provision flagged as a gap. Keep it transparent — never hide which provision an action discharges.

## When generating model prompts (phase two)
Instruct the model to describe what it sees, name the candidate hazard and the control at issue,
give a confidence level, and stop there — provisions and actions are looked up deterministically,
not generated. Mark all model output advisory and human-in-the-loop.
