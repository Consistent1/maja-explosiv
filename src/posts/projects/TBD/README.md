# TBD — projects with no settled category

**A staging area, not a destination.** Everything here is waiting on a decision about which of
the new site's four categories it belongs to. Emptying this folder is a release condition of
the migration, alongside `unassigned.tsv`.

## Why this folder exists

The old site organised work into **six** categories; the new site uses **four** —
`sculptures`, `installations`, `performance`, `paintings`. The mapping is not one-to-one.

Owner's rule, 2026-08-26: **anything that does not fall neatly into a new category comes here
rather than being guessed at.** A project sitting in `TBD/` is a visible open question. A
project forced into the nearest-looking category is a silent error, and this project already
has one of those in its history — see the whale, below.

## What mapped without judgement (60 projects)

| old container | → new category | projects |
|---|---|---|
| `sculptural-work` → *Sculptures* | `sculptures` | 29 |
| `sculptural-work` → *Installations* | `installations` | 17 |
| `performance` | `performance` | 6 |
| `murals` | `paintings` | 3 |
| `paper-work` | `paintings` | 5 |

The 46 in `sculptural-work` — the largest and apparently hardest group — needed no decision at
all. **The old site had already split them into *Sculptures* and *Installations*,** which is
exactly the distinction the new site draws.

## What is here, and why (5 projects)

### ~~`collaborations` — 8 projects~~ → moved to `sculptures/` (owner, 2026-08-27)

Hand of Man · Wheel of Power · Forget me Not · Throne · Elephant · Destroy HIV · Gong Trophy ·
Metal Group XIX

**Moved provisionally**, on the owner's instruction and with the explicit note that it can be
reversed. By material these are metal sculptures, so `sculptures/` is right on filing grounds.

**There is no open question.** `collaborations` does not exist as a category on the new site,
so the only decision was ever which of the four each project belongs to. An earlier note here
framed it as a curatorial choice about preserving collaborative work as a body — that premise
was wrong and has been withdrawn.

Seven folders moved; **Metal Group XIX has no images at all**, so it exists only as a future
content page.

### `event-organisation` — 3 projects

Dada Festwochen · Eurokon · Eurokot

**Events, not artworks.** `performance` is the closest of the four and still wrong: these are
things Maja organised, not pieces she performed. Note their photographs overlap heavily with
individual sculptures shown at them — `Eurokon` shares images with *Nailed Tanks*, *Torso* and
*Eagle*; `Eurokot` with *Iron Channel* (see `image-archive/DUPLICATES.md`).

### `possibilities` — 2 projects

**Breath Under Water** (77 images) and **Alchemy Bar** (36 images).

Both substantial, both under a container the old site kept hidden.

**Breath Under Water is the whale, and it is why this folder exists.** It is a whale
*sculpture*. An earlier migration attempt classified projects by keyword heuristic and filed
it under **paintings** — the error is cited in `CLAUDE.md` and the migration plan as the reason
category assignment must never be guessed. It reached `TBD/` this time instead of reaching
`paintings/`, which is the rule working.

It is also the target of a shortcut page (uid 982) and shares images with a hidden `Whale`
page — so expect duplicate-looking entries when it is migrated.

## What was here and is not (2 pages)

`recent-work` contributed two entries, **`Installations` (uid 1041) and `Sculptures` (uid
1042)**, which looked like projects because they sit where projects sit.

**They are not projects.** Verified 2026-08-26: **zero content rows, zero child pages, zero
images** each. Empty container pages left over from a navigation structure. They should produce
no project pages at all, and are excluded rather than parked here.

That took `TBD/` from 15 to 13.

## Resolving an entry

Move the project's folder to its category, and move the matching folder under
`src/assets/images/projects/`. Record the decision in `PLAN.md`, since the mapping table in
the migration plan (decision 13) is the reference other stages read.
