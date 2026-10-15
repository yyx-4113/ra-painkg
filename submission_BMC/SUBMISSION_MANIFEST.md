# Submission Manifest — RA-PainKG → BMC Bioinformatics

**Journal:** *BMC Bioinformatics* (Springer Nature / BMC)
**ISSN:** 1471-2105 (electronic)
**Article type:** Research article
**Submission system:** Editorial Manager / Snapp — https://bmcbioinformatics.biomedcentral.com
**Verified metrics (online, 2026-10-15/16):** 2025 Journal Impact Factor **4.4**; **SCIE** (Web of Science Core Collection); JCR Q (mathematics & computational biology / biochemical research methods multi-4区 per x-mol); 中科院2025 大类生物学4区, 小类多4区. Editorial policy: **soundness-only** (does not judge interest/impact) — methodologically tolerant of computational/resource papers.
**APC:** BMC Bioinformatics is fully open access; APC applies upon acceptance (verify current amount at submission — not hardcoded here).

## BMC required format checklist (verified against journal submission-guidelines)

| Requirement | Status | Where |
|-------------|--------|-------|
| Title + author + affiliation + ORCID | ✅ | manuscript_BMC.md / .docx |
| Structured abstract (Background / Results / Conclusions), ≤350 words | ✅ (248 words) | manuscript |
| Keywords 3–10 | ✅ (7) | manuscript |
| Background / Methods / Results / Discussion / Conclusions | ✅ | manuscript |
| List of abbreviations | ✅ | manuscript |
| Declarations (all subsections) | ✅ | manuscript (Ethics/Consent/Funding/Competing/Authors'/Availability/Acknowledgements) |
| AI-use disclosed in Methods | ✅ | manuscript Methods |
| References Vancouver numbered | ✅ | manuscript |
| Figures as separate files | ✅ | figures/fig1–fig6.png |
| No Elsevier-style Highlights required | ✅ (omitted) | — |
| Article type = Research article | ✅ | cover_letter / portal |

## Folder contents

```
submission_BMC/
├── manuscript_BMC.md            # BMC-structured source of truth (≤3500 words body)
├── manuscript_BMC.docx          # generated from the .md above
├── cover_letter.md              # addressed to BMC Bioinformatics editorial board
├── declarations.md              # mirror of embedded Declarations (quick reference)
├── REVISION_NOTE.md            # integrity correction + journal-switch note
├── SUBMISSION_MANIFEST.md      # this file
├── md2docx.py                  # Markdown→DOCX converter used to build the docx
├── graphical_abstract.png
├── figures/fig1–fig6.png
└── supplementary/supplementary_tables.docx
```

## Before you submit (author to-do)

1. **Read REVISION_NOTE.md** — the prior-draft coverage-gap claim ("72 missing genes / 120 (62.5%) matched") was false and has been corrected to verified 188/192 = 97.9% recovery. The reframing has been ratified by the author (2026-10-15/16).
2. **GitHub repository (data availability):** https://github.com/yyx-4113/ra-painkg must be public (✅ verified 2026-10-16) AND should carry a **release tag** matching the submitted version, with the README citation updated from the stale "Scientific Data" target to *BMC Bioinformatics*. (AI cannot create git tags — author action.)
3. **Confirm APC** amount and institutional/open-access funding at submission.
4. **Verify current JIF/SCIE status** at mjl.clarivate.com / journal site immediately before final submit (metrics above are 2026-10-15/16 snapshots).
5. Self-citation [19] repo title can be updated if desired.
