# Archive Manifest

Everything listed here was **moved**, never deleted, from its original location into
`project_docs/_archive/` (or, for two orphaned config files, from `src/_user/`). Git history for
every tracked file is preserved via `git mv`; a handful of files were untracked (new,
never committed) and were relocated with a plain filesystem `mv` since there was no git
history to preserve. Nothing here was altered in content — only moved.

All moves are currently **unstaged/uncommitted** working-tree changes (per instructions,
no `git add`/`git commit` was run). Run `git status` to review before committing.

---

## sessions/ — session logs, handoffs, scratch dumps

| File | Original location | Reason |
|---|---|---|
| RESUME-WORK-HERE.md | project_docs/ | Stale "resume work" handoff note from a past session |
| SESSION-2025-10-29-SUMMARY.md | project_docs/ | Dated session summary, superseded by later work |
| session-2025-12-28-dam-investigation.md | project_docs/ | Dated session log from the Dec 28 DAM investigation |
| story-1.2-completion-report.md | project_docs/ | BMAD-style story completion report, historical |
| story-1.2-handoff.md | project_docs/ | BMAD-style story handoff note, historical |
| bmm-workflow-status.md | project_docs/ | Stale workflow-status snapshot from a BMAD session |
| temp-info.md | / (root) | 144KB raw scratch dump; was the raw input later polished into `project_docs/MIGRATION-STATUS-REPORT.md`, which supersedes it |

## investigations/ — superseded investigation artifacts

| File | Original location | Reason |
|---|---|---|
| encoding-fix-summary.md | project_docs/ | Point-in-time investigation note, findings folded into typo3-technical-findings.md |
| breath-under-water-investigation.md | project_docs/ | Investigation into page 982; resolution now summarized in typo3-technical-findings.md / MIGRATION-STATUS-REPORT.md |
| dam-gallery-investigation-summary.md | project_docs/ | Dec 28 DAM/gallery investigation summary, superseded by gallery-images-configured.json + typo3-technical-findings.md |
| sisyphos-gate-migration-report.md | project_docs/ | One-off migration report for a single project, historical |
| INVESTIGATION-SUMMARY.md | project_docs/ | Untracked duplicate that had reappeared in project_docs/ (root copy of the same name is a separate, already-deleted tracked file left untouched per instructions) |
| content-storage-mechanism-findings.md | project_docs/ | Dec 28 investigation into TYPO3 content storage (page 982); same investigation family as breath-under-water-investigation.md, content already covered in typo3-technical-findings.md and MIGRATION-STATUS-REPORT.md. *(Not on the original candidate list — added on inspection; flagged in final report.)* |

## superseded-docs/ — duplicate or superseded reference docs

