CSS = r"""
/* ---- iA Writer Quattro S, the Kernwerk face (SIL OFL) ---- */
@font-face{font-family:'iAWriterQuattroS';src:url(data:font/woff2;base64,__F_REG__) format('woff2');font-weight:normal;font-style:normal;font-display:swap}
@font-face{font-family:'iAWriterQuattroS';src:url(data:font/woff2;base64,__F_BLD__) format('woff2');font-weight:bold;font-style:normal;font-display:swap}
@font-face{font-family:'iAWriterQuattroS';src:url(data:font/woff2;base64,__F_ITA__) format('woff2');font-weight:normal;font-style:italic;font-display:swap}
@font-face{font-family:'iAWriterQuattroS';src:url(data:font/woff2;base64,__F_BIT__) format('woff2');font-weight:bold;font-style:italic;font-display:swap}

*{font-family:'iAWriterQuattroS',ui-monospace,SFMono-Regular,Menlo,monospace;box-sizing:border-box}

/* light is the base; night overrides only tokens */
:root{
  color-scheme:light;
  --red:#ee5253; --yellow:#ffa801; --green:#27ae60; --select:#00b894;
  --bg:#ecf0f1; --front:#34495e;
  --dim:#34495ea6; --line:#34495e42; --line2:#34495e1f;
  --card:#ffffff; --cardEdge:#34495e1a;
  --shadow:0 1px 2px #34495e14, 0 10px 30px -18px #34495e40;
}
@media (prefers-color-scheme:dark){
  :root:where(:not([data-theme="light"])){
    color-scheme:dark;
    --red:#f35b5b; --yellow:#ffa801; --green:#00b894; --select:#00b894;
    --bg:#3a5168; --front:#ecf0f1;
    --dim:#ecf0f1b0; --line:#ecf0f145; --line2:#ecf0f11f;
    --card:#33475b; --cardEdge:#ecf0f11f;
    --shadow:0 1px 2px #0003, 0 10px 30px -18px #0006;
  }
}
:root[data-theme="night"]{
  color-scheme:dark;
  --red:#f35b5b; --yellow:#ffa801; --green:#00b894; --select:#00b894;
  --bg:#3a5168; --front:#ecf0f1;
  --dim:#ecf0f1b0; --line:#ecf0f145; --line2:#ecf0f11f;
  --card:#33475b; --cardEdge:#ecf0f11f;
  --shadow:0 1px 2px #0003, 0 10px 30px -18px #0006;
}

html,body{height:100%}
/* One fluid scale, on the ROOT, so every rem in the sheet follows it.
   Putting it on <body> left headings (sized in rem) pinned to 16px while body
   text grew -- which is why the sizes stopped relating to each other. */
html{font-size:clamp(15px, 0.58vw + 0.66vh, 20px)}
body{
  margin:0;background:var(--bg);color:var(--front);
  /* Scale with BOTH axes. A vw-only scale leaves a tall window mostly empty,
     which is what made every slide look like a small block floating in
     whitespace. */
  font-size:1rem;line-height:1.5;overflow:hidden;
  -webkit-font-smoothing:antialiased;
}

/* ================= chrome ================= */
.bar{
  position:fixed;left:0;right:0;z-index:40;display:flex;align-items:center;gap:14px;
  padding:14px clamp(16px,3vw,34px);font-size:13px;
}
.bar.top{top:0}
.bar.bot{bottom:0;color:var(--dim)}
.mark{color:var(--select);font-weight:bold}
.wordmark{font-weight:bold;letter-spacing:-.01em;text-decoration:none;color:var(--front)}
.sep{color:var(--line);user-select:none}
.spacer{flex:1}
.chip{
  border:1px solid var(--line);border-radius:2px;padding:2px 8px;color:var(--dim);
  font-size:11px;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap;
}
.btn{
  background:none;border:1px solid var(--line);border-radius:2px;color:var(--dim);
  padding:3px 9px;font-size:12px;cursor:pointer;transition:.15s;
}
.btn:hover{color:var(--select);border-color:var(--select)}
.btn:focus-visible{outline:2px solid var(--select);outline-offset:2px}
.count{font-variant-numeric:tabular-nums;color:var(--dim);font-size:12px}

/* progress ticks */
.ticks{display:flex;gap:3px;align-items:center}
.tick{width:14px;height:3px;background:var(--line);border-radius:1px;transition:.25s;cursor:pointer}
.tick.on{background:var(--select)}
.tick.ax{width:6px;opacity:.6}

/* ================= slides ================= */
.deck{position:relative;height:100%;width:100%}
.slide{
  position:absolute;inset:0;display:none;
  padding:clamp(52px,7vh,72px) clamp(18px,4vw,54px) clamp(44px,6vh,60px);
  overflow-y:auto;overflow-x:hidden;
}
.slide.live{display:block}
.inner{max-width:1545px;margin:0 auto;min-height:100%;display:flex;flex-direction:column;justify-content:center}

/* entrance */
.slide.live .anim{animation:rise .5s cubic-bezier(.16,.84,.44,1) backwards}
.slide.live .anim:nth-child(1){animation-delay:.02s}
.slide.live .anim:nth-child(2){animation-delay:.08s}
.slide.live .anim:nth-child(3){animation-delay:.14s}
.slide.live .anim:nth-child(4){animation-delay:.2s}
.slide.live .anim:nth-child(5){animation-delay:.26s}
.slide.live .anim:nth-child(6){animation-delay:.32s}
@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){
  .slide.live .anim{animation:none}
  *{transition:none!important}
}

/* ================= type ================= */
.eyebrow{
  font-size:0.66rem;letter-spacing:.18em;text-transform:uppercase;color:var(--select);
  margin:0 0 14px;display:flex;align-items:center;gap:9px;
}
.eyebrow::before{content:"";width:9px;height:9px;background:var(--select);border-radius:2px;flex:none}
h1{font-size:2.55rem;line-height:1.1;letter-spacing:-.02em;margin:0 0 18px;font-weight:bold;text-wrap:balance}
h2{font-size:1.72rem;line-height:1.18;letter-spacing:-.015em;margin:0 0 16px;font-weight:bold;text-wrap:balance}
h3{font-size:1.02rem;margin:0 0 8px;font-weight:bold}
p{margin:0 0 12px;overflow-wrap:break-word}
.lead{font-size:1.16rem;line-height:1.5;color:var(--dim);max-width:62ch}
.tiny{font-size:0.76rem;color:var(--dim);line-height:1.45}
.dim{color:var(--dim)}
.hl{color:var(--select)}
.warn{color:var(--yellow)}
.bad{color:var(--red)}
b,strong{font-weight:bold}
em{font-style:italic}
a{color:var(--select)}

/* ================= bento ================= */
.bento{display:grid;gap:clamp(10px,1.1vh,16px);grid-template-columns:repeat(12,1fr);align-content:center}
/* Rows are sized to their content and the block is centred. Stretching them
   to fill the frame made every card tall with its text pinned to the top, so
   the space just moved from around the block to inside each card. The real
   cause of the original emptiness was the type scale, fixed on :root. */
.inner > .bento{align-content:center}
.cell{
  background:var(--card);border:1px solid var(--cardEdge);border-radius:7px;
  padding:clamp(16px,1.8vw,26px);box-shadow:var(--shadow);
  display:flex;flex-direction:column;gap:clamp(9px,1.2vh,14px);
  /* min-width:0 lets a grid child actually shrink; without it long words and
     wide tables push the cell past its column and collide with the next one */
  min-width:0;overflow-wrap:break-word;
}
.cell > *{min-width:0;max-width:100%}
.cell.flat{background:none;box-shadow:none;border-color:var(--line)}
.cell.bare{background:none;box-shadow:none;border:none;padding:0}
.cell.mark{border-left:3px solid var(--select)}
.cell.hot{border-left:3px solid var(--red)}
.cell.warmb{border-left:3px solid var(--yellow)}
.cell.pad0{padding:0;overflow:hidden}
.c3{grid-column:span 3}.c4{grid-column:span 4}.c5{grid-column:span 5}
.c6{grid-column:span 6}.c7{grid-column:span 7}.c8{grid-column:span 8}
.c9{grid-column:span 9}.c12{grid-column:span 12}
@media (max-width:900px){
  .c3,.c4,.c5,.c6,.c7,.c8,.c9{grid-column:span 12}
  .slide{padding-top:58px}
}

/* inline bar plots -- one hue, light to dark, no status colours */
.plot{display:flex;flex-direction:column;gap:6px;margin:2px 0 4px}
.bars{display:flex;align-items:flex-end;gap:10px;height:clamp(54px,7vh,84px)}
/* NOTE the class names. These were .bar / .fill and collided with the chrome's
   .bar -- the fixed top and bottom navigation bars. The plot rule set flex and
   height but not POSITION, so position:fixed;left:0;right:0;z-index:40 leaked
   in and every plot bar became a full-viewport block painted over the deck.
   Prefixed names make that collision impossible. */
.bars .pbar{flex:1;height:100%;display:flex;align-items:flex-end;min-width:0}
.bars .pfill{width:100%;background:var(--select);border-radius:3px 3px 0 0;display:block}
.bars .pfill.soft{opacity:.55}
.bars .pfill.ghost{background:var(--front);opacity:.20}
/* the number in the third cell stands where the other two have bars, so all
   three visuals share a baseline and the row reads as one rhythm */
.statslot{height:clamp(54px,7vh,84px);display:flex;align-items:flex-end}
.statslot .stat{line-height:0.9}
.blabels{display:flex;gap:10px}
.blabels span{flex:1;min-width:0;text-align:center;font-size:0.62rem;line-height:1.3;color:var(--dim)}
.blabels b{color:var(--front);font-weight:bold}
.claim{font-size:0.95rem;line-height:1.45;margin:0}
.src{font-size:0.68rem;line-height:1.35;color:var(--dim);margin:auto 0 0}

/* stat */
.stat{font-size:2.45rem;line-height:1;font-weight:bold;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.stat.sm{font-size:1.62rem}
.label{font-size:0.66rem;letter-spacing:.13em;text-transform:uppercase;color:var(--dim)}

/* step icons: inline SVG so they take the accent from currentColor, stay
   sharp at any projector size, and cost nothing to load */
.stepicon{
  width:clamp(36px,4.6vh,48px);height:clamp(36px,4.6vh,48px);
  display:block;color:var(--select);flex:none;
  /* the cell is a flex column, so align-self is what centres it; a margin
     would fight the cell's own gap */
  align-self:center;
}

/* .mark paints a whole cell in the accent. On the step cards that is too much
   green at once, so keep the accent on the heading and return the body copy to
   normal ink; .hl spans inside still highlight because they set colour directly. */
.steps .cell.mark{color:var(--front);font-weight:normal}
.steps .cell.mark h3{color:var(--select)}

/* media */
.shot{position:relative;border-radius:7px;overflow:hidden;background:#000;line-height:0}
.shot img{width:100%;height:100%;object-fit:cover;display:block}
.shot .cap{
  position:absolute;left:0;right:0;bottom:0;padding:10px 12px;
  background:linear-gradient(transparent,#000c);color:#fff;font-size:0.74rem;line-height:1.35;
}
figure{margin:0}
figure img{width:100%;display:block;border-radius:7px;border:1px solid var(--cardEdge)}
.only-night{display:none}
@media (prefers-color-scheme:dark){
  :root:where(:not([data-theme="light"])) .only-night{display:block}
  :root:where(:not([data-theme="light"])) .only-day{display:none}
}
:root[data-theme="night"] .only-night{display:block}
:root[data-theme="night"] .only-day{display:none}

/* table */
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:7px}
table{border-collapse:collapse;width:100%;font-size:0.79rem;min-width:30rem}
th,td{padding:8px 11px;text-align:left;border-bottom:1px solid var(--line2);white-space:nowrap}
thead th{font-size:0.62rem;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);font-weight:normal}
tbody tr:last-child td{border-bottom:none}
td.n{text-align:right;font-variant-numeric:tabular-nums}
tr.hero td{background:color-mix(in srgb,var(--select) 12%,transparent);font-weight:bold}

/* comparison matrix -- built to be READ ACROSS, not word by word.
   Every cell gets a status square, so the pattern down a column is visible
   before any of the text is. */
.mx{font-size:0.82rem;table-layout:fixed}
.mx th,.mx td{white-space:normal;vertical-align:top;padding:11px 12px;line-height:1.35}
.mx thead th{font-size:0.64rem;letter-spacing:.09em;padding-bottom:9px}
.mx th.rh{
  text-align:left;font-weight:normal;color:var(--dim);
  font-size:0.63rem;letter-spacing:.09em;text-transform:uppercase;width:9rem;
}
.mx col.us{width:14rem}
.mx .k{
  display:inline-block;width:9px;height:9px;border-radius:2px;
  margin-right:8px;vertical-align:1px;flex:none;
}
.k.ok{background:var(--select)}
.k.mid{background:var(--yellow)}
.k.no{background:var(--red)}
.mx tbody td:last-child{background:color-mix(in srgb,var(--select) 7%,transparent)}
.mx tbody tr:last-child td{background:color-mix(in srgb,var(--front) 4%,transparent)}
.mx tbody tr:last-child td:last-child{background:color-mix(in srgb,var(--select) 10%,transparent)}
.mx thead th:last-child{color:var(--select)}
.mxkey{display:flex;gap:16px;flex-wrap:wrap;font-size:0.66rem;color:var(--dim);margin-top:10px}
.mxkey span{display:flex;align-items:center}

/* lists */
ul.clean{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
/* A hanging indent, NOT a grid. As a two-column grid every inline element
   inside the item became its own grid item -- so "text <b>x</b> text" was
   three items wrapping onto extra rows, which is why a bolded phrase jumped
   to its own line. Absolute positioning keeps the marker put and leaves the
   item's content in normal inline flow. */
ul.clean li{
  position:relative;padding-left:18px;
  font-size:0.84rem;line-height:1.45;overflow-wrap:break-word;
}
ul.clean li::before{
  content:"";position:absolute;left:0;top:0.52em;
  width:7px;height:7px;background:var(--select);border-radius:2px;
}
ul.clean li.no::before{background:var(--red)}
ul.clean li.warnb::before{background:var(--yellow)}

/* placeholder for assets not yet supplied */
.slot{
  border:1px dashed var(--line);border-radius:7px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:6px;color:var(--dim);
  text-align:center;padding:22px;min-height:150px;
}
.slot .ic{font-size:22px;color:var(--select)}

canvas{display:block;width:100%;height:100%}
.canvasbox{position:relative;width:100%;min-height:190px;flex:1;min-width:0;overflow:hidden}
.cover ul.clean li{font-size:0.95rem;line-height:1.5}
.cover ul.clean li::before{top:0.55em}

/* cover -- the fire runs full bleed behind everything, and a scrim keeps the
   copy on solid ground. The scrim is built from --bg, so it works in either
   theme without the fire needing to know which one is active. */
.slide.hero{padding:0}
.bgfire{position:absolute;inset:0;width:100%;height:100%;z-index:0;opacity:.85}
/* Embers read brighter against a dark ground, so night can carry more of them.
   Declared in BOTH dark scopes: the media query covers the OS setting, the
   data-theme scope covers the toggle. */
@media (prefers-color-scheme:dark){
  :root:where(:not([data-theme="light"])) .bgfire{opacity:.92}
}
:root[data-theme="night"] .bgfire{opacity:.92}

/* Only a bottom fade now. Legibility is carried by the frosted panel below,
   which lets the copy sit OVER the plume instead of beside it. */
.scrim{
  position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(to top, var(--bg) 0%,
             color-mix(in srgb, var(--bg) 45%, transparent) 16%, transparent 40%);
}
.slide.hero .inner{
  position:relative;z-index:2;
  padding:clamp(52px,7vh,72px) clamp(18px,4vw,54px) clamp(44px,6vh,60px);
  justify-content:center;
}
.herocopy{
  max-width:min(88ch,92%);
  padding:clamp(26px,3.2vh,40px) clamp(28px,3.2vw,48px);
  border-radius:10px;
  border:1px solid var(--cardEdge);
  background:color-mix(in srgb, var(--bg) 70%, transparent);
  /* frosted, so the plume stays visible through the copy rather than being
     masked out behind it */
  backdrop-filter:blur(20px) saturate(1.15);
  -webkit-backdrop-filter:blur(20px) saturate(1.15);
  box-shadow:var(--shadow);
}
@supports not (backdrop-filter:blur(1px)){
  /* no blur available: fall back to a more opaque panel so text stays legible */
  .herocopy{background:color-mix(in srgb, var(--bg) 92%, transparent)}
}
@media (max-width:900px){
  .herocopy{max-width:100%}
}

/* old two-column cover */
.cover{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(24px,4vw,60px);align-items:center}
@media (max-width:900px){.cover{grid-template-columns:1fr}.cover .art{display:none}}
.hero ul.clean li{font-size:0.95rem;line-height:1.5}
.hero ul.clean li::before{top:0.55em}
.rule{height:1px;background:var(--line);margin:20px 0}

/* appendix divider slide */
.big-center{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:14px;min-height:60vh}

/* help overlay */
.help{
  position:fixed;inset:0;background:color-mix(in srgb,var(--bg) 92%,transparent);
  z-index:60;display:none;align-items:center;justify-content:center;
}
.help.on{display:flex}
.help .box{background:var(--card);border:1px solid var(--cardEdge);border-radius:7px;padding:26px 30px;box-shadow:var(--shadow);max-width:34rem}
kbd{border:1px solid var(--line);border-radius:2px;padding:1px 6px;font-size:12px;background:var(--bg)}
"""
