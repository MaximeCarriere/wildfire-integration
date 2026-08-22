import base64, pathlib, sys
sys.path.insert(0, "/tmp/deck-build")
from deck_css import CSS
from deck_js import JS
from deck_slides import SLIDES

S = pathlib.Path("/tmp/deck-build")
REPO = pathlib.Path("/Users/maximecarriere/src/wild-fire-integrator")

def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def raw64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

css = (CSS.replace("__F_REG__", raw64("/tmp/kwfonts/Regular.woff2"))
          .replace("__F_BLD__", raw64("/tmp/kwfonts/Bold.woff2"))
          .replace("__F_ITA__", raw64("/tmp/kwfonts/Italic.woff2"))
          .replace("__F_BIT__", raw64("/tmp/kwfonts/BoldItalic.woff2")))

slides = (SLIDES
  .replace("__IMG_TINY__",     b64(S/"img/plume_tiny.jpg", "image/jpeg"))
  .replace("__IMG_NIGHT__",    b64(S/"img/night.jpg", "image/jpeg"))
  .replace("__IMG_EMPTY__",    b64(S/"img/empty.jpg", "image/jpeg"))
  .replace("__IMG_PARETO__",   b64(REPO/"results/figures/pareto.png", "image/png"))
  .replace("__IMG_PARETO_N__", b64(REPO/"results/figures/pareto-dark.png", "image/png")))

MAIN = 18

HTML = """<title>Nobody Is Watching the Thousandth Camera</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>__CSS__</style>
<body data-main="__MAIN__">

<div class="bar top">
  <span class="mark">&#8251;</span>
  <a class="wordmark" href="#" onclick="return false">Kernwerk</a>
  <span class="sep">/</span>
  <span class="chip">wildfire integrator</span>
  <span class="spacer"></span>
  <button class="btn" id="theme" title="Toggle day / night (T)">day&nbsp;/&nbsp;night</button>
</div>

<main class="deck">__SLIDES__</main>

<div class="bar bot">
  <div class="ticks" id="ticks"></div>
  <span class="count" id="count">1 / 15</span>
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
  <p class="tiny" style="margin:0">15 slides, then 6 appendix slides. Click anywhere to close.</p>
</div></div>

<script>__JS__</script>
"""

out = (HTML.replace("__CSS__", css)
           .replace("__SLIDES__", slides)
           .replace("__JS__", JS)
           .replace("__MAIN__", str(MAIN)))

p = S / "kernwerk-deck.html"
p.write_text(out)
n = out.count('<section class="slide">')
print(f"wrote {p}")
print(f"  {p.stat().st_size/1024/1024:.2f} MB, {n} slides ({MAIN} main + {n-MAIN} appendix)")
