SLIDES = r"""
<!-- 1 COVER -->
<section class="slide"><div class="inner">
 <div class="cover">
  <div>
   <p class="eyebrow anim">Resilient America Preparedness Challenge &middot; Track A</p>
   <h1 class="anim">Nobody is<br>watching the<br><span class="hl">thousandth camera.</span></h1>
   <p class="lead anim">America has built a nervous system for wildfire and forgotten
   to build the brain. We built the brain &mdash; small enough to run on a $50 board,
   at the tower, with the network down.</p>
   <div class="rule anim"></div>
   <p class="tiny anim"><span class="mark">&#8251;</span> <b>Kernwerk</b> &nbsp;&mdash;&nbsp;
   confidential edge AI, built small and sealed shut &nbsp;&middot;&nbsp;
   <span class="dim">press <kbd>&rarr;</kbd> to advance, <kbd>?</kbd> for keys</span></p>
  </div>
  <div class="art anim"><div class="canvasbox" style="min-height:300px"><canvas data-anim="bearing"></canvas></div></div>
 </div>
</div></section>

<!-- 2 PROBLEM -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">01 &middot; the problem</p>
 <h2 class="anim">Wildfire cameras don't have a detection problem.<br>They have an <span class="bad">interruption</span> problem.</h2>
 <div class="bento anim" style="margin-top:8px">
  <div class="cell c4 mark"><span class="label">deployed today</span>
   <span class="stat">1,000+</span><p class="tiny">AI cameras watching California alone.
   The network works. It sees fires.</p></div>
  <div class="cell c4 hot"><span class="label">and therefore</span>
   <span class="stat bad">~1,000</span><p class="tiny">false alarms every day, network-wide.
   Cloud. Fog. Dust. Steam off a geothermal plant.</p></div>
  <div class="cell c4 warmb"><span class="label">resolved by</span>
   <span class="stat warn">a person</span><p class="tiny">looking at each one. The same way it
   was done in 1935, just with more screens.</p></div>
  <div class="cell c12 flat"><p style="margin:0">Operators had to teach the software, by hand, to
  ignore the steam from the Geysers field. <b>The confirmation step is a human being</b> &mdash;
  and that human is the part of the system you cannot buy more of.</p></div>
 </div>
</div></section>

<!-- 3 WHAT THE CAMERA SEES -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">02 &middot; why it is hard</p>
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
 <p class="eyebrow anim">03 &middot; the trap</p>
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

<!-- 5 THE IDEA -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">04 &middot; the idea</p>
 <h2 class="anim">Stop treating cameras as alarms.<br>Treat them as <span class="hl">nerve endings</span>.</h2>
 <div class="bento anim">
  <div class="cell c5"><span class="label">a single nerve ending</span>
   <p style="margin:6px 0 0">is not trusted on its own. It is <b>weak, noisy, and constantly
   wrong</b>. Your brain does not act on one. It waits for the signal to persist, and for
   other nerves to agree.</p></div>
  <div class="cell c7 mark"><span class="label">so each camera sends</span>
   <div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap">
     <span class="stat hl">16 bytes</span>
     <span class="tiny" style="max-width:28ch">not a video stream. A twitch: <em>&ldquo;something,
     this direction, this confident.&rdquo;</em></span>
   </div>
   <p class="tiny" style="margin:8px 0 0">Small enough to cross LoRa, satellite, or a dying
   cellular link. Video cannot. When the network fails, the thinking carries on locally.</p></div>
  <div class="cell c6 flat"><h3><span class="hl">Layer 1</span> &mdash; at the camera</h3>
   <p class="tiny" style="margin:0">Integrates over <b>time</b>. &ldquo;Is this plume still there,
   or did it flicker once?&rdquo;</p></div>
  <div class="cell c6 flat"><h3><span class="hl">Layer 2</span> &mdash; on the board</h3>
   <p class="tiny" style="margin:0">Integrates over <b>space</b>. &ldquo;Do towers looking from
   different angles agree on a place?&rdquo;</p></div>
 </div>
</div></section>

<!-- 6 STATEWIDE END TO END -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">05 &middot; end to end</p>
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
 <p class="eyebrow anim">06 &middot; layer one</p>
 <h2 class="anim">Patience, in one number.</h2>
 <div class="bento anim">
  <div class="cell c7 pad0" style="padding:14px 6px 6px">
    <div class="canvasbox" style="min-height:250px"><canvas data-anim="lif"></canvas></div></div>
  <div class="cell c5"><p>Each camera keeps a single running number: <b>how much evidence
  have I seen lately?</b></p>
  <p>Every detection pushes it up. It <b class="hl">leaks away</b> constantly, so old evidence
  fades on its own.</p>
  <p>A flicker &mdash; a bird, a glint, one bad frame &mdash; never builds. A real plume keeps
  pushing, and the number climbs until it crosses a line.</p>
  <p class="tiny" style="margin-top:auto"><b>Why it matters:</b> this alone is the step that
  published work credits with cutting false alarms from 52% to 4%. It costs 8 bytes of memory.</p></div>
 </div>
</div></section>

<!-- 7 LAYER 2 ANIMATED -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">07 &middot; layer two</p>
 <h2 class="anim">One tower gives you a direction.<br>Two give you a <span class="hl">place</span>.</h2>
 <div class="bento anim">
  <div class="cell c5"><p>A camera cannot tell how <em>far</em> away smoke is &mdash; distance is
  genuinely ambiguous in a single image. But it knows the <b>direction</b> well.</p>
  <p>So the board spreads each report along that direction, as a wedge of possibility.
  Where wedges from different towers <b class="hl">overlap</b>, evidence piles up.</p>
  <p>A dust plume in front of one camera cannot be confirmed from a different angle.
  A real fire can.</p>
  <p class="tiny" style="margin-top:auto">Nothing here calculates an intersection. The overlaps
  simply add up, and the strongest point wins.</p></div>
  <div class="cell c7 pad0" style="padding:10px">
    <div class="canvasbox" style="min-height:290px"><canvas data-anim="bearing"></canvas></div></div>
 </div>
</div></section>

<!-- 8 OSBORNE -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">08 &middot; precedent</p>
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
 <p class="eyebrow anim">09 &middot; the hard case</p>
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
 <p class="eyebrow anim">10 &middot; after the alert</p>
 <h2 class="anim">The alert isn't the end. It's a question.</h2>
 <div class="bento anim">
  <div class="cell c12 flat"><p style="margin:0">How strong the evidence is decides how much it is
  worth spending to check. <b class="hl">Cheap look first, expensive look only if needed.</b></p></div>
  <div class="cell c4 mark"><span class="label">tier 1 &middot; seconds</span><h3>Point a camera at it</h3>
   <p class="tiny">The towers already pan and zoom. Slew the nearest one to the bearing, zoom in,
   run the detector on the close-up. Free, instant, legal, uses hardware already bolted to the pole.</p></div>
  <div class="cell c4 warmb"><span class="label">tier 2 &middot; ~20 minutes</span><h3>Send a drone</h3>
   <p class="tiny">Only when the camera cannot settle it &mdash; a ridge in the way, out of range,
   darkness. Dispatched automatically, before any fire is confirmed and before aircraft fly.</p></div>
  <div class="cell c4 hot"><span class="label">tier 3</span><h3>Send people</h3>
   <p class="tiny">Once something is confirmed. By this point a human is being handed a location
   and a photograph, not a shrug.</p></div>
  <div class="cell c7"><h3>And it remembers the answer</h3>
   <p class="tiny" style="margin:0">Whatever comes back is fed into the grid. &ldquo;Nothing there&rdquo;
   raises the bar <em>at that spot</em> above whatever just triggered it &mdash; so a steam vent goes
   quiet, while the hillside next to it stays as sensitive as ever.</p></div>
  <div class="cell c5 flat"><h3 class="warn">The detail that matters</h3>
   <p class="tiny" style="margin:0">Drones near confirmed fires <b>ground firefighting aircraft</b>.
   So ours is recalled automatically the moment a fire is confirmed or a flight restriction is
   issued. It checks, then gets out of the way.</p></div>
 </div>
</div></section>

<!-- 11 RESULTS -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">11 &middot; does it work</p>
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
 <p class="eyebrow anim">12 &middot; the nuisance test</p>
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
 <p class="eyebrow anim">13 &middot; the hardware</p>
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

<!-- 14 NOT A REPLACEMENT -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">14 &middot; where we fit</p>
 <h2 class="anim">Satellites own <span class="hl">everywhere</span>.<br>We own the <span class="hl">first ten minutes</span>.</h2>
 <div class="bento anim">
  <div class="cell c12 mark"><p style="margin:0;font-size:1.04rem">Nothing watches the whole planet at once.
  A geostationary satellite stares continuously but at 2 km pixels, and cannot see a fire until it is
  already burning hard. A polar orbiter sees small fires beautifully &mdash; twice a day, as it passes.
  <b>Continuous-and-coarse, or fine-and-occasional: you cannot currently buy both.</b>
  <b class="hl">Ground cameras are the earliest practical signal in the first minutes after ignition</b>,
  which is exactly the window in which a fire is still cheap to stop.</p></div>

  <div class="cell c12 pad0"><div class="tw"><table class="mx">
   <colgroup><col style="width:9rem"><col><col><col><col class="us"></colgroup>
   <thead><tr>
     <th>&nbsp;</th><th>Human lookout</th><th>Satellite</th>
     <th>Cameras alone</th><th>Cameras + us</th></tr></thead>
   <tbody>
    <tr><th class="rh">time to alert</th>
      <td><i class="k mid"></i>5&ndash;15 min, if facing it</td>
      <td><i class="k no"></i>minutes to hours</td>
      <td><i class="k ok"></i>5&ndash;10 min</td>
      <td><i class="k ok"></i>5&ndash;10 min, corroborated</td></tr>
    <tr><th class="rh">gap between looks</th>
      <td><i class="k mid"></i>none, while awake</td>
      <td><i class="k no"></i>2&times;/day &rarr; 20 min at best</td>
      <td><i class="k ok"></i>none &mdash; it watches</td>
      <td><i class="k ok"></i>none &mdash; it watches</td></tr>
    <tr><th class="rh">sees under cloud</th>
      <td><i class="k mid"></i>below the deck only</td>
      <td><i class="k no"></i>no &mdash; masked out</td>
      <td><i class="k ok"></i>yes &mdash; looks sideways</td>
      <td><i class="k ok"></i>yes</td></tr>
    <tr><th class="rh">reaches a crew</th>
      <td><i class="k ok"></i>a radio call</td>
      <td><i class="k no"></i>1&ndash;3 h, via an agency</td>
      <td><i class="k mid"></i>a control room</td>
      <td><i class="k ok"></i>decided at the tower</td></tr>
    <tr><th class="rh">where it works</th>
      <td><i class="k no"></i>one horizon</td>
      <td><i class="k ok"></i>everywhere &mdash; eventually</td>
      <td><i class="k mid"></i>20 km, line of sight</td>
      <td><i class="k mid"></i>20 km, line of sight</td></tr>
    <tr><th class="rh">blind spot</th>
      <td><i class="k no"></i>fatigue, night, few left</td>
      <td><i class="k no"></i>the revisit gap</td>
      <td><i class="k no"></i>1,000 false alarms a day</td>
      <td><i class="k mid"></i>the cameras' coverage gaps</td></tr>
   </tbody></table></div>
   <div class="mxkey">
     <span><i class="k ok"></i>strength</span>
     <span><i class="k mid"></i>partial</span>
     <span><i class="k no"></i>weakness</span>
     <span class="dim">&mdash; every column has all three. Detail in appendix A6.</span>
   </div></div>

  <div class="cell c4 mark"><h3 class="hl">What only we do</h3>
   <p class="tiny" style="margin:0">Turn a layer that is <em>too noisy to staff</em> into one a dispatcher can
   act on &mdash; <b>4.4&times; fewer false alarms at the same detection rate</b>, with a location attached.</p></div>
  <div class="cell c4 flat"><h3>What only satellites do</h3>
   <p class="tiny" style="margin:0">Find the fire nobody has a camera pointed at, and map a perimeter once it
   is burning. <b>We cannot see past a ridgeline. They can.</b> Our failure modes are different from theirs,
   which is the whole reason to run both.</p></div>
  <div class="cell c4 flat"><h3>What only people do</h3>
   <p class="tiny" style="margin:0">Decide. We do not remove the watchstander &mdash; their attention is the
   scarcest thing in the system, and we stop spending it on cloud and dust.</p></div>
 </div>
</div></section>

<!-- 15 MANY SENSORS -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">15 &middot; what comes next</p>
 <h2 class="anim">Cameras are the first sensor.<br>But they don't all join the <span class="hl">same way</span>.</h2>
 <div class="bento anim">
  <div class="cell c12 mark"><p style="margin:0;font-size:1.03rem">A new sensor answers one of three
  different questions, and each enters the network by a different door.
  <b class="hl">All three doors already exist in the code</b> &mdash; they are the three calls the integrator
  exposes. Adding a modality is a projection function, not a redesign.</p></div>

  <div class="cell c4 mark"><span class="label">door 1 &middot; ember_grid_inject()</span>
   <h3>&ldquo;Is something burning there?&rdquo;</h3>
   <p class="tiny" style="margin:0"><b>Evidence.</b> Votes into the membrane. Needs a location or a bearing,
   a class and a confidence.</p>
   <ul class="clean" style="margin-top:8px">
    <li><b>Cameras</b> &mdash; today. The plume at 5&ndash;10 min, from 20 km.</li>
    <li><b>People / 911</b> &mdash; a report is a sensor reading with a location on it. The oldest one, still
    among the best.</li>
    <li class="warnb"><b>Gas &amp; particle sensors</b> &mdash; read the small print, right.</li>
   </ul></div>

  <div class="cell c4 flat"><span class="label">door 2 &middot; ember_grid_prior()</span>
   <h3>&ldquo;Should I be more suspicious here?&rdquo;</h3>
   <p class="tiny" style="margin:0"><b>A prior.</b> Not evidence &mdash; nothing is burning yet. It lowers the
   threshold in one place for a while.</p>
   <ul class="clean" style="margin-top:8px">
    <li><b>Lightning strike feeds</b> &mdash; NLDN geolocates strikes by radio timing from the ground,
    GOES-GLM optically from orbit. A <em>subscription</em>, not hardware you deploy. A strike can smoulder for
    days before it shows. 44% of western fires, <b>71% of the area burned</b>.</li>
    <li><b>Fire weather &amp; fuel moisture</b> &mdash; already built. The global version of the same idea.</li>
   </ul>
   <p class="tiny hl" style="margin:8px 0 0"><b>A prior alone never raises an alert.</b> Suspicion is not
   detection &mdash; and that is a test in the suite, not a good intention.</p></div>

  <div class="cell c4 flat"><span class="label">door 3 &middot; ember_grid_confirm()</span>
   <h3>&ldquo;Was that one real?&rdquo;</h3>
   <p class="tiny" style="margin:0"><b>Confirmation.</b> Arrives after the alert and teaches the grid.</p>
   <ul class="clean" style="margin-top:8px">
    <li><b>Camera slew + zoom</b> &mdash; today. Seconds, free.</li>
    <li><b>Satellite hotspots</b> &mdash; <b class="hl">this is where they belong</b>, not at the input. Heat
    lags smoke and delivery runs 1&ndash;3 h, so by the time a hotspot appears the cameras have long since
    alerted. But as a confirmer it is <em>free</em> &mdash; no asset to dispatch &mdash; and physically
    uncorrelated with a camera. Cheapest tier in the broker: check it before spending a drone.</li>
    <li><b>Drone, then crew</b> &mdash; minutes, then people.</li>
   </ul></div>

  <div class="cell c7 warmb"><h3 class="warn">The small print on gas sensors</h3>
   <p class="tiny" style="margin:0">They detect a smouldering fire <em>before there is a flame</em> &mdash;
   genuinely earlier than anything optical. But the detection radius is <b>80&ndash;100 m</b>, and the
   recommended density is <b>0.7 sensors per hectare</b> in dense wildland-urban interface. Covering the
   40&nbsp;&times;&nbsp;40 km region we simulate would need roughly <b>110,000 of them, against 8 cameras.</b>
   So they are not a coverage layer and we will not pretend otherwise &mdash; they are <b>asset
   protection</b>: the edge of a town, a substation corridor, a campground. Tiny footprint, very high
   confidence, and a strong vote in the few cells they can see.</p></div>

  <div class="cell c5 hot"><h3 class="bad">Why any of this helps</h3>
   <p class="tiny" style="margin:0">Coincidence gain rewards agreement between <b>independent</b> sources
   &mdash; and two cameras are not fully independent, since the same dust plume fools both.
   <b class="hl">A camera, a gas sensor and a lightning-primed cell cannot be fooled by the same thing.</b>
   Nothing physically couples their failure modes. Each modality added makes every existing alert harder
   to fake.</p></div>
 </div>
</div></section>

<!-- 14 HONEST -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">16 &middot; what we don't claim</p>
 <h2 class="anim">Three things we could have hidden.</h2>
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
  <div class="cell c12 mark"><p style="margin:0">We are also careful about the neuroscience. A single
  one of these cells is, honestly, a weighted average with a threshold &mdash; and we say so.
  <b class="hl">The contribution is the network</b>: agreement across angles, the surround
  subtraction, and the memory of past mistakes.</p></div>
 </div>
</div></section>

<!-- 15 CLOSE -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">17 &middot; where this goes</p>
 <h2 class="anim">The core is built, measured, and already runs on the chip.</h2>
 <div class="bento anim">
  <div class="cell c3 mark"><span class="stat sm hl">44</span><span class="label">tests passing</span></div>
  <div class="cell c3 mark"><span class="stat sm hl">116 KB</span><span class="label">memory, fixed</span></div>
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
   <p class="tiny">for a 64&times;64 grid, inside the STM32U585's 786&nbsp;KB, statically sized</p></div>
  <div class="cell c4 flat"><span class="label">update</span><span class="stat sm">56 &micro;s</span>
   <p class="tiny">per tick on the development host, 4,096 cells</p></div>
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
    <tr><td>Ground camera network</td><td class="n">&mdash;</td><td class="n">continuous</td><td>smoke</td>
        <td>line of sight only; ~1 false positive per camera per day</td></tr>
    <tr class="hero"><td>&hellip;with this integrator</td><td class="n">500 m cell</td>
        <td class="n">continuous</td><td>agreement between cameras</td>
        <td>adds no sensing range; removes ~4&times; the false alarms at equal detection</td></tr>
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
 <p class="eyebrow anim">A7 &middot; references</p>
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
