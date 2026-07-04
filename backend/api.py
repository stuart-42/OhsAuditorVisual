"""FastAPI layer over the SiteSentry deterministic reasoning core.

Serves a browser test harness at GET / and a JSON API for the Flutter app.

Run:
    pip install -r api_requirements.txt
    python -m uvicorn api:app --reload      # from backend/

Then open http://localhost:8000
"""
from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Ensure the backend directory is on sys.path when launched from elsewhere
sys.path.insert(0, str(Path(__file__).parent))

from sitesentry.comments import render_comment
from sitesentry.consolidation import consolidate
from sitesentry.knowledge_base import KnowledgeBase
from sitesentry.models import Finding, PriorityBand
from sitesentry.reasoning import engage

PACK = Path(__file__).resolve().parent.parent / "packs" / "construction" / "knowledge_base"
kb = KnowledgeBase(PACK)

app = FastAPI(title="SiteSentry Reasoning Core", version="0.1.0-milestone1")


# ── Request / response models ─────────────────────────────────────────────────

class FindingIn(BaseModel):
    id: Optional[str] = None
    hazard: str = ""
    control_at_issue: str = ""
    tags: List[str]
    reason_codes: List[str]
    who: str = "An operative"
    hazard_context: str = "the work area"
    outcome: str = "injury"
    priority: str = "medium"


class ConsolidateRequest(BaseModel):
    findings: List[FindingIn]


def _to_finding(f: FindingIn) -> Finding:
    try:
        priority = PriorityBand(f.priority)
    except ValueError:
        priority = PriorityBand.medium
    tag = f.tags[0] if f.tags else ""
    return Finding(
        id=f.id or str(uuid.uuid4())[:8],
        hazard=f.hazard or tag.replace(".", "_"),
        control_at_issue=f.control_at_issue or tag.split(".")[-1],
        tags=f.tags,
        reason_codes=f.reason_codes,
        who=f.who,
        hazard_context=f.hazard_context,
        outcome=f.outcome,
        priority=priority,
    )


# ── API endpoints ─────────────────────────────────────────────────────────────

@app.get("/vocabulary")
def vocabulary():
    """All tags, reason codes, and document types from the construction domain pack."""
    return json.loads((PACK / "vocabulary.json").read_text())


@app.post("/consolidate")
def consolidate_findings(req: ConsolidateRequest):
    """
    Run the full reasoning and consolidation pipeline over a list of findings.
    Returns audit comments per finding, the consolidated action plan, and any gaps.
    All output is advisory and subject to professional judgement.
    """
    if not req.findings:
        raise HTTPException(status_code=400, detail="At least one finding is required.")
    findings = [_to_finding(f) for f in req.findings]
    for f in findings:
        engage(f, kb)
    comments = {f.id: render_comment(f, kb) for f in findings}
    result = consolidate(findings, kb)
    return {
        "advisory": True,
        "comments": [
            {"finding_id": fid, "text": text}
            for fid, text in comments.items()
        ],
        "actions": [
            {
                "action_id": a.action_id,
                "label": a.label,
                "acop_derived": a.acop_derived,
                "from_findings": a.from_findings,
                "discharges": [
                    {
                        "id": p.id,
                        "instrument": p.instrument,
                        "section": p.section,
                        "duty_scope": p.duty_scope.value,
                        "legal_status": p.legal_status.value,
                    }
                    for p in a.discharges_here
                ],
            }
            for a in result.actions
        ],
        "gaps": [
            {
                "provision_id": g.provision.id,
                "instrument": g.provision.instrument,
                "section": g.provision.section,
                "summary": g.provision.summary,
                "from_findings": g.from_findings,
            }
            for g in result.gaps
        ],
    }


# ── Browser test harness ──────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def test_harness():
    return _HARNESS_HTML


