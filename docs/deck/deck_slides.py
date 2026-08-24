import re
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
    <li>The integrator is small enough to run on an <b>Arduino UNO Q</b>.</li>
   </ul>
   <div class="rule anim"></div>
   <p class="tiny anim"><span class="mark">&#8251;</span> <b>Kernwerk</b> &nbsp;&middot;&nbsp;
   confidential edge AI, built small and sealed shut &nbsp;&middot;&nbsp;
   <span class="dim">press <kbd>&rarr;</kbd> to advance, <kbd>?</kbd> for keys</span></p>
  </div>
 </div>
</section>

<!-- 1 STAKES -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">__N__ &middot; the problem</p>
 <h2 class="anim">More land burns, and it costs more.<br>Nearly all of it comes from the few fires that were <span class="hl">not caught in time</span>.</h2>
 <div class="bento anim" style="gap:clamp(14px,1.8vw,22px)">

  <div class="cell c4 mark">
   <span class="label">how much burns</span>
   <div class="plot">
    <div class="bars">
     <div class="pbar"><span class="pfill ghost" style="height:43%"></span></div>
     <div class="pbar"><span class="pfill soft" style="height:67%"></span></div>
     <div class="pbar"><span class="pfill" style="height:100%"></span></div>
    </div>
    <div class="blabels"><span>1990s avg<br>3.3 M</span><span>2025<br>5.1 M</span><span>2015&ndash;24 avg<br>7.6 M</span></div>
   </div>
   <p class="claim"><b class="hl">7.6 million acres</b> a year now, more than double the 1990s.
   77,850 fires in 2025 alone.</p>
   <p class="src">National Interagency Fire Center, annual reports</p>
  </div>

  <div class="cell c4 mark">
   <span class="label">what it costs</span>
   <div class="plot">
    <div class="bars">
     <div class="pbar"><span class="pfill soft" style="height:74%"></span></div>
     <div class="pbar"><span class="pfill" style="height:100%"></span></div>
    </div>
    <div class="blabels"><span>2015&ndash;24 avg<br>$2.9 bn</span><span>2050 projected<br>$3.9 bn</span></div>
   </div>
   <p class="claim"><b class="hl">$2.9 bn a year</b> to fight them, averaged 2015&ndash;24, rising
   <b>42% by 2050</b>. All in: <b>$394&ndash;893 bn a year</b>.</p>
   <p class="src">USDA Forest Service R&amp;D &middot; US Joint Economic Committee, 2023</p>
  </div>

  <div class="cell c4 mark">
   <span class="label">why finding them early matters</span>
   <div class="plot">
    <div class="bars">
     <div class="pbar"><span class="pfill ghost" style="height:12%"></span></div>
     <div class="pbar"><span class="pfill" style="height:100%"></span></div>
    </div>
    <div class="blabels"><span><b>1 in 10</b> fires<br>escapes&hellip;</span><span>&hellip;and burns
    <b>85%</b> of<br>all the land lost</span></div>
   </div>
   <p class="claim">The <b class="hl">earlier a fire is found</b>, the better the chance to stop it.</p>
   <p class="src">NE Alberta, reported in <i>Int. J. Wildland Fire</i> &middot; ASME Open J. Eng. 2025</p>
  </div>

 </div>
</div></section>

