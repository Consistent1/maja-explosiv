# What documentation exists, and which of it to trust

Written 2026-08-27. **If you are new here, read `CLAUDE.md` first, then this.**

Documentation accumulated faster than anyone indexed it, and several documents contradict each
other because they were written at different points and never retired. This page says which is
which. **Where two documents disagree, the one marked CURRENT below wins.**

---

## Start here

| doc | what it is |
|---|---|
| **`CLAUDE.md`** | Ground rules, working agreements, where the sources of truth are. The session entry point |
| **`project_docs/PLAN.md`** | Project status, the **extracted Figma specs** (sidebar, homepage, About components, **Project Page**), and the **single list of open questions** needing the owner's judgement |
| **`project_docs/DOCS.md`** | This page |
| `README.md` | How the Eleventy template works — collections, layouts, the `src/_user/` override system |

## The content migration — all CURRENT

| doc | what it is |
|---|---|
| **`project_docs/content-migration-plan.md`** | **The governing document.** Approved 2026-08-25. Sources, verification standard, stage order, and the numbered owner decisions (1–14). Read before touching content. **Its final section, `HANDOFF — the rest of the migration`, is the entry point for Stages 6–14**: project context, the two-repo boundary, reading list, per-stage brief, pitfalls, tips |
| `project_docs/NEXT-SESSION.md` | Onboarding for whoever picks this up next; retires several cautions that are no longer true |
| `migrated-content/README.md` | Index of the migration output, per-stage status, and the one thing to know before running anything (the database must be loaded from the *current* dump) |
| `migrated-content/<type>/SOURCE.md` | Per stage: exactly where the content came from, what was done to it, what was excluded and why |
| **`migrated-content/projects/SOURCE.md`** | **Stages 6–9 (the project stages).** Every decision, every anomaly, every bug the pipeline now guards against. Read before writing any project-stage code |
| `migrated-content/<type>/verification/report.md` | Per stage: which checks ran, which passed, what gap remains |
| `migrated-content/<type>/excluded/` | Source records deliberately **not** migrated, with every field preserved — currently `timeline/excluded/excluded-records.json` (4 records) |
| `migrated-content/<type>/normalized/*.json` | The parsed, source-shaped intermediate for each stage. Useful when a conversion needs re-deriving without re-querying the database |
| `migrated-content/press/GALLERY-COMPANIONS.md` | A deliberate deviation and how to undo it: three PDF entries carry a JPG companion so the gallery matches the old site |
| `migrated-content/press/GALLERY-ORDER.md` | Why the press gallery's image order differs from the live site in 21 of 48 positions, and what matching it would take |
| **`migrated-content/_tools/RUNBOOK-images.md`** | **How to actually run the image pipeline**, what to do when a new backup arrives, and how to prove a conversion was lossless |

## Content stores that are deliberately not built

Each has a README explaining what it holds and why it is not part of the site:

| directory | holds |
|---|---|
| `pre-migration-content/` | The 38 Markdown files and 149 assets that predate the migration. Moved, never deleted |
| `migrated-hidden-content/` | Content TYPO3 marked `hidden` — migrated, not published |
| `migrated-deleted-content/` | Content TYPO3 marked `deleted`. **Only 9 of 202 records are Maja's**; the rest belong to other sites that shared the database |
| `src/posts/projects/TBD/` | Projects with no settled category. `README.md` there explains each one |

## The image archive

`image-archive/` is gitignored (562 MB) but its documentation matters:

| doc | what it is |
|---|---|
| `image-archive/README.md` | What the archive is, how it is organised, what "original form" means |
| `image-archive/DUPLICATES.md` | The 236 files that appear in more than one place, and where |
| `image-archive/live/about/portraits/README.md` | 6 portraits of Maja reachable only through body text, not DAM — including the Bio portrait at 5× the resolution the old site used |
| `image-archive/live/about/timeline-excluded/README.md` | 4 timeline records (`Elxt 90`, 2000–2003) that are live in the database but selected by no plugin, so invisible on the old site. Every field preserved in `excluded-records.json` beside it |
| `image-archive/live/uncategorised/README.md`, `image-archive/hidden/uncategorised/README.md` | Why those folders exist: site furniture and design drafts (`entwurf`, `design 2`, `show`, two draft homepages), not artwork |
| **`image-archive/RECOVERED-2026-08-27.md`** | The 34 files recovered from the live server, **and the NFC/NFD filename trap** — read this before writing anything that matches database paths against disk |
| `old/TYPO3BU/AUGMENTED.md` | Records that the "January 2025 backup" is no longer purely that: 36 recovered files were merged in |

## Superseded — do not act on these

They are kept because they contain useful reconnaissance, but their **conclusions are wrong or
overtaken**:

| doc | why |
|---|---|
| `project_docs/typo3-technical-findings.md` | Claims "82% of painting pages use STATIC HTML instead of database content" and recommends web-scraping. **Disproved** — those pages have `tt_content` rows all along (plan §D7). Acting on it would also violate the no-live-content rule |
| `project_docs/paintings-migration.md`, `typo3-database-analysis.md`, `typo3-filesystem-analysis.md` | Pre-migration reconnaissance. Counts derived by grepping the SQL dump text and **wrong against the loaded database** (plan §2.2) |
| `project_docs/asset-organization-strategy.md` | The target directory shape is still right and is being followed. The rest predates the archive and the six→four mapping |
| `project_docs/pending-changes.md` | **Empty.** Implies tracking that is not happening |
| `project_docs/epics.md`, `tasks.md`, `PRD.md`, `ux-specification.md`, `templates.md` | From an earlier planning framework, not used |
| `project_docs/_archive/**` | Superseded documents and the **retired Figma PNG exports**. `CLAUDE.md` §4 explains why those exports must not be used |
| `changes.md`, `GEMINI.md` | Historical; not maintained |

## Design work

| doc | what it is |
|---|---|
| `project_docs/figma-audit-guide.md` | The method for finding design mismatches numerically rather than by eye. Its §8 "Traps" is the part that matters |
| `project_docs/homepage-changes.md` | Homepage audit findings |

Design questions live in `PLAN.md` § *Open items needing input*, mixed in with migration ones —
that section is **the single list**, and `PLAN.md` § *Resume here* points at it. Extracted Figma
specs (sidebar, homepage, About components, **Project Page**) live in `PLAN.md` Phase 2.

---

## A note on numbers in old documents

Several figures repeated across these documents turned out to be wrong when checked against the
loaded database — "26 projects converted" (it was 23), "~94 active pages" (155), "seven months
stale" (nineteen), "zero content drift" (one row). **Treat any count in a document that predates
2026-08-25 as unverified**, and check it before building on it.

The recurring cause is worth knowing: `deleted = 0` alone does not mean live. TYPO3 hides
records via `deleted` *and* `hidden`, at both content and page level. See `CLAUDE.md` §5.
