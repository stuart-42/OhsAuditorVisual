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

## Current issues — Milestone Zero completion (updated 2026-07-04)

Note: the "thin slice" list below described the original vision-first design, which was
superseded by the audit-first reorder at Stage 7. The current priority order is:

1. **Persistence layer** — add a local SQLite or flat-file store so `Finding` records (with
   their new Milestone Zero fields: `tenant_id`, `site_id`, `recurrence_key`, status,
   `audit_log`) are actually persisted and can be recalled. The data model already has all
   required fields; this issue is a storage adapter only.
2. **Adjudication** — a qualified person verifies the L25 provisions in
   `packs/construction/knowledge_base/findings_ppe_DRAFT.md` and settles the first batch.
   Resolve the flagged Control of Substances Hazardous to Health Regulations decision for
   chemical eye-hazard findings.
3. **Template JSON** — author `packs/construction/template.json` (premises / practices / people
   sections, prompted elements per section, element-to-vocabulary-tag mappings). Element
   outcomes (satisfactory / finding / not applicable) must be stored from the first audit so
   coverage and compliance measures are available from day one.
4. **DPIA completion** — `docs/DPIA.md` exists as a skeleton. A qualified person must review
   and sign it, and the data controller must confirm the lawful basis, before any real-site use.
5. **Flutter shell** — scaffold `app/` so the CI Flutter job activates; implement the
   section-and-prompted-element capture screen against the real data model and the
   `/vocabulary` + `/consolidate` API. No vision yet.
6. **Protect main** — confirm branch protection is active and the CI job is required before
   merge. Remove the `|| true` fallbacks on pip-audit and bandit once the codebase stabilises.