<!-- WHO BENEFITS -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">__N__ &middot; who benefits</p>
 <h2 class="anim">The people who <span class="hl">live in it</span>,<br>and the people <span class="hl">sent into it</span></h2>
 <div class="bento anim" style="gap:clamp(14px,1.8vw,22px)">

  <div class="cell c4 mark">
   <span class="label">who is exposed</span>
   <div class="plot">
    <div class="bars">
     <div class="pbar"><span class="pfill ghost" style="height:71%"></span></div>
     <div class="pbar"><span class="pfill" style="height:100%"></span></div>
    </div>
    <div class="blabels"><span>1990<br><b>30.8 M</b> homes</span><span>2010<br><b>43.4 M</b> homes</span></div>
   </div>
   <p class="claim"><b class="hl">About one in three American homes</b> now sits in the
   wildland&ndash;urban interface, the fastest-growing land use in the country.</p>
   <p class="src">Radeloff et&nbsp;al., <i>PNAS</i> 115(13):3314, 2018</p>
  </div>

  <div class="cell c4 mark">
   <span class="label">what it costs to send them</span>
   <div class="plot">
    <div class="statslot"><span class="stat hl">$14,000</span></div>
    <div class="blabels"><span>an hour for an air tanker, and about <b>$150,000 a day</b> for a heavy helicopter</span></div>
   </div>
   <p class="claim">Crews and aircraft are <b>the most expensive part</b> of fighting a fire, and
   there are never enough of either.</p>
   <p class="src">Aerial firefighting cost reporting, 2024&ndash;25</p>
  </div>

  <div class="cell c4 mark">
   <span class="label">what it costs them</span>
   <div class="plot">
    <div class="statslot"><span class="stat hl">20</span></div>
    <div class="blabels"><span>wildland firefighters killed <b>every year</b></span></div>
   </div>
   <p class="claim">Only a fifth die in the fire itself. Aircraft and vehicle accidents account for
   <b class="hl">nearly half</b>: the danger is in being sent.</p>
   <p class="src">US Forest Service &middot; CDC MMWR, 2000&ndash;2013</p>
  </div>

  <div class="cell c12 flat">
   <p style="margin:0"><b class="hl">More homes at risk every year, more days of fire weather, and
   more potential casualties.</b></p>
  </div>

 </div>
</div></section>

<!-- THE IDEA -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">__N__ &middot; the idea</p>
 <h2 class="anim">Four steps, and only one of them is <span class="hl">new hardware</span></h2>
 <div class="bento headsonly anim" style="gap:clamp(12px,1.5vw,18px)">

  <div class="cell c3 mark">
   <span class="label">step 1 &nbsp;&rarr;&nbsp; the cameras</span>
   <svg class="stepicon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4.5" y="14.5" width="39" height="26" rx="4.5"/><path d="M17.5 14.5v-2a3 3 0 0 1 3-3h7a3 3 0 0 1 3 3v2"/><circle cx="24" cy="27.5" r="8"/><circle cx="36.5" cy="20.5" r="1.7" fill="currentColor" stroke="none"/></svg>
   <h3>Use what is already there</h3>
   <p class="claim" style="font-size:0.9rem"><b class="hl">1,600+</b> cameras are already installed
   across eight western states. New ones go up only where there is a gap.</p>
  </div>

  <div class="cell c3 mark">
   <span class="label">step 2 &nbsp;&rarr;&nbsp; the model</span>
   <svg class="stepicon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13.4 14.4 21 19.2M13.4 24 21 20.4M13.4 33.6 21 29.4M13.4 24 21 28.2"/><path d="M27 19.6 34.2 23.2M27 29 34.2 24.8"/><circle cx="9.5" cy="14.4" r="3.6"/><circle cx="9.5" cy="24" r="3.6"/><circle cx="9.5" cy="33.6" r="3.6"/><circle cx="24" cy="19" r="3.6"/><circle cx="24" cy="29.6" r="3.6"/><circle cx="38" cy="24" r="3.6"/><circle cx="9.5" cy="24" r="1.7" fill="currentColor" stroke="none"/><circle cx="24" cy="19" r="1.7" fill="currentColor" stroke="none"/><circle cx="38" cy="24" r="1.7" fill="currentColor" stroke="none"/></svg>
   <h3>Look on the pole</h3>
   <p class="claim" style="font-size:0.9rem">A <b class="hl">small AI model</b>, about 7 million
   parameters, runs on the camera itself and spots plumes, smoke and fire.
   <b>The picture never leaves the pole.</b></p>
  </div>

  <div class="cell c3 mark">
   <span class="label">step 3 &nbsp;&rarr;&nbsp; the link</span>
   <svg class="stepicon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 28v11M17 39h14"/><circle cx="24" cy="24" r="2.6" fill="currentColor" stroke="none"/><path d="M17.6 17.6a9 9 0 0 0 0 12.8M30.4 17.6a9 9 0 0 1 0 12.8"/><path d="M12.6 12.6a16 16 0 0 0 0 22.8M35.4 12.6a16 16 0 0 1 0 22.8"/></svg>
   <h3>Send a verdict, not a photo</h3>
   <p class="claim" style="font-size:0.9rem">The camera radios <b class="hl">a few bytes</b>: what it
   thinks it saw, and how sure it is. Small enough to cross any radio, anywhere.</p>
  </div>

  <div class="cell c3 mark">
   <span class="label">step 4 &nbsp;&rarr;&nbsp; the integrator</span>
   <svg class="stepicon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 12.5v25"/><path d="M24 13.2c-1.8-2.6-6.4-2.6-8 .5-3.7.3-5.5 4-3.7 6.7-2.7 1.9-2.7 6.4 0 8.3-.3 3.7 3 6.4 6.5 5.5 1.4 2.2 4.2 2.4 5.2.6"/><path d="M24 13.2c1.8-2.6 6.4-2.6 8 .5 3.7.3 5.5 4 3.7 6.7 2.7 1.9 2.7 6.4 0 8.3.3 3.7-3 6.4-6.5 5.5-1.4 2.2-4.2 2.4-5.2.6"/><path d="M16.6 20.4h3.6L24 23.4M16.2 30.2h4l3.8-3"/><path d="M31.4 20.4h-3.6L24 23.4M31.8 30.2h-4L24 27.2"/><circle cx="15" cy="20.4" r="1.6"/><circle cx="14.6" cy="30.2" r="1.6"/><circle cx="33" cy="20.4" r="1.6"/><circle cx="33.4" cy="30.2" r="1.6"/></svg>
   <h3>Decide, then check</h3>
   <p class="claim" style="font-size:0.9rem">An <b class="hl">Arduino UNO Q</b> gathers those reports
   and weighs them. Only when several agree does it <b>send a drone to confirm</b>.</p>
  </div>

  <div class="cell c12 flat">
   <p style="margin:0;font-size:1.04rem">No new towers, and no images leaving the hillside.</p>
   <p style="margin:7px 0 0;font-size:1.04rem"><b class="hl">The cameras are the eyes</b>: each one
   decides whether it saw something worth reporting.</p>
   <p style="margin:4px 0 0;font-size:1.04rem"><b class="hl">The integrator is the brain</b>: it
   decides whether those reports add up to an alert.</p>
  </div>

 </div>
