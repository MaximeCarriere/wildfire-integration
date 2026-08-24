SLIDES = r"""
<!-- 1 COVER -->
<section class="slide hero">
 <canvas class="bgfire" data-anim="fire"></canvas>
 <div class="scrim"></div>
 <div class="inner">
  <div class="herocopy">
   <p class="eyebrow anim">Resilient America Preparedness Challenge &middot; Track A</p>
   <h1 class="anim">Early wildfire detection:<br>the <span class="hl">integrator layer</span></h1>
   <ul class="clean anim" style="margin:0 0 6px;gap:11px">
    <li>America has built a nervous system for wildfire and forgotten to build the brain.</li>
    <li>A thousand cameras already watch the ridgelines. Nobody can afford to read what they report.</li>
    <li>We built the layer that turns them into one trustworthy, located alert.</li>
    <li>Small enough to run on an <b>Arduino UNO Q</b>, at the tower, with the network down.</li>
   </ul>
   <div class="rule anim"></div>
   <p class="tiny anim"><span class="mark">&#8251;</span> <b>Kernwerk</b> &nbsp;&mdash;&nbsp;
   confidential edge AI, built small and sealed shut &nbsp;&middot;&nbsp;
   <span class="dim">press <kbd>&rarr;</kbd> to advance, <kbd>?</kbd> for keys</span></p>
  </div>
 </div>
</section>

<!-- 1 STAKES -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">01 &middot; the problem</p>
 <h2 class="anim">More land burns, it costs more,<br>and the fires that matter are the ones caught <span class="hl">late</span>.</h2>
 <div class="bento anim">
  <div class="cell c4 hot"><span class="label">how much burns</span>
   <span class="stat bad">2&times;</span>
   <p class="tiny" style="margin:0">Human-caused warming <b>doubled the cumulative western-US forest
   fire area over 1984&ndash;2015</b>, and drove more than half the rise in fuel aridity since the
   1970s.</p>
   <p class="tiny dim" style="margin:6px 0 0">Abatzoglou &amp; Williams, <i>PNAS</i> 113(42):11770,
   2016. Western-US <em>forest</em> area, that window &mdash; not a pre-suppression baseline.</p></div>

  <div class="cell c4 warmb"><span class="label">what it costs</span>
   <span class="stat warn">$2.9 bn</span>
   <p class="tiny" style="margin:0">a year in federal suppression alone, averaged over the last decade
   and projected to rise <b>42% by 2050</b>. Counting health, property and disruption:
   <b>$394&ndash;893 bn</b> a year.</p>
   <p class="tiny dim" style="margin:6px 0 0">USDA Forest Service R&amp;D; US Joint Economic
   Committee, 2023.</p></div>

  <div class="cell c4 mark"><span class="label">where the leverage is</span>
   <span class="stat hl">initial<br>attack</span>
   <p class="tiny" style="margin:0">Almost every fire is stopped on first attack. Detecting a fire
   <b>while its behaviour is still benign</b> is what lets crews deploy in time to keep that success
   rate up.</p>
   <p class="tiny dim" style="margin:6px 0 0">ASME Open J. Eng., <i>A Review of Technologies for the
   Early Detection of Wildfires</i>, 2025.</p></div>

  <div class="cell c12 flat"><h3>But we will not overclaim this, because the evidence is mixed</h3>
   <p style="margin:0">The mechanism &mdash; earlier detection, higher initial-attack success &mdash; is
   well established in the fire-management literature. The <em>economic</em> effect of shaving reporting
   delay is not. Ba&#803;lek et&nbsp;al. (<i>PLOS ONE</i>, 2024) analysed Western Canadian fires
   2015&ndash;2020 and found <b>no evidence that fire size increases with reporting delay</b>; an hour
   saved buys about <b>0.25%</b> of suppression cost.
   <b class="hl">The value of detection is greatest where detection is currently poor</b> &mdash; and in
   a network already drowning in alerts, the binding problem is not speed. It is that nobody can read
   them. That is slide 02.</p></div>
 </div>
</div></section>

<!-- 2 PROBLEM -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">02 &middot; the obstacle</p>
 <h2 class="anim">America already built the sensors.<br>The alerts are <span class="bad">unusable</span> at scale.</h2>
 <div class="bento anim" style="margin-top:8px">
  <div class="cell c4 mark"><span class="label">deployed today</span>
   <span class="stat">1,000+</span><p class="tiny">AI cameras watching California alone.
   The network works. It sees fires.</p></div>
  <div class="cell c4 hot"><span class="label">and therefore</span>
   <span class="stat bad">~1,000</span><p class="tiny">false alarms every day, network-wide.
   Cloud. Fog. Dust. Steam off a geothermal plant.</p></div>
  <div class="cell c4 warmb"><span class="label">costing, every day</span>
   <span class="stat warn">33 hours</span><p class="tiny">of somebody's undivided attention &mdash;
   <b>more than four full shifts</b> &mdash; spent looking at cloud and dust. At two minutes a check.</p></div>
  <div class="cell c12 flat"><p style="margin:0">Every one of those is resolved the same way it was in
  1935: <b>a person looks.</b> Operators even had to teach the software, by hand, to ignore the steam
  off the Geysers field. <b class="hl">The confirmation step is a human being</b> &mdash; and that
  human is the one part of the system you cannot buy more of.</p></div>
 </div>
</div></section>

<!-- 3 WHAT THE CAMERA SEES -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">03 &middot; why it is hard</p>
 <h2 class="anim">This is what the camera actually sees.</h2>
 <div class="bento anim">
  <div class="cell c4 pad0"><div class="shot" style="aspect-ratio:16/9">
    <img src="__IMG_TINY__" alt="A wide hillside landscape with a very small smoke plume marked by a tiny box">
    <div class="cap">A real fire. The plume is <b>under 0.1%</b> of the frame.</div></div></div>
  <div class="cell c4 pad0"><div class="shot" style="aspect-ratio:16/9">
    <img src="__IMG_NIGHT__" alt="A near-black night frame with a small marked fire">
    <div class="cap">Night. Most of the frame is black.</div></div></div>
  <div class="cell c4 pad0"><div class="shot" style="aspect-ratio:16/9">
    <img src="__IMG_EMPTY__" alt="An empty hillside landscape with no fire">
    <div class="cap">Nothing at all &mdash; <b>47%</b> of frames.</div></div></div>
  <div class="cell c12 flat"><p style="margin:0">A detector good enough to catch the first
  picture will also fire on haze, on a dust plume off a road, on headlights, on a cloud
  shadow crossing a ridge. <b>Better models do not fix this.</b> Ambiguity is in the pixels.</p></div>
 </div>
 <p class="tiny anim" style="margin-top:10px">Frames: HPWREN / ALERTCalifornia tower network, from our own detector benchmark.</p>
</div></section>

<!-- 4 SCALING PARADOX -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">04 &middot; the trap</p>
 <h2 class="anim">Every camera you add makes the problem<br>better <em>and</em> worse.</h2>
 <div class="bento anim">
  <div class="cell c6 mark"><h3 class="hl">What scales</h3>
   <ul class="clean">
    <li>Coverage &mdash; more ridgelines watched</li>
    <li>Redundancy &mdash; a fire seen from two angles</li>
    <li>Speed &mdash; someone is always looking</li>
   </ul></div>
  <div class="cell c6 hot"><h3 class="bad">What doesn't</h3>
   <ul class="clean">
    <li class="no">The person confirming each alert</li>
    <li class="no">Their attention at 3&nbsp;a.m. on day nine of a siege</li>
    <li class="no">Their patience after the 200th cloud</li>
   </ul></div>
  <div class="cell c12"><p style="margin:0;font-size:1.05rem">So the fix cannot be a better camera
  or a better model. <b class="hl">It has to be a layer that sits above all of them</b> and decides,
  from many weak and unreliable signals, whether anything is really burning &mdash; and where.</p></div>
 </div>
</div></section>

<!-- WHO BENEFITS -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">05 &middot; who benefits</p>
 <h2 class="anim">The first beneficiary is the person<br>we stop <span class="hl">interrupting</span>.</h2>
 <div class="bento anim">
  <div class="cell c6 mark"><h3 class="hl">Dispatchers and watchstanders</h3>
   <p class="tiny" style="margin:0">They absorb the false-alarm load today. Their attention is the
   scarcest resource in the system, and it runs out exactly when it is needed most &mdash; on a
   red-flag day, when alarm volume peaks.</p></div>
  <div class="cell c6"><h3>Wildland-urban-interface communities</h3>
   <p class="tiny" style="margin:0">California, Oregon, Nevada, Colorado. The minutes between ignition
   and first response decide whether an incident stays a spot fire. Every false alarm cleared faster
   is attention available for the real one.</p></div>
  <div class="cell c6"><h3>Volunteer and small municipal departments</h3>
   <p class="tiny" style="margin:0">They cannot staff a 24-hour camera watch, so they are excluded from
   the benefit of networks their counties already pay for. A filtered, located alert is one they can
   actually act on.</p></div>
  <div class="cell c6"><h3>Tribal and remote land managers</h3>
   <p class="tiny" style="margin:0">Operating where backhaul is intermittent or absent. A system that
   needs the cloud to think stops thinking exactly when it is needed.</p></div>
  <div class="cell c12 flat"><p style="margin:0">And nobody is displaced. <b class="hl">We do not remove
  the watchstander</b> &mdash; we stop spending them on cloud and dust so they are still sharp for the
  alert that matters.</p></div>
 </div>
</div></section>

<!-- 5 THE IDEA -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">06 &middot; the idea</p>
 <h2 class="anim">Stop treating cameras as alarms.<br>Treat them as <span class="hl">nerve endings</span>.</h2>
 <div class="bento anim">
  <div class="cell c5"><p style="margin:0">A single nerve ending is <b>weak, noisy and often wrong</b>.
  Your brain never acts on one. It waits to see whether the signal persists, and whether other nerves
  agree.</p></div>
  <div class="cell c7 mark"><span class="label">so each camera sends</span>
   <div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap">
     <span class="stat hl">16 bytes</span>
     <span class="tiny" style="max-width:30ch">a twitch, not a video stream. Small enough for LoRa,
     satellite, or a dying cellular link.</span></div></div>

  <div class="cell c12 hot"><h3 class="bad">It never sends a picture</h3>
   <p class="mono" style="margin:0 0 8px;font-size:12px;letter-spacing:.04em;color:var(--dim)">
    94 10 05 00&nbsp; 29 00&nbsp; 00 00&nbsp; 02&nbsp; <b class="hl">02</b>&nbsp; cf&nbsp; 02&nbsp; 00 00&nbsp; b9 07</p>
   <p style="margin:0"><b>Camera 41, at 09:12, says <span class="hl">2</span>, four fifths sure.</b>
   1 means plume, 2 means fire &mdash; the whole vocabulary. <b class="hl">The camera decides <em>whether</em>;
   the board decides <em>where</em>.</b> Zero bytes of image leave the pole, so there is nothing to
   intercept, breach or subpoena, and no surveillance capability to misuse.</p></div>

  <div class="cell c6 flat"><h3><span class="hl">Layer 1</span> &mdash; at the camera</h3>
   <p class="tiny" style="margin:0">Integrates over <b>time</b>. &ldquo;Is this plume still there?&rdquo;</p></div>
  <div class="cell c6 flat"><h3><span class="hl">Layer 2</span> &mdash; on the board</h3>
   <p class="tiny" style="margin:0">Integrates over <b>space</b>. &ldquo;Do towers at different angles agree?&rdquo;</p></div>
  <div class="cell c12"><p style="margin:0;font-size:1.04rem">
   <b class="hl">Early detection</b> from cameras already on the ridge &nbsp;&rarr;&nbsp;
   <b class="hl">a drone confirms</b> before anyone is dispatched &nbsp;&rarr;&nbsp;
   <b class="hl">a dial for how paranoid to be</b>, set by the operator and by the fire weather.
   <span class="dim">No new towers. No new cameras. No images leaving the hillside.</span></p></div>
 </div>
</div></section>

<!-- 6 STATEWIDE END TO END -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">07 &middot; end to end</p>
 <h2 class="anim">One fire, from first wisp to a drone overhead.</h2>
 <div class="bento anim" style="flex:1;align-content:stretch">
  <div class="cell c8 pad0" style="padding:8px">
   <div class="canvasbox" style="min-height:min(58vh,460px)"><canvas data-anim="statewide"></canvas></div></div>
  <div class="cell c4 bare" style="gap:10px;justify-content:center">
   <div class="cell mark" style="box-shadow:none;padding:12px 14px">
     <span class="label">1 &middot; the network</span>
     <p class="tiny" style="margin:0">A thousand cameras, each one cheap, tireless and
     <b>individually unreliable</b>.</p></div>
   <div class="cell warmb" style="box-shadow:none;padding:12px 14px">
     <span class="label">2 &middot; the noise</span>
     <p class="tiny" style="margin:0">They flicker constantly. Dust, cloud, glare.
     <b>None of it reaches anyone.</b></p></div>
   <div class="cell hot" style="box-shadow:none;padding:12px 14px">
     <span class="label">3 &middot; the agreement</span>
     <p class="tiny" style="margin:0">Three neighbours report smoke, then fire, along
     sightlines that <b>cross at one place</b>.</p></div>
   <div class="cell mark" style="box-shadow:none;padding:12px 14px">
     <span class="label">4 &middot; the answer</span>
     <p class="tiny" style="margin:0">Threshold crossed &rarr; one alert with coordinates
     &rarr; <b>a drone goes and looks</b>.</p></div>
   <p class="tiny dim" style="margin:0">Runs in real time on the board at the tower &mdash;
   no cloud, no video leaving the hillside.</p>
  </div>
 </div>
</div></section>

<!-- 6 LAYER 1 ANIMATED -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">08 &middot; layer one</p>
 <h2 class="anim">Patience, in one number.</h2>
 <div class="bento anim">
  <div class="cell c8 pad0" style="padding:14px 6px 6px">
    <div class="canvasbox" style="min-height:min(52vh,360px)"><canvas data-anim="lif"></canvas></div></div>
  <div class="cell c4"><p>The integrator keeps a single running number: <b>how much evidence
  have I seen here lately?</b></p>
  <p>Every report pushes it up. It <b class="hl">leaks away</b> constantly, so old evidence
  fades on its own. A flicker never builds. A real plume keeps pushing, and the number climbs
  until it crosses the bar &mdash; and <b>crossing the bar is what sends the drone</b>.</p>
  <p><b class="hl">The bar moves.</b> An operator can raise it, or fire weather lowers it, and
  the same evidence then alerts sooner or later.</p>
  <p><b class="hl">And every place keeps its own.</b> A steam vent that has been investigated
  three times sits behind a higher bar; a cell where lightning struck two days ago sits behind
  a lower one. Same network, same evidence, different answer per place.</p>
  <p class="tiny" style="margin-top:auto"><b>Cost:</b> one 32-bit number per place. That is the
  whole reason this fits on a microcontroller.</p></div>
 </div>
</div></section>

<!-- 7 LAYER 2 ANIMATED -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">09 &middot; layer two</p>
 <h2 class="anim">One tower gives you a direction.<br>Two give you a <span class="hl">place</span>.</h2>
 <div class="bento anim">
  <div class="cell c5"><p>A camera cannot tell how <em>far</em> away smoke is &mdash; distance is
  genuinely ambiguous in a single image. What it has is a <b>rough direction</b>.</p>
  <p>So the board spreads each report out as a <b>wedge of possibility</b> &mdash; and if the
  direction is unknown, simply as a <b class="hl">20 km disc</b> around the camera. Where the
  shapes from different towers <b class="hl">overlap</b>, evidence piles up.</p>
  <p>A dust plume in front of one camera cannot be corroborated from somewhere else. A real
  fire can.</p>
  <p class="tiny" style="margin-top:auto">Nothing here calculates an intersection. The overlaps
  simply add up, and the strongest point wins &mdash; which is why the same code works whether
  the shape is a hairline or a circle.</p></div>
  <div class="cell c7 pad0" style="padding:10px">
    <div class="canvasbox" style="min-height:290px"><canvas data-anim="bearing"></canvas></div></div>
 </div>
</div></section>

<!-- 8 OSBORNE -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">10 &middot; precedent</p>
 <h2 class="anim">This is a 1911 idea, done in silicon.</h2>
 <div class="bento anim">
  <div class="cell c7"><p style="font-size:1.06rem">For most of the last century, fires were found
  by people sitting in towers with a brass instrument called an <b>Osborne Firefinder</b> &mdash;
  a sighting ring over a map.</p>
  <p>A lookout sighted the smoke and phoned in a <em>bearing</em>. Alone it was almost useless.
  But a second tower phoned in a second bearing, someone drew both lines on a map, and where
  they crossed, that was the fire.</p>
  <p><b class="hl">We are rebuilding that, with a thousand tireless lookouts</b> whose lines are
  drawn and crossed automatically, sixty times a minute.</p></div>
  <div class="cell c5 mark"><span class="label">what changed</span>
   <ul class="clean" style="margin-top:6px">
    <li>The lookouts never sleep or blink</li>
    <li>Every one is a little unreliable &mdash; so agreement matters more, not less</li>
    <li>The map is a grid of cells, and each cell keeps its own running score</li>
   </ul>
   <p class="tiny" style="margin-top:auto">The old system's weakness was too few observers.
   Ours is too many signals. Same instrument, opposite problem.</p></div>
 </div>
</div></section>

<!-- 9 HAZE / SURROUND -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">11 &middot; the hard case</p>
 <h2 class="anim">Agreement alone would make things <span class="bad">worse</span>.</h2>
 <div class="bento anim">
  <div class="cell c5"><p>Here is the trap. If you simply reward agreement, then a marine layer
  rolling in &mdash; which <b>every</b> tower sees at once &mdash; looks like the most confirmed
  fire in history.</p>
  <p>The fix comes from the eye. A retina does not measure brightness; it measures how much a
  spot <b class="hl">stands out from its surroundings</b>. That is why you can read this in
  sunlight and in a dim room.</p>
  <p>So each cell subtracts its own neighbourhood. Haze lifts a cell <em>and</em> its
  neighbourhood equally, and cancels. A fire is a sharp peak, and survives.</p></div>
  <div class="cell c7 pad0" style="padding:14px 6px 6px">
    <div class="canvasbox" style="min-height:250px"><canvas data-anim="surround"></canvas></div></div>
  <div class="cell c12 flat"><p class="tiny" style="margin:0"><b>We measured this.</b> With the
  subtraction removed, the <em>edge of a haze bank</em> alone scored higher than a genuine
  two-camera fire. With it in place, a fire burning <em>inside</em> 50% haze is detected just as
  fast as one on a clear day.</p></div>
 </div>
</div></section>

<!-- 10 CONFIRMATION -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">12 &middot; after the alert</p>
 <h2 class="anim">The alert isn't the end. It's a question.</h2>
 <div class="bento anim">
  <div class="cell c12 flat"><p style="margin:0">How strong the evidence is decides how much it is worth
  spending to check. <b class="hl">Cheap look first; expensive look only if needed.</b></p></div>

  <div class="cell c4 mark"><span class="label">tier 1 &middot; seconds</span><h3>Point a camera at it</h3>
   <p class="tiny" style="margin:0">The towers already pan and zoom. Slew the nearest, zoom, re-run the
   detector on the close-up. Free, instant, uses hardware already on the pole.</p></div>
  <div class="cell c4 warmb"><span class="label">tier 2 &middot; ~20 minutes</span><h3>Send a drone</h3>
   <p class="tiny" style="margin:0">Only when the camera cannot settle it &mdash; a ridge in the way,
   out of range, darkness.</p></div>
  <div class="cell c4 hot"><span class="label">tier 3</span><h3>Send people</h3>
   <p class="tiny" style="margin:0">Once confirmed. By now a human is handed a location and a
   photograph, not a shrug.</p></div>

  <div class="cell c7"><h3>And it remembers the answer</h3>
   <p class="tiny" style="margin:0">&ldquo;Nothing there&rdquo; raises the bar <em>at that spot</em> above
   whatever just triggered it. A steam vent goes quiet; the hillside beside it stays as sensitive as ever.</p></div>
  <div class="cell c5 flat"><h3 class="warn">The detail that matters</h3>
   <p class="tiny" style="margin:0">Drones near confirmed fires <b>ground firefighting aircraft</b>. Ours is
   recalled automatically the moment a fire is confirmed or a flight restriction issued.</p></div>
 </div>
</div></section>

<!-- 11 RESULTS -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">13 &middot; does it work</p>
 <h2 class="anim">Eight simulated days. Same cameras, same evidence, four ways of reading it.</h2>
 <div class="bento anim">
  <div class="cell c7 pad0" style="padding:12px">
   <figure><img class="only-day" src="__IMG_PARETO__" alt="Chart: false alerts per day against fires detected. Our curve sits below and left of the alternatives.">
   <img class="only-night" src="__IMG_PARETO_N__" alt="Chart: false alerts per day against fires detected. Our curve sits below and left of the alternatives."></figure></div>
  <div class="cell c5 mark"><span class="label">at the same 96% detection rate</span>
   <span class="stat hl">4.4&times;</span>
   <p style="margin:4px 0 0">fewer false alarms than the classical method of crossing bearings
   &mdash; <b>47 a day instead of 208</b>.</p>
   <p class="tiny" style="margin-top:10px">And at a more sensitive setting it beats that method on
   <em>both</em> counts at once: fewer false alarms <b>and</b> catches more fires.</p>
   <p class="tiny">Lower and further left is better. Every point is eight independent 24-hour
   scenarios.</p></div>
 </div>
</div></section>

<!-- 12 STEAM VENT -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">14 &middot; the nuisance test</p>
 <h2 class="anim">A steam vent that two towers can see, running for six hours.</h2>
 <div class="bento anim">
  <div class="cell c3 hot"><span class="label">raw detections</span><span class="stat bad">2,700</span>
   <p class="tiny">what the cameras actually fired on</p></div>
  <div class="cell c3 mark"><span class="label">alerts raised</span><span class="stat hl">12</span>
   <p class="tiny">what a person was asked to look at</p></div>
  <div class="cell c6"><h3>It learns the vent, not the landscape</h3>
   <p class="tiny" style="margin:0">Each time the check comes back &ldquo;nothing there&rdquo;, the
   bar rises at <em>that spot</em>. After a couple of rounds it settles to about two checks an hour
   &mdash; deliberately re-testing now and then, in case something really does start there.</p></div>
  <div class="cell c12 flat"><p style="margin:0;font-size:1.05rem">Then we lit a real fire
  <b>12&nbsp;km away</b> on the same grid, after six hours of that suppression.
  <b class="hl">Detected immediately, at full strength.</b> The system had learned one stubborn
  chimney &mdash; it had not gone blind.</p></div>
 </div>
</div></section>

<!-- 13 HARDWARE -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">15 &middot; the hardware</p>
 <h2 class="anim">Two brains, and we use both for what they're for.</h2>
 <div class="bento anim">
  <div class="cell c5 pad0" id="unoq-slot">
   <div class="slot" style="min-height:200px"><span class="ic">&#8251;</span>
    <b>Arduino UNO Q</b><span class="tiny">photo slot &mdash; send me the file path<br>and I'll drop it in here</span></div></div>
  <div class="cell c7"><div class="bento" style="gap:10px">
    <div class="cell c12 mark" style="box-shadow:none"><span class="label">the small brain &middot; STM32U585</span>
     <p class="tiny" style="margin:0">Always on, always predictable, sips power. It runs the
     integrator &mdash; whole-number arithmetic only, no floating point, memory fixed at
     <b>116&nbsp;KB</b> and never allocated at runtime. It cannot stall or surprise you.</p></div>
    <div class="cell c12 flat" style="box-shadow:none"><span class="label">the big brain &middot; Dragonwing QRB2210</span>
     <p class="tiny" style="margin:0">Full Linux. Takes in radio traffic, runs the vision model on
     the zoomed-in confirmation shot, talks to dispatch. Sleeps the rest of the time.</p></div>
  </div></div>
  <div class="cell c12 flat"><p class="tiny" style="margin:0">Most entries will treat this board as
  a small Linux computer and leave the second brain idle. <b>The split is the point:</b> the part
  that must never miss anything runs on the part that never gets busy. The towers' viewing
  geometry is worked out once on the Linux side and handed over as a lookup table, so the
  real-time core never computes an angle.</p></div>
 </div>
</div></section>

<!-- WHY EDGE -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">16 &middot; why the edge, not the cloud</p>
 <h2 class="anim">Three reasons. Only one is <span class="hl">bandwidth</span>.</h2>
 <div class="bento anim">
  <div class="cell c4 mark"><span class="label">1 &middot; survivability</span>
   <h3>Fire destroys comms</h3>
   <p class="tiny" style="margin:0">When the uplink fails, an edge integrator keeps reasoning on
   whatever still arrives. A cloud service simply stops &mdash; and it stops during the event it
   exists for. <b class="hl">The decision is made at the tower, in microseconds.</b></p></div>
  <div class="cell c4 flat"><span class="label">2 &middot; privacy</span>
   <h3>Nothing to leak</h3>
   <p class="tiny" style="margin:0">The detector runs on the pole and the image dies there. A cloud
   design would have to ship frames, creating a surveillance capability, a breach surface and a
   subpoena target where none need exist.</p></div>
  <div class="cell c4 flat"><span class="label">3 &middot; reach</span>
   <h3>Where there is no link</h3>
   <p class="tiny" style="margin:0">Nine bytes crosses LoRa or satellite IoT. Video cannot. This puts a
   sensor on a ridge that could never have supported a stream &mdash; which is most of the country
   that burns.</p></div>
  <div class="cell c12 hot"><p style="margin:0"><b>And a reason we will not claim.</b> It is not about
  latency. The cloud round-trip is milliseconds; a fire develops over minutes.
  <b class="hl">Anyone arguing edge-for-latency here is arguing badly</b> &mdash; the honest case is
  that the link is unreliable, the imagery is sensitive, and half the ground has no link at all.</p></div>
 </div>
</div></section>

<!-- 14 NOT A REPLACEMENT -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">17 &middot; where we fit</p>
 <h2 class="anim">Satellites own <span class="hl">everywhere</span>.<br>We own the <span class="hl">first ten minutes</span>.</h2>
 <div class="bento anim">
  <div class="cell c12 mark"><p style="margin:0;font-size:1.04rem">Nothing watches the whole planet at
  once. <b>Continuous-and-coarse, or fine-and-occasional &mdash; you cannot currently buy both.</b>
  <b class="hl">Ground cameras are the earliest practical signal in the first minutes after
  ignition</b>, which is exactly when a fire is still cheap to stop.</p></div>

  <div class="cell c12 pad0"><div class="tw"><table class="mx">
   <colgroup><col style="width:10rem"><col><col><col class="us"></colgroup>
   <thead><tr>
     <th>&nbsp;</th><th>Human lookout</th><th>Satellite</th>
     <th>Cameras + integrator</th></tr></thead>
   <tbody>
    <tr><th class="rh">time to alert</th>
      <td><i class="k mid"></i>5&ndash;15 min, if they happen to be facing it</td>
      <td><i class="k no"></i>minutes to hours &mdash; the fire must first grow hot</td>
      <td><i class="k ok"></i>5&ndash;10 min, corroborated by two towers</td></tr>
    <tr><th class="rh">gap between looks</th>
      <td><i class="k mid"></i>none, while awake</td>
      <td><i class="k no"></i>twice a day today; 20 min at best, later this decade</td>
      <td><i class="k ok"></i>none &mdash; it watches, it does not sample</td></tr>
    <tr><th class="rh">sees under cloud</th>
      <td><i class="k mid"></i>only below the deck</td>
      <td><i class="k no"></i>no &mdash; thick cloud is masked out entirely</td>
      <td><i class="k ok"></i>yes &mdash; it looks sideways, beneath it</td></tr>
    <tr><th class="rh">reaches a crew</th>
      <td><i class="k ok"></i>a radio call</td>
      <td><i class="k no"></i>1&ndash;3 h through an agency; under a minute only near four antennas</td>
      <td><i class="k ok"></i>decided at the tower, in microseconds</td></tr>
    <tr><th class="rh">where it works</th>
      <td><i class="k no"></i>one horizon per tower</td>
      <td><i class="k ok"></i>everywhere on Earth &mdash; eventually, not at once</td>
      <td><i class="k mid"></i>line of sight, about 20 km</td></tr>
    <tr><th class="rh">blind spot</th>
      <td><i class="k no"></i>fatigue, darkness, and almost none remain</td>
      <td><i class="k no"></i>the gap between passes, and heat arrives after smoke</td>
      <td><i class="k mid"></i>cannot see past a ridgeline</td></tr>
   </tbody></table></div>
   <div class="mxkey">
     <span><i class="k ok"></i>strength</span>
     <span><i class="k mid"></i>partial</span>
     <span><i class="k no"></i>weakness</span>
     <span class="dim">&mdash; every column carries all three. Detail in appendix A6.</span>
   </div></div>

  <div class="cell c4 mark"><h3 class="hl">Only we</h3>
   <p class="tiny" style="margin:0">Turn a layer <em>too noisy to staff</em> into one a dispatcher can act
   on: <b>4.4&times; fewer false alarms at the same detection rate</b>, with a location attached.</p></div>
  <div class="cell c4 flat"><h3>Only satellites</h3>
   <p class="tiny" style="margin:0">Find the fire nobody has a camera pointed at, and map a perimeter once
   it burns. <b>We cannot see past a ridgeline. They can.</b></p></div>
  <div class="cell c4 flat"><h3>Only people</h3>
   <p class="tiny" style="margin:0">Decide. We do not remove the watchstander &mdash; we stop spending them
   on cloud and dust.</p></div>
 </div>
</div></section>

<!-- 14 HONEST -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">18 &middot; what we don't claim</p>
 <h2 class="anim">Four things we could have hidden.</h2>
 <div class="bento anim">
  <div class="cell c4 warmb"><h3>A simpler method logs fewer alarms</h3>
   <p class="tiny">Counting how many cameras agree, ignoring geometry, gives 30 a day to our 47.
   <b>But it produces no location</b> &mdash; you are told something is burning somewhere.
   Ours arrives with coordinates. That is a difference in kind, not a score we can win.</p></div>
  <div class="cell c4 warmb"><h3>Our aim is coarser</h3>
   <p class="tiny">We place fires to about <b>650&nbsp;m</b>; the classical calculation manages
   <b>343&nbsp;m</b>. We round to 500&nbsp;m squares. Halving the square halves the error and
   quadruples the memory &mdash; a dial, not a wall.</p></div>
  <div class="cell c4 warmb"><h3>One case we cannot solve</h3>
   <p class="tiny">A controlled burn, or smoke drifting in from a fire outside the region, is
   <b>geometrically identical to an ignition</b>. No amount of cleverness in the maths fixes that.
   Only going and looking does.</p></div>
  <div class="cell c12 hot"><h3 class="bad">The fourth, and the largest: we cannot claim fewer acres</h3>
   <p style="margin:0">Ba&#803;lek et&nbsp;al. (PLOS ONE, 2024) found <b>no evidence that fire size
   increases with reporting delay</b> across Western Canada 2015&ndash;2020, and that detection
   investment is not justified on suppression-cost savings alone. Their setting is remote boreal fire,
   many of them monitored rather than fought, and they measure suppression cost rather than evacuation
   lead time or property loss &mdash; but it is good evidence and it points away from us.
   <b class="hl">We therefore claim an operational result, not an outcome one:</b> 4.4&times; fewer
   things a human must look at. Whether that converts into fewer acres is unproven, and we have not
   tried to prove it.</p></div>
  <div class="cell c12 mark"><p style="margin:0">We are also careful about the neuroscience. A single
  one of these cells is, honestly, a weighted average with a threshold &mdash; and we say so.
  <b class="hl">The contribution is the network</b>: agreement across angles, the surround
  subtraction, and the memory of past mistakes.</p></div>
 </div>
</div></section>

<!-- BUILDING IN THE OPEN -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">19 &middot; building in the open</p>
 <h2 class="anim">We are not promising to.<br>We already <span class="hl">are</span>.</h2>
 <div class="bento anim">
  <div class="cell c6 mark"><h3 class="hl">Already public</h3>
   <ul class="clean" style="margin-top:6px">
    <li>Apache-2.0 from the first commit &mdash; deliberately permissive, and kept separate from the
    AGPL detector by a process boundary</li>
    <li>The simulator is public too, <b>so anyone can attack our numbers with our own tools</b></li>
    <li>Every figure regenerates with one command</li>
   </ul></div>
  <div class="cell c6 hot"><h3 class="bad">Including the mistakes</h3>
   <p class="tiny" style="margin:0 0 6px">An appendix of this deck is titled <em>&ldquo;four things the
   measurements forced us to fix&rdquo;</em>. It documents a normalisation scheme that masked real fires,
   an adaptation rule that did nothing, and a rate-coding bug of our own making.</p>
   <p class="tiny" style="margin:0"><b class="hl">Negative results get published at the same volume as
   positive ones.</b> A build log that only contains successes is marketing.</p></div>
  <div class="cell c12 flat"><h3>Through Stage Two</h3>
   <div class="bento" style="gap:10px">
    <div class="cell c4 bare"><span class="label">build notes</span>
     <p class="tiny" style="margin:0">At each milestone: what was tried, what the measurement said,
     what changed as a result.</p></div>
    <div class="cell c4 bare"><span class="label">hardware files</span>
     <p class="tiny" style="margin:0">Wiring, radio choice and node build published alongside the
     firmware, so the prototype is reproducible and not just watchable.</p></div>
    <div class="cell c4 bare"><span class="label">adaptation guidance</span>
     <p class="tiny" style="margin:0">A written account of how to retarget it &mdash; the thresholds
     are deployment-specific, and saying so is more useful than shipping ours.</p></div>
   </div></div>
 </div>
</div></section>

<!-- 15 CLOSE -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">20 &middot; where this goes</p>
 <h2 class="anim">The core is built, measured, and already runs on the chip.</h2>
 <div class="bento anim">
  <div class="cell c3 mark"><span class="stat sm hl">53</span><span class="label">tests passing</span></div>
  <div class="cell c3 mark"><span class="stat sm hl">116 KB</span><span class="label">map memory, fixed</span></div>
  <div class="cell c3 mark"><span class="stat sm hl">56 &micro;s</span><span class="label">per update</span></div>
  <div class="cell c3 mark"><span class="stat sm hl">0</span><span class="label">floating point ops</span></div>
  <div class="cell c7"><h3>Why we are not waiting for the board</h3>
   <p class="tiny" style="margin:0">Because the maths uses whole numbers only, the code gives
   <b>bit-for-bit identical answers</b> on a laptop and on the microcontroller. A fingerprint test
   proves the chip version is correct <em>before the kit ships in September</em> &mdash; which
   removes the biggest schedule risk in any hardware contest. It already compiles clean for the
   target chip today.</p></div>
  <div class="cell c5 flat"><h3>Stage Two</h3>
   <ul class="clean">
    <li>3&ndash;4 physical camera nodes over LoRa</li>
    <li>Alert firing on the board itself</li>
    <li>Camera slew-to-confirm closing the loop</li>
   </ul>
   <p class="tiny" style="margin:6px 0 0">The ingest layer is already built for this shape.
   Stage Two is assembly, not a rewrite.</p></div>
  <div class="cell c12"><p style="margin:0;font-size:1.05rem"><span class="mark">&#8251;</span>
   <b>Kernwerk</b> &mdash; <span class="dim">confidential edge AI, built small and sealed shut.</span>
   &nbsp; <span class="hl">Press <kbd>A</kbd> for the technical appendix.</span></p></div>
 </div>
</div></section>

<!-- INDEX -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">coverage</p>
 <h2 class="anim">The six things a proposal must answer.</h2>
 <div class="bento anim">
  <div class="cell c6 mark"><span class="label">1 &middot; the problem, and who it affects</span>
   <p class="tiny" style="margin:0">Warming has doubled the western-US forest area that burns &mdash;
   and a thousand cameras whose alerts nobody can afford to read.
   <span class="dim">&rarr; 01&ndash;04</span></p></div>
  <div class="cell c6 mark"><span class="label">2 &middot; who benefits</span>
   <p class="tiny" style="margin:0">Dispatchers first, then everyone downstream of a faster first
   response. <span class="dim">&rarr; 05</span></p></div>
  <div class="cell c6 flat"><span class="label">3 &middot; technical approach, hardware, edge AI</span>
   <p class="tiny" style="margin:0">A two-layer spiking network on the Arduino UNO Q, fed by a
   detector that never leaves the pole. <span class="dim">&rarr; 06&ndash;12, 15</span></p></div>
  <div class="cell c6 flat"><span class="label">4 &middot; why it must be the edge, not the cloud</span>
   <p class="tiny" style="margin:0">Three reasons, only one of which is bandwidth.
   <span class="dim">&rarr; 16</span></p></div>
  <div class="cell c6 flat"><span class="label">5 &middot; building in the open</span>
   <p class="tiny" style="margin:0">Already public, already reproducible, mistakes included.
   <span class="dim">&rarr; 19</span></p></div>
  <div class="cell c6 warmb"><span class="label">6 &middot; an honest read on feasibility</span>
   <p class="tiny" style="margin:0">What is built and measured, and what could still sink it.
   <span class="dim">&rarr; 13, 14, 18, 20</span></p></div>
  <div class="cell c12"><p style="margin:0"><b>No code is required at this stage.</b> We wrote it
  anyway &mdash; not as the deliverable, but because it is the only way to answer question six with
  numbers instead of intentions.</p></div>
 </div>
</div></section>

<!-- ===== APPENDIX ===== -->
<section class="slide"><div class="inner"><div class="big-center">
 <p class="eyebrow anim" style="justify-content:center">appendix</p>
 <h1 class="anim" style="max-width:22ch">The parts we left out of the story.</h1>
 <p class="lead anim" style="text-align:center">Mechanisms, method, baselines, and the four things
 the measurements forced us to change.</p>
</div></div></section>

<section class="slide"><div class="inner">
 <p class="eyebrow anim">A1 &middot; the four mechanisms</p>
 <h2 class="anim">What each cell actually computes.</h2>
 <div class="bento anim">
  <div class="cell c6"><h3>1 &middot; Coincidence gain</h3><p class="tiny" style="margin:0">Each cell
  tracks <em>which</em> cameras contributed, as a bitmask, inside a rolling window. Current from N
  <b>distinct</b> cameras is superlinear (&asymp;1, 2.5, 4). The dominant false-positive modes are
  single-camera, so this is where most of the rejection comes from.</p></div>
  <div class="cell c6"><h3>2 &middot; Lateral coupling</h3><p class="tiny" style="margin:0">A discrete
  Laplacian, not a plain neighbour sum. A plain sum injects energy every tick and a uniform field
  runs away; the Laplacian spreads a peak while leaving a flat field untouched. Absorbs bearing
  error, so two crossing wedges reinforce without inventing evidence.</p></div>
  <div class="cell c6"><h3>3 &middot; Center-surround + divisive gain</h3><p class="tiny" style="margin:0">
  <code>response = (V &minus; surround) / (1 + k&middot;surround)</code>. Subtraction removes the
  background; division makes the system progressively more conservative as the scene hazes over
  without ever zeroing its sensitivity. Surround is a separable box blur &mdash; two running-sum
  passes, no per-cell division.</p></div>
  <div class="cell c6"><h3>4 &middot; Adaptation</h3><p class="tiny" style="margin:0">A rejection raises
  the local threshold <em>above the response that caused the false alarm</em>, scaled to the actual
  stimulus rather than a fixed step, applied across a disc rather than a single cell. Decays with a
  time constant of about an hour.</p></div>
  <div class="cell c12 flat"><p class="tiny" style="margin:0"><b>Threshold:</b>
  <code>&theta; = &theta;<sub>base</sub> &times; preset &times; fire-weather + local adaptation</code>.
  Presets are Normal / Elevated / Red Flag at 1.00 / 0.85 / 0.70.</p></div>
 </div>
</div></section>

<section class="slide"><div class="inner">
 <p class="eyebrow anim">A2 &middot; method</p>
 <h2 class="anim">How the numbers were produced.</h2>
 <div class="bento anim">
  <div class="cell c6 mark"><h3>Grounded, not invented</h3>
   <ul class="clean">
    <li>Detector accuracy taken from our own benchmarked result: <b>0.778 mAP50</b>, YOLOv5s @512px
    on D-Fire, measured on a Jetson Orin Nano</li>
    <li>Nuisance rates tuned so that after per-camera confirmation each camera reports
    <b>&asymp;1 false positive per day</b> &mdash; the published ALERTCalifornia figure</li>
    <li>The simulator drives the <b>real firmware code</b> through a C binding, so these numbers and
    the shipped firmware cannot drift apart</li>
   </ul></div>
  <div class="cell c6"><h3>Three families of false positive</h3>
   <ul class="clean">
    <li>Single-camera nuisances &mdash; road dust, lens glint, a cloud shadow crossing one view</li>
    <li>A persistent fixed source &mdash; geothermal steam, an industrial stack</li>
    <li class="warnb"><b>Correlated regional events</b> &mdash; marine layer, distant smoke drift,
    seen by every tower at once across a 40&ndash;90&deg; arc</li>
   </ul>
   <p class="tiny" style="margin:6px 0 0">Every method receives the identical detector stream and
   the identical confirmation budget &mdash; one dispatch per alert, same verdict accuracy.</p></div>
 </div>
</div></section>

<section class="slide"><div class="inner">
 <p class="eyebrow anim">A3 &middot; baselines</p>
 <h2 class="anim">What we compared against, and the full table.</h2>
 <div class="tw anim"><table>
  <thead><tr><th>Method</th><th>False alerts/day</th><th>Detected</th><th>Latency</th><th>Localises</th></tr></thead>
  <tbody>
   <tr><td>Raw detector output</td><td class="n">29,820</td><td class="n">100%</td><td class="n">0 min</td><td class="bad">no</td></tr>
   <tr><td>Per-camera temporal only</td><td class="n">143</td><td class="n">100%</td><td class="n">11 min</td><td class="bad">no</td></tr>
   <tr><td>M-of-N vote</td><td class="n">30</td><td class="n">100%</td><td class="n">11 min</td><td class="bad">no</td></tr>
   <tr><td>Cross-bearing triangulation</td><td class="n">208</td><td class="n">96%</td><td class="n">12 min</td><td class="n">343 m</td></tr>
   <tr class="hero"><td>This work, &theta;=5</td><td class="n">113</td><td class="n">100%</td><td class="n">12 min</td><td class="n">674 m</td></tr>
   <tr class="hero"><td>This work, &theta;=8</td><td class="n">47</td><td class="n">96%</td><td class="n">13 min</td><td class="n">680 m</td></tr>
   <tr class="hero"><td>This work, &theta;=13</td><td class="n">6</td><td class="n">83%</td><td class="n">16 min</td><td class="n">630 m</td></tr>
  </tbody></table></div>
 <p class="tiny anim" style="margin-top:12px"><b>Cross-bearing triangulation</b> is the serious
 competitor: intersect the bearing rays, cluster the intersections, reject near-parallel pairs
 (geometric dilution of precision), and require several towers to support a cluster before
 alerting. It is what an engineer would actually build. A location-less vote is not a fair
 comparator for a system whose entire output is a location.</p>
</div></section>

<section class="slide"><div class="inner">
 <p class="eyebrow anim">A4 &middot; engineering</p>
 <h2 class="anim">Why the chip version is already trustworthy.</h2>
 <div class="bento anim">
  <div class="cell c6 mark"><h3>No floating point, no library, no allocator</h3>
   <p class="tiny" style="margin:0">Everything is Q16.16 fixed point. The leak is an arithmetic
   shift, so it is exact on every target. The core depends on <code>&lt;stdint.h&gt;</code> alone
   &mdash; not even a C library &mdash; and cross-compiles clean for Cortex-M33 (thumbv8m.main,
   freestanding, <code>-Werror</code>) today.</p></div>
  <div class="cell c6"><h3>The fingerprint test</h3>
   <p class="tiny" style="margin:0">A fixed scenario is run and every spike plus the whole final
   state is hashed. Host and target must produce the <b>same hash</b>. It survived two invasive
   refactors unchanged &mdash; removing the C library and moving the surround maths to 32-bit
   &mdash; which is exactly the property doing its job.</p></div>
  <div class="cell c4 flat"><span class="label">state</span><span class="stat sm">116 KB</span>
   <p class="tiny">a 64&times;64 <b>map</b> of 500 m ground cells &mdash; 4,096 of them, 29 bytes each.
   No pixels: there is no image buffer on the board at all.</p></div>
  <div class="cell c4 flat"><span class="label">update</span><span class="stat sm">56 &micro;s</span>
   <p class="tiny">per tick on the development host, across all 4,096 ground cells</p></div>
  <div class="cell c4 flat"><span class="label">wire record</span><span class="stat sm">16 B</span>
   <p class="tiny">CRC-16 protected; a corrupt event is dropped, never guessed</p></div>
 </div>
</div></section>

<section class="slide"><div class="inner">
 <p class="eyebrow anim">A5 &middot; what changed</p>
 <h2 class="anim">Four things the measurements forced us to fix.</h2>
 <div class="bento anim">
  <div class="cell c6 hot"><h3>Global normalisation was dangerous</h3>
   <p class="tiny" style="margin:0">The first design divided every cell by total grid activity. It
   killed haze correctly &mdash; and <b>masked a real fire burning inside 10% haze entirely</b>.
   A miss is far worse than a false alarm. Replaced with center-surround, which is what the retina
   actually does.</p></div>
  <div class="cell c6 hot"><h3>A fixed adaptation step did nothing</h3>
   <p class="tiny" style="margin:0">Raising a threshold by a constant cannot suppress a source
   scoring three times that. Adaptation now scales to the magnitude of the stimulus that fired.</p></div>
  <div class="cell c6 hot"><h3>Suppressing one cell was useless</h3>
   <p class="tiny" style="margin:0">Non-maximum suppression simply promoted the neighbouring cell,
   and the same vent re-alerted from next door. A verdict is about a <em>place</em>, so it now
   applies across a disc.</p></div>
  <div class="cell c6 hot"><h3>We wrote &ldquo;low rate&rdquo; and sent every tick</h3>
   <p class="tiny" style="margin:0">The weak tier was documented as a low spike rate, then emitted
   continuously &mdash; eight times the current the core was tuned for. Implementing the rate coding
   properly roughly halved the false alarms.</p></div>
  <div class="cell c12 flat"><p class="tiny" style="margin:0">Each of these is now a regression test.
  The suite fails if a fire inside haze is ever masked again.</p></div>
 </div>
</div></section>

<section class="slide"><div class="inner">
 <p class="eyebrow anim">A6 &middot; the sensing layers</p>
 <h2 class="anim">The numbers behind the comparison.</h2>
 <div class="bento anim">
  <div class="cell c12 pad0"><div class="tw"><table>
   <thead><tr><th>System</th><th>Resolution</th><th>Revisit</th><th>Detects</th><th>Practical floor</th></tr></thead>
   <tbody>
    <tr><td>GOES-16/18 ABI</td><td class="n">2 km</td><td class="n">5&ndash;15 min</td><td>heat</td>
        <td>struggles below ~34.5 MW radiative power &mdash; an already-established fire</td></tr>
    <tr><td>VIIRS (S-NPP, NOAA-20/21)</td><td class="n">375 m</td><td class="n">~2&times; per day</td><td>heat</td>
        <td>better resolution, but long gaps between passes</td></tr>
    <tr><td>FireSat (Earth Fire Alliance)</td><td class="n">5 m</td>
        <td class="n">2&times;/day today</td><td>heat, multispectral IR</td>
        <td>first three operational satellites launched 7 July 2026; hourly revisit targeted for 2029, 20 min at the full 50-satellite constellation</td></tr>
    <tr class="hero"><td>Ground cameras + integrator</td><td class="n">500 m ground cell</td>
        <td class="n">continuous</td><td>smoke, and agreement between cameras</td>
        <td>line of sight only. Raw cameras give ~1 false positive per camera per day; the integrator
        removes ~4&times; of them at equal detection</td></tr>
   </tbody></table></div></div>
  <div class="cell c12 flat"><h3>Two limits that are easy to miss</h3>
   <p class="tiny" style="margin:0 0 6px"><b>Delivery.</b> NASA FIRMS near-real-time products arrive
   <b>1&ndash;3 hours</b> after overpass. An ultra-real-time path exists at <b>under 60 s</b>
   (MODIS ~25 s, VIIRS ~50 s) &mdash; but only through direct-broadcast antennas, of which there are four:
   Madison &times;2, Hampton, Mayag&uuml;ez. Outside their footprint, hours. URT is a quick look and is
   replaced by NRT after six hours. Delivery is to an agency by subscription or API, not to a crew.</p>
   <p class="tiny" style="margin:0"><b>Cloud.</b> Thermal infrared does not penetrate thick cloud &mdash; it is
   masked out of the product entirely, and thin cloud or heavy smoke <em>depresses</em> the measured fire
   intensity, which can drop a real fire below the detection threshold. Cloud also generates false positives.
   A tower camera looks horizontally, beneath the deck. Fog at camera level blinds it in turn &mdash; the point
   is not that cameras are immune, but that <b>the two failure modes are uncorrelated</b>.</p></div>
  <div class="cell c7"><h3>Why smoke beats heat for <em>early</em> detection</h3>
   <p class="tiny" style="margin:0">A plume is visible well before the fire radiates enough energy to
   register from orbit. That is the window ground cameras own, and it is the window in which a fire is
   still cheap to stop. Satellites own everything after that &mdash; and everywhere no camera looks.</p></div>
  <div class="cell c5 flat"><h3>Honest note</h3>
   <p class="tiny" style="margin:0">FireSat is very good and getting better fast. If hourly global
   revisit at 5 m arrives on schedule, the early-detection gap narrows. It does not close: a satellite
   passing hourly still cannot watch a ridge continuously, and our layer costs no new hardware in orbit.</p></div>
 </div>
</div></section>

<section class="slide"><div class="inner">
 <p class="eyebrow anim">A7 &middot; does it need a direction?</p>
 <h2 class="anim">No. It just costs you.</h2>
 <div class="bento anim">
  <div class="cell c12 flat"><p style="margin:0">A PTZ tower knows its pan angle, so a bearing is usually
  available &mdash; but not always, and a gas sensor, a 911 call or a utility fault have
  <b>no direction at all</b>. Each geometry below is tuned to its <em>own</em> best threshold: comparing
  them at one threshold only reports which geometry that threshold was chosen for. Eight scenarios each,
  the same as the headline table.</p></div>
  <div class="cell c12 pad0"><div class="tw"><table>
   <thead><tr><th>what the sensor reports</th><th>shape on the map</th><th>false alerts/day</th>
   <th>detected</th><th>location error</th></tr></thead>
   <tbody>
    <tr class="hero"><td>bearing to &plusmn;2&deg;</td><td>a hairline wedge</td><td class="n">113</td>
      <td class="n">100%</td><td class="n">674 m</td></tr>
    <tr><td>bearing to &plusmn;10&deg; <span class="dim">(a camera's field of view)</span></td>
      <td>a fat wedge</td><td class="n">201</td><td class="n">88%</td><td class="n">1,121 m</td></tr>
    <tr><td>bearing to &plusmn;30&deg;</td><td>a quadrant</td><td class="n">756</td>
      <td class="n">88%</td><td class="n">1,292 m</td></tr>
    <tr><td><b>nothing but its GPS position</b></td><td><b>a 20 km disc</b></td>
      <td class="n">724</td><td class="n">83%</td><td class="n">1,279 m</td></tr>
   </tbody></table></div></div>
  <div class="cell c6 mark"><h3 class="hl">It works without a direction</h3>
   <p class="tiny" style="margin:0">83% of fires still found, still placed to about a kilometre.
   Overlapping discs concentrate evidence the same way overlapping wedges do &mdash; the code does
   not change, only the shape injected into it.</p></div>
  <div class="cell c6 warmb"><h3 class="warn">But direction is worth about 6&times;</h3>
   <p class="tiny" style="margin:0">113 false alerts a day against ~720, and 100% detection against 83%.
   The cliff sits between &plusmn;10&deg; and &plusmn;30&deg;, so the target is <b>ten degrees, not
   two</b> &mdash; which a pan encoder gives for free.</p></div>
  <div class="cell c12 flat"><p class="tiny" style="margin:0"><b>Why this matters beyond cameras:</b>
  supporting a bearing-less source is exactly what lets a gas sensor, a 911 call or a utility fault
  sensor join the same network. They are not a degraded fallback &mdash; they are points with a
  radius, which is the same maths.</p></div>

  <div class="cell c7 pad0"><div class="tw"><table>
   <thead><tr><th>towers</th><th>seen by &ge;3</th><th>ambiguity area</th><th>as a radius</th></tr></thead>
   <tbody>
    <tr><td class="n">4</td><td class="n">37%</td><td class="n">160 km&sup2;</td><td class="n">7,100 m</td></tr>
    <tr><td class="n">8</td><td class="n">100%</td><td class="n">48 km&sup2;</td><td class="n">3,900 m</td></tr>
    <tr><td class="n">16</td><td class="n">100%</td><td class="n">11 km&sup2;</td><td class="n">1,870 m</td></tr>
    <tr><td class="n">32</td><td class="n">100%</td><td class="n">3 km&sup2;</td><td class="n">1,020 m</td></tr>
   </tbody></table></div>
   <p class="tiny dim" style="margin:8px 0 0">Two places are indistinguishable if exactly the same
   cameras can see both. This is the resulting ambiguity, and it shrinks as towers are added
   &mdash; density beating precision, again.</p></div>

  <div class="cell c5 mark"><h3 class="hl">But the disc is not flat</h3>
   <p class="tiny" style="margin:0">At 8 towers the table says the fix cannot be tighter than
   <b>3,900 m</b>. The simulator measures <b class="hl">1,184 m</b> &mdash; three times better.</p>
   <p class="tiny" style="margin:8px 0 0">Because a report is not a hard-edged circle. Detection
   confidence falls off with range, so a cell near the camera scores higher than one at the rim.
   Overlapping discs therefore produce a <b>peak, not a plateau</b> &mdash; and that gradient quietly
   recovers the range information a set-intersection throws away.</p></div>
 </div>
</div></section>

<section class="slide"><div class="inner">
 <p class="eyebrow anim">A8 &middot; the radio, honestly</p>
 <h2 class="anim">The least-validated part of this design.</h2>
 <div class="bento anim">
  <div class="cell c12 warmb"><h3 class="warn">Where &ldquo;32 km&rdquo; came from: nowhere physical</h3>
   <p class="tiny" style="margin:0">A 64&times;64 map was chosen because a power of two suits the
   microcontroller, and 500 m cells because that was the localisation target. <b>32 km simply fell out
   of 64 &times; 500 m.</b> Cameras were then placed on a ring inside it with 20 km reach, which
   conveniently covers it. Nothing was derived from the radio, and it should not be quoted as though it
   were a deployment spec.</p></div>

  <div class="cell c6 pad0"><div class="tw"><table>
   <thead><tr><th>siting</th><th>radio horizon</th></tr></thead>
   <tbody>
    <tr><td>two 10 m masts, flat ground</td><td class="n">22.6 km</td></tr>
    <tr><td>two 30 m masts</td><td class="n">39.1 km</td></tr>
    <tr><td>30 m mast &rarr; 150 m ridge</td><td class="n">63.3 km</td></tr>
    <tr class="hero"><td>two mountaintop sites</td><td class="n">101 km</td></tr>
   </tbody></table></div>
   <p class="tiny dim" style="margin:8px 0 0">d &asymp; 3.57 &times; (&radic;h&#8321; + &radic;h&#8322;) km.
   Our worst link &mdash; corner to centre of the region &mdash; is 22.6 km.</p></div>

  <div class="cell c6 pad0"><div class="tw"><table>
   <thead><tr><th>distance</th><th>path loss</th><th>margin</th></tr></thead>
   <tbody>
    <tr><td class="n">10 km</td><td class="n">111.7 dB</td><td class="n">50 dB</td></tr>
    <tr class="hero"><td class="n">22.6 km</td><td class="n">118.8 dB</td><td class="n">43 dB</td></tr>
    <tr><td class="n">45 km</td><td class="n">124.7 dB</td><td class="n">37 dB</td></tr>
   </tbody></table></div>
   <p class="tiny dim" style="margin:8px 0 0">LoRa 915 MHz SF10: +20 dBm, 5 dBi each end,
   &minus;132 dBm sensitivity &rarr; 162 dB budget. <b>The binding constraint is line of sight, not
   power</b> &mdash; which is why siting on ridges matters more than any antenna.</p></div>

  <div class="cell c12 mark"><h3 class="hl">And most cameras are not on LoRa at all</h3>
   <div class="bento" style="gap:12px">
    <div class="cell c6 bare"><span class="label">case A &middot; existing networks</span>
     <p class="tiny" style="margin:0">ALERTCalifornia and its peers already run microwave, fibre or
     cellular backhaul to mountaintop sites <b>because they stream video</b>. Sixteen bytes is nothing on
     such a link. <b class="hl">Here the bandwidth argument is worth zero</b> &mdash; the value is the
     fusion, the privacy of not shipping frames, and continuing to decide when the backhaul drops.</p></div>
    <div class="cell c6 bare"><span class="label">case B &middot; new or remote sites</span>
     <p class="tiny" style="margin:0">Where there is no backhaul, a video camera is simply not an option.
     <b class="hl">This is where 9 bytes earns its keep</b> &mdash; it puts a sensor on a ridge that could
     never have supported a stream, over LoRa, LTE-M, NB-IoT or satellite IoT.</p></div>
   </div>
   <p class="tiny" style="margin:10px 0 0"><b>Note on the board:</b> the UNO Q has Wi-Fi 5 and Bluetooth
   5.1 &mdash; <b>no LoRa and no cellular</b>. Any wide-area link is an add-on radio, and that is a real
   line on the bill of materials.</p></div>

  <div class="cell c7 hot"><h3 class="bad">The five bytes that mattered</h3>
   <p class="tiny" style="margin:0">LoRaWAN US915 at <b>DR0</b> &mdash; the slowest, longest-reaching
   setting &mdash; caps the payload at <b>11 bytes</b>. Our 16-byte record missed it by five, so on the
   one setting where range matters most it could not be sent at all. Dropping the node timestamp (the
   gateway stamps arrival) and bit-packing the rest gives a <b class="hl">9-byte profile</b> that fits,
   with confidence quantised to 64 levels and the CRC intact. Implemented and tested.</p></div>
  <div class="cell c5 flat"><h3>What is still unproven</h3>
   <p class="tiny" style="margin:0">We have measured the fusion behaviour hard and taken the radio on
   faith. What is solid: the payload is small enough that <em>any</em> LPWAN carries it. What is not: a
   link budget for real terrain between real tower sites. That needs profiles, not arithmetic.</p></div>
 </div>
</div></section>

<section class="slide"><div class="inner">
 <p class="eyebrow anim">15 &middot; what comes next</p>
 <h2 class="anim">Cameras are the first sensor.<br>They don't all join the <span class="hl">same way</span>.</h2>
 <div class="bento anim">
  <div class="cell c12 mark"><p style="margin:0">A new sensor answers one of three questions, and each
  enters by a different door. <b class="hl">All three already exist in the code</b> &mdash; adding a
  modality is a projection function, not a redesign.</p></div>

  <div class="cell c4 mark"><span class="label">door 1 &middot; inject()</span>
   <h3>&ldquo;Is something burning there?&rdquo;</h3>
   <ul class="clean" style="margin-top:6px">
    <li><b>Cameras</b> &mdash; today</li>
    <li><b>911 calls</b> &mdash; a report is a reading with a location on it</li>
    <li class="warnb"><b>Gas sensors</b> &mdash; see below</li>
   </ul></div>

  <div class="cell c4 flat"><span class="label">door 2 &middot; prior()</span>
   <h3>&ldquo;Be more suspicious here&rdquo;</h3>
   <ul class="clean" style="margin-top:6px">
    <li><b>Lightning feeds</b> &mdash; a subscription, not hardware. 44% of western fires,
    <b>71% of the area burned</b></li>
    <li><b>Fire weather</b> &mdash; already built</li>
   </ul>
   <p class="tiny hl" style="margin:8px 0 0"><b>A prior alone never alerts.</b> Suspicion is not
   detection &mdash; and that is a test, not an intention.</p></div>

  <div class="cell c4 flat"><span class="label">door 3 &middot; confirm()</span>
   <h3>&ldquo;Was that one real?&rdquo;</h3>
   <ul class="clean" style="margin-top:6px">
    <li><b>Camera slew</b> &mdash; today. Seconds, free</li>
    <li><b>Satellites</b> &mdash; <b class="hl">here, not at the input</b>. Heat lags smoke, so a
    hotspot arrives long after the cameras. But it is free and uncorrelated: check it before
    spending a drone</li>
    <li><b>Drone, then crew</b></li>
   </ul></div>

  <div class="cell c6 warmb"><h3 class="warn">Gas sensors: read the small print</h3>
   <p class="tiny" style="margin:0">They catch a fire <em>before there is a flame</em> &mdash; but the
   radius is <b>80&ndash;100 m</b> at <b>0.7 per hectare</b>. Covering our region would take
   <b>110,000 of them against 8 cameras</b>. Not a coverage layer, and we will not pretend otherwise:
   they are <b>asset protection</b> for a town edge or a substation.</p></div>
  <div class="cell c6 hot"><h3 class="bad">Why it makes the network stronger</h3>
   <p class="tiny" style="margin:0">Coincidence gain rewards agreement between <b>independent</b>
   sources &mdash; and two cameras are not independent, since the same dust plume fools both.
   <b class="hl">A camera, a gas sensor and a lightning-primed cell cannot be.</b> Each modality added
   makes every existing alert harder to fake.</p></div>
 </div>
</div></section>

<section class="slide"><div class="inner">
 <p class="eyebrow anim">A9 &middot; references</p>
 <h2 class="anim">Sources, code, licence.</h2>
 <div class="bento anim">
  <div class="cell c6"><h3>Code</h3>
   <ul class="clean">
    <li><b>wild-fire-integrator</b> &mdash; this system. Apache-2.0.</li>
    <li><b>wildfire-detection</b> &mdash; the companion detector study on Jetson Orin Nano
    (D-Fire, TensorRT). AGPL-3.0 via YOLOv5.</li>
   </ul>
   <p class="tiny" style="margin:8px 0 0">The integrator reaches the detector across a
   <b>process boundary</b> rather than linking it, so both licences stay intact and the
   commercialisation path stays open.</p></div>
  <div class="cell c6"><h3>Figures cited</h3>
   <ul class="clean">
    <li>ALERTCalifornia: 1,000+ cameras, &ldquo;less than one false positive per day per camera&rdquo;</li>
    <li>Temporal confirmation reducing false-alarm rates from 52% to 4%</li>
    <li>Documented failure modes: cloud, fog, dust, geothermal and industrial steam</li>
    <li>Our own measurement: 0.778 mAP50, YOLOv5s @512px, D-Fire, Jetson Orin Nano</li>
   </ul></div>
  <div class="cell c12 mark"><p style="margin:0"><span class="mark">&#8251;</span> <b>Kernwerk</b>
   &mdash; <span class="dim">confidential edge AI, built small and sealed shut.</span></p></div>
 </div>
</div></section>
"""
