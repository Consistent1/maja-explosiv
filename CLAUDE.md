# Maja Explosiv — agent onboarding

Read this first, every session. It exists so the owner does not have to re-explain the
same ground rules each time. If something here turns out to be wrong or stale, fix it
here rather than just working around it.

---

## 1. What this is

The portfolio site of **Maja Thommen / Maja Explosiv**, a Berlin-based multidisciplinary
artist (sculpture, installation, performance, painting). It is an in-progress redesign
and migration off an old TYPO3 site.

- **This repo** (`Consistent1/maja-explosiv`) — Maja's site.
- **Upstream template** (`Xpanda-org/explosive-11ty`) — a generic 11ty template, owned by
  the same person, checked out locally at `/home/miichael/Code/explosive`.

Stack: Eleventy 3, Nunjucks, Markdown, Open Props + normalize.css, Datastar for the
carousel.

## 2. Read these before doing anything

| File | Why |
|---|---|
| `project_docs/PLAN.md` | **The status document.** Where the project stands, what is next, extracted design specs, and the open-questions list. Start here. |
| `README.md` | How the template works — collections, layouts, the override system. |
| `project_docs/pending-changes.md` | Small queued items. |

Ignore `project_docs/_archive/` unless chasing history. It holds superseded docs and the
**retired Figma PNG exports** — see §4.

## 3. The two sources of truth

Do not conflate these. Almost every mistake in this project's history came from doing so.

**Figma governs design — it, and the owner's current instructions, and nothing else.**
Not the CSS, not this file, not PLAN.md, not any earlier decision however well argued. If
the design and a recorded conclusion disagree, the design wins and the record gets
corrected. (Proven the hard way: PLAN.md asserted the sidebar sub-items shared a left edge
with their headings, and the base stylesheet's 8px indent was deleted on that basis. Figma
gives each item `paddingLeft: 10`. The doc was wrong and had made the site worse.)

The only carve-outs are common sense: mock/placeholder text and stock imagery are not
design, and neither are non-rendering helpers like mask sources.

