"""
Worked example: a complete OHS site audit using the SiteSentry backend.

Run with:
    python -m sitesentry.demo          (from backend/)
"""

from __future__ import annotations

import json

from .checker import build_report
from .models import ComplianceStatus, Severity
from .reporter import generate_json_report, generate_text_report

P = ComplianceStatus.PASS
F = ComplianceStatus.FAIL
NA = ComplianceStatus.NOT_APPLICABLE


def _demo_acme_warehouse():
    """Simulate a real-world warehouse audit with a mix of pass/fail findings."""
    answers = {
        "FE-001": (P,  "All 12 extinguishers tagged; last service Jan 2026", None),
        "FE-002": (P,  "4 exits clearly marked and unobstructed", None),
        "FE-003": (F,  "Last test was 18 months ago — overdue", Severity.HIGH),
        "FE-004": (P,  "Warden list posted on noticeboard, updated Feb 2026", None),
        "EL-001": (P,  "3 distribution boards: all labeled and accessible", None),
        "EL-002": (F,  "Frayed cable found near server room entry door", Severity.CRITICAL),
        "EL-003": (P,  "RCDs tested 6 weeks ago; records on file", None),
        "EL-004": (F,  "Extension leads in office B have no PAT tags", Severity.MEDIUM),
        "CH-001": (P,  "SDS binder complete and indexed", None),
        "CH-002": (F,  "Unlabelled drum in storage room B", Severity.HIGH),
        "CH-003": (P,  "Two spill kits, both fully stocked", None),
        "WK-001": (P,  "All walkways clear", None),
        "WK-002": (P,  "Adequate lighting confirmed in all areas", None),
        "WK-003": (P,  "First aid kit restocked 2025-12-01; expiry 2027", None),
        "WK-004": (F,  "Last incident entry dated 4 months ago — gap suspected", Severity.LOW),
        "WK-005": (P,  "All mandatory signage visible and legible", None),
        "PP-001": (P,  "Hard hats, vests, safety glasses in good condition", None),
        "PP-002": (NA, "PPE station instructions not applicable — office zone", None),
        "PP-003": (P,  "No damaged/expired PPE found", None),
        "MH-001": (P,  "2 pallet jacks and a reach stacker available", None),
        "MH-002": (F,  "3 new warehouse staff have no manual handling training record", Severity.MEDIUM),
    }
    return build_report("Acme Warehouse — Site A", "J. Smith", answers)


def main() -> None:
    print("SiteSentry OHS Audit Backend — Worked Example")
    print("=" * 60)

    report = _demo_acme_warehouse()

    print("\n[1] Text report\n")
    print(generate_text_report(report))

    print("\n[2] JSON report (summary fields)\n")
    data = json.loads(generate_json_report(report))
    print(f"  Site          : {data['site_name']}")
    print(f"  Auditor       : {data['auditor']}")
    print(f"  Compliance    : {data['compliance_rate']}%")
    print(f"  Total findings: {len(data['findings'])}")

    print("\n[3] Actionable findings (FAIL)\n")
    for finding in report.failed:
        sev = f"  [{finding.severity.label()}]" if finding.severity else ""
        print(f"  {finding.item.id}  {finding.item.description}{sev}")
        if finding.notes:
            print(f"       → {finding.notes}")

    print()


if __name__ == "__main__":
    main()
