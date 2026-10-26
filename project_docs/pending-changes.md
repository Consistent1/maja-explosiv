# Pending Changes

Remove the temp directory from the passthrough performed by 11ty.

Where is the image for the footer stored?

Automate the insertion of collections to the tab bar (in Projects).
The collections are currently hardcoded.  

After the migration is over (post Stage 14): correct the misspelled source paths too.
The visible text and published file names were corrected 2026-10-26, but the provenance paths
still carry the old spelling because the database does: `original:` in
`src/posts/projects/sculptures/wacken-skull.md` (`2012WackenScull/`), and press `source_file`
(`1993_wohlgrott.jpg`, `1993_wohlgrott2.jpg`, `2012_Wacken_Scull_….pdf`). Renaming the folders
in `old/TYPO3BU/` and `image-archive/` (untracked, so plain `mv`) breaks re-runs of the pipeline,
which is why it waits.

Video embedding (owner, 2026-10-26): embed video where a project needs it. Releases the five
held projects — `casino-gitano`, `elxt-90` (`STAGES[9]['hold']`), `wheel-of-power`,
`destroy-hiv` (`STAGES[10]['hold']`), `the-helixes` (`STAGES['11b']['hold']`). Figma has no
video component, so the design is needed too. PLAN.md item "what should happen to the videos?".

Homepage category tabs: list each project under the old site's page title (`source_page_title`,
e.g. "Eurokon"), not the full heading. The project page itself keeps the full heading
("Eurokon, 2. Symposium für interaktives Recycling"), as now.

Homepage bug: projects without a year show "1900". Likely cause: `convert_projects.py` writes
the placeholder `date: 1900-01-01` when the year is missing, and `home.njk` prints
`post.data.date | date('YYYY')`. A missing year should show nothing.

Homepage category tabs: order projects by time, newest first. Depends on the years — most are
still missing (see the 1900 item above), so the order is only meaningful once Maja adds them.

Link project names to their project pages, in the timeline and in the homepage's project lists.
For the timeline, the source HTML already carries internal links to the project page
(e.g. `<link 1046 …>` in `source_bodytext_html`, where 1046 is the project's `source_uid`).

Press page: remove the list under the gallery. Careful — the gallery links each clipping's
image, not its PDF, so the PDFs are reachable only through the list today. Two PDF entries have
no image at all (Wacken Skull, The Alchemy Bar) and would disappear from the page; the three
with a JPG companion would lose their PDF link.