| File | Original location | Reason |
|---|---|---|
| typo3-technical-findings (copy).md | project_docs/ | Confirmed exact-subset duplicate of typo3-technical-findings.md (diff showed it's missing 754 lines present in the current file, including the encoding root-cause section); current file kept in place |
| paintings-migration.md.backup | project_docs/ | Backup of paintings-migration.md; diff confirmed it's an earlier (552-line) version vs. the current 601-line file |
| product-brief-Maja-Explosiv-Website-Redesign-2025-10-22.md | project_docs/ | Superseded by PRD.md |
| ui-figma-next-steps.md | project_docs/ | Documents *approximate* Figma token guesses ("confirm exact Figma tokens," "approx"); will be redone with exact Figma values. Non-token content worth preserving: a verification/testing checklist (build+serve, check CSS vars, corner image, sidebar fixed-width, mobile breakpoints) and a "files to update" component inventory — not duplicated elsewhere, should be folded into the new plan doc |
| ui-phase-b.md | project_docs/ | Same approximate-token issue as above. Non-token content worth preserving: JS behavior added (`initTabs`, `initProjectPreview`), a QA/testing checklist (tab switching, keyboard nav, focus ring, project-preview wiring), and accessibility notes (ARIA tablist pattern) — not duplicated elsewhere |
| homepage-changes-plan.md | project_docs/ | The pre-implementation *plan*; homepage-changes.md (kept) is the actual execution/change log that tracks real work against this plan and extends further (through the Dec 22 Contact Modal work, which this plan doesn't cover) |
| paintings-final-status.md | project_docs/ | One of three overlapping paintings-status docs (all dated Dec 27, all claim "COMPLETE"); paintings-migration.md is the longest/most detailed (601 lines vs. 210) and is the one referenced by other kept docs — kept it, archived this |
| paintings-completion-summary.md | project_docs/ | Same reasoning as above; shorter (213 lines), redundant with paintings-migration.md |
| GALLERY-IMAGES-REFERENCE.md | project_docs/ | Verified its content (page IDs, DAM folder IDs, per-project image lists/counts) is fully and exactly reproduced in gallery-images-configured.json; the "how to use" Python snippets are generic boilerplate, nothing unique to preserve |

## superseded-json/ — duplicate/dead JSON data files

| File | Original location | Reason |
|---|---|---|
| actual-gallery-images.json | project_docs/ | Superseded by gallery-images-configured.json (per task instructions); not read by any script as input |
| gallery-analysis-results.json | project_docs/ | Investigation intermediate output; not read by any script as input |
| dam-extraction-results.json | project_docs/ | 2.4MB raw DAM extraction dump; investigation intermediate, not read by any script as input |
| typo3-page-structure.json | project_docs/ | Investigation output; not read by any script as input |
| gallery-images-final.json | project_docs/ | Compared against gallery-images-configured.json: every project entry has `image_count: 0` and an empty `images` array — a broken/incomplete extraction attempt, clearly inferior to the configured file |
| paintings_comprehensive_data.json (underscore) | project_docs/ | Written only by scripts/extract_paintings_comprehensive.py; not read by any other script or doc. The hyphenated paintings-comprehensive-data.json is the one actually consumed by copy_paintings_images.py, generate_paintings_markdown.py, and update_paintings_markdown.py — kept that one |
| paintings-data-extracted.json | project_docs/ | Written only by scripts/extract_paintings_data.py; not read as input by any other script (only mentioned in prose in two docs that are themselves being archived) |
| painting_pages_raw.json | project_docs/ | Not referenced by any script or any remaining doc |

## dead-config/ — orphaned/duplicate site configuration

| File | Original location | Reason |
|---|---|---|
| theme.js.orphaned | src/_user/_data/theme.js | **Dead file** — wrong directory name (`_data` instead of `data`); `.eleventy.js` only ever reads `src/_user/data/` (confirmed via grep, no reference to `_user/_data` anywhere in the build config). Held stale, non-Figma placeholder colors (`background: #C8C8C8`, `accent: tomato`). The live file at `src/_user/data/theme.js` is far more complete (full Figma-aligned color/typography/font token set with detailed comments) and was left in place. The now-empty `src/_user/_data/` directory was removed |
| site.json | src/_user/data/site.json | Empty file (0 bytes). Its `.js` sibling (`src/_user/data/site.js`, kept) contains the real, fully-commented site config. Both extensions populated the same Eleventy global data key (`site`) via the `.eleventy.js` data-override loop (~lines 202-254), which is undefined/fragile behavior with two same-key files present |
| collectionData.json | src/_user/data/collectionData.json | Empty file (0 bytes). Its `.js` sibling (kept) contains the real, commented collection config (projects/sculptures/installations/performance/paintings/news). Same duplicate-data-key issue as site.json/site.js above |
| .eleventy.js.new | / (root) | Stray draft/alternate Eleventy config, superseded by the current `.eleventy.js` |

---

## Explicitly left in place (verified, not moved)

- `paintings-image-copy-results.json` — **active**: written by `scripts/copy_paintings_images.py` and read by `scripts/update_paintings_markdown.py`. Originally flagged as ambiguous but grep confirmed it's a live pipeline file.
- `paintings-comprehensive-data.json` (hyphen) — **active**: read/written by 4 scripts (see superseded-json/ entry above).
- `homepage-changes.md` — kept over homepage-changes-plan.md; it's the more current/complete doc and root `changes.md` does not cover its most recent content (Contact Modal, Dec 22).
- `paintings-migration.md` — kept as the authoritative paintings status doc over paintings-final-status.md and paintings-completion-summary.md.
- `MIGRATION-STATUS-REPORT.md` — reconciled after this report was written: moved to `sessions/MIGRATION-STATUS-REPORT.md`, since `project_docs/PLAN.md` (written in the same work session, in parallel with this archive pass) now supersedes it as the current-state/roadmap doc.
- Everything under `project_docs/design_screenshots/`, `PRD.md`, `epics.md`, `ux-specification.md`, `asset-organization-strategy.md`, `typo3-technical-findings.md`, `typo3-database-analysis.md`, `typo3-filesystem-analysis.md`, `extracted-projects.json`, `gallery-images-configured.json`, `tasks.md`, `pending-changes.md`, `templates.md` — all per explicit instructions.
