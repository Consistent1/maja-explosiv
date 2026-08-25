# Pre-migration content — quarantined 2026-08-25

**This is not site content and is not built.** It sits outside Eleventy's input directory
(`.eleventy.js` sets `dir.input = "src"`), so nothing here is collected, routed or rendered.

## What this is

Every Markdown file that lived under `src/pages/` and `src/posts/` before the TYPO3 content
migration began. **Moved here, not deleted**, at Stage 0b of
`project_docs/content-migration-plan.md` (§5.1), on the owner's instruction: the current site
could be destroyed, but these files had to be kept and kept *separate*.

Paths mirror their origin exactly — `pre-migration-content/pages/about/bio.md` was
`src/pages/about/bio.md`. That mirroring is the only record of where each file came from.

## Why it was moved rather than left in place

Installing migrated content only overwrites files whose slugs the migration reproduces. The
migration extracts by the old site's **six** categories and maps them to the new **four**, so
slugs do not line up. Anything left behind would have survived, kept building, and shipped
indistinguishable from migrated content — and no check in §6 of the plan would have caught it,
because no check looks at files the migration did not write.

Moving it produces an invariant that a directory listing can settle:

> `src/pages/` and `src/posts/` contain only content the migration produced.

## What is in here

38 files, in three classes — see `migrated-content/_census/quarantine.tsv` for the per-file list.

| Class | Count | What it is |
|---|---|---|
| `maja-content` | 30 | The earlier hand-migration: 23 projects, plus bio, links, press, timeline, about, contact, impressum |
| `category-stub` | 4 | `placeholder-*.md` stubs that kept empty categories from breaking |
| `template-demo` | 4 | Upstream `explosive` template demo posts — never Maja's content, and no migration stage replaces them |

**The four `template-demo` files are an open question for the owner** (logged in `PLAN.md`):
they belong to the template, not to TYPO3. They are quarantined here because the invariant above
admits no exceptions and a move is reversible — not because the migration claims them.

## Is this content a source?

**No.** Decision 1 of the migration plan: content comes from the database and the filesystem
backup only. Nothing in this directory is read, consulted, or diffed against during migration.
It is kept because the owner asked for it to be kept.

Note the About pages here were *transcribed from the live site* by an earlier session — which is
exactly what the plan forbids, and why they are not usable as a cross-check even informally.

## Recovering a file

These files are tracked in git, so the move appears as deletions plus untracked additions and
the originals remain in history regardless of what happens to this directory.
