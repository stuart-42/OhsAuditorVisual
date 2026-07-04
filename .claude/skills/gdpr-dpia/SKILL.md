---
name: gdpr-dpia
description: UK GDPR and Data Protection Act 2018 compliance rules for this app, plus a DPIA skeleton. Use this skill whenever the work touches personal data, image/video of people, storage, retention, deletion/erasure, consent or lawful basis, data residency, encryption, audit logging, data-subject rights, redaction of faces or number plates, or any feature that processes site media. Trigger it even if the user only says "storage", "privacy", "GDPR", "data", "delete", or "compliance", and even if they don't name this skill. Default to the privacy-protective option whenever there is doubt.
---

# GDPR / DPIA

This app processes images and video of worksites that will frequently contain **personal
data** (identifiable people, faces, number plates). Treat privacy as a build-time constraint.

## Principles to enforce in code

- **Lawful basis** — most likely *legitimate interests* (workplace safety) with a documented
  Legitimate Interests Assessment, or *legal obligation*. Record the basis per tenant.
- **Data minimisation** — capture only what the inspection needs; prefer redacted frames.
- **Redaction-before-upload** — faces and number plates must be blur-able on-device before any
  media leaves the phone. Cloud reasoning should run on redacted media wherever possible.
- **Storage limitation** — configurable retention per tenant; auto-purge on expiry.
- **Security** — encrypt in transit and at rest; tenant isolation on every record and S3
  prefix; least-privilege IAM; AWS OIDC, no long-lived keys.
- **Data residency** — all storage and inference in `eu-west-2`.
- **Accountability** — append-only audit log of who saw/changed/deleted what, and when.

## Data-subject rights (must be supported)

- **Erasure** — deletion must truly remove the record, its media, derived data, thumbnails,
  and backups; log the erasure event.
- **Access / portability** — export a subject's data on request.
- **Rectification** — the human-edit path already covers this; ensure it is logged.

## DPIA skeleton (fill in `docs/DPIA.md`)

1. Description of processing (what, why, data flows, edge vs cloud).
2. Necessity & proportionality (lawful basis, minimisation, retention).
3. Personal data inventory (faces, plates, location, inspector identity, tenant).
4. Risks to individuals (covert monitoring perception, re-identification, breach).
5. Mitigations (on-device redaction, encryption, residency, access controls, retention).
6. Residual risk + sign-off (the data controller decides).

This is **high-risk processing** (systematic image capture of people in a workplace), so a
DPIA is expected before real-world deployment. Flag this to the user; do not let the app go
to live sites without it.
