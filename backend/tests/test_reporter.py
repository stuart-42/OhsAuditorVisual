import json
import pytest
from sitesentry.models import AuditItem, AuditReport, ComplianceStatus, Finding, Severity
from sitesentry.reporter import generate_json_report, generate_text_report


def _simple_report() -> AuditReport:
    findings = [
        Finding(AuditItem("T-001", "Test", "Item one"),  ComplianceStatus.PASS, "all good"),
        Finding(AuditItem("T-002", "Test", "Item two"),  ComplianceStatus.FAIL, "broken", Severity.HIGH),
    ]
    return AuditReport("Test Site", "Tester", findings)


class TestTextReport:
    def test_returns_string(self):
        assert isinstance(generate_text_report(_simple_report()), str)

    def test_contains_site_name(self):
        assert "Test Site" in generate_text_report(_simple_report())

    def test_contains_auditor(self):
        assert "Tester" in generate_text_report(_simple_report())

    def test_contains_ohs_header(self):
        assert "OHS AUDIT REPORT" in generate_text_report(_simple_report())

    def test_contains_pass_and_fail(self):
        text = generate_text_report(_simple_report())
        assert "PASS" in text
        assert "FAIL" in text

    def test_compliance_rate_shown(self):
        assert "50.0%" in generate_text_report(_simple_report())

    def test_notes_included(self):
        text = generate_text_report(_simple_report())
        assert "all good" in text
        assert "broken" in text

    def test_critical_warning_shown(self):
        item = AuditItem("C-001", "Cat", "Critical thing")
        report = AuditReport("S", "A", [
            Finding(item, ComplianceStatus.FAIL, "boom", Severity.CRITICAL),
        ])
        assert "CRITICAL" in generate_text_report(report)

    def test_empty_report_does_not_crash(self):
        text = generate_text_report(AuditReport("S", "A", []))
        assert "OHS AUDIT REPORT" in text

    def test_summary_section_present(self):
        assert "SUMMARY" in generate_text_report(_simple_report())


class TestJsonReport:
    def test_returns_valid_json(self):
        json.loads(generate_json_report(_simple_report()))  # must not raise

    def test_site_name_in_json(self):
        assert json.loads(generate_json_report(_simple_report()))["site_name"] == "Test Site"

    def test_auditor_in_json(self):
        assert json.loads(generate_json_report(_simple_report()))["auditor"] == "Tester"

    def test_findings_list_length(self):
        data = json.loads(generate_json_report(_simple_report()))
        assert len(data["findings"]) == 2

    def test_compliance_rate_in_json(self):
        assert json.loads(generate_json_report(_simple_report()))["compliance_rate"] == 50.0

    def test_severity_serialised(self):
        data = json.loads(generate_json_report(_simple_report()))
        failed = [f for f in data["findings"] if f["status"] == "fail"]
        assert len(failed) == 1
        assert failed[0]["severity"] == "high"

    def test_no_severity_is_null(self):
        data = json.loads(generate_json_report(_simple_report()))
        passed = [f for f in data["findings"] if f["status"] == "pass"]
        assert passed[0]["severity"] is None

    def test_conducted_at_present(self):
        data = json.loads(generate_json_report(_simple_report()))
        assert data["conducted_at"] is not None
