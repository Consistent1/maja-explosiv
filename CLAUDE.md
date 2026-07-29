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
| `.goosehints` | Short, still accurate; upstream path and workflow expectations. |

Ignore `project_docs/_archive/` unless chasing history. It holds superseded docs and the
**retired Figma PNG exports** — see §4.

## 3. The two sources of truth

Do not conflate these. Almost every mistake in this project's history came from doing so.

**Figma governs design.** Structure, layout, spacing, typography, colour.
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
- Before a change, be able to state why it helps, what should change, and how you will
  know it did. Verify it actually happened before moving on.
- Open questions of the "needs the owner's judgement" kind go in **one place**:
  `project_docs/PLAN.md` § *Open items needing input*. Resolved items get struck through
  with the resolution, not deleted.

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

- Generic fixes belong **upstream** in `/home/miichael/Code/explosive`, then sync down.
  Maja-specific work belongs in `src/_user/`.
- `src/_layouts/`, `src/_includes/`, `src/assets/css/main.css` are **base template**
  files. Editing them directly is a boundary violation; there is a known backlog of these
  (see PLAN.md Phase 0).
- **`custom.css` is messy** — a large block of rules is declared two or three times with
  the later copy silently winning. A verified de-duplication pass has been done; what
  remains is logged in PLAN.md. Do not add to the mess; append new sections at the end.

## 7. Running and verifying

```bash
npx eleventy --dryrun      # build check
```

Serve via the preview tooling (`.claude/launch.json`, name `maja-explosiv-dev`, port 8080),
never a raw shell command. The browser pane must be **visible** for screenshots to work —
if they time out, ask the owner to open it.

Pre-existing build noise you can ignore: `Missing image title/year for caption` errors for
`sisyphos-gate`, `murals-europe`, and the paintings collections.

**Verify visually, not just by computed style.** A real bug was missed because CSS
metrics were checked but element positions were not — a base rule
(`.content-wrapper p, li { margin-inline: auto }`) was silently centring list items.

## 8. Where things stand

Phases are in PLAN.md; the short version:

- **Design tokens** — locked (Geist throughout, grey scale, 224px sidebar).
- **About sections** — done, built against the Figma components.
- **Sidebar** — done, rebuilt against the `Navigation6 Flip Yellow` variant.
- **Homepage, single project** — structurally close, need a token-accurate pass.
- **Content migration** — ~26 of ~71 projects converted; most lack images. Not started at
  scale.
- **Deployment** — GitHub Pages and VPS both deferred.