_HARNESS_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SiteSentry — Audit Test Harness</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; font-size: 15px; background: #f4f5f7; color: #1a1a2e; }
  header { background: #1a1a2e; color: #fff; padding: 18px 28px; display: flex; align-items: center; gap: 14px; }
  header h1 { font-size: 1.2rem; font-weight: 600; letter-spacing: .02em; }
  header span.sub { font-size: .85rem; opacity: .65; }
  .advisory-banner {
    background: #fff3cd; border-left: 4px solid #e6a817; color: #7a5200;
    padding: 10px 28px; font-size: .88rem; font-weight: 500;
  }
  main { max-width: 900px; margin: 28px auto; padding: 0 16px; }
  .card { background: #fff; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,.1); margin-bottom: 22px; overflow: hidden; }
  .card-head { background: #f0f2f5; padding: 12px 20px; font-weight: 600; font-size: .92rem; border-bottom: 1px solid #e2e4e8; }
  .card-body { padding: 18px 20px; }
  .form-row { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 12px; }
  .form-group { display: flex; flex-direction: column; gap: 5px; flex: 1; min-width: 180px; }
  label { font-size: .82rem; font-weight: 600; color: #555; text-transform: uppercase; letter-spacing: .04em; }
  select, input[type=text] {
    padding: 8px 10px; border: 1px solid #cdd0d5; border-radius: 5px;
    font-size: .92rem; background: #fafbfc; color: #1a1a2e; width: 100%;
  }
  select:focus, input:focus { outline: none; border-color: #4a6fa5; box-shadow: 0 0 0 2px rgba(74,111,165,.18); }
  .btn {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 9px 20px; border: none; border-radius: 5px;
    font-size: .92rem; font-weight: 600; cursor: pointer; transition: opacity .15s;
  }
  .btn:hover { opacity: .87; }
  .btn-add  { background: #4a6fa5; color: #fff; }
  .btn-run  { background: #2d6a4f; color: #fff; font-size: 1rem; padding: 11px 28px; }
  .btn-clear{ background: #e8eaf0; color: #555; }
  #queue { list-style: none; }
  #queue li {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 14px; border: 1px solid #e2e4e8; border-radius: 6px;
    margin-bottom: 8px; background: #fafbfc; gap: 12px;
  }
  #queue li .info { flex: 1; }
  #queue li .tag-pill {
    display: inline-block; background: #e8f0fe; color: #1a3a6e;
    border-radius: 12px; padding: 2px 10px; font-size: .8rem; font-weight: 600; margin-right: 6px;
  }
  #queue li .reason-pill {
    display: inline-block; background: #fff0e0; color: #7a4200;
    border-radius: 12px; padding: 2px 10px; font-size: .8rem; font-weight: 600; margin-right: 6px;
  }
  #queue li .priority-HIGH   { color: #c0392b; font-weight: 700; }
  #queue li .priority-MEDIUM { color: #e67e22; font-weight: 700; }
  #queue li .priority-LOW    { color: #27ae60; font-weight: 700; }
  .btn-remove { background: none; border: none; cursor: pointer; color: #999; font-size: 1.1rem; padding: 2px 6px; }
  .btn-remove:hover { color: #c0392b; }
  #queue-empty { color: #999; font-style: italic; font-size: .9rem; }
  .run-row { display: flex; gap: 12px; align-items: center; margin-top: 4px; }
  #results { display: none; }
  .result-section { margin-bottom: 20px; }
  .result-section h3 { font-size: .92rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; color: #555; margin-bottom: 10px; }
  .comment-block { background: #f0f4ff; border-left: 3px solid #4a6fa5; border-radius: 0 5px 5px 0; padding: 10px 14px; margin-bottom: 8px; font-size: .93rem; line-height: 1.55; }
  .comment-block .finding-id { font-size: .78rem; font-weight: 700; color: #4a6fa5; text-transform: uppercase; margin-bottom: 4px; }
  .action-card { border: 1px solid #e2e4e8; border-radius: 6px; padding: 12px 16px; margin-bottom: 10px; }
  .action-card .action-label { font-weight: 600; margin-bottom: 8px; }
  .action-card .acop-badge {
    display: inline-block; background: #2d6a4f; color: #fff;
    border-radius: 3px; padding: 1px 7px; font-size: .75rem; font-weight: 700; margin-left: 8px; vertical-align: middle;
  }
  .action-card .discharge { font-size: .82rem; color: #555; margin-bottom: 3px; }
  .action-card .discharge .scope-specific { color: #1a3a6e; font-weight: 600; }
  .action-card .discharge .scope-general  { color: #555; }
  .action-card .from-findings { font-size: .8rem; color: #888; margin-top: 6px; }
  .gap-card { border: 1px solid #f5c6cb; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; background: #fff8f8; }
  .gap-card .gap-label { font-weight: 600; color: #c0392b; font-size: .92rem; }
  .gap-card .gap-summary { font-size: .83rem; color: #555; margin-top: 4px; }
  .no-gaps { color: #2d6a4f; font-weight: 600; font-size: .92rem; }
  #error-msg { background: #fff0f0; border-left: 3px solid #c0392b; padding: 10px 14px; border-radius: 0 5px 5px 0; color: #c0392b; margin-bottom: 12px; display: none; }
  .spinner { display: none; width: 20px; height: 20px; border: 3px solid #ccc; border-top-color: #4a6fa5; border-radius: 50%; animation: spin .7s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body>

<header>
  <div>
    <h1>SiteSentry</h1>
    <span class="sub">Deterministic Reasoning Core — Manual Test Harness</span>
  </div>
</header>
<div class="advisory-banner">
  ⚠ Advisory only — all outputs are indicative and subject to the judgement of a qualified professional. This is not a legal determination.
</div>

<main>

  <!-- Add Finding -->
  <div class="card">
    <div class="card-head">Add a Finding</div>
    <div class="card-body">
      <div class="form-row">
        <div class="form-group">
          <label>Control tag</label>
          <select id="tag-select"><option value="">Loading…</option></select>
        </div>
        <div class="form-group">
          <label>Reason</label>
          <select id="reason-select"><option value="">Loading…</option></select>
        </div>
        <div class="form-group" style="max-width:120px">
          <label>Priority</label>
          <select id="priority-select">
            <option value="high">High</option>
            <option value="medium" selected>Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Who (optional)</label>
          <input type="text" id="who-input" placeholder="An operative" value="An operative">
        </div>
        <div class="form-group">
          <label>Hazard context (optional)</label>
          <input type="text" id="context-input" placeholder="the work area" value="the work area">
        </div>
        <div class="form-group">
          <label>Outcome (optional)</label>
          <input type="text" id="outcome-input" placeholder="injury" value="injury">
        </div>
      </div>
      <button class="btn btn-add" onclick="addFinding()">+ Add to queue</button>
    </div>
  </div>

  <!-- Queue -->
  <div class="card">
    <div class="card-head">Findings Queue (<span id="queue-count">0</span>)</div>
    <div class="card-body">
      <ul id="queue"></ul>
      <p id="queue-empty">No findings added yet.</p>
      <div class="run-row" style="margin-top:14px">
        <button class="btn btn-run" onclick="runAudit()">▶ Run Audit</button>
        <button class="btn btn-clear" onclick="clearAll()">✕ Clear all</button>
        <div class="spinner" id="spinner"></div>
      </div>
    </div>
  </div>

  <!-- Results -->
  <div id="results">
    <div id="error-msg"></div>

    <div class="card">
      <div class="card-head">Audit Comments</div>
      <div class="card-body result-section" id="comments-section"></div>
    </div>

    <div class="card">
      <div class="card-head">Consolidated Corrective Action Plan</div>
      <div class="card-body result-section" id="actions-section"></div>
    </div>

    <div class="card">
      <div class="card-head">Gaps — Engaged Provisions with No Action Authored</div>
      <div class="card-body result-section" id="gaps-section"></div>
    </div>
  </div>

</main>

<script>
  const findings = [];
  let tagLabels = {};
  let reasonLabels = {};

  async function loadVocabulary() {
    const vocab = await fetch('/vocabulary').then(r => r.json());
    const ts = document.getElementById('tag-select');
    const rs = document.getElementById('reason-select');
    ts.innerHTML = '';
    rs.innerHTML = '';
    vocab.tags.forEach(t => {
      tagLabels[t.id] = t.label;
      const o = document.createElement('option');
      o.value = t.id; o.textContent = t.label;
      ts.appendChild(o);
    });
    vocab.reason_codes.forEach(r => {
      reasonLabels[r.id] = r.label;
      const o = document.createElement('option');
      o.value = r.id; o.textContent = r.label;
      rs.appendChild(o);
    });
  }

  function addFinding() {
    const tag      = document.getElementById('tag-select').value;
    const reason   = document.getElementById('reason-select').value;
    const priority = document.getElementById('priority-select').value;
    const who      = document.getElementById('who-input').value.trim() || 'An operative';
    const context  = document.getElementById('context-input').value.trim() || 'the work area';
    const outcome  = document.getElementById('outcome-input').value.trim() || 'injury';
    if (!tag || !reason) return;
    findings.push({ id: 'obs_' + (findings.length + 1), tags: [tag], reason_codes: [reason], priority, who, hazard_context: context, outcome });
    renderQueue();
  }

  function removeFinding(idx) {
    findings.splice(idx, 1);
    // Re-number ids
    findings.forEach((f, i) => { f.id = 'obs_' + (i + 1); });
    renderQueue();
  }

  function clearAll() {
    findings.length = 0;
    renderQueue();
    document.getElementById('results').style.display = 'none';
  }

  function renderQueue() {
    const ul = document.getElementById('queue');
    const empty = document.getElementById('queue-empty');
    const count = document.getElementById('queue-count');
    ul.innerHTML = '';
    count.textContent = findings.length;
    if (findings.length === 0) { empty.style.display = ''; return; }
    empty.style.display = 'none';
    findings.forEach((f, i) => {
      const li = document.createElement('li');
      const tagLabel    = tagLabels[f.tags[0]] || f.tags[0];
      const reasonLabel = reasonLabels[f.reason_codes[0]] || f.reason_codes[0];
      li.innerHTML = `
        <div class="info">
          <span class="tag-pill">${tagLabel}</span>
          <span class="reason-pill">${reasonLabel}</span>
          <span class="priority-${f.priority.toUpperCase()}">${f.priority.toUpperCase()}</span>
          <span style="color:#888;font-size:.8rem;margin-left:8px">${f.id} · ${f.who}</span>
        </div>
        <button class="btn-remove" onclick="removeFinding(${i})" title="Remove">✕</button>`;
      ul.appendChild(li);
    });
  }

  async function runAudit() {
    if (findings.length === 0) return;
    document.getElementById('spinner').style.display = 'inline-block';
    document.getElementById('error-msg').style.display = 'none';
    document.getElementById('results').style.display = 'none';
    try {
      const resp = await fetch('/consolidate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({findings}),
      });
      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.detail || 'Server error');
      }
      const data = await resp.json();
      renderResults(data);
    } catch (e) {
      const el = document.getElementById('error-msg');
      el.textContent = 'Error: ' + e.message;
      el.style.display = 'block';
    } finally {
      document.getElementById('spinner').style.display = 'none';
    }
  }

  function renderResults(data) {
    // Comments
    const cs = document.getElementById('comments-section');
    cs.innerHTML = '';
    data.comments.forEach(c => {
      cs.innerHTML += `
        <div class="comment-block">
          <div class="finding-id">${c.finding_id}</div>
          ${c.text}
        </div>`;
    });

    // Actions
    const as = document.getElementById('actions-section');
    as.innerHTML = '';
    if (data.actions.length === 0) {
      as.innerHTML = '<p style="color:#999;font-style:italic">No actions derived.</p>';
    } else {
      data.actions.forEach(a => {
        const badge = a.acop_derived ? '<span class="acop-badge">ACoP</span>' : '';
        const discharges = a.discharges.map(d =>
          `<div class="discharge">
             <span class="scope-${d.duty_scope}">${d.instrument} ${d.section}</span>
             <span style="color:#aaa"> [${d.duty_scope}]</span>
           </div>`
        ).join('');
        as.innerHTML += `
          <div class="action-card">
            <div class="action-label">${a.label}${badge}</div>
            ${discharges}
            <div class="from-findings">From: ${a.from_findings.join(', ')}</div>
          </div>`;
      });
    }

    // Gaps
    const gs = document.getElementById('gaps-section');
    gs.innerHTML = '';
    if (data.gaps.length === 0) {
      gs.innerHTML = '<p class="no-gaps">✓ No gaps — all engaged provisions are discharged by an authored action.</p>';
    } else {
      data.gaps.forEach(g => {
        gs.innerHTML += `
          <div class="gap-card">
            <div class="gap-label">⚠ ${g.instrument} ${g.section}</div>
            <div class="gap-summary">${g.summary}</div>
            <div style="font-size:.8rem;color:#888;margin-top:4px">From: ${g.from_findings.join(', ')}</div>
          </div>`;
      });
    }

    document.getElementById('results').style.display = 'block';
    document.getElementById('results').scrollIntoView({behavior: 'smooth', block: 'start'});
  }

  loadVocabulary();
</script>
</body>
</html>
"""
