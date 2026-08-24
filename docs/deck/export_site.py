"""Export the deck as a standalone, hand-editable file for the website.

Editability was the whole point of the request, so the binary payload is kept
OUT of the markup you would actually want to change:

  * slide text sits at the top, as plain semantic HTML
  * every image is a CSS custom property, referenced by name, so no base64
    ever appears inside a slide
  * all font and image data is one clearly-fenced block at the very bottom

The result is ~1,900 readable lines followed by one block you scroll past.
"""
import base64, pathlib, re, sys
S = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(S))
from deck_css import CSS
from deck_js import JS
from deck_slides import SLIDES

REPO = pathlib.Path("/Users/maximecarriere/src/wild-fire-integrator")
OUT  = pathlib.Path("/Users/maximecarriere/src/website/slides/wildfire-integrator.html")

def raw64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

IMAGES = {
    "--img-plume-tiny": (S/"img/plume_tiny.jpg", "image/jpeg"),
    "--img-plume-small":(S/"img/plume_small.jpg","image/jpeg"),
    "--img-plume-large":(S/"img/plume_large.jpg","image/jpeg"),
    "--img-night":      (S/"img/night.jpg",      "image/jpeg"),
    "--img-empty":      (S/"img/empty.jpg",      "image/jpeg"),
    "--img-pareto":     (REPO/"results/figures/pareto.png",      "image/png"),
    "--img-pareto-dk":  (REPO/"results/figures/pareto-dark.png", "image/png"),
    "--img-unoq":       (REPO/"docs/media/unoq.webp",            "image/webp"),
}
TOKEN = {"__IMG_TINY__":"--img-plume-tiny",
         "__IMG_SMALL__":"--img-plume-small", "__IMG_LARGE__":"--img-plume-large", "__IMG_NIGHT__":"--img-night",
         "__IMG_EMPTY__":"--img-empty", "__IMG_PARETO__":"--img-pareto",
         "__IMG_PARETO_N__":"--img-pareto-dk",
         "__IMG_UNOQ__":"--img-unoq"}

# ---- swap every <img> for a var-driven div so no base64 lands in the markup ----
slides = SLIDES
def img_sub(m):
    tag = m.group(0)
    tok = re.search(r'(__IMG_[A-Z_]+__)', tag)
    alt = re.search(r'alt="([^"]*)"', tag)
    cls = re.search(r'class="([^"]*)"', tag)
    var = TOKEN[tok.group(1)]
    classes = ("ph " + cls.group(1)) if cls else "ph"
    return (f'<div class="{classes}" role="img" aria-label="{alt.group(1) if alt else ""}"'
            f' style="background-image:var({var})"></div>')
slides = re.sub(r'<img[^>]*__IMG_[A-Z_]+__[^>]*>', img_sub, slides)
assert "__IMG_" not in slides, "an image token survived"

EXTRA_CSS = """
/* image placeholders -- the picture itself is a CSS variable, defined in the
   ASSETS block at the very bottom of this file */
.ph{width:100%;height:100%;background-size:cover;background-position:center;display:block}
figure .ph{aspect-ratio:940/664;background-size:contain;background-repeat:no-repeat;
           background-color:var(--card);border:1px solid var(--cardEdge);border-radius:7px}
"""

ASSETS = ["\n/* ============================================================\n"
          "   ASSETS  —  generated data. Nothing here needs hand-editing.\n"
          "   Fonts: iA Writer Quattro S (SIL OFL). Images: base64.\n"
          "   To swap a picture, replace the url(...) for its variable.\n"
          "   ============================================================ */"]
for name, w in [("normal","Regular"),("bold","Bold")]:
    ASSETS.append(f"@font-face{{font-family:'iAWriterQuattroS';font-weight:{name};font-style:normal;"
                  f"font-display:swap;src:url(data:font/woff2;base64,{raw64('/tmp/kwfonts/'+w+'.woff2')}) format('woff2')}}")
for name, w in [("normal","Italic"),("bold","BoldItalic")]:
    ASSETS.append(f"@font-face{{font-family:'iAWriterQuattroS';font-weight:{name};font-style:italic;"
                  f"font-display:swap;src:url(data:font/woff2;base64,{raw64('/tmp/kwfonts/'+w+'.woff2')}) format('woff2')}}")
