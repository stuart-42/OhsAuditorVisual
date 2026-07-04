"""Domain models for the reasoning core — standard-library only, no external dependency.

Only the entities the deterministic reasoning needs are modelled here; the wider hierarchy
(tenant, client, region, site, inspection, evidence) is referenced by identifier and fleshed out
as milestones land. Validation/serialisation libraries can wrap these at the API layer later; the
core stays dependency-free. Nothing here decides substance with a language model.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class LegalStatus(str, Enum):
    law = "law"
    approved_code_of_practice = "acop"
    guidance = "guidance"


class DutyScope(str, Enum):
    general = "general"
    specific = "specific"


class PriorityBand(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


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
class Finding:
    """An on-site observation. The hazard and the control-at-issue are recorded separately."""
    id: str
    hazard: str
    control_at_issue: str
    tags: list[str]
    reason_codes: list[str]
    who: str = "Operative"
    hazard_context: str = "the work area"
    outcome: str = "injury"
    priority: PriorityBand = PriorityBand.medium
    engaged_provisions: list[str] = field(default_factory=list)   # DERIVED by the engine
    applicable_actions: list[str] = field(default_factory=list)   # DERIVED by the engine


@dataclass
class ConsolidatedAction:
    """One canonical action shown once, with every engaged provision it discharges."""
    action_id: str
    label: str
    discharges_here: list[Provision]   # engaged provisions covered, specific first
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
