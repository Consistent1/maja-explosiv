# Contact & Datenschutz — source record

**Stage:** 5 · **Migrated:** 2026-08-27 · **Legal text transcribed verbatim, never edited** (plan §8)

## Scope — and the Impressum question, answered

| page | uid | live path | elements migrated |
|---|---|---|---|
| Contact | 973 | `info/contact` | **1311 only** — 1450 documented but not migrated |
| Datenschutz | 1065 | `info/datenschutz` | 1620, 1619 |

**There is no separate Impressum page for Maja.** The database has one — `pages.uid = 809` —
but it sits under **pid 733, `pyrofessor`**, a different site sharing the install. The live Maja
site links no impressum anywhere: its nav and footer reference only `info/contact.html`,
`info/datenschutz.html`, `tools/sitemap.html` and `footer/search.html`.

**The impressum content is on the contact page.** Both migrated elements there are headed
`Impressum:` — the responsible person with phone and email (1311), and the web-design credit
for Werner Trunk with a Ust-Id (1450). That is the German Impressum obligation discharged inside
the contact page rather than on its own.

## Excluded

| | why |
|---|---|
| `Kontakt` (952), element 1278 | **A placeholder stub.** Its entire content is `"Maja ExplosivAdresse.."`. The page is not linked from the live site |
| `contact` elements 1451, 1279, 1477 | `hidden = 1` — see the section below, where each is recorded in full |
| `Impressum` (809), `Datenschutz` (1066), `Kontakt` (771) | belong to `pyrofessor` |

## The complete original contact page, verbatim

The old page carried exactly this, in this order. **Only the first block is migrated.**

### `tt_content 1311` — MIGRATED

```
For commissions, collaborations or bookings please do not hesitate to contact:
Maja Thommen                        <- bold in the source
0049 (0)30 505 970 27
m-e@maja-explosiv.com               <- bold in the source
```

### `tt_content 1450` — DOCUMENTED, NOT MIGRATED

**Deliberately not carried over to the new site** (owner, 2026-08-27). Preserved here and as raw
bytes in `raw/db/tt_content-1450.bodytext.html`.

```
Webdesign and Realisation:          <- bold in the source
Werner Trunk
Oppelnerstr.9
10997 Berlin

Ust Id DE 190483520
wtweb.com                           <- linked to http://www.wtweb.com/
```

Header on both elements in TYPO3: `Impressum:`.

**This is the only postal address anywhere in the migrated source, and it is the web designer's,
not Maja's.** The old site published no studio address for her. Note the design's hardcoded
`ATELIER / MAAS & THOMMEN / 10997 BERLIN` shares the **10997** postcode with Werner Trunk's
Kreuzberg address — worth Maja confirming rather than assuming.

The removal means the built contact page contains **no** occurrence of `Werner Trunk`, `wtweb`,
`Oppelner` or `Ust Id` — verified.

## The three hidden contact elements, recorded in full

None is published on the live site. Each is set down here so nothing rests only in a database
that will eventually be switched off.

### `tt_content 1477` — text, hidden

**Empty.** No bodytext, no header, no image. An element that was created and never filled.

### `tt_content 1279` — "Anfrage", hidden

A `th_mailformplus_pi1` enquiry-form plugin. **Its content is the extension's own shipped
example**, not anything Maja wrote — verbatim:

```
# Example content:
Name: | *name = input,40 | Enter your name here
Email: | *email=input,40 |
Address: | address=textarea,40,5 |
Contact me: | tv=check | 1

|formtype_mail = submit | Send form!
|html_enabled=hidden | 1
|subject=hidden| This is the subject
```

So a contact form was **started and abandoned before being configured**. The new site has no
contact form. Whether it should is a question for Maja, not a migration gap.

### `tt_content 1451` — image, hidden

**`kartePariskl.jpg`** — 707×785. The filename reads as *Karte Paris klein*, "small map of
Paris". Already archived at **`image-archive/hidden/about/contact/kartePariskl.jpg`**, having
been picked up as hidden content by the archive builder.

## How the new contact page differs from the old one

Three differences, **all deliberate** — the design stays as it is (owner, 2026-08-27). Recorded
so they are visible rather than discovered later.

| | old site | new site |
|---|---|---|
| studio address | **none** anywhere in the migrated source | **`ATELIER / MAAS & THOMMEN / 10997 BERLIN`** — from Figma, hardcoded in `src/_user/layouts/contact.njk` |
| photograph | `webthanksxy.jpg`, 1876×1916, `tt_content 1478`, a **visible** element rendered via a `typo3temp` derivative | the design's own `contact-image.png`, used twice |
| contact details | phone and email in body text | the same text, migrated verbatim |

**The old photograph is deliberately not carried over** (owner, 2026-08-27). The new design
uses its own imagery; there is no intention to restore hers. It is preserved, not lost:

> **`image-archive/live/about/contact/webthanksxy.jpg`** — 1876×1916, from
> `uploads/pics/webthanksxy.jpg`, referenced by `tt_content 1478` on `pages.uid 973`.

One point remains for Maja, logged in `PLAN.md`: **the atelier address cannot be verified.** It
appears in the design and nowhere in the migrated source, so unlike the phone and email — which
migrated verbatim and match the live site — there is nothing to check it against. Normally
`CLAUDE.md` §3 would put such content in a data file rather than the template; it is being left
hardcoded deliberately.

## Conversion

- `<b>` on a line of its own → a Markdown `##` heading. The privacy policy uses **31** of them
  as section headings; inline bold within a sentence is left as text.
- `<br />` → line break; `<link>` and `<a>` → Markdown links.
- Nothing reworded, reordered or corrected.

| page | headings | bold | paragraphs |
|---|---|---|---|
| contact | 0 | 2 | 2 |
| datenschutz | 31 | 0 | 101 |

A bold line is treated as a **section heading** only where the page uses it that way. The privacy
policy does — 31 of them. On the contact page the same markup is emphasis, so `Maja Thommen` and
the email render bold rather than as `<h2>`; an earlier pass got this wrong and made them
headings.

## Verification

| | |
|---|---|
| contact | **2 of 2** migrated paragraphs present; the 3 belonging to `1450` are excluded by decision |
| datenschutz | **128 of 128** live paragraphs present |
| encoding | `Datenschutzerklärung`, `gemäß`, `personenbezogene` correct throughout |

## Two things needing a decision

**1. ~~`site.js` carries a placeholder email.~~ CORRECTED 2026-08-27.** `contactInfo.email` was
`info@maja-explosiv.com`, commented *"Placeholder - update with actual email"*, and
`contactInfo.phone` was empty. Both now carry the migrated values —
**`m-e@maja-explosiv.com`** and **`0049 (0)30 505 970 27`** — sourced from `tt_content 1311`
and confirmed against the live site. The build no longer references the placeholder anywhere.

**2. The privacy policy has not been reviewed.** It is a 24,834-character GDPR text of unknown
provenance and unknown date, migrated verbatim because that is the rule for legal text. Whether
it is current, and whether it should carry Maja's name at all, is not a migration question.
