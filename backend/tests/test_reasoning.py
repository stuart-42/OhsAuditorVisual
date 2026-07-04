from pathlib import Path

import pytest

from sitesentry.consolidation import consolidate
from sitesentry.knowledge_base import KnowledgeBase
from sitesentry.models import Finding, PriorityBand
from sitesentry.reasoning import engage

PACK = Path(__file__).resolve().parents[2] / "packs" / "construction" / "knowledge_base"


@pytest.fixture
def kb():
    return KnowledgeBase(PACK)


def _head():
    return Finding(id="obs_001", hazard="head_injury", control_at_issue="ppe_head",
                   tags=["control.ppe.head"], reason_codes=["not_worn"], priority=PriorityBand.high)


def _foot():
    return Finding(id="obs_002", hazard="foot_injury", control_at_issue="ppe_foot",
                   tags=["control.ppe.foot"], reason_codes=["not_worn"], priority=PriorityBand.medium)


def test_lookup_is_exact(kb):
    assert kb.lookup("control.ppe.head", "not_worn") is not None
    assert kb.lookup("control.ppe.head", "no_such_reason") is None


def test_engage_derives_provisions_and_actions(kb):
    f, unmapped = engage(_head(), kb)
    assert unmapped == []
    assert set(f.engaged_provisions) == {"ppe_reg4", "ppe_reg10", "mhswr_reg3", "hswa_s2", "ppe_reg7"}
    assert "ca_reassess" in f.applicable_actions


def test_shared_action_consolidated_once(kb):
    # both findings engage the general risk-assessment action; it must appear exactly once
    result = consolidate([_head(), _foot()], kb)
    reassess = [a for a in result.actions if a.action_id == "ca_reassess"]
    assert len(reassess) == 1
    assert set(reassess[0].from_findings) == {"obs_001", "obs_002"}


def test_citation_accumulation_and_ordering(kb):
    result = consolidate([_head()], kb)
    reassess = next(a for a in result.actions if a.action_id == "ca_reassess")
    ids = [p.id for p in reassess.discharges_here]
    assert set(ids) == {"mhswr_reg3", "hswa_s2"}
    # specific duties must lead general ones
    scopes = [p.duty_scope.value for p in
              next(a for a in result.actions if a.action_id == "ca_provide_head").discharges_here]
    assert scopes == sorted(scopes, key=lambda s: 0 if s == "specific" else 1)


def test_gap_detection(kb):
    # head protection engages a maintenance duty (ppe_reg7) with no action authored yet -> a gap
    result = consolidate([_head()], kb)
    assert any(g.provision.id == "ppe_reg7" for g in result.gaps)


def test_unmapped_combination_is_flagged(kb):
    f = Finding(id="x", hazard="h", control_at_issue="c",
                tags=["control.ppe.eye"], reason_codes=["not_worn"])  # eye not in mapping yet
    _, unmapped = engage(f, kb)
    assert unmapped == ["control.ppe.eye x not_worn"]