</div></section>

<!-- STEP 1 THE CAMERA -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">__N__ &middot; steps one and two, the camera and the model</p>
 <h2 class="anim">What one camera can <span class="hl">honestly</span> see</h2>
 <div class="bento headsonly anim">
  <div class="cell c4 pad0"><div class="shot" style="height:clamp(108px,20vh,206px)">
    <img src="__IMG_LARGE__" alt="A wide smoke plume filling most of a hillside frame">
    <div class="cap">Big, or close. <b>Anyone can see this one.</b></div></div></div>
  <div class="cell c4 pad0"><div class="shot" style="height:clamp(108px,20vh,206px)">
    <img src="__IMG_SMALL__" alt="A hillside with a modest smoke plume marked by a box">
    <div class="cap">Under <b>1%</b> of the frame. Accuracy <b>0.61</b>.</div></div></div>
  <div class="cell c4 pad0"><div class="shot" style="height:clamp(108px,20vh,206px)">
    <img src="__IMG_TINY__" alt="The same hillside with a barely visible smoke plume">
    <div class="cap">Under <b>0.1%</b>, about 20&times;20 px. Accuracy <b>0.14</b>.</div></div></div>

  <div class="cell c5 mark"><span class="label">on the pole</span>
   <h3>A small model, measured on real hardware</h3>
   <p class="tiny" style="margin:0">YOLOv5s: <b>7 million parameters</b>, 14.4 MB, fed 512-pixel
   frames. <b>0.778 accuracy at 179 frames a second, on 8.5 watts</b>, or 474 frames a second in
   17 MB once converted for the runtime. All measured by us on a $249 Jetson.</p>
   <p class="tiny dim" style="margin:auto 0 0">Frames: HPWREN / ALERTCalifornia. Accuracy is
   mAP50 on D-Fire.</p></div>

  <div class="cell c7"><span class="label">how far</span>
   <h3>Range is not how far it can see. It is <span class="hl">pixels on the smoke</span>.</h3>
   <p class="tiny" style="margin:0">A ridgetop camera sees tens of kilometres. Detection stops far
   sooner, because an early plume is only a few pixels wide and below roughly 20&times;20 pixels the
   detector mostly misses it. That puts useful detection at <b class="hl">about 15 km</b> per camera.
   And since a fire has to be seen by <b>two</b> cameras before it can be placed rather than merely
   reported, it means <b class="hl">one camera every 10 to 15 km</b> along the ridges, which is the
   density of our eight-camera test region.</p>
   <p class="tiny dim" style="margin:auto 0 0">And it is a trade, not a setting: wide enough to
   watch everything and an early plume is a pixel or two; tight enough to resolve one and the
   camera sees two degrees of a 360-degree horizon. Range figures are geometry, not a field
   trial.</p></div>

  <div class="cell c12 flat"><p style="margin:0">A distant camera is a weak witness on its own.
  <b class="hl">The answer is more cameras, and the next two steps.</b></p></div>
 </div>