ASSETS.append(":root{")
for var,(path,mime) in IMAGES.items():
    ASSETS.append(f"  {var}: url(data:{mime};base64,{raw64(path)});")
ASSETS.append("}")

# main CSS minus the @font-face rules (they move to the bottom)
css = re.sub(r"@font-face\{[^}]*\}\n?", "", CSS)
css = re.sub(r"/\* ---- iA Writer Quattro S[^\n]*\n", "", css)

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Nobody Is Watching the Thousandth Camera — Kernwerk</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Spiking evidence fusion for wildfire sensor networks. Kernwerk.">
<!--
  ============================================================================
  HOW TO EDIT THIS FILE

  Structure, top to bottom:
    1. <style>   the design system. Colours are CSS variables in :root
                 (and again under [data-theme="night"]). Change them once
                 and the whole deck follows.
    2. <body>    the slides. Each is one <section class="slide">, in order.
                 Edit the text directly -- it is plain HTML, no build step.
    3. <script>  navigation and the three canvas animations.
    4. ASSETS    fonts and images as base64. Skip past it.

  To add a slide:      copy any <section class="slide">...</section> block.
  To reorder:          move the blocks. Numbering in the eyebrow is manual.
  To change the count: update data-main on <body> (main slides before the
                       appendix). Everything after that is appendix.

  Layout uses a 12-column grid: .c4 spans 4 columns, .c8 spans 8, etc.
  Accent classes: .hl (teal) .warn (amber) .bad (red) .dim (muted).
  ============================================================================
-->
<style>
__CSS__
__EXTRA__
</style>
</head>
<body data-main="__MAIN__">
"""

TAIL = """
<script>
__JS__
</script>

<!-- Everything below is generated data: fonts and images, base64-encoded.
     It sits at the END of the file on purpose, so the slides above stay
     readable. Nothing here needs hand-editing. -->
<style id="assets">
__ASSETS__
</style>
</body>
</html>
"""

CHROME_TOP = """
<div class="bar top">
  <span class="mark">&#8251;</span>
  <a class="wordmark" href="/">Kernwerk</a>
  <span class="sep">/</span>
  <span class="chip">wildfire integrator</span>
  <span class="spacer"></span>
  <button class="btn" id="theme" title="Toggle day / night (T)">day&nbsp;/&nbsp;night</button>
</div>

<main class="deck">"""

CHROME_BOT = """</main>

<div class="bar bot">
  <div class="ticks" id="ticks"></div>
  <span class="count" id="count">1 / 18</span>
  <span class="spacer"></span>
  <button class="btn" id="appx" title="Jump to appendix (A)">appendix</button>
  <button class="btn" id="prev" title="Previous (&larr;)">&larr;</button>
  <button class="btn" id="next" title="Next (&rarr;)">&rarr;</button>
</div>

<div class="help" id="help"><div class="box">
  <p class="eyebrow">keys</p>
  <p><kbd>&rarr;</kbd> <kbd>space</kbd> next &nbsp;&middot;&nbsp; <kbd>&larr;</kbd> back
  &nbsp;&middot;&nbsp; <kbd>A</kbd> appendix &nbsp;&middot;&nbsp; <kbd>T</kbd> day/night
  &nbsp;&middot;&nbsp; <kbd>F</kbd> fullscreen &nbsp;&middot;&nbsp; <kbd>?</kbd> this panel</p>
  <p class="tiny" style="margin:0">Click anywhere to close.</p>
</div></div>
"""

MAIN = 12
html = (HEAD.replace("__CSS__", css).replace("__EXTRA__", EXTRA_CSS)
            .replace("__MAIN__", str(MAIN))
        + CHROME_TOP + slides + CHROME_BOT
        + TAIL.replace("__JS__", JS).replace("__ASSETS__", "\n".join(ASSETS)))

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html)
lines = html.count("\n") + 1
assets_start = html.index("ASSETS  —  generated data")
readable = html[:assets_start].count("\n")
print(f"wrote {OUT}")
print(f"  {OUT.stat().st_size/1024/1024:.2f} MB, {lines} lines")
print(f"  readable markup/CSS/JS before the assets block: {readable} lines")
nslides = html.count('<section class="slide">')
print(f"  slides: {nslides}")