**Where the design is internally inconsistent, render it as Figma has it and raise the
inconsistency as an open item.** Do *not* normalise it, snap it to a palette, or otherwise
tidy it up — and never treat such a tidy-up as a reason to change something, or as a reason
to leave something unchanged. Deciding what to reconcile is the owner's call, always.
(2026-07-29: an off-palette `#000000` was struck off the owner's open list on the reasoning
that the nearest palette value was already being rendered. That reasoning was invented and
was not the owner's instruction.)

Structure, layout, spacing, typography, colour.
File: [MajaExplosiv_Website Redesign](https://www.figma.com/design/18tst8uq38FlDlaZA5cPCz/MajaExplosiv_Website-Redesign)
— owner's personal copy, view-only, opened through a real logged-in Chrome session.

**The live site governs content.** `maja-explosiv.com`, a frameset-based TYPO3 site.
Projects, links, photos, press, timeline entries — anything migrated in bulk. Figma's
text is placeholder and is frequently wrong or invented; never copy copy out of it.

Corollaries the owner has stated explicitly:

- **Nothing is hardcoded** — design values become tokens, content comes from front matter
  or data files. Exceptions must be approved individually.
- **The site is populated by the migration.** Mock or partial content is fine and expected
  while building; the real content arrives in bulk later. Never hand-migrate at scale.
- Small wording differences in the main prose (bio and similar) are not worth chasing —
  those get swapped easily. This does *not* extend to bulk content.
- Fixed UI chrome (button labels, tab labels, section eyebrows) is template text, not
  content. Flag anything ambiguous.

## 4. Figma: how to not get this wrong

Three separate people-hours have been lost to these. All are recorded here so they are
not rediscovered.

- **The file contains many near-identical draft frames.** Searching for text lands you in
  stale exploration regions. The canonical locations are:
  - Homepage → big label **"Onepager Solution"** → **"Updated Components"** → the
    **"Main container"** frame beneath it. These labels are floating text, not parents.
  - Single project → **"Project Page"** under **"(Updated Reusable) Components"**.
  - Components → **`Assets / Components`**, then the relevant floating label
    (e.g. **"About Components"**).
- **Where variants exist, only one is current.** The marker is inconsistent: sidebar
  variants use floating **`In Use` / `Not In Use`** text labels; the Press component uses
  an **`Old - `** name prefix. Check before trusting a variant.
- **The archived PNG exports are retired — do not use them.** They predate the wrong-frame
  correction, carry no record of which frame they came from, and at least one is
  mislabelled (`press.png` is a byte-identical duplicate of `links.png`). Read Figma
  directly and take fresh screenshots.
- Figma navigation is slow on this machine. **That is not a reason to skip it** — the
  owner has said to take the time if it buys any accuracy.
- Adhere closely but **not religiously**. 34.9545793px may as well be 35px. Do not chase
  decimals.

## 5. Working agreements

These are the owner's standing instructions. They are not negotiable defaults.

- **Never start implementing until explicitly told to.** This resets constantly. A
  decision being settled, or the owner confirming a conclusion, is *not* permission to
  write code. After a discussion about a problem, wait for a fresh go-ahead.
- **"One operation" means exactly one line changed.** Not three, not seven. If an adjacent
  line genuinely needs to move too, say so and wait — do not bundle it in.
- **Be brief**, without dropping detail. No emoji without reason.
- **Surface every decision made**, however small.
- **Ask in plain text**, not the option-picker UI.
- **Never create a git branch without explicit permission.** Work and commit on `main`.
  This repo is solo and its whole history is on `main`; a branch only adds a merge step.
  The generic "don't commit to the default branch" habit does not apply here — asked for
  and corrected 2026-07-29, when a commit was put on a branch unprompted.
- Before a change, be able to state why it helps, what should change, and how you will
  know it did. Verify it actually happened before moving on.
- Open questions of the "needs the owner's judgement" kind go in **one place**:
  `project_docs/PLAN.md` § *Open items needing input*. Resolved items get struck through
  with the resolution, not deleted.
- **When counting anything in the TYPO3 database, `deleted = 0` is not enough.** TYPO3 hides
  records via `deleted` *and* `hidden`, at both content and page level. Filter all four, and
  **state the filter next to the number** — "1,049 images on visible pages", not "1,049
  images". This has produced an overstated figure three times; see the migration plan §3.
- **Keep things simple, without sacrificing reliability, adherence to web standards, or
  ease of use.** The overall bar for the project.

## 6. Code layout

The template's override system is the whole point of the fork — respect it.

```
src/_user/          Maja-specific overrides. Most work belongs here.
  layouts/          home.njk, about-page.njk, project.njk, sidebar-layout.njk, base.njk
  includes/         left-nav.njk, footer.njk, about-content.njk, ...
  data/             site.js, theme.js, collectionData.js, featuredProjects.json
  assets/css/       custom.css   <- the site's real stylesheet
src/pages/          Static pages, incl. about/{bio,timeline,press,links}.md
src/posts/projects/ Project entries by category
src/assets/images/  Site images
```

- Generic fixes belong **upstream**. Make the change in `/home/miichael/Code/explosive`
  itself, push it, then sync this repo with the updated template — do not patch a template
  file here and hope it survives the next pull. Maja-specific work belongs in `src/_user/`.
- `src/_layouts/`, `src/_includes/` are **base template** files. Editing them directly is
  a boundary violation; there is a known backlog of these (see PLAN.md Phase 0).
- **`src/assets/css/main.css` is the exception — edit it freely** (owner, 2026-07-29).
  It is nominally a template file, but this repo's copy has already diverged: upstream is
  1048 lines and contains no `.left-sidebar` at all, ours is 1276, with ~239 added lines
  of Maja-specific styling (`.left-sidebar`, `.main-container`, `.hero-*`,
  `.project-detail`, `.tab-*`, `.posts-grid`). It is out of sync with the template
  regardless, so treating it as untouchable buys nothing. If editing it improves the site,
  edit it.
- **`custom.css` is messy** — a large block of rules is declared two or three times with
  the later copy silently winning. A verified de-duplication pass has been done; what
  remains is logged in PLAN.md. Do not add to the mess; append new sections at the end.

## 7. Running and verifying

**The shell is allowed for this** (owner, 2026-08-25). Build the site, start the dev server,
fetch pages, drive a browser — run them directly rather than asking. This replaces the earlier
rule that said to serve only via the preview tooling and never a raw shell command; that rule
predated the preview tooling being unavailable in some sessions, and it left work blocked with
no alternative.

Still ask before anything that reaches outside this machine or is hard to undo: pushing,
deploying, or hitting a third-party service beyond the rate agreed in §7a.

```bash
node node_modules/.bin/eleventy --dryrun     # build check
node node_modules/.bin/eleventy              # full build to _site/
node node_modules/.bin/eleventy --serve --port=8080   # dev server
```

**`npx` and `npm` are not on `PATH` in agent shells** — only `/usr/bin/node` is, and it may be
the wrong version. Prefix with the nvm path first, or the commands above simply fail with
`npx: command not found`:

```bash
export PATH="/home/miichael/.nvm/versions/node/v22.21.1/bin:$PATH"
```

Run the server with `run_in_background` and poll its log until `Server at http://localhost:8080/`
appears; then `curl` it to confirm routes actually resolve. The preview tooling
(`.claude/launch.json`, `maja-explosiv-dev`, port 8080) still works when available — its browser
pane must be **visible** for screenshots, and if they time out, ask the owner to open it.

### 7a. Fetching the live site

`curl` is approved for `maja-explosiv.com` (owner, 2026-08-25), **sequentially, ~1 request every
2 seconds, never in parallel.** It is TYPO3 4.2 on shared hosting; a burst can degrade it for
real visitors or trip flood protection, and the resulting errors read as missing content.
`migrated-content/_tools/fetch.sh` already enforces this and records raw bytes, headers and a
fetch timestamp.

Note the site 301-redirects apex → `www` and `http` → `https`; the canonical host is
`https://www.maja-explosiv.com/`. That is the site's own redirect, not something to "fix".

### 7b. Things that will bite

**Editing anything in `src/_user/layouts/` or `src/_user/includes/` requires restarting the
dev server.** `.eleventy.js` copies both into `.cache/` at config time, so a running server
keeps serving the old markup and the change looks like it did nothing. Only
`src/_user/assets/css/` is a watch target and hot-reloads.

**Expected build errors right now:** four `Featured project '…' not found in any collection`
lines. `src/_user/data/featuredProjects.json` names projects by slug that Stage 0b quarantined.
The build still completes. It resolves when Stages 6–11 migrate the projects, though the
entries will need repointing rather than just reappearing — the slugs change under the six→four
category mapping. Logged in PLAN.md.

The old `Missing image title/year for caption` noise for `sisyphos-gate`, `murals-europe` and the
paintings collections is **gone** — those files are quarantined.

**The site is mostly empty during the migration and that is correct.** One real page
(`/about/links/`), a homepage whose Bio/Timeline/Press tabs are blank, empty collection pages,
no featured projects. Do not "fix" it.

**Verify visually, not just by computed style.** A real bug was missed because CSS
metrics were checked but element positions were not — a base rule
(`.content-wrapper p, li { margin-inline: auto }`) was silently centring list items.

## 8. Where things stand

Phases are in PLAN.md; the short version:

- **Design tokens** — locked (Geist throughout, grey scale, 224px sidebar).
- **About sections** — done, built against the Figma components.
- **Sidebar** — done, rebuilt against the `Navigation6 Flip Yellow` variant.
- **Homepage, single project** — structurally close, need a token-accurate pass.
- **Content migration** — **underway, and it now governs `src/` content.** Read
  `project_docs/content-migration-plan.md` (approved 2026-08-25) before touching content.
  - Stages **0 (census)**, **0b (quarantine)** and **1 (Links)** are done; Stage 1 passes
    19/19 checks, only V8 (visual comparison) outstanding. Stages 2–14 not started.
  - **`src/pages/` and `src/posts/` now contain only migration output** — currently one file,
    `about/links.md`. The 38 pre-existing Markdown files were **moved**, not deleted, to
    `pre-migration-content/`. The old "~26 of ~71 projects converted" line was wrong twice
    over: it was 23, not 26, and none of it is a baseline to build on.
  - Three sibling directories hold content that is deliberately **not built** and each has a
    README: `pre-migration-content/` (39 files), `migrated-hidden-content/` (TYPO3
    `hidden=1`), `migrated-deleted-content/` (TYPO3 `deleted=1`, 308 files — of which only 9
    records are Maja's; the rest belong to other sites that shared the database).
  - The database is a local MySQL 8 (`usr_p51487_2`, user `maja`), and **it must be loaded
    from the current dump**: `SELECT LENGTH(bodytext) FROM tt_content WHERE uid=1399;` must
    return **8441**. If it returns 10340 the January 2025 dump is loaded and every extraction
    will be silently stale — that happened, and passed all eleven local checks.
- **Deployment** — GitHub Pages **live** at <https://consistent1.github.io/maja-explosiv/>.
  **Mid-transition (2026-08-26):** `.github/workflows/deploy-pages.yml` now builds and
  publishes via GitHub Actions (`path-prefix: /maja-explosiv/`, runs on push to `main`).
  Actions is free here because the repo is public.
  **Two manual steps remain, in this order:**
  1. **Settings → Pages → Source: `GitHub Actions`** (currently "Deploy from a branch: main
     /docs"). Until this is flipped the workflow builds and then fails at the deploy step.
  2. **Only then** stop tracking `docs/` (231 files). Doing it first takes the live site down.

  Why the change: `docs/` is a committed second copy of the whole build, and `copy:docs` does
  `rm -rf docs && cp -r _site docs`, so every deploy rewrites every file and git grows by the
  asset payload each time. Already 42 MB duplicated; the image archive would make it ~200 MB.
  The old flow (`npm run deploy:github`, commit `docs/`, push) still works until step 1 happens.
  VPS still deferred — `deploy-server.yml` exists upstream, manual-trigger only, unconfigured.
