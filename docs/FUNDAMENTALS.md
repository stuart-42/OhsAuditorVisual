# FUNDAMENTALS — the agreed basis of the system

Written out in full. This is the north-star document: if a build decision conflicts with
anything here, the conflict is resolved in favour of this document.

## Purpose and framing
An advisory aid for a qualified professional, never a definitive determination. Every output —
a detected hazard, a regulation reference, a recommended action, a priority — is labelled
advisory and remains subject to professional judgement. The system never states a legal
conclusion. Users are mixed in expertise, from non-specialist site managers to safety managers.

## Human oversight at every stage
A qualified person can accept, amend, or delete any observation, recommendation, tag, or action
at any point. The system only proposes; it never finalises, closes, or deletes a record on its
own. Automated suggestions (text now, image later) propose into a controlled vocabulary, and the
human disposes.

## Data protection by design
United Kingdom data protection law (General Data Protection Regulation and Data Protection Act)
is built in: data minimisation, purpose limitation, storage limitation, security. Site images
contain personal data, so faces and vehicle plates must be removable on the device before
transmission. Deletion is true erasure, including derived data and backups. Free-text fields are
treated as a personal-data surface.

## Offline-first
Capture, review, tagging, and any reasoning not requiring the cloud must work with no
connectivity. Cloud reasoning is an enhancement that reconciles when a connection returns.

## Multi-tenant from the data model
Every record and storage location carries a tenant identity from the first line of code; no query
may be unscopeable by tenant. The organisation-administration interface is deferred; the isolation
is never retrofitted.

## Domain-pack architecture
The core engine is domain-agnostic. Everything domain-specific lives in a swappable domain pack:
the whole template and its layout, the hazard taxonomy, the prompted elements, the regulation
knowledge, the corrective-action library, the report template. Occupational health and safety is
the first pack; food safety is a separate pack with its own template, built second.

## Hazard versus control
A hazard is something with the potential to cause harm (working at height, a falling object, a
moving vehicle). Personal protective equipment is a control — the last line of the hierarchy of
control — not a hazard. A finding names the hazard and the control that is missing or inadequate
separately, and corrective actions are framed around the hierarchy of control, not the equipment
alone.

## The reasoning core is deterministic
A hazard maps to the regulation provisions it engages, which map to corrective actions, as a
many-to-many graph keyed on the combination of tag and reason. Corrective actions are
consolidated: one action that discharges several breaches is shown once and annotated with every
provision it satisfies; engaged provisions with no action are surfaced as gaps. Shared obligations
converge on a single canonical corrective action by design, so deduplication is a property of the
structure, not a cleaning step. Provisions are marked general or specific so the output leads with
the specific duty and notes the general one. All of this is reproducible and produced without a
language model.

## Corrective actions sourced from Approved Code of Practice and guidance
Legislation states the duty; the Approved Codes of Practice and guidance state how to comply.
Corrective actions are authored from Approved Code of Practice and guidance text, cited to the
legislation, and weighted by whether their basis is an Approved Code of Practice (special legal
status) or ordinary guidance.

## Structured capture
Findings use a hierarchical, multi-label controlled vocabulary of tags plus a second controlled
dimension of reason codes, plus optional free-text. The template is owned by the domain pack and
organised by that pack's own scheme (premises, practices, people for occupational health and
safety; a separate recognised scheme for food safety). Each section carries prompted key elements
to look for, so a satisfactory result is positively recorded rather than absent. Each addressed
element resolves to an outcome — satisfactory, a finding, or not applicable — with an optional
comment in every case, including positive comments; an adverse outcome becomes a full observation.

## Audit comment
A finding is rendered in the practitioner form "observation of hazard leading to outcome, with
priority sentiment". It is built from a comment template held against each canonical finding, with
slots for site-specific particulars and a sentiment phrase selected from the computed priority
band. The language model only fills or smooths the template; it never originates substance or
priority.

## Prioritisation
Three bands: high, medium, low. Computed by a transparent risk assessment (severity and
likelihood, weighted by legal status, recurrence, and number of people exposed) and confirmed or
overridden by the professional. The record stores the computed features, the suggested band, the
confirmed band, and the human adjustment as separate fields from the first audit; the confirmed
band also labels any attached image. These become training data for a later prioritisation
classifier (structured inputs first, images later). The rule-based band stays the explainable
default; any learned model arrives later as a reviewed suggestion, not a replacement.

