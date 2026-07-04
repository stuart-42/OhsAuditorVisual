"""Report formatters for AuditReport objects."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import AuditReport


def generate_text_report(report: "AuditReport") -> str:
    """Return a human-readable plaintext audit report."""
    lines: list = []

    def h1(text: str) -> None:
        lines.append("")
        lines.append("=" * 60)
        lines.append(f"  {text}")
        lines.append("=" * 60)

    def h2(text: str) -> None:
        lines.append("")
        lines.append(f"  {text}")
        lines.append("  " + "─" * (len(text) + 2))

    h1("OHS AUDIT REPORT")
    lines.append(f"  Site    : {report.site_name}")
    lines.append(f"  Auditor : {report.auditor}")
    if report.conducted_at:
        lines.append(f"  Date    : {report.conducted_at.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"  Score   : {report.compliance_rate:.1f}% compliant")

    if report.critical_failures:
        lines.append("")
        lines.append("  !! CRITICAL ISSUES REQUIRE IMMEDIATE ACTION !!")
        for f in report.critical_failures:
            lines.append(f"     [{f.item.id}] {f.item.description}")
            if f.notes:
                lines.append(f"           → {f.notes}")

    for category in report.categories():
        h2(category)
        for finding in report.findings_by_category(category):
            status_label = finding.status.label()
            sev = f"  [{finding.severity.label()}]" if finding.severity else ""
            lines.append(
                f"  {status_label:<8} {finding.item.id}  {finding.item.description}{sev}"
            )
            if finding.notes:
                lines.append(f"           → {finding.notes}")

    h2("SUMMARY")
    lines.append(f"  Passed         : {len(report.passed)}")
    lines.append(f"  Failed         : {len(report.failed)}")
    lines.append(f"  Not Applicable : {len(report.not_applicable)}")
    lines.append(f"  Pending        : {len(report.pending)}")
    lines.append(f"  Compliance     : {report.compliance_rate:.1f}%")
    lines.append("")
    lines.append("=" * 60)
    lines.append("")

    return "\n".join(lines)


def generate_json_report(report: "AuditReport") -> str:
    """Return a JSON-serialised audit report."""
    return json.dumps(report.to_dict(), indent=2, default=str)