</div></section>

<!-- STEP 2 THE VERDICT -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">__N__ &middot; step three, the verdict</p>
 <h2 class="anim">It never sends a <span class="hl">picture</span></h2>
 <div class="bento headsonly anim">
  <div class="cell c12 mark">
   <span class="label">the whole transmission, exactly as it goes out over the air</span>
   <p class="mono" style="margin:6px 0 10px;font-size:12px;letter-spacing:.04em;color:var(--dim)">
    90 10 05 00&nbsp; 29 00&nbsp; 6f 0b&nbsp; 02&nbsp; <b class="hl">02</b>&nbsp; cf&nbsp; 02&nbsp; 9f 04&nbsp; 18 ad</p>
   <p style="margin:0"><b>Camera 41, at 09:13, looking along 292.7&deg;, says <span class="hl">2</span>,
   four fifths sure.</b> All of it &mdash; <b>sixteen bytes</b>.</p>
  </div>

  <div class="cell c3"><span class="label">what it says</span>
   <h3>A two-word vocabulary</h3>
   <p class="tiny" style="margin:0"><b class="hl">1</b> means plume or smoke. <b class="hl">2</b> means
   fire. Nothing else. Smoke comes early and is often wrong, fire comes late and rarely is, so the two
   are weighed differently.</p></div>

  <div class="cell c4"><span class="label">where to look</span>
   <h3>Who, and which way</h3>
   <p class="tiny" style="margin:0">Each camera's position is already known, so it never sends it. It
   sends the <b>direction it was looking</b>, to a tenth of a degree, and <b>how tightly it holds
   it</b>, here &plusmn;2&deg;. One camera gives a line; two give a place.</p></div>

  <div class="cell c5"><span class="label">how it travels</span>
   <h3>Usually on the link that is already there</h3>
   <p class="tiny" style="margin:0">Most of these towers already carry backhaul for their video, and
   sixteen bytes costs nothing there: <b>use it wherever it exists</b>. On a ridge without it, a
   <b>9-byte</b> profile crosses LoRa, where line of sight sets the range, not power:
   <b class="hl">~23 km</b> mast to mast, <b class="hl">60 km+</b> ridge to ridge, comfortably past
   the spacing between cameras.</p></div>

  <div class="cell c12"><h3><span class="hl">No picture is ever sent</span>, and that is what makes it
   acceptable to live beside</h3>
   <p style="margin:0">Those sixteen bytes go out; the frame does not. A ridge camera sees more than
   forest &mdash; roads, driveways, back gardens. With no image leaving the pole there is <b>no footage
   of anybody to store, leak or hand over</b>. <b class="hl">It watches for fire without ever watching
   people.</b></p></div>
 </div>
</div></section>

