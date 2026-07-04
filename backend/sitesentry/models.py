"""Core data models for OHS audit management."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    def label(self) -> str:
        return {
            Severity.LOW: "Low",
            Severity.MEDIUM: "Medium",
            Severity.HIGH: "High",
            Severity.CRITICAL: "CRITICAL",
        }[self]


class ComplianceStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    PENDING = "pending"

    def label(self) -> str:
        return {
            ComplianceStatus.PASS: "PASS",
            ComplianceStatus.FAIL: "FAIL",
            ComplianceStatus.NOT_APPLICABLE: "N/A",
            ComplianceStatus.PENDING: "PENDING",
        }[self]


@dataclass
class AuditItem:
    """A single item to be checked during an OHS audit."""

    id: str
    category: str
    description: str
    required: bool = True

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AuditItem):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Finding:
    """The result of auditing a single AuditItem."""

    item: AuditItem
    status: ComplianceStatus
    notes: str = ""
    severity: Optional[Severity] = None

    @property
    def is_actionable(self) -> bool:
        return self.status == ComplianceStatus.FAIL

    def to_dict(self) -> dict:
        return {
            "id": self.item.id,
            "category": self.item.category,
            "description": self.item.description,
            "status": self.status.value,
            "notes": self.notes,
            "severity": self.severity.value if self.severity else None,
        }


@dataclass
class AuditReport:
    """A complete OHS audit report for a site."""

    site_name: str
    auditor: str
    findings: List[Finding] = field(default_factory=list)
    conducted_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.conducted_at is None:
            self.conducted_at = datetime.now()

    # ── filters ───────────────────────────────────────────────────────────────

    @property
    def passed(self) -> List[Finding]:
        return [f for f in self.findings if f.status == ComplianceStatus.PASS]

    @property
    def failed(self) -> List[Finding]:
        return [f for f in self.findings if f.status == ComplianceStatus.FAIL]

    @property
    def not_applicable(self) -> List[Finding]:
        return [f for f in self.findings if f.status == ComplianceStatus.NOT_APPLICABLE]

    @property
    def pending(self) -> List[Finding]:
        return [f for f in self.findings if f.status == ComplianceStatus.PENDING]

    @property
    def applicable(self) -> List[Finding]:
        return [f for f in self.findings if f.status != ComplianceStatus.NOT_APPLICABLE]

    @property
    def critical_failures(self) -> List[Finding]:
        return [f for f in self.failed if f.severity == Severity.CRITICAL]

    # ── metrics ───────────────────────────────────────────────────────────────

    @property
    def compliance_rate(self) -> float:
        """Percentage of scored (PASS or FAIL) items that passed (0–100)."""
        scored = [
            f for f in self.applicable
            if f.status in (ComplianceStatus.PASS, ComplianceStatus.FAIL)
        ]
        if not scored:
            return 0.0
        return len([f for f in scored if f.status == ComplianceStatus.PASS]) / len(scored) * 100

    # ── grouping ──────────────────────────────────────────────────────────────

    def categories(self) -> List[str]:
        seen: List[str] = []
        for f in self.findings:
            if f.item.category not in seen:
                seen.append(f.item.category)
        return seen

    def findings_by_category(self, category: str) -> List[Finding]:
        return [f for f in self.findings if f.item.category == category]

    # ── serialisation ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "site_name": self.site_name,
            "auditor": self.auditor,
            "conducted_at": self.conducted_at.isoformat() if self.conducted_at else None,
            "compliance_rate": round(self.compliance_rate, 1),
            "findings": [f.to_dict() for f in self.findings],
        }
