# Development Guide

## Philosophy: lean now, scalable later

Build the prototype, but don't paint yourself into corners. Two cheap decisions make the
prototype safely extensible into a multi-tenant SaaS:

1. **`tenant_id` everywhere** — on every record and every S3 prefix from commit one. We don't
   build org-management UI in v0, but no query may be unscopeable by tenant. Retrofitting
   isolation later is the expensive part; a column now is free.
2. **Stub the seams** — the on-device detector, the redaction step, and the domain-pack
   interface exist as thin stubs in v0. Filling them in is additive, not a rewrite.

## Branching model (trunk-based)

- `main` is always deployable and **protected** (require a PR + green CI + review).
- Short-lived branches: `feat/*`, `fix/*`, `chore/*`.
- Claude Code on the web pushes to `claude/*` branches and opens PRs — CI gates them like any
  other branch.
- **Squash-merge** to keep history clean. Delete branches after merge.
- Conventional-commit style messages (`feat:`, `fix:`, `docs:`...).

## CI (`.github/workflows/ci.yml`)

Runs on every PR and on push to `main`:
- Backend: ruff lint + format, mypy types, pytest, pip-audit, bandit.
- Frontend: flutter analyze + flutter test.
- Secret scanning (gitleaks).

Job guards (`hashFiles`) let CI pass before `backend/` or `app/` exist, so you can scaffold
incrementally. Tighten the `|| true` fallbacks (pip-audit, bandit) into hard failures once the
codebase stabilises.

## Deploy (`.github/workflows/deploy.yml`)

Manually gated, AWS OIDC (no stored keys), region pinned to `eu-west-2`. Add required
reviewers to a `production` environment in GitHub settings so a human approves each deploy.
Set repo secret `AWS_DEPLOY_ROLE_ARN`. Wire your Terraform/CDK apply into the placeholder step.

## Environments

Prototype: `dev` + a guarded `production`. Add `staging` when you onboard real external users.
Everything in `eu-west-2`.

## Suggested repo layout

```
.
├── CLAUDE.md
├── .claude/skills/...        # the four skills
├── .github/workflows/        # ci.yml, deploy.yml
├── app/                      # Flutter client
├── backend/                  # Python API
├── packs/construction/       # first domain pack
├── infra/                    # Terraform or CDK
└── docs/                     # DEVELOPMENT.md, DPIA.md, ARCHITECTURE.md
```

## Definition of done (every PR)

Green CI · tenant-scoped reads/writes · audit-logged state changes · AI output labelled
advisory · human edit/delete path intact · no secrets · no non-`eu-west-2` data path.

## Suggested first issues (v0 thin slice)

1. Scaffold `app/` (Flutter) and `backend/` (Python) so CI jobs activate.
2. Capture a photo → upload to S3 (`eu-west-2`, encrypted, tenant-prefixed).
3. Backend endpoint → Bedrock (Claude) → returns detections + reg refs + draft actions.
4. Observation review screen: accept / amend / delete, record action taken (HITL).
5. Generate a PDF report from observations.
6. Stub: on-device redaction + edge detector interfaces (no model yet).
