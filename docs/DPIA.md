# DPIA — Data Protection Impact Assessment (skeleton)

> **Status: DRAFT — not yet completed or signed off. Real-site use must not begin until this
> document is reviewed and signed by the data controller.**
>
> This is high-risk processing (systematic image capture of people in a workplace). A DPIA is
> required under United Kingdom General Data Protection Regulation Article 35 before deployment.
> Each tenant organisation must also satisfy itself that this assessment covers its own context.

---

## 1. Description of processing

**What is processed.** SiteSentry records occupational health and safety inspection findings.
Data processed includes:

- Site photographs, which will routinely contain images of workers and members of the public
  (identifiable faces, vehicle registration plates, clothing, gait).
- Free-text observation notes, which may name or describe individuals.
- Inspector identity (user account) and timestamps linked to each record.
- Documents and certificates (training records, insurance certificates, examination certificates)
  which carry names, membership numbers, and other personal identifiers.
- Employer and client organisation details (commercial, not usually personal data).

**Why it is processed.** To support a qualified health and safety professional in conducting
a statutory inspection and producing a corrective-action plan. The legal basis is likely
*legitimate interests* (workplace safety management, compliance with health and safety legislation)
or, for inspectors acting under a statutory duty, *legal obligation*. The lawful basis must be
documented and recorded per tenant before processing begins.

**Data flows.**
- Capture: on the inspector's device (smartphone or tablet).
- Phase One: site photographs remain optional (evidence capture); free-text and structured
  findings are the primary data. On-device reasoning; cloud only for report generation.
- Phase Two (future): images are redacted on-device (faces and plates blurred) before
  transmission; redacted frames are sent to cloud inference; raw unredacted frames are not
  transmitted.
- Storage: encrypted at rest in Amazon Web Services Simple Storage Service, region eu-west-2
  (London), with tenant-scoped prefixes. No data leaves the United Kingdom.
- Report output: structured report delivered to the inspector and client; contains findings and
  actions but not raw images by default.

**Edge versus cloud.** The deterministic reasoning core runs entirely on-device or on a local
server — no personal data is required for this step. Language-model use is confined to language
tasks (tag suggestion, wording smoothing, report overview). The cloud model for Phase Two image
reasoning receives only redacted media.

---

## 2. Necessity and proportionality

**Necessity.** Structured inspection records are required by health and safety legislation and
are standard professional practice. The system does not process more data than a conventional
paper-based inspection would; it structures what is already collected.

**Minimisation.**
- Images: capture is optional; when captured, on-device redaction of faces and plates applies
  before transmission.
- Free text: auditors are reminded that the description field is a personal-data surface and
  should not name individuals. [ UI reminder not yet implemented — required before real-site use. ]
- Documents: extracted fields are confirmed by the auditor and stored; raw document images are
  retained only as long as necessary.

**Retention.** Retention periods must be configured per tenant. Suggested defaults:
- Active inspection records: for the duration of the client relationship plus six years
  (limitation period for civil claims).
- Closed records with no associated enforcement or legal action: three years from closure.
- Raw site photographs: twelve months from the inspection date unless a specific reason exists.
- Documents and certificates: until superseded or expired plus twelve months.

[ Retention periods not yet implemented — auto-purge logic required before real-site use. ]

**Proportionality.** The processing is proportionate to the safety benefit. The system operates
as an aid to a qualified professional and does not take autonomous decisions about individuals.

---

## 3. Personal data inventory

| Data item | Category | Sensitivity | Where stored | Retention |
|---|---|---|---|---|
| Facial images in site photographs | Personal data (biometric-adjacent) | High | S3 eu-west-2, tenant-prefixed | 12 months |
| Vehicle registration plates in site photographs | Personal data | Medium | S3 eu-west-2, tenant-prefixed | 12 months |
| Inspector user account (name, employer, role) | Personal data | Medium | Database, tenant-scoped | Duration of account |
| Free-text observation notes | Personal data (may name individuals) | Medium | Database, tenant-scoped | Per retention schedule |
| Training records (names, certificate numbers) | Personal data | High | S3 eu-west-2, tenant-prefixed | Per retention schedule |
| Insurance certificates (employer names, reference numbers) | Personal/commercial | Medium | S3 eu-west-2, tenant-prefixed | Per retention schedule |
| Confirmed field extractions from documents | Personal data | Medium | Database, tenant-scoped | Per retention schedule |
| Audit logs (who accessed/changed what) | Personal data (inspector identity) | Low | Append-only log, tenant-scoped | 7 years |

---

## 4. Risks to individuals

**Covert monitoring perception.** Workers may not be aware that site photographs are being
taken for an inspection system. If not communicated, this may erode trust.
*Mitigation: require tenant organisations to notify workers through their safety management
communications before SiteSentry is used on a site.*

**Re-identification from redacted images.** Blurring faces and plates reduces but does not
eliminate re-identification risk (gait, distinctive clothing, context).
*Mitigation: redaction as defence-in-depth, not sole protection; minimise retention of raw
frames; do not use raw images in training sets without separate consent.*

**Data breach.** Unauthorised access to inspection records, photographs, or documents could
expose worker identities and workplace vulnerabilities.
*Mitigation: encryption in transit (TLS) and at rest (AES-256); tenant isolation; least-privilege
IAM; no long-lived credentials; AWS OIDC for deployment.*

**Training data re-use.** Images or text used to train or fine-tune models could expose
personal data beyond the inspection context.
*Mitigation: redact descriptions before training use; training use requires a separate lawful
basis or explicit opt-in; document the training use in this DPIA update before it begins.*

**Scope creep.** Records authorised for inspection purposes used for other purposes (for example,
performance management of individual workers).
*Mitigation: purpose limitation enforced at the application layer; data minimisation on
individual worker detail; tenant terms of service prohibit personal-data re-use.*

---

## 5. Mitigations (implemented or planned)

| Risk | Mitigation | Status |
|---|---|---|
| Images of people | On-device redaction of faces and plates before transmission | Phase Two — not yet built |
| Free-text naming individuals | UI reminder; description field is PII surface | Not yet implemented |
| Tenant data isolation | tenant_id on every record and S3 prefix | Model field present; persistence not yet built |
| Data breach | TLS, at-rest encryption, least-privilege IAM, OIDC | Planned in infra/ — not yet built |
| Retention | Auto-purge per tenant retention schedule | Not yet built |
| Erasure requests | True erasure of record, media, derived data, and backups | Not yet built |
| Audit trail | Append-only audit_log on every observation | Field present in model; persistence not yet built |
| Training data | Redact before training use; document separate lawful basis | Policy only — no training yet |
| Worker awareness | Tenant notification obligation | Governance document — not technical |
| Data residency | All storage and inference in eu-west-2 | Enforced in deploy workflow; infra not yet built |

---

## 6. Residual risk and sign-off

**Residual risks after mitigations.** Re-identification from contextual cues in redacted images
remains possible. Purpose limitation depends on tenant compliance with terms of service.
Training-data governance requires a future DPIA update before any training run begins.

**Conclusion.** The processing is necessary and proportionate. The mitigations described above
are required before real-site deployment. This document must be reviewed by the data controller
(the organisation deploying SiteSentry) and updated whenever the processing changes materially.

| Role | Name | Date | Signature |
|---|---|---|---|
| Data Protection Officer or equivalent | | | |
| Product owner | | | |
| Legal review | | | |

---

*Contains public sector information licensed under the Open Government Licence v3.0.*