<!-- 6 LAYER 1 ANIMATED -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">__N__ &middot; step four, the integrator</p>
 <h2 class="anim">Patience, in one number.</h2>
 <div class="bento anim">
  <div class="cell c8 pad0" style="padding:14px 6px 6px">
    <div class="canvasbox" style="min-height:min(52vh,360px)"><canvas data-anim="lif"></canvas></div></div>
  <div class="cell c4"><p>The integrator keeps a single running number: <b>how much evidence
  have I seen here lately?</b></p>
  <p>Every report pushes it up. It <b class="hl">leaks away</b> constantly, so old evidence
  fades on its own. A flicker never builds. A real plume keeps pushing, and the number climbs
  until it crosses the bar, and <b>crossing the bar is what sends the drone</b>.</p>
  <p><b class="hl">The bar moves.</b> An operator can raise it, or fire weather lowers it, and
  the same evidence then alerts sooner or later.</p>
  <p><b class="hl">And every place keeps its own.</b> A steam vent that has been investigated
  three times sits behind a higher bar; a cell where lightning struck two days ago sits behind
  a lower one. Same network, same evidence, different answer per place.</p>
  <p class="tiny" style="margin-top:auto"><b>In time:</b> evidence halves about every
  <b>3&frac12; minutes</b> if nothing renews it, and across eight simulated days the median fire is
  alerted <b>13 minutes</b> after it starts.<br><b>In memory:</b> one 32-bit number per place, which
  is the whole reason this fits on a microcontroller.</p></div>
 </div>
</div></section>

<!-- 6 STATEWIDE END TO END -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">__N__ &middot; the demo, end to end</p>
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
   <p class="tiny dim" style="margin:0">Runs in real time on the board at the tower,
   no cloud, no video leaving the hillside.</p>
  </div>
 </div>
</div></section>

<!-- WHY EDGE -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">__N__ &middot; why the edge, not the cloud</p>
 <h2 class="anim">Three reasons. <span class="hl">None of them is speed</span>.</h2>
 <div class="bento headsonly anim">
  <div class="cell c6 mark"><span class="label">1 &middot; the link is the constraint</span>
   <h3>371 ms, under a 400 ms ceiling</h3>
   <p class="tiny" style="margin:0">US rules cap a single transmission at <b>400 ms</b> on these
   channels. Our nine-byte report takes <b class="hl">371 ms</b>. The full sixteen-byte record takes
   <b>412 ms</b> and does not fit: the short profile exists because of that ceiling, not because we
   liked it.</p>
   <p class="tiny" style="margin:8px 0 0">Volume hits the same wall. A detector reading every frame
   produces thousands of detections a day, and shipping them all to a data centre is <b>about an hour
   of transmitting per camera, every day</b>, on a channel shared with every other camera on the ridge.
   Shipping only the conclusions is <b class="hl">under a minute</b> &mdash; and when the link drops,
   nine bytes wait in a queue where a video stream would simply have been lost.</p></div>

  <div class="cell c3"><span class="label">2 &middot; privacy</span>
   <h3>Nothing is sent, so nothing can leak</h3>
   <p class="tiny" style="margin:0">To decide in a data centre you have to send it pictures. Then
   images of roads, driveways and back gardens sit on somebody's servers, for as long as somebody
   keeps them. Here the frame is read on the camera and deleted there.</p></div>

  <div class="cell c3"><span class="label">3 &middot; nobody else in the loop</span>
   <h3>No subscription, no vendor, no surprises</h3>
   <p class="tiny" style="margin:0">Eight cameras share one link out instead of a data plan each, and
   there is <b>no monthly bill for the deciding</b>. The integrator is a small fixed program, pinned
   to golden test vectors, so the same evidence always gives the same alert. <b>It cannot be re-tuned
   overnight, and it does not stop when a company does.</b></p></div>

  <div class="cell c12 flat"><p class="tiny" style="margin:0"><b>And three things we will not
  claim.</b> It is not latency: a round trip to a data centre takes a fraction of a second, and a fire
  takes minutes. <b>It is not power either</b> &mdash; the detector on the camera outweighs its radio
  by four orders of magnitude, so running the intelligence on the hillside <em>costs</em> energy
  rather than saving it. And if the link out is fully down the alert cannot leave: the integrator
  keeps deciding, but somebody still has to hear it.</p></div>
 </div>
 <p class="tiny anim" style="margin-top:8px">Airtime from the Semtech time-on-air formula at
 LoRaWAN US915 DR0 (SF10, 125 kHz, CR 4/5), including the 13-byte LoRaWAN header.</p>
