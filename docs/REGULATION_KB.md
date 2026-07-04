# REGULATION_KB — sourcing, storage, recall of regulatory content

Scoped to United Kingdom government Legislation, Guidance, and Approved Codes of Practice. Written
out in full.

## The three tiers and their legal weight
- **Legislation (Acts and Regulations)** — the law itself, the duty.
- **Approved Code of Practice** — special legal status: if a dutyholder is prosecuted and shown not
  to have followed the relevant provisions, they must prove they complied some other way or be found
  at fault; alternative methods are allowed. A citation to an Approved Code of Practice carries real
  weight.
- **Guidance** — persuasive, not binding: following it normally means doing enough, and inspectors
  may cite it as good practice, but other action is permitted.

Legal status is a property of each **text node**, not of a whole regulation — a provision may have
law only, law plus guidance, or law plus Approved Code of Practice plus guidance (work at height,
for example, has guidance but no Approved Code of Practice). Tag every node `law | acop | guidance`.

## Licensing — all reusable, with named exclusions
Legislation (from legislation.gov.uk) and the great majority of Health and Safety Executive material
are Crown copyright and reusable free of charge under the Open Government Licence, including
commercially and inside your own product, provided the source is acknowledged. Store text, not
branding (skip logos; a few named items such as the law poster and the accident book are excluded;
some embedded images are third-party). Carry the attribution line: "Contains public sector
information licensed under the Open Government Licence v3.0." Because everything here is openly
licensed, it can be stored and embedded in full — unlike published standards.

## Standards are out of scope (for now)
Published standards from the British Standards Institution and the International Organization for
Standardization are copyright-restricted: they may not be reproduced or stored in a retrieval system
without a licence. A future standards layer holds only the reference (number, title, clause), your
own paraphrased note, and a pointer that the user needs a licensed copy — never the text. Not built
in the prototype.

## Sourcing map for the first hazard areas
Health and Safety Executive publications bundle Regulations, Approved Code of Practice, and guidance
in single books:
- Protective equipment → publication L25 (Personal Protective Equipment at Work Regulations).
- Work equipment / plant → publication L22 (Provision and Use of Work Equipment Regulations).
- Housekeeping, slips and trips, traffic routes → publication L24 (Workplace Regulations).
- Construction overall → publication L153 (Construction Design and Management Regulations 2015 —
  guidance, no Approved Code of Practice).
- Work at height → Work at Height Regulations 2005 plus guidance (no Approved Code of Practice).

## Storage — three tiers
- **Provision graph** — structured records (stable id, instrument, section, legal status,
  duty scope general/specific, effective dates, own-words summary, source link, attribution). This
  is what the (tag x reason) mapping points at, and where corrective actions attach.
- **Full text** — for legislation and Open-Government-Licence guidance/Approved Code of Practice,
  store and embed freely for semantic search.
- **Versioning** — store effective dates; cite the version in force at the audit date. Note that
  the consolidated "as amended" view can lag, so record which version was used.

## Recall — deterministic first, retrieval as assist
- **Primary path** — deterministic lookup: (tag x reason) → provision id → canonical action. A
  table join, not a generation: auditable, reproducible, cannot fabricate a citation. Works offline,
  so the provision records and summaries are bundled locally per domain pack and synced when online.
- **Assist** — retrieval-based semantic search over the open-licensed text to ground cloud reasoning
  and to handle free-text. Rule: retrieve then cite, never generate a citation.

## Corrective actions are sourced here
Legislation states the duty; the Approved Code of Practice and guidance state how to comply. So
corrective actions are authored from Approved Code of Practice and guidance text, cited to the
legislation, and marked `acop_derived` where their basis is an Approved Code of Practice (stronger
weight, surfaced to the user). See DATA_MODEL.md for the canonical-action shape.
