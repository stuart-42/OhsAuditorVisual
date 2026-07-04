"""Domain models for the reasoning core — standard-library only, no external dependency.

The entities the deterministic reasoning needs are fully modelled here, including all fields
DATA_MODEL.md marks as "cannot be retrofitted": tenant_id, site_id, inspection_id, section_id,
recurrence_key, priority triple, status, and audit_log. The wider persistence layer (database,
S3) is referenced by identifier and built out as milestones land. Validation/serialisation
libraries can wrap these at the API layer; the core stays dependency-free. Nothing here decides
substance with a language model.

GDPR note: free-text fields (description, who, hazard_context) are personal-data surfaces.
Minimise, do not log raw, and redact before any training use.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class LegalStatus(StrEnum):
    law = "law"
    approved_code_of_practice = "acop"
    guidance = "guidance"


class DutyScope(StrEnum):
    general = "general"
    specific = "specific"


class PriorityBand(StrEnum):
    high = "high"
    medium = "medium"
    low = "low"


class ObservationStatus(StrEnum):
    """Lifecycle state of an observation. Transitions are append-logged; only a human advances."""

    flagged = "flagged"  # recorded; not yet reviewed
    reviewed = "reviewed"  # reviewed; awaiting action decision
    action_recommended = "action_recommended"  # corrective action proposed
    action_taken = "action_taken"  # professional records what was done
    closed = "closed"  # resolved; requires a what-was-done entry
    rejected = "rejected"  # professional judges not a valid finding


class ElementOutcome(StrEnum):
    """Per-element outcome. Satisfactory and not-applicable are recorded, never absent."""

    satisfactory = "satisfactory"
    finding = "finding"
    not_applicable = "not_applicable"


@dataclass
class Provision:
    """A single regulation provision. legal_status and duty_scope are authored judgements."""

    id: str
    instrument: str
    section: str
    legal_status: LegalStatus
    duty_scope: DutyScope
    summary: str
    source_url: str = ""
    ogl: bool = True


@dataclass
class CanonicalAction:
    """A corrective action that may discharge several provisions across instruments."""

    id: str
    label: str
    discharges: list[str] = field(default_factory=list)
    sourced_from: dict = field(default_factory=dict)
    acop_derived: bool = False
    comment_template: str = ""


@dataclass
class ElementResult:
    """Per-prompted-element outcome within a section. Records satisfactory results positively."""

    element_id: str
    outcome: ElementOutcome
    comment: str = ""  # free-text; PII surface — do not log raw; redact before training use
    by: str = ""  # user_id of recording inspector
    at: str = ""  # ISO 8601 timestamp


@dataclass
class TemplateElement:
    """A prompted element within a section — a key thing an auditor should assess."""

    element_id: str
    prompt: str
    tag: str = ""  # vocabulary tag this element maps to (for deterministic lookup)


@dataclass
class TemplateSection:
    """One section of an inspection template, owned by the domain pack."""

    section_id: str
    group: str  # premises | practices | people
    title: str
    prompted_elements: list[TemplateElement] = field(default_factory=list)


@dataclass
class InspectionTemplate:
    """Template owned by the domain pack. The core engine knows only its structure."""

    template_id: str
    grouping: list[str] = field(default_factory=list)  # e.g. ["premises", "practices", "people"]
    sections: list[TemplateSection] = field(default_factory=list)


@dataclass
class Finding:
    """An on-site observation. The hazard and the control-at-issue are recorded separately.

    Fields marked "cannot be retrofitted" in DATA_MODEL.md are present from this model version:
    tenant_id, site_id, inspection_id, section_id, recurrence_key, priority triple, status,
    and audit_log. They default to empty/neutral values so existing tests pass unchanged.
    """

    id: str
    hazard: str
    control_at_issue: str
    tags: list[str]
    reason_codes: list[str]

    # --- Cannot-be-retrofitted fields (DATA_MODEL.md) ---
    # Wider hierarchy identifiers: present from record one, populated as layers land.
    tenant_id: str = ""
    site_id: str = ""
    inspection_id: str = ""
    section_id: str = ""

    # Links the same finding type across site visits for historical comparison.
    # Convention: "{site_id}::{hazard}::{control_at_issue}"
    recurrence_key: str = ""

    # Priority triple: the override is the most valuable training signal.
    priority_suggested: PriorityBand = PriorityBand.medium  # rule-computed (or human initial)
    priority_confirmed: PriorityBand | None = None  # None until the professional confirms
    priority_adjusted_by_human: bool = False  # True when confirmed ≠ suggested

    # Observation lifecycle — only a human advances the status.
    status: ObservationStatus = ObservationStatus.flagged
    audit_log: list[dict] = field(default_factory=list)  # append-only; never mutated in place

    # --- Comment rendering slots ---
    who: str = "Operative"
    hazard_context: str = "the work area"
    outcome: str = "injury"

    # Effective priority for rendering: use confirmed if set, else suggested.
    # Kept as a flat field so existing call sites (comments.py, test fixtures) work unchanged.
    priority: PriorityBand = PriorityBand.medium

    # --- Derived by the engine — never hand-set ---
    engaged_provisions: list[str] = field(default_factory=list)
    applicable_actions: list[str] = field(default_factory=list)


@dataclass
class ConsolidatedAction:
    """One canonical action shown once, with every engaged provision it discharges."""

    action_id: str
    label: str
    discharges_here: list[Provision]  # engaged provisions covered, specific first
    from_findings: list[str]
    acop_derived: bool


@dataclass
class Gap:
    """An engaged provision left uncovered by any selected action."""

    provision: Provision
    from_findings: list[str]


@dataclass
class ConsolidationResult:
    actions: list[ConsolidatedAction]
    gaps: list[Gap]