</div></section>

<!-- BUILDING IN THE OPEN -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">__N__ &middot; building in the open</p>
 <h2 class="anim">We are not promising to.<br>We already <span class="hl">are</span>.</h2>
 <div class="bento headsonly anim">
  <div class="cell c4 mark"><span class="label">two repositories, both public</span>
   <h3>The integrator and the detector</h3>
   <p class="tiny" style="margin:0">This system is <b>Apache-2.0 from the first commit</b>. The
   detector is a separate public study, <b>AGPL-3.0</b> because YOLOv5 is. They meet across a
   <b>process boundary</b> rather than by linking, so both licences stay intact and the commercial
   path stays open.</p></div>

  <div class="cell c4"><span class="label">where the pictures come from</span>
   <h3>D-Fire, and the gap we do not hide</h3>
   <p class="tiny" style="margin:0">Trained on <b>D-Fire</b>: 21,527 labelled fire and smoke images,
   published by Ven&acirc;ncio et al. in 2022, free to download. The tower frames here are HPWREN /
   ALERTCalifornia. <b class="hl">But D-Fire is ground-level surveillance and web photos from Brazil,
   not tower imagery from a Californian ridge</b>, so the detector has not been tested on the domain it
   would work in. A named risk, not a footnote.</p></div>

  <div class="cell c4"><span class="label">how the numbers stay honest</span>
   <h3>One harness, frozen splits</h3>
   <p class="tiny" style="margin:0">Every measurement goes through one harness with a version stamp:
   change it and earlier results are void and get re-run. Splits are frozen and checksummed, so
   <b>training refuses to start</b> if they drift. Accuracy is bit-reproducible, and no figure is
   drawn by hand.</p></div>

  <div class="cell c7 hot"><h3 class="bad">Including everything that failed</h3>
   <p class="tiny" style="margin:0 0 6px">Pruning <b>lost on accuracy and speed at once</b>. One
   default quantisation setting cost <b>67% of the accuracy</b>. In this repo: a normalisation scheme that masked real fires, an
   adaptation rule that did nothing, a rate-coding bug of our own making.</p>
   <p class="tiny" style="margin:0"><b class="hl">Negative results get published as loudly as
   positive ones.</b> A log of only successes is marketing.</p></div>

  <div class="cell c5 flat"><h3>Through Stage Two</h3>
   <p class="tiny" style="margin:0"><b>Build notes</b> at each milestone: what was tried, what the
   measurement said, what changed. <b>Hardware files</b> beside the firmware, so the prototype is
   reproducible and not merely watchable. <b>Retargeting guidance</b>, since the thresholds are
   deployment-specific and saying so beats shipping ours.</p></div>
 </div>
</div></section>

