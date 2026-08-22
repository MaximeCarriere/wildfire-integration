# The deck

Source for the presentation. Two builds from the same three modules:

| file | what it makes |
|---|---|
| `build_deck.py` | a single self-contained page (for publishing as an artifact) |
| `export_site.py` | `website/slides/wildfire-integrator.html` — hand-editable |

`deck_slides.py` holds the slide markup, `deck_css.py` the design system,
`deck_js.py` the navigation and the four canvas animations.

The website export deliberately keeps binary data out of the markup: every
image is a CSS custom property, and all font/image base64 sits in one fenced
block at the very end of the file. 99% of the file is editable by hand
without a build step — edit the HTML directly and it just works.
