# EVIDENCE — documents, certificates, and training records

A second kind of record alongside the hazard finding. A **finding** records something wrong and
routes to a corrective action. An **evidence record** captures a document that exists — a Lifting
Operations and Lifting Equipment Regulations thorough-examination certificate, a pressure-system
written scheme of examination, an insurance certificate, a training record — whose value is in its
contents and validity, not in a breach. Many are simply evidence that a duty has been met; some
become findings when missing or expired.

## Generic record, controlled document-type vocabulary
One generic evidence record type. The **document type** is a controlled vocabulary value (the same
pattern as hazard tags), so new types are added by extending the vocabulary, not by new record
types. Fields per record: document type, auditor tags, uploaded media, extracted fields with
confirmation status, and provenance.

## Surfaced through a management-documentation section
Documentation is not a hazard theme, so it lives as its own **section** under the "practices"
grouping: a management-documentation section whose prompted elements are the expected documents
(Lifting Operations and Lifting Equipment Regulations examinations, pressure-system schemes,
insurance certificate, training records). The auditor uploads and tags against the prompt; a missing
expected document is a recorded **gap**, exactly like a missing control.

## Extraction (later, additive)
Optical character recognition plus a light extraction model reads structured fields off a document —
issue and expiry dates, equipment or plant identifier, examining body, certificate number, the
standard or regulation it is issued under. Extraction is advisory and human-confirmed: the model
proposes, the auditor confirms or corrects. Once dates are structured, validity logic follows almost
free — flag expired or soon-to-expire certificates, surface plant with no certificate on file — and
an expired certificate legitimately generates a finding through the same reasoning core.

## Training use (the flywheel, extended)
Every document the auditor labels — its type, its tags, its confirmed fields — is a confirmed,
in-distribution training example for the extraction and classification models, improving the same
way the tag suggester and vision detector do. Capture, from the first upload: document type, tags,
extracted fields with confirmation status, provenance — so nothing is reconstructed later.

## Constraints (carried, with more force)
- **Personal data.** Training and insurance documents carry substantial personal and commercial data
  (names, membership and certificate numbers). Heavier personal-data surface than a site photo:
  minimisation, retention, and redaction apply with more force, including before any document enters
  a training set.
- **Retention and recall.** These are retained and recalled against a site over time, not transient
  captures. A site accumulates an evidence file; the report shows what is on file, what is valid, and
  what is missing or expired.

## Phasing
Reserve the record, the document-type vocabulary, and the management-documentation section at
Milestone Zero (cannot be retrofitted). Upload-and-tag arrives with reports (Milestone One/Two).
Extraction and validity logic are later and additive.