## Reports as living records
Hierarchy: client, then site, then a dated inspection, then observations, then actions. A report is
recalled by site, rendered on demand from structured data, and reopened so an action is completed
with a record of what was done and the date. Reports carry header and site detail, a key-data
summary built from aggregations the system already holds, and, later, comparison against the
site's history.

## Access by hierarchy
Roles map to scope: a site manager sees their site(s), a regional manager a region, a safety
manager or administrator everything within the tenant. Identifiers and role-to-scope grants are
modelled from the start and enforced once authentication is added.

## Performance measurement as aggregation
Because capture is structured, measures are aggregations over it: coverage of expected elements,
compliance rate, severity breakdown, open versus overdue actions, time to close, repeat findings,
gaps, and leading categories — by section, site, region, inspector, and over time. Controlled
categories, a persistent site identity, and a recurrence key must exist from the first stored
audit, because comparison cannot be retrofitted onto prose.

## The regulation knowledge base
Scoped to United Kingdom government legislation, guidance, and Approved Codes of Practice — all
Crown copyright and reusable under the Open Government Licence, so storable and searchable in full.
Every text node is tagged with its legal status (law, Approved Code of Practice, or guidance), and
not every regulation has all three. Recall runs on a deterministic lookup from the tag-and-reason
combination to the provision, with retrieval-based search only as an assist that grounds cloud
reasoning; the rule is retrieve then cite, never generate a citation. Published standards from the
British Standards Institution and the International Organization for Standardization are
copyright-restricted, referenced and paraphrased only, never reproduced, and out of scope for now.

## Efficient language-model use
The cheapest token is the one never sent: most of the product is deterministic and costs nothing in
inference. The language model is confined to language tasks — turning prose into structured input,
optionally smoothing selected wording, drafting the report overview from structured figures.
Small, cheap models for these; the larger cloud model reserved for the hard image reasoning of
phase two. Prompts are built from the structured record, not raw documents. Every language-model
call records its token count and model, attributed to the inspection and tenant, from the first
call.

## Traceability of every output
Three kinds of output, all traceable. Looked-up output (citations) explains itself by pointing at
the provision. Rule-computed output (priority bands) explains itself by showing the rule. Learned
output (tag suggester, prioritisation classifier, image models) carries feature attribution —
Shapley additive explanations for structured-input models, attribution maps for image models —
surfaced as the reason for a suggestion and available for auditing the model against its training
data. The deterministic core is explainable by construction and needs no such machinery. The
report summary is anchored by stable references to the findings and actions it summarises, so the
overview is traceable into the body and the language model is held to summarising referenced data.

## Evidence and documents
Alongside hazard findings the system holds evidence records — certificates, examinations, insurance,
training records — as a generic record with a controlled document-type vocabulary, surfaced through a
management-documentation section whose prompted elements are the expected documents; a missing one is
a gap. Optical-character extraction reads structured fields (issue/expiry, identifiers, examining
body) advisorily for human confirmation; once structured, expiry and validity checks follow, and an
expired certificate becomes a finding. Auditor-supplied tags and confirmed fields are training data
for the extraction models. These carry more personal and commercial data than a site photo, so
minimisation and redaction apply with more force, and they are retained and recalled against a site
over time.

## High-priority hazard photos as the priority training set
A hazard photo carrying confirmed tags, the auditor's comment, and a confirmed high-priority band is
a first-class labelled unit and the most valuable, and rarest, training example for the phase-two
vision model. It is captured whole from the first audit; the training label is always the
human-confirmed one; the comment is redacted before any training use.

## Two-phase build
Phase one is the human-driven audit and reasoning product, with no image analysis: sellable on its
own, near-zero running cost, and the source of the labelled data phase two needs. Phase two adds
vision, which pre-fills tags for the human to confirm under the same oversight model.

## Development approach
A GitHub repository, trunk-first, protected main branch, short-lived branches, automated checks on
every change (linting, type-checking, tests, dependency and secret scanning), and a manually
approved deployment using short-lived federated credentials. The context file and skills are
committed so every build session inherits these decisions; a progress log is kept current; secrets
hygiene is enforced locally and in the automated checks.
