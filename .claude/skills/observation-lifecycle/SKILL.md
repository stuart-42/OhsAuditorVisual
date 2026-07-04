---
name: observation-lifecycle
description: The canonical Observation data model and its human-in-the-loop state machine. Use this skill whenever the work involves creating or changing how observations/detections are stored, reviewed, amended, deleted, tracked, or reported, designing any API endpoint or UI screen that touches an observation, recording action taken, or enforcing the rule that AI never finalises anything. Trigger it even if the user only mentions "observation", "record", "review", "status", "action taken", "audit", or "delete", and even if they don't name this skill. Every endpoint and screen that touches an observation must respect this model.
---

# Observation Lifecycle

The unit of work is an **Observation**. Humans control every transition; the AI only proposes.

## State machine

```
draft ──▶ flagged(AI) ──▶ reviewed(human) ──▶ action_recommended ──▶ action_taken ──▶ closed
                              │
                              └─▶ rejected (human dismisses the flag)
```

Rules:
- `flagged` is the only state the AI may set. **Every** later transition is human-driven.
- A human may **amend** or **delete** an observation in any state.
- The AI may **never** move an observation to `reviewed`, `action_taken`, or `closed`, and
  may never delete one.
- Deletion is a true erasure (see `gdpr-dpia`) and is itself audit-logged.

## Schema

```json
{
  "id": "uuid",
  "tenant_id": "uuid",              // ALWAYS present; never unscopeable
  "site_id": "uuid",
  "inspector_id": "uuid",
  "created_at": "iso8601",
  "updated_at": "iso8601",
  "media": [{ "type": "photo|video", "s3_key": "...", "redacted": true }],
  "ai_detections": [{
    "hazard_id": "wah_unguarded_edge",
    "confidence": 0.82,
    "source": "edge|bedrock",
    "model_version": "...",         // provenance is mandatory
    "advisory": true
  }],
  "human_edits": [{ "by": "uuid", "at": "iso8601", "change": "..." }],
  "severity": "low|medium|high",
  "regulation_refs": ["Work at Height Regulations 2005 (reg 6)"],
  "recommended_action": "string (advisory)",
  "action_taken": { "description": "string", "by": "uuid", "at": "iso8601" },
  "status": "draft|flagged|reviewed|rejected|action_recommended|action_taken|closed",
  "audit_log": [{ "event": "...", "by": "uuid", "at": "iso8601" }]
}
```

## Enforcement

- Validate `tenant_id` on every read and write.
- Reject any AI-initiated write that targets a human-only state.
- Append to `audit_log` on every state change, edit, and deletion.
- Surface `advisory: true` and `confidence` in the UI so the professional sees them.
