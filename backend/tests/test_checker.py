import pytest
from sitesentry.checker import STANDARD_CHECKLIST, build_report, run_checklist
from sitesentry.models import AuditItem, AuditReport, ComplianceStatus, Severity


class TestStandardChecklist:
    def test_no_duplicate_ids(self):
        ids = [item.id for item in STANDARD_CHECKLIST]
        assert len(ids) == len(set(ids))

    def test_all_have_categories(self):
        for item in STANDARD_CHECKLIST:
            assert item.category, f"{item.id} has empty category"

    def test_all_have_descriptions(self):
        for item in STANDARD_CHECKLIST:
            assert item.description, f"{item.id} has empty description"

    def test_minimum_ten_items(self):
        assert len(STANDARD_CHECKLIST) >= 10


class TestRunChecklist:
    def test_empty_answers_all_pending(self):
        findings = run_checklist({})
        assert all(f.status == ComplianceStatus.PENDING for f in findings)

    def test_finding_count_matches_checklist(self):
        assert len(run_checklist({})) == len(STANDARD_CHECKLIST)

    def test_pass_recorded(self):
        first = STANDARD_CHECKLIST[0]
        findings = run_checklist({first.id: (ComplianceStatus.PASS, "all good", None)})
        result = next(f for f in findings if f.item.id == first.id)
        assert result.status == ComplianceStatus.PASS
        assert result.notes == "all good"
        assert result.severity is None

    def test_fail_with_severity_recorded(self):
        first = STANDARD_CHECKLIST[0]
        findings = run_checklist({first.id: (ComplianceStatus.FAIL, "broken", Severity.CRITICAL)})
        result = next(f for f in findings if f.item.id == first.id)
        assert result.status == ComplianceStatus.FAIL
        assert result.severity == Severity.CRITICAL

    def test_na_recorded(self):
        first = STANDARD_CHECKLIST[0]
        findings = run_checklist({first.id: (ComplianceStatus.NOT_APPLICABLE, "n/a", None)})
        result = next(f for f in findings if f.item.id == first.id)
        assert result.status == ComplianceStatus.NOT_APPLICABLE

    def test_custom_checklist(self):
        custom = [AuditItem("C-001", "Custom", "Custom item")]
        findings = run_checklist({"C-001": (ComplianceStatus.PASS, "", None)}, custom)
        assert len(findings) == 1
        assert findings[0].status == ComplianceStatus.PASS

    def test_unknown_answer_id_ignored(self):
        custom = [AuditItem("C-001", "Custom", "Item")]
        answers = {
            "C-001": (ComplianceStatus.PASS, "", None),
            "UNKNOWN-ID": (ComplianceStatus.FAIL, "", None),
        }
        findings = run_checklist(answers, custom)
        assert [f.item.id for f in findings] == ["C-001"]

    def test_all_statuses_survive_round_trip(self):
        first = STANDARD_CHECKLIST[0]
        for status in ComplianceStatus:
            findings = run_checklist({first.id: (status, "", None)})
            result = next(f for f in findings if f.item.id == first.id)
            assert result.status == status


class TestBuildReport:
    def test_returns_audit_report(self):
        assert isinstance(build_report("Site X", "Alice", {}), AuditReport)

    def test_site_and_auditor_set(self):
        report = build_report("Warehouse A", "Bob", {})
        assert report.site_name == "Warehouse A"
        assert report.auditor == "Bob"

    def test_findings_count_matches_checklist(self):
        report = build_report("S", "A", {})
        assert len(report.findings) == len(STANDARD_CHECKLIST)

    def test_with_custom_checklist(self):
        custom = [AuditItem("Z-001", "Z", "Zap")]
        report = build_report("S", "A", {"Z-001": (ComplianceStatus.PASS, "", None)}, custom)
        assert len(report.findings) == 1
        assert report.findings[0].status == ComplianceStatus.PASS
