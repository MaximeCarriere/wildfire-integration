# Archived slides

The live deck is the ten-slide short version: cover, 01–08, and *building in
the open*. Everything else was cut on request, not deleted.

| file | what it is |
|---|---|
| `deck_slides_full.py` | the complete 24-main + 11-appendix source, as it stood before the cut |
| `removed_slides.html` | just the 25 removed slide blocks, in their original order |

**To restore everything:** copy `deck_slides_full.py` over `../deck_slides.py`
and set `MAIN = 24` in `../build_deck.py` and `../export_site.py`.

**To restore a single slide:** paste its block from `removed_slides.html` into
`../deck_slides.py` before the closing triple quote, and raise `MAIN` by one if
it belongs in the main run. The `__N__`, `__A__` and `__REF:` tokens resolve at
build time, so nothing needs renumbering by hand.

Among the cut slides are three that answer required questions on their own:
*the hardware* (question 3), *does it work* (the evidence), and *what we don't
claim* (question 6, honest feasibility), plus the *coverage* slide that maps the
deck to all six.
