import pytest
from sitesentry.models import (
    AuditItem, AuditReport, ComplianceStatus, Finding, Severity,
)


def make_item(id="X-001", category="Test", description="Test item", required=True):
    return AuditItem(id, category, description, required)


def make_finding(item=None, status=ComplianceStatus.PASS, notes="", severity=None):
    return Finding(item or make_item(), status, notes, severity)


class TestAuditItem:
    def test_equality_by_id(self):
        assert AuditItem("X-001", "Cat", "A") == AuditItem("X-001", "Cat", "B")

    def test_inequality_different_id(self):
        assert AuditItem("X-001", "Cat", "D") != AuditItem("X-002", "Cat", "D")

    def test_hashable(self):
        item = make_item()
        assert item in {item}

    def test_required_default(self):
        assert AuditItem("X-001", "Cat", "Desc").required is True


class TestComplianceStatus:
    @pytest.mark.parametrize("status,expected", [
        (ComplianceStatus.PASS, "PASS"),
        (ComplianceStatus.FAIL, "FAIL"),
        (ComplianceStatus.NOT_APPLICABLE, "N/A"),
        (ComplianceStatus.PENDING, "PENDING"),
    ])
    def test_label(self, status, expected):
        assert status.label() == expected


class TestSeverity:
    @pytest.mark.parametrize("severity,expected", [
        (Severity.LOW, "Low"),
        (Severity.MEDIUM, "Medium"),
        (Severity.HIGH, "High"),
        (Severity.CRITICAL, "CRITICAL"),
    ])
    def test_label(self, severity, expected):
        assert severity.label() == expected


class TestFinding:
    def test_is_actionable_when_failed(self):
        assert make_finding(status=ComplianceStatus.FAIL).is_actionable is True

    def test_not_actionable_when_passed(self):
        assert make_finding(status=ComplianceStatus.PASS).is_actionable is False

    @pytest.mark.parametrize("status", [
        ComplianceStatus.NOT_APPLICABLE,
        ComplianceStatus.PENDING,
    ])
    def test_not_actionable_for_other_statuses(self, status):
        assert make_finding(status=status).is_actionable is False

    def test_to_dict_with_severity(self):
        item = make_item("T-001")
        d = Finding(item, ComplianceStatus.FAIL, "bad", Severity.HIGH).to_dict()
        assert d["id"] == "T-001"
        assert d["status"] == "fail"
        assert d["notes"] == "bad"
        assert d["severity"] == "high"

    def test_to_dict_no_severity(self):
        assert make_finding().to_dict()["severity"] is None


class TestAuditReport:
    def _mixed_report(self):
        findings = [
            Finding(AuditItem("P-001", "Cat", "Pass"), ComplianceStatus.PASS),
            Finding(AuditItem("F-001", "Cat", "Fail"), ComplianceStatus.FAIL, severity=Severity.MEDIUM),
            Finding(AuditItem("N-001", "Cat", "NA"),   ComplianceStatus.NOT_APPLICABLE),
            Finding(AuditItem("Q-001", "Cat", "Pend"), ComplianceStatus.PENDING),
        ]
        return AuditReport("Site", "Auditor", findings)

    def test_passed_filter(self):
        report = self._mixed_report()
        assert len(report.passed) == 1
        assert report.passed[0].item.id == "P-001"

    def test_failed_filter(self):
        report = self._mixed_report()
        assert len(report.failed) == 1
        assert report.failed[0].item.id == "F-001"

    def test_compliance_rate_excludes_na_and_pending(self):
        # 1 pass, 1 fail scored → 50 %
        assert abs(self._mixed_report().compliance_rate - 50.0) < 0.01

    def test_compliance_rate_empty(self):
        assert AuditReport("S", "A", []).compliance_rate == 0.0

    def test_compliance_rate_all_na(self):
        item = AuditItem("N-001", "Cat", "NA")
        report = AuditReport("S", "A", [Finding(item, ComplianceStatus.NOT_APPLICABLE)])
        assert report.compliance_rate == 0.0

    def test_compliance_rate_all_pending(self):
        item = AuditItem("Q-001", "Cat", "Pend")
        report = AuditReport("S", "A", [Finding(item, ComplianceStatus.PENDING)])
        assert report.compliance_rate == 0.0

    def test_critical_failures(self):
        findings = [
            Finding(AuditItem("C-001", "Cat", "Crit"), ComplianceStatus.FAIL, severity=Severity.CRITICAL),
            Finding(AuditItem("C-002", "Cat", "High"), ComplianceStatus.FAIL, severity=Severity.HIGH),
        ]
        report = AuditReport("S", "A", findings)
        assert len(report.critical_failures) == 1
        assert report.critical_failures[0].item.id == "C-001"

    def test_categories_order_preserved(self):
        findings = [
            Finding(AuditItem("A-001", "Alpha", "x"), ComplianceStatus.PASS),
            Finding(AuditItem("B-001", "Beta",  "y"), ComplianceStatus.PASS),
            Finding(AuditItem("A-002", "Alpha", "z"), ComplianceStatus.PASS),
        ]
        assert AuditReport("S", "A", findings).categories() == ["Alpha", "Beta"]

    def test_findings_by_category(self):
        findings = [
            Finding(AuditItem("A-001", "Alpha", "x"), ComplianceStatus.PASS),
            Finding(AuditItem("B-001", "Beta",  "y"), ComplianceStatus.FAIL),
            Finding(AuditItem("A-002", "Alpha", "z"), ComplianceStatus.PASS),
        ]
        report = AuditReport("S", "A", findings)
        assert len(report.findings_by_category("Alpha")) == 2
        assert len(report.findings_by_category("Beta")) == 1
        assert len(report.findings_by_category("Gamma")) == 0

    def test_to_dict_structure(self):
        report = self._mixed_report()
        d = report.to_dict()
        assert d["site_name"] == "Site"
        assert d["auditor"] == "Auditor"
        assert "compliance_rate" in d
        assert len(d["findings"]) == 4

    def test_conducted_at_defaults_to_now(self):
        from datetime import datetime
        assert isinstance(AuditReport("S", "A", []).conducted_at, datetime)
