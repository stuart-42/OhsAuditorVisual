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
    return Finding(
        id="obs_001",
        hazard="head_injury",
        control_at_issue="ppe_head",
        tags=["control.ppe.head"],
        reason_codes=["not_worn"],
        priority=PriorityBand.high,
    )


def _foot():
    return Finding(
        id="obs_002",
        hazard="foot_injury",
        control_at_issue="ppe_foot",
        tags=["control.ppe.foot"],
        reason_codes=["not_worn"],
        priority=PriorityBand.medium,
    )


def test_lookup_is_exact(kb):
    assert kb.lookup("control.ppe.head", "not_worn") is not None
    assert kb.lookup("control.ppe.head", "no_such_reason") is None


def test_engage_derives_provisions_and_actions(kb):
    f, unmapped = engage(_head(), kb)
    assert unmapped == []
    assert set(f.engaged_provisions) == {
        "ppe_reg4",
        "ppe_reg10",
        "mhswr_reg3",
        "hswa_s2",
        "ppe_reg7",
    }
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
    scopes = [
        p.duty_scope.value
        for p in next(a for a in result.actions if a.action_id == "ca_provide_head").discharges_here
    ]
    assert scopes == sorted(scopes, key=lambda s: 0 if s == "specific" else 1)


def test_gap_detection():
    # Synthetic KB: one provision engaged by a finding, but the selected action does not discharge it.
    # Tests the gap-detection mechanism independently of the production KB's completeness state.
    import json
    import tempfile

    prov = [
        {
            "id": "syn_p1",
            "instrument": "Synthetic Act",
            "section": "s1",
            "legal_status": "law",
            "duty_scope": "specific",
            "summary": "Synthetic provision",
        }
    ]
    acts = [
        {
            "id": "syn_a1",
            "label": "Synthetic action",
            "discharges": [],
            "sourced_from": {},
            "acop_derived": False,
            "comment_template": "",
        }
    ]
    mapp = [
        {
            "tag": "syn.tag",
            "reason": "syn_reason",
            "hazard": "syn",
            "provisions": ["syn_p1"],
            "actions": ["syn_a1"],
        }
    ]
    vocab = {"tags": [], "reason_codes": [], "document_types": []}

    with tempfile.TemporaryDirectory() as td:
        from pathlib import Path

        tdp = Path(td)
        (tdp / "provisions.json").write_text(json.dumps({"provisions": prov}))
        (tdp / "actions.json").write_text(json.dumps({"actions": acts}))
        (tdp / "mapping.json").write_text(json.dumps({"map": mapp}))
        (tdp / "vocabulary.json").write_text(json.dumps(vocab))
        syn_kb = KnowledgeBase(tdp)

    f = Finding(
        id="gap_obs",
        hazard="h",
        control_at_issue="c",
        tags=["syn.tag"],
        reason_codes=["syn_reason"],
    )
    engage(f, syn_kb)
    result = consolidate([f], syn_kb)
    assert any(g.provision.id == "syn_p1" for g in result.gaps)


def test_maintenance_action_closes_ppe_reg7_gap(kb):
    # Adding ca_maintain_ppe to the KB should discharge ppe_reg7 so it is no longer a gap.
    result = consolidate([_head()], kb)
    assert not any(g.provision.id == "ppe_reg7" for g in result.gaps)
    assert any(a.action_id == "ca_maintain_ppe" for a in result.actions)


def test_unmapped_combination_is_flagged(kb):
    # hi-vis / doesnt_fit is not authored in the mapping — must surface as unmapped.
    f = Finding(
        id="x",
        hazard="h",
        control_at_issue="c",
        tags=["control.ppe.hiviz"],
        reason_codes=["doesnt_fit"],
    )
    _, unmapped = engage(f, kb)
    assert unmapped == ["control.ppe.hiviz x doesnt_fit"]


def test_eye_protection_now_mapped(kb):
    # eye x not_worn was previously unmapped; it must now resolve to provisions and actions.
    f = Finding(
        id="y",
        hazard="h",
        control_at_issue="c",
        tags=["control.ppe.eye"],
        reason_codes=["not_worn"],
    )
    f, unmapped = engage(f, kb)
    assert unmapped == []
    assert "ca_provide_eye" in f.applicable_actions
    assert "ppe_reg4" in f.engaged_provisions
