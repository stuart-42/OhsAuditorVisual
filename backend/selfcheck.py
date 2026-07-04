"""
Self-check script using only the Python standard library.
Verifies package structure, models, checker, and reporter without
requiring any third-party packages.

Run with:
    python selfcheck.py          (from backend/)
"""

from __future__ import annotations

import json
import os
import sys
import traceback
from typing import Callable, List, Tuple

# Ensure the backend directory is on sys.path when run from there
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_OK = "\033[32m  OK\033[0m"
_FAIL = "\033[31m  FAIL\033[0m"

_results: List[Tuple[str, bool, str]] = []


def check(name: str) -> Callable:
    """Decorator: run the function immediately and record pass/fail."""
    def decorator(fn: Callable) -> Callable:
        try:
            fn()
            _results.append((name, True, ""))
        except Exception:
            _results.append((name, False, traceback.format_exc()))
        return fn
    return decorator


# ── Individual checks ─────────────────────────────────────────────────────────

@check("import sitesentry package")
def _import_package() -> None:
    import sitesentry
    assert hasattr(sitesentry, "__version__"), "__version__ missing"


@check("import sitesentry.models")
def _import_models() -> None:
    from sitesentry.models import (  # noqa: F401
        AuditItem, AuditReport, ComplianceStatus, Finding, Severity,
    )


@check("import sitesentry.checker")
def _import_checker() -> None:
    from sitesentry.checker import (  # noqa: F401
        STANDARD_CHECKLIST, build_report, run_checklist,
    )


@check("import sitesentry.reporter")
def _import_reporter() -> None:
    from sitesentry.reporter import (  # noqa: F401
        generate_json_report, generate_text_report,
    )


@check("AuditItem equality by id")
def _audit_item_equality() -> None:
    from sitesentry.models import AuditItem
    a = AuditItem("X-001", "Cat", "Desc A")
    b = AuditItem("X-001", "Cat", "Desc B")
    c = AuditItem("X-002", "Cat", "Desc A")
    assert a == b, "same id should be equal"
    assert a != c, "different id should not be equal"


@check("ComplianceStatus labels")
def _status_labels() -> None:
    from sitesentry.models import ComplianceStatus
    assert ComplianceStatus.PASS.label() == "PASS"
    assert ComplianceStatus.FAIL.label() == "FAIL"
    assert ComplianceStatus.NOT_APPLICABLE.label() == "N/A"
    assert ComplianceStatus.PENDING.label() == "PENDING"


@check("Severity labels")
def _severity_labels() -> None:
    from sitesentry.models import Severity
    assert Severity.LOW.label() == "Low"
    assert Severity.MEDIUM.label() == "Medium"
    assert Severity.HIGH.label() == "High"
    assert Severity.CRITICAL.label() == "CRITICAL"


@check("run_checklist — PENDING for missing items")
def _pending_for_missing() -> None:
    from sitesentry.checker import run_checklist
    from sitesentry.models import ComplianceStatus
    findings = run_checklist({})
    assert all(f.status == ComplianceStatus.PENDING for f in findings)


@check("run_checklist — correct status recorded")
def _status_recorded() -> None:
    from sitesentry.checker import STANDARD_CHECKLIST, run_checklist
    from sitesentry.models import ComplianceStatus
    first_id = STANDARD_CHECKLIST[0].id
    findings = run_checklist({first_id: (ComplianceStatus.PASS, "ok", None)})
    result = next(f for f in findings if f.item.id == first_id)
    assert result.status == ComplianceStatus.PASS


@check("AuditReport.compliance_rate calculation")
def _compliance_rate() -> None:
    from sitesentry.checker import run_checklist
    from sitesentry.models import AuditItem, AuditReport, ComplianceStatus
    checklist = [
        AuditItem("T-001", "Test", "Item 1"),
        AuditItem("T-002", "Test", "Item 2"),
        AuditItem("T-003", "Test", "Item 3"),
        AuditItem("T-004", "Test", "Item 4"),
    ]
    answers = {
        "T-001": (ComplianceStatus.PASS, "", None),
        "T-002": (ComplianceStatus.PASS, "", None),
        "T-003": (ComplianceStatus.FAIL, "", None),
        "T-004": (ComplianceStatus.NOT_APPLICABLE, "", None),
    }
    findings = run_checklist(answers, checklist)
    report = AuditReport("Site", "Auditor", findings)
    # 2 pass out of 3 scored (NOT_APPLICABLE excluded; no PENDING)
    expected = 200 / 3
    assert abs(report.compliance_rate - expected) < 0.01, (
        f"expected {expected:.4f}, got {report.compliance_rate:.4f}"
    )


@check("AuditReport.critical_failures filter")
def _critical_failures() -> None:
    from sitesentry.models import AuditItem, AuditReport, ComplianceStatus, Finding, Severity
    item = AuditItem("C-001", "Cat", "Critical item")
    finding = Finding(item, ComplianceStatus.FAIL, "bad", Severity.CRITICAL)
    report = AuditReport("S", "A", [finding])
    assert len(report.critical_failures) == 1
    assert report.critical_failures[0].item.id == "C-001"


@check("generate_text_report produces non-empty string with header")
def _text_report() -> None:
    from sitesentry.checker import build_report
    from sitesentry.reporter import generate_text_report
    report = build_report("Site", "Auditor", {})
    text = generate_text_report(report)
    assert isinstance(text, str) and len(text) > 100
    assert "OHS AUDIT REPORT" in text


@check("generate_json_report produces valid JSON with expected keys")
def _json_report() -> None:
    from sitesentry.checker import build_report
    from sitesentry.reporter import generate_json_report
    report = build_report("Site", "Auditor", {})
    data = json.loads(generate_json_report(report))
    assert data["site_name"] == "Site"
    assert data["auditor"] == "Auditor"
    assert isinstance(data["findings"], list)


@check("STANDARD_CHECKLIST has no duplicate IDs")
def _no_duplicate_ids() -> None:
    from sitesentry.checker import STANDARD_CHECKLIST
    ids = [item.id for item in STANDARD_CHECKLIST]
    assert len(ids) == len(set(ids)), "Duplicate item IDs detected"


@check("AuditReport.findings_by_category filters correctly")
def _findings_by_category() -> None:
    from sitesentry.models import AuditItem, AuditReport, ComplianceStatus, Finding
    a = AuditItem("A-001", "Alpha", "Item A")
    b = AuditItem("B-001", "Beta", "Item B")
    report = AuditReport("S", "A", [
        Finding(a, ComplianceStatus.PASS),
        Finding(b, ComplianceStatus.FAIL),
    ])
    assert len(report.findings_by_category("Alpha")) == 1
    assert len(report.findings_by_category("Beta")) == 1
    assert len(report.findings_by_category("Gamma")) == 0


# ── Runner ────────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"\n{'=' * 58}")
    print("  SiteSentry self-check  (standard library only)")
    print(f"{'=' * 58}\n")

    for name, passed, tb in _results:
        icon = _OK if passed else _FAIL
        print(f"{icon}  {name}")
        if tb:
            for line in tb.strip().splitlines():
                print(f"         {line}")

    total = len(_results)
    n_passed = sum(1 for _, ok, _ in _results if ok)
    n_failed = total - n_passed

    print(f"\n  {n_passed}/{total} checks passed", end="")
    if n_failed:
        print(f", {n_failed} failed")
    else:
        print(" — all good!")
    print()

    sys.exit(0 if n_failed == 0 else 1)


if __name__ == "__main__":
    main()
