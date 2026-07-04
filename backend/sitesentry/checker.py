"""Standard OHS checklist and result aggregation."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .models import AuditItem, AuditReport, ComplianceStatus, Finding, Severity

# ── Standard OHS checklist ────────────────────────────────────────────────────

STANDARD_CHECKLIST: List[AuditItem] = [
    # Fire Safety
    AuditItem("FE-001", "Fire Safety", "Fire extinguishers present and in-date"),
    AuditItem("FE-002", "Fire Safety", "Emergency exits clearly marked and unobstructed"),
    AuditItem("FE-003", "Fire Safety", "Fire alarm system tested within 12 months"),
    AuditItem("FE-004", "Fire Safety", "Fire warden list posted and current"),
    # Electrical
    AuditItem("EL-001", "Electrical", "Electrical panels accessible and labeled"),
    AuditItem("EL-002", "Electrical", "No exposed wiring or damaged cables visible"),
    AuditItem("EL-003", "Electrical", "RCDs tested and documented within 3 months"),
    AuditItem("EL-004", "Electrical", "Portable appliances tested (PAT) and tagged"),
    # Chemical / Hazmat
    AuditItem("CH-001", "Chemical", "SDS sheets available for all hazardous substances"),
    AuditItem("CH-002", "Chemical", "All chemicals correctly labelled and stored"),
    AuditItem("CH-003", "Chemical", "Spill kits available and stocked"),
    # Workplace / General
    AuditItem("WK-001", "Workplace", "Walkways free of obstructions and trip hazards"),
    AuditItem("WK-002", "Workplace", "Adequate lighting in all work areas"),
    AuditItem("WK-003", "Workplace", "First aid kit stocked, accessible, and in-date"),
    AuditItem("WK-004", "Workplace", "Incident register up to date"),
    AuditItem("WK-005", "Workplace", "Safety signage visible and legible"),
    # PPE
    AuditItem("PP-001", "PPE", "Required PPE available and in good condition"),
    AuditItem("PP-002", "PPE", "PPE usage instructions posted at point of use"),
    AuditItem("PP-003", "PPE", "Damaged or expired PPE removed from service"),
    # Manual Handling
    AuditItem("MH-001", "Manual Handling", "Manual handling aids available where required"),
    AuditItem("MH-002", "Manual Handling", "Staff trained in safe manual handling"),
]

# ── Types ─────────────────────────────────────────────────────────────────────

AnswerTuple = Tuple[ComplianceStatus, str, Optional[Severity]]
AnswerMap = Dict[str, AnswerTuple]

# ── Public API ────────────────────────────────────────────────────────────────


def run_checklist(
    answers: AnswerMap,
    checklist: Optional[List[AuditItem]] = None,
) -> List[Finding]:
    """
    Build a list of Findings from *answers* (a map of item_id → (status, notes, severity)).
    Items in *checklist* that have no answer are recorded as PENDING.
    Unknown keys in *answers* are silently ignored.
    """
    if checklist is None:
        checklist = STANDARD_CHECKLIST
    findings: List[Finding] = []
    for item in checklist:
        if item.id in answers:
            status, notes, severity = answers[item.id]
            findings.append(Finding(item, status, notes, severity))
        else:
            findings.append(Finding(item, ComplianceStatus.PENDING))
    return findings


def build_report(
    site_name: str,
    auditor: str,
    answers: AnswerMap,
    checklist: Optional[List[AuditItem]] = None,
) -> AuditReport:
    """Convenience wrapper: run the checklist and return a complete AuditReport."""
    findings = run_checklist(answers, checklist)
    return AuditReport(site_name=site_name, auditor=auditor, findings=findings)