<!-- FEASIBILITY -->
<section class="slide"><div class="inner">
 <p class="eyebrow anim">__N__ &middot; an honest read on feasibility</p>
 <h2 class="anim">What is built, what is measured, and <span class="hl">what could still sink it</span>.</h2>
 <div class="bento headsonly anim">
  <div class="cell c4 mark"><span class="label">built</span>
   <h3>The integrator already exists</h3>
   <p class="tiny" style="margin:0">A portable C99 core in fixed point, with <b>no floating point, no
   allocation and no libc</b>, that cross-compiles for the Cortex-M33 on the UNO Q. <b>53 tests</b> and
   a set of golden vectors pin its behaviour. The simulator drives this same code, so what we measured
   is what would ship.</p></div>

  <div class="cell c4"><span class="label">measured</span>
   <h3>Eight simulated days, four methods</h3>
   <p class="tiny" style="margin:0">Same cameras, same evidence, read four ways. At the same <b>96%</b>
   of fires found, ours raises <b class="hl">4.4&times; fewer false alarms</b> than the classical
   crossing of bearings, 47 a day against 208 &mdash; while placing fires to about <b>650 m</b>, where
   that method manages 343 m.</p></div>

  <div class="cell c4 warmb"><span class="label">not yet</span>
   <h3>What we have not done</h3>
   <p class="tiny" style="margin:0">No board in hand. The footprint is designed for and the
   host-to-target parity harness is written, <b>but has not been run</b>. Every number above comes from
   our own simulator, whose nuisance model we invented and fitted to one published aggregate. The
   evidence is <b>24 fires</b>, which is thin.</p></div>

  <div class="cell c6 hot"><h3 class="bad">The risk we would test first</h3>
   <p class="tiny" style="margin:0">The threshold rises where the system has been wrong before. But
   people start fires near roads, and roads are where dust and headlights are too.
   <b>The mechanism may be quietly anti-correlated with risk</b>, learning to ignore the very places
   most likely to burn. Untested, and the first experiment we would run.</p></div>

  <div class="cell c6 hot"><h3 class="bad">And the largest: we cannot claim fewer acres</h3>
   <p class="tiny" style="margin:0">Ba&#803;lek et al. (PLOS ONE, 2024) found <b>no evidence that fire
   size grows with reporting delay</b> across Western Canada, and that detection investment is not
   justified on suppression savings alone. A different setting, but good evidence, and it points away
   from us. <b class="hl">So we claim an operational result, not an outcome one:</b> fewer things a
   human must look at. Whether that becomes fewer acres is unproven, and we have not tried to prove
   it.</p></div>
 </div>
</div></section>

<!-- CLOSE -->
<section class="slide hero">
 <canvas class="bgfire" data-anim="fire"></canvas>
 <div class="scrim"></div>
 <div class="inner">
  <div class="herocopy">
   <p class="eyebrow anim">thank you</p>
   <h1 class="anim">The cameras are already there.<br>So is the <span class="hl">fire</span>.</h1>
   <ul class="clean anim" style="margin:0 0 6px;gap:11px">
    <li>What is missing is the layer between them, and it runs on a board at the tower.</li>
    <li>One located alert, instead of a thousand that nobody can afford to read.</li>
    <li>Public from the first commit, mistakes included, and every number re-runnable.</li>
    <li>Stage Two: the same integrator, on the <b>Arduino UNO Q</b>, in the field.</li>
   </ul>
   <div class="rule anim"></div>
   <p class="tiny anim"><span class="mark">&#8251;</span> <b>Kernwerk</b> &nbsp;&middot;&nbsp;
   confidential edge AI, built small and sealed shut</p>
  </div>
 </div>
</section>

"""

# Slide numbers are assigned here, in document order, rather than written into
# each slide by hand. Reordering the deck can then never leave behind a
# duplicate number or a gap -- which it did, twice, when they were hardcoded.
def _number(s):
    n = a = 0
    out = []
    for chunk in re.split(r'(__N__|__A__)', s):
        if chunk == "__N__":
            n += 1; out.append(f"{n:02d}")
        elif chunk == "__A__":
            a += 1; out.append(f"A{a}")
        else:
            out.append(chunk)
    return "".join(out), n, a


SLIDES, _MAIN_NUMBERED, _APX_NUMBERED = _number(SLIDES)

# the deck's own contents page: numbers must run 01..N with nothing missing
# Cross-references are written by NAME in the source (__REF:the obstacle__) and
# resolved to numbers here, so a reorder can never leave a slide pointing at the
# wrong place. The coverage slide had been pointing at five wrong slides.
_LABELS = {lab.strip(): num for num, lab in
           re.findall(r'<p class="eyebrow anim">(\d\d) &middot; ([^<]*)</p>', SLIDES)}


def _resolve_refs(s):
    def sub(m):
        key = m.group(1).strip()
        assert key in _LABELS, f"cross-reference to unknown slide: {key!r}"
        return _LABELS[key]
    return re.sub(r'__REF:([^_]+)__', sub, s)


SLIDES = _resolve_refs(SLIDES)
assert "__REF:" not in SLIDES

_seen = re.findall(r'<p class="eyebrow anim">(\d\d) &middot;', SLIDES)
assert _seen == [f"{i:02d}" for i in range(1, _MAIN_NUMBERED + 1)], \
    f"slide numbering is not contiguous: {_seen}"
