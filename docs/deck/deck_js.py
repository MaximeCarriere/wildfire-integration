JS = r"""
(function(){
'use strict';
var slides=[].slice.call(document.querySelectorAll('.slide'));
var MAIN=parseInt(document.body.dataset.main,10)||15;
var i=0, running=[];
var reduce=window.matchMedia('(prefers-reduced-motion:reduce)').matches;

/* ---------- theme ---------- */
function curTheme(){
  var t=document.documentElement.getAttribute('data-theme');
  if(t) return t;
  return window.matchMedia('(prefers-color-scheme:dark)').matches?'night':'light';
}
function tok(n){return getComputedStyle(document.documentElement).getPropertyValue(n).trim();}
document.getElementById('theme').addEventListener('click',function(){
  document.documentElement.setAttribute('data-theme', curTheme()==='night'?'light':'night');
  restart();
});

/* ---------- nav ---------- */
var ticks=document.getElementById('ticks');
slides.forEach(function(s,n){
  var b=document.createElement('button');
  b.className='tick'+(n>=MAIN?' ax':'');
  b.title=(n<MAIN?'Slide '+(n+1):'Appendix '+(n-MAIN+1));
  b.addEventListener('click',function(){go(n);});
  ticks.appendChild(b);
});
var tickEls=[].slice.call(ticks.children);

function go(n){
  n=Math.max(0,Math.min(slides.length-1,n));
  if(n===i && slides[i].classList.contains('live')) return;
  slides[i].classList.remove('live');
  i=n;
  slides[i].classList.add('live');
  slides[i].scrollTop=0;
  tickEls.forEach(function(t,k){t.classList.toggle('on',k<=i);});
  document.getElementById('count').textContent =
    (i<MAIN? (i+1)+' / '+MAIN : 'A'+(i-MAIN+1)+' / A'+(slides.length-MAIN));
  restart();
}
function next(){go(i+1);} function prev(){go(i-1);}

document.getElementById('next').addEventListener('click',next);
document.getElementById('prev').addEventListener('click',prev);
document.getElementById('appx').addEventListener('click',function(){go(MAIN);});

document.addEventListener('keydown',function(e){
  if(e.metaKey||e.ctrlKey||e.altKey) return;
  var k=e.key;
  if(k==='ArrowRight'||k==='PageDown'||k===' '||k==='j'){e.preventDefault();next();}
  else if(k==='ArrowLeft'||k==='PageUp'||k==='k'){e.preventDefault();prev();}
  else if(k==='Home'){e.preventDefault();go(0);}
  else if(k==='End'){e.preventDefault();go(slides.length-1);}
  else if(k==='a'||k==='A'){go(MAIN);}
  else if(k==='t'||k==='T'){document.getElementById('theme').click();}
  else if(k==='f'||k==='F'){
    if(document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen();
  }
  else if(k==='?'||k==='/'){document.getElementById('help').classList.toggle('on');}
  else if(k==='Escape'){document.getElementById('help').classList.remove('on');}
});
document.getElementById('help').addEventListener('click',function(){this.classList.remove('on');});

/* ---------- animation registry ---------- */
function stopAll(){running.forEach(function(h){cancelAnimationFrame(h.id);});running=[];}
function restart(){
  stopAll();
  var cvs=slides[i].querySelectorAll('canvas[data-anim]');
  [].forEach.call(cvs,function(c){ var f=ANIM[c.dataset.anim]; if(f) f(c); });
}
function fit(c){
  var r=c.getBoundingClientRect(), d=window.devicePixelRatio||1;
  c.width=Math.max(1,r.width*d); c.height=Math.max(1,r.height*d);
  var x=c.getContext('2d'); x.setTransform(d,0,0,d,0,0);
  return {x:x,w:r.width,h:r.height};
}
function loop(fn){
  /* one handle per animation, not one per frame -- pushing an id every
     frame grew this array without bound over a long presentation. */
  var h={id:0}; running.push(h);
  (function step(){ fn(); h.id=requestAnimationFrame(step); })();
}

var ANIM={};

/* ===== 0. the cover =====
   Not a diagram -- the thesis, ambient. A field of sensors twitching at
   nothing, most of the time. Now and then a few near each other agree, and
   exactly one alert rises out of the noise. That is the whole argument, and
   it needs no caption.
   The cover deliberately does NOT reuse a later slide's diagram: showing the
   geometry here would spend the explanation before the problem is stated. */
ANIM.cover=function(c){
  var g=fit(c),W=g.w,H=g.h,x=g.x;
  var A=tok('--select'),D=tok('--dim'),R=tok('--red'),Y=tok('--yellow');
  var t0=performance.now();

  if(!c._field || c._fw!==W){
    var rnd=mulberry(80231), pts=[], cols=Math.max(9,Math.round(W/34));
    var rows=Math.max(6,Math.round(H/34));
    for(var j=0;j<rows;j++)for(var i=0;i<cols;i++){
      pts.push({x:(i+0.5+(rnd()-0.5)*0.72)/cols,
                y:(j+0.5+(rnd()-0.5)*0.72)/rows,
                ph:rnd()*6.28, r:rnd()});
    }
    var ev=[];
    for(var k=0;k<5;k++){
      var seed=pts[Math.floor(rnd()*pts.length)];
      var near=pts.map(function(q,idx){return {idx:idx,
          d:Math.hypot((q.x-seed.x)*W,(q.y-seed.y)*H)};})
        .sort(function(a2,b2){return a2.d-b2.d;}).slice(0,3);
      ev.push({at:0.12+k*0.19, who:near.map(function(o){return o.idx;}),
               x:seed.x, y:seed.y});
    }
    c._field=pts; c._ev=ev; c._fw=W;
  }
  var pts=c._field, EV=c._ev, DUR=26000;

  loop(function(){
    var p=((performance.now()-t0)%DUR)/DUR, now=performance.now()/1000;
    x.clearRect(0,0,W,H);
    var cur=null, age=0;
    for(var e=0;e<EV.length;e++){
      var a2=p-EV[e].at;
      if(a2>=0 && a2<0.115){ cur=EV[e]; age=a2/0.115; }
    }
    pts.forEach(function(q,idx){
      var px=q.x*W, py=q.y*H, col=D, rad=1.6, al=.30;
      var fl=(now*0.55+q.ph)%6.28;
      if(fl<0.5 && q.r>0.55){ col=Y; rad=2.4; al=.22+.42*(1-fl/0.5); }
      if(cur && cur.who.indexOf(idx)>=0){
        var on=Math.min(1,age/0.22);
        col=age<0.45?Y:R; rad=2.4+on*1.8; al=.4+.6*on;
        if(age>0.2){
          x.strokeStyle=col; x.globalAlpha=.28*(1-Math.min(1,(age-0.2)/0.5));
          x.lineWidth=1; x.beginPath();
          x.moveTo(px,py); x.lineTo(cur.x*W,cur.y*H); x.stroke(); x.globalAlpha=1;
        }
      }
      x.globalAlpha=al; x.fillStyle=col;
      x.beginPath(); x.arc(px,py,rad,0,7); x.fill(); x.globalAlpha=1;
    });
    if(cur && age>0.42){
      var k2=(age-0.42)/0.58, ax=cur.x*W, ay=cur.y*H, pl=(now*1.5)%1;
      x.globalAlpha=(1-pl)*.55*(1-k2*0.6); x.strokeStyle=R; x.lineWidth=1.6;
      x.beginPath(); x.arc(ax,ay,6+pl*30,0,7); x.stroke();
      x.globalAlpha=.85*(1-k2*0.5); x.fillStyle=R;
      x.beginPath(); x.arc(ax,ay,4,0,7); x.fill();
      x.globalAlpha=.7*(1-k2*0.5); x.strokeStyle=R; x.lineWidth=1.2;
      x.strokeRect(ax-11,ay-11,22,22); x.globalAlpha=1;
    }
  });
};

/* ===== 1. evidence -> threshold -> fire -> drone =====
   Three things at once, because they are the same idea:
     - evidence ACCUMULATES and leaks; crossing the bar dispatches a drone
     - the bar MOVES: operators raise it or fire weather lowers it
     - every place keeps its OWN bar, learned from what happened there
   The loop replays identical evidence against three settings, so the only
   thing that changes between acts is the height of the line. */
var LIF_EV=[0.10,0.17,0.23,0.30,0.35,0.41,0.46,0.52,0.57,0.63,0.69,0.75,0.82,0.89];
var LIF_W =[0.10,0.10,0.09,0.20,0.10,0.20,0.10,0.22,0.10,0.22,0.11,0.24,0.12,0.24];
var LIF_TAU=0.30;

function lifV(t){
  var v=0,last=LIF_EV[0]-0.001;
  for(var i=0;i<LIF_EV.length;i++){
    if(LIF_EV[i]>t) break;
    v*=Math.exp(-(LIF_EV[i]-last)/LIF_TAU); last=LIF_EV[i]; v+=LIF_W[i];
  }
  if(t>last) v*=Math.exp(-(t-last)/LIF_TAU);
  return v;
}
function lifCross(th){
  for(var t=0;t<1;t+=0.002) if(lifV(t)>=th) return t;
  return -1;
}

ANIM.lif=function(c){
  var g=fit(c),W=g.w,H=g.h,x=g.x;
  var A=tok('--select'),F=tok('--front'),D=tok('--dim'),R=tok('--red'),Y=tok('--yellow');
  var CARD=tok('--card'),EDGE=tok('--cardEdge');
  var t0=performance.now(), DUR=16500;

  var PRESET=[{n:'NORMAL',th:0.78,c:D},{n:'ELEVATED',th:0.60,c:Y},{n:'RED FLAG',th:0.44,c:R}];
  /* every cell keeps its own bar, and remembers why */
  var CELLS=[
    {n:'ridge 41',      off: 0.00, why:'default'},
    {n:'steam vent',    off: 0.30, why:'learned: 3 false alarms'},
    {n:'burn scar',     off: 0.14, why:'learned: 1 false alarm'},
    {n:'strike 2d ago', off:-0.24, why:'lightning prior'},
    {n:'town edge',     off:-0.12, why:'operator: protect'}
  ];

  loop(function(){
    var p=((performance.now()-t0)%DUR)/DUR;
    var act=Math.floor(p*3)%3, u=(p*3)%1;
    var P=PRESET[act], th=P.th, cross=lifCross(th);
    x.clearRect(0,0,W,H);

    var stripH=Math.min(74,H*0.30);
    var pad={l:52,r:74,t:26,b:stripH+26};
    var gw=W-pad.l-pad.r, gh=H-pad.t-pad.b, gb=pad.t+gh;
    var X=function(t){return pad.l+t*gw;}, Yv=function(v){return gb-Math.min(v,1.15)/1.15*gh;};

    /* frame */
    x.strokeStyle=D; x.globalAlpha=.3; x.lineWidth=1;
    x.beginPath(); x.moveTo(pad.l,pad.t-4); x.lineTo(pad.l,gb); x.lineTo(pad.l+gw,gb); x.stroke();
    x.globalAlpha=1;
    x.save(); x.translate(13,pad.t+gh/2); x.rotate(-Math.PI/2);
    x.fillStyle=D; x.font='9px ui-monospace,monospace'; x.textAlign='center';
    x.fillText('evidence',0,0); x.restore();

    /* the movable bar: ghosts of the other two settings, so it is visibly a DIAL */
    PRESET.forEach(function(q,i){
      if(i===act) return;
      x.strokeStyle=q.c; x.globalAlpha=.20; x.lineWidth=1; x.setLineDash([2,5]);
      x.beginPath(); x.moveTo(pad.l,Yv(q.th)); x.lineTo(pad.l+gw,Yv(q.th)); x.stroke();
      x.setLineDash([]); x.globalAlpha=1;
      x.fillStyle=q.c; x.globalAlpha=.45; x.font='8px ui-monospace,monospace'; x.textAlign='left';
      x.fillText(q.n,pad.l+gw+6,Yv(q.th)+3); x.globalAlpha=1;
    });
    x.strokeStyle=P.c; x.lineWidth=1.6; x.setLineDash([5,4]);
    x.beginPath(); x.moveTo(pad.l,Yv(th)); x.lineTo(pad.l+gw,Yv(th)); x.stroke(); x.setLineDash([]);
    x.fillStyle=P.c; x.font='bold 9px ui-monospace,monospace'; x.textAlign='left';
    x.fillText(P.n,pad.l+gw+6,Yv(th)+3);

    /* the trace */
    var started=false;
    x.strokeStyle=A; x.lineWidth=2; x.beginPath();
    for(var s=0;s<=u;s+=1/260){
      var gx=X(s),gy=Yv(lifV(s));
      started?x.lineTo(gx,gy):(x.moveTo(gx,gy),started=true);
    }
    if(started){
      x.stroke();
      x.globalAlpha=.13; x.fillStyle=A; x.beginPath(); x.moveTo(X(0),gb);
      for(var s2=0;s2<=u;s2+=1/260) x.lineTo(X(s2),Yv(lifV(s2)));
      x.lineTo(X(u),gb); x.closePath(); x.fill(); x.globalAlpha=1;
    }
    /* arriving reports */
    for(var i2=0;i2<LIF_EV.length;i2++){
      if(LIF_EV[i2]>u) break;
      var big=LIF_W[i2]>0.15;
      x.strokeStyle=big?R:Y; x.lineWidth=big?2:1.4;
      x.beginPath(); x.moveTo(X(LIF_EV[i2]),gb+2); x.lineTo(X(LIF_EV[i2]),gb+(big?9:6)); x.stroke();
    }
    x.fillStyle=D; x.font='8px ui-monospace,monospace'; x.textAlign='left';
    x.fillText('reports arriving  ( tall = fire, short = smoke )',pad.l,gb+20);

    /* crossing -> fire -> drone */
    if(cross>=0 && u>=cross){
      var age=u-cross;
      x.fillStyle=P.c; x.beginPath(); x.arc(X(cross),Yv(th),4.5,0,7); x.fill();
      var pl=Math.min(1,age/0.10);
      x.globalAlpha=(1-pl)*.8; x.strokeStyle=P.c; x.lineWidth=2;
      x.beginPath(); x.arc(X(cross),Yv(th),5+pl*22,0,7); x.stroke(); x.globalAlpha=1;
      /* the drone leaves */
      var fly=Math.min(1,Math.max(0,(age-0.04)/0.34));
      if(fly>0){
        var dx=X(cross)+fly*(pad.l+gw+50-X(cross)), dy=Yv(th)-18-Math.sin(fly*3.14)*14;
        x.save(); x.translate(dx,dy); x.strokeStyle=A; x.lineWidth=1.5;
        x.beginPath(); x.moveTo(-5,-3.2); x.lineTo(5,3.2);
        x.moveTo(5,-3.2); x.lineTo(-5,3.2); x.stroke();
        var sp=(performance.now()/1000*22)%6.28;
        [[-5,-3.2],[5,3.2],[5,-3.2],[-5,3.2]].forEach(function(r){
          x.globalAlpha=.7; x.beginPath();
          x.ellipse(r[0],r[1],3.3,1.2,sp,0,6.28); x.stroke(); x.globalAlpha=1;});
        x.restore();
        if(fly>0.25){
          x.fillStyle=A; x.font='bold 9px ui-monospace,monospace'; x.textAlign='right';
          x.fillText('drone sent',X(cross)-8,Yv(th)-20);
        }
      }
      x.fillStyle=P.c; x.font='9px ui-monospace,monospace'; x.textAlign='center';
      x.fillText('alert at '+Math.round(cross*100)+'% of the evidence',X(cross),pad.t-10);
    }

    /* ---- every place keeps its own bar ---- */
    var sy=H-stripH+8, cw=(W-pad.l-14)/CELLS.length;
    x.fillStyle=D; x.font='8px ui-monospace,monospace'; x.textAlign='left';
    x.fillText('AND EVERY PLACE KEEPS ITS OWN BAR',pad.l,sy-2);
    var vnow=lifV(u);
    CELLS.forEach(function(cl,i){
      var bx=pad.l+i*cw+4, bw=cw-12, by=sy+8, bh=stripH-30;
      var lth=Math.max(0.08,Math.min(1.12,th+cl.off));
      var fired=vnow>=lth;
      x.fillStyle=CARD; x.globalAlpha=.85;
      x.beginPath(); if(x.roundRect)x.roundRect(bx,by,bw,bh,3); else x.rect(bx,by,bw,bh);
      x.fill(); x.globalAlpha=1; x.strokeStyle=EDGE; x.lineWidth=1; x.stroke();
      /* fill level = current evidence */
      var fh=Math.min(1,vnow/1.15)*(bh-6);
      x.fillStyle=fired?P.c:A; x.globalAlpha=fired?.30:.18;
      x.fillRect(bx+3,by+bh-3-fh,bw-6,fh); x.globalAlpha=1;
      /* this cell's own bar */
      var ly=by+bh-3-Math.min(1,lth/1.15)*(bh-6);
      x.strokeStyle=fired?P.c:D; x.lineWidth=fired?2:1.2;
      x.beginPath(); x.moveTo(bx+2,ly); x.lineTo(bx+bw-2,ly); x.stroke();
      if(fired){
        x.fillStyle=P.c; x.font='bold 8px ui-monospace,monospace'; x.textAlign='center';
        x.fillText('FIRES',bx+bw/2,by+11);
      }
      x.fillStyle=fired?F:D; x.font='8px ui-monospace,monospace'; x.textAlign='center';
      x.fillText(cl.n,bx+bw/2,by+bh+10);
      x.fillStyle=D; x.globalAlpha=.7; x.font='7px ui-monospace,monospace';
      x.fillText(cl.why,bx+bw/2,by+bh+19); x.globalAlpha=1;
    });
  });
};

/* ===== 2. Layer 2 -- overlapping shapes on the map =====
   A report is not a line. If the camera knows roughly where it is pointed the
   shape is a wedge; if it knows nothing but its own GPS position the shape is
   simply a 20 km disc. The integrator does not care which -- it adds up
   whatever overlaps. The loop shows both, so the cost of losing the direction
   is visible rather than asserted: the disc fix is a region, the wedge fix is
   a point. Measured, that difference is about 7x in false alarms. */
ANIM.bearing=function(c){
  var g=fit(c),W=g.w,H=g.h,x=g.x;
  var A=tok('--select'),F=tok('--front'),D=tok('--dim'),R=tok('--red'),Y=tok('--yellow');
  var t0=performance.now(), DUR=15000;
  var KM=60;                                   /* the canvas spans ~60 km */
  var fire={x:0.54,y:0.42};
  var towers=[{x:0.16,y:0.78},{x:0.86,y:0.70},{x:0.34,y:0.13}];

  loop(function(){
    var p=((performance.now()-t0)%DUR)/DUR, now=performance.now()/1000;
    x.clearRect(0,0,W,H);
    var m=16, w=W-2*m, h=H-2*m;
    var X=function(u){return m+u*w;}, Yv=function(v){return m+v*h;};
    var Rpx=(20/KM)*w;                          /* 20 km detection radius */
    var fx=X(fire.x), fy=Yv(fire.y);

    /* grid */
    x.strokeStyle=D; x.globalAlpha=.12; x.lineWidth=1;
    for(var k=0;k<=12;k++){
      x.beginPath(); x.moveTo(m+k*w/12,m); x.lineTo(m+k*w/12,m+h); x.stroke();
      x.beginPath(); x.moveTo(m,m+k*h/12); x.lineTo(m+w,m+k*h/12); x.stroke();
    }
    x.globalAlpha=1;

    var live = p<0.14?0 : p<0.26?1 : p<0.38?2 : 3;
    /* narrow: 0 = full disc (no direction), 1 = tight wedge (bearing known) */
    var narrow = p<0.56?0 : Math.min(1,(p-0.56)/0.16);
    var ease = narrow*narrow*(3-2*narrow);

    towers.forEach(function(T,n){
      var tx=X(T.x), ty=Yv(T.y);
      if(n<live){
        var ang=Math.atan2(fy-ty,fx-tx);
        var half=Math.PI*(1-ease) + 0.10*ease;   /* pi = whole disc -> 0.1 rad */
        var grd=x.createRadialGradient(tx,ty,0,tx,ty,Rpx);
        grd.addColorStop(0,'transparent'); grd.addColorStop(.35,A);
        grd.addColorStop(1,'transparent');
        x.globalAlpha=.14+.06*ease; x.fillStyle=grd;
        x.beginPath(); x.moveTo(tx,ty);
        x.arc(tx,ty,Rpx,ang-half,ang+half); x.closePath(); x.fill();
        x.globalAlpha=1;
        /* boundary */
        x.strokeStyle=A; x.globalAlpha=.35; x.lineWidth=1; x.setLineDash([4,4]);
        x.beginPath(); x.arc(tx,ty,Rpx,ang-half,ang+half);
        if(ease>0.05){ x.lineTo(tx,ty); x.closePath(); }
        x.stroke(); x.setLineDash([]); x.globalAlpha=1;
      }
      x.fillStyle= n<live? A : D;
      x.beginPath(); x.arc(tx,ty,5,0,7); x.fill();
      x.strokeStyle=x.fillStyle; x.globalAlpha=.35; x.lineWidth=1.4;
      x.beginPath(); x.arc(tx,ty,9,0,7); x.stroke(); x.globalAlpha=1;
      x.fillStyle=D; x.font='10px ui-monospace,monospace'; x.textAlign='center';
      x.fillText('tower '+(n+1), tx, ty+24);
    });

    /* the fix: a region while the shapes are discs, a point once they narrow */
    if(live>=2){
      var spread=(1-ease);
      var rr=(6+spread*46);
      x.globalAlpha=.85; x.fillStyle=live>=3?R:Y;
      if(spread>0.05){
        x.globalAlpha=.16; x.beginPath(); x.arc(fx,fy,rr,0,7); x.fill(); x.globalAlpha=.9;
      }
      x.beginPath(); x.arc(fx,fy,live>=3?(5+2*ease):4,0,7); x.fill(); x.globalAlpha=1;
      x.strokeStyle=live>=3?R:Y; x.lineWidth=1.5;
      x.strokeRect(fx-rr*0.7,fy-rr*0.7,rr*1.4,rr*1.4);
      if(ease>0.6){
        var pl=(now*1.6)%1;
        x.globalAlpha=(1-pl)*.6; x.beginPath(); x.arc(fx,fy,7+pl*24,0,7); x.stroke();
        x.globalAlpha=1;
      }
    }

    /* scale bar */
    x.strokeStyle=D; x.globalAlpha=.5; x.lineWidth=1;
    x.beginPath(); x.moveTo(m+4,m+h-6); x.lineTo(m+4+(20/KM)*w,m+h-6); x.stroke();
    x.fillStyle=D; x.font='9px ui-monospace,monospace'; x.textAlign='left';
    x.fillText('20 km',m+4,m+h-11); x.globalAlpha=1;

    var msg,col=D;
    if(live===0){ msg='quiet — nothing reported'; }
    else if(live===1){ msg='one tower reports. somewhere within 20 km of it. no alert.'; col=Y; }
    else if(live===2){ msg='a second tower agrees. the discs overlap — but it is still a region.'; col=Y; }
    else if(ease<0.05){ msg='three towers, GPS only. a fix about a kilometre across. it works.'; col=R; }
    else if(ease<0.95){ msg='now add a rough direction — ten degrees is enough…'; col=R; }
    else { msg='…and the same evidence lands on one cell. ~7× fewer false alarms.'; col=R; }
    x.textAlign='left'; x.font='11px ui-monospace,monospace'; x.fillStyle=col;
    x.fillText(msg, m+2, m+h+2);
  });
};

/* ===== 3. haze vs fire -- why subtracting the surround works ===== */
ANIM.surround=function(c){
  var g=fit(c),W=g.w,H=g.h,x=g.x;
  var A=tok('--select'),D=tok('--dim'),R=tok('--red'),Y=tok('--yellow');
  var t0=performance.now(), DUR=8000;
  loop(function(){
    var p=((performance.now()-t0)%DUR)/DUR;
    x.clearRect(0,0,W,H);
    var pad={l:34,r:12,t:22,b:30};
    var pw=W-pad.l-pad.r, ph=H-pad.t-pad.b, yb=pad.t+ph;
    var X=function(u){return pad.l+u*pw;}, Yv=function(v){return yb-v*ph;};
    var haze = p<0.35?0 : Math.min(1,(p-0.35)/0.2);
    var sub  = p<0.68?0 : Math.min(1,(p-0.68)/0.18);

    function profile(u){
      var fire=0.62*Math.exp(-Math.pow((u-0.5)/0.045,2));
      var hz=haze*0.42*(0.85+0.15*Math.sin(u*9));
      return {f:fire,h:hz};
    }
    /* signal */
    x.lineWidth=2; x.strokeStyle=A; x.beginPath();
    for(var s=0;s<=200;s++){
      var u=s/200,q=profile(u); var v=q.f+q.h-(sub?q.h:0);
      s?x.lineTo(X(u),Yv(v)):x.moveTo(X(u),Yv(v));
    }
    x.stroke();
    /* background estimate */
    if(haze>0&&sub<1){
      x.strokeStyle=Y; x.setLineDash([4,4]); x.lineWidth=1.5; x.beginPath();
      for(var s2=0;s2<=200;s2++){var u2=s2/200,q2=profile(u2);
        s2?x.lineTo(X(u2),Yv(q2.h)):x.moveTo(X(u2),Yv(q2.h));}
      x.stroke(); x.setLineDash([]);
    }
    /* threshold */
    x.strokeStyle=R; x.setLineDash([3,3]); x.lineWidth=1.2;
    x.beginPath(); x.moveTo(pad.l,Yv(0.5)); x.lineTo(pad.l+pw,Yv(0.5)); x.stroke(); x.setLineDash([]);
    x.fillStyle=D; x.font='10px ui-monospace,monospace'; x.textAlign='left';
    x.fillText('alert threshold',pad.l+3,Yv(0.5)-4);

    x.font='11px ui-monospace,monospace'; x.textAlign='left';
    var msg = p<0.35? 'a fire: a sharp local peak. clears the bar.'
            : p<0.68? 'haze rolls in. everything lifts — including the fire.'
            : 'subtract the local background. the fire is exactly as visible as before.';
    x.fillStyle = p<0.35? A : (p<0.68? Y : A);
    x.fillText(msg, pad.l, yb+22);
  });
};


/* ===== 4. the whole system, statewide, end to end =====
   Four things this picture has to say at once:
     - the sensor field is LARGE and individually unreliable
     - integration is DISTRIBUTED: many integrators, each owning a patch
     - evidence arrives ASYNCHRONOUSLY, from several cameras, over minutes
     - the decision is a MEMBRANE POTENTIAL crossing a threshold, not a rule
   The drone launch time is not scripted: it is whenever the integration
   actually crosses, computed once from the event schedule. */
var CA=[
[-124.21,42.00],[-120.00,42.00],[-120.00,39.32],[-114.64,35.00],[-114.63,34.87],
[-114.47,34.71],[-114.14,34.30],[-114.44,34.08],[-114.53,33.55],[-114.72,33.40],
[-114.68,33.04],[-114.52,32.76],[-114.72,32.71],[-117.13,32.53],[-117.25,32.67],
[-117.32,33.10],[-117.60,33.39],[-118.09,33.74],[-118.41,33.74],[-118.52,34.02],
[-119.21,34.15],[-119.56,34.42],[-120.47,34.45],[-120.64,34.58],[-120.62,35.13],
[-120.90,35.42],[-121.28,35.67],[-121.90,36.31],[-121.89,36.58],[-121.79,36.80],
[-121.81,36.93],[-122.41,37.20],[-122.52,37.78],[-122.98,38.11],[-123.07,38.32],
[-123.73,38.95],[-123.83,39.77],[-124.11,40.10],[-124.41,40.44],[-124.15,41.05],
[-124.25,41.79],[-124.21,42.00]];

function inPoly(px,py,poly){
  var c=false;
  for(var a=0,b=poly.length-1;a<poly.length;b=a++){
    var xi=poly[a][0],yi=poly[a][1],xj=poly[b][0],yj=poly[b][1];
    if(((yi>py)!==(yj>py)) && (px < (xj-xi)*(py-yi)/(yj-yi)+xi)) c=!c;
  }
  return c;
}
function mulberry(s){return function(){s|=0;s=s+0x6D2B79F5|0;var t=Math.imul(s^s>>>15,1|s);
  t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}

var W_SMOKE=0.085, W_FIRE=0.20, V_TAU=0.085, V_TH=0.80;

ANIM.statewide=function(c){
  var g=fit(c),W=g.w,H=g.h,x=g.x;
  var A=tok('--select'),F=tok('--front'),D=tok('--dim'),R=tok('--red'),Y=tok('--yellow');
  var CARD=tok('--card'), EDGE=tok('--cardEdge');

  var lo0=999,lo1=-999,la0=999,la1=-999;
  CA.forEach(function(p){lo0=Math.min(lo0,p[0]);lo1=Math.max(lo1,p[0]);
                         la0=Math.min(la0,p[1]);la1=Math.max(la1,p[1]);});
  var latm=(la0+la1)/2, kx=Math.cos(latm*Math.PI/180);
  var pad=16, availW=W-2*pad, availH=H-2*pad;
  var spanX=(lo1-lo0)*kx, spanY=(la1-la0);
  var sc=Math.min(availW/spanX, availH/spanY);
  var offX=pad+(availW-spanX*sc)/2, offY=pad+(availH-spanY*sc)/2;
  function PX(lon){return offX+(lon-lo0)*kx*sc;}
  function PY(lat){return offY+(la1-lat)*sc;}

  if(!c._built){
    var rnd=mulberry(20260906), cams=[], guard=0;
    while(cams.length<330 && guard++<60000){
      var lon=lo0+rnd()*(lo1-lo0), lat=la0+rnd()*(la1-la0);
      if(!inPoly(lon,lat,CA)) continue;
      if(lon>-116.5 && lat<35.5 && rnd()<0.6) continue;   /* thin the desert */
      cams.push({lon:lon,lat:lat,ph:rnd()*6.28});
    }
    var fire={lon:-120.72,lat:39.30};
    var KM_LAT=111, KM_LON=111*kx;

    /* Witnesses placed deliberately: close in (14-26 km) and spread around the
       fire in ANGLE. Towers strung along one line give near-parallel sightlines
       and no usable crossing -- the geometry that defeats real triangulation. */
    var specs=[[210,15],[330,14],[95,17],[265,23],[30,26],[150,19]];
    specs.forEach(function(w,n){
      var a=w[0]*Math.PI/180;
      cams.unshift({lon:fire.lon+Math.sin(a)*w[1]/KM_LON,
                    lat:fire.lat+Math.cos(a)*w[1]/KM_LAT, ph:n*2.1});
    });
    var NW=specs.length;

    /* Integrators: a distributed mesh, each owning the patch around it.
       There is no central brain to lose. */
    var ints=[], iguard=0, MIN_SEP=1.35;
    while(ints.length<15 && iguard++<40000){
      var ilon=lo0+rnd()*(lo1-lo0), ilat=la0+rnd()*(la1-la0);
      if(!inPoly(ilon,ilat,CA)) continue;
      var ok=true;
      for(var q=0;q<ints.length;q++){
        if(Math.hypot((ints[q].lon-ilon)*kx,(ints[q].lat-ilat))<MIN_SEP){ok=false;break;}
      }
      if(ok) ints.push({lon:ilon,lat:ilat});
    }
    /* the one that owns the incident */
    var home=0,hd=1e9;
    ints.forEach(function(m,idx){
      var d=Math.hypot((m.lon-fire.lon)*kx,(m.lat-fire.lat));
      if(d<hd){hd=d;home=idx;}
    });

    /* Asynchronous evidence: cameras report at their own pace, some smoke,
       some escalating to fire. Nothing here is synchronised. */
    var EV=[
      [0.330,0,0],[0.352,2,0],[0.371,0,0],[0.389,1,0],[0.404,3,0],
      [0.421,0,1],[0.436,2,0],[0.452,1,1],[0.466,4,0],[0.481,2,1],
      [0.497,5,0],[0.510,0,1],[0.524,3,1],[0.538,1,1],[0.551,4,1]
    ].map(function(e){return {t:e[0],w:e[1],fire:!!e[2]};});

    /* Integrate once to find when it ACTUALLY crosses -- the drone launch is
       driven by the accumulation, not by a hand-picked timestamp. */
    function vAt(p){
      var v=0, last=EV[0].t-0.001;
      for(var n=0;n<EV.length;n++){
        if(EV[n].t>p) break;
        v*=Math.exp(-(EV[n].t-last)/V_TAU); last=EV[n].t;
        v+=EV[n].fire?W_FIRE:W_SMOKE;
      }
      if(p>last) v*=Math.exp(-(p-last)/V_TAU);
      return v;
    }
    var cross=-1;
    for(var s2=0.33;s2<0.75;s2+=0.001){ if(vAt(s2)>=V_TH){cross=s2;break;} }
    if(cross<0) cross=0.58;

    c._cams=cams; c._nw=NW; c._fire=fire; c._ints=ints; c._home=home;
    c._ev=EV; c._vAt=vAt; c._cross=cross;
    /* Drone base: the NEAREST integrator site beyond ~35 km, not the farthest.
       Picking the farthest made the flight read at 179 km, which no drone
       flies -- and the rest of this deck is careful about drone realism. */
    var best=-1,bd=1e9;
    ints.forEach(function(m,idx){
      var d=Math.hypot((m.lon-fire.lon)*KM_LON,(m.lat-fire.lat)*KM_LAT);
      if(d>35 && d<bd){bd=d;best=idx;}
    });
    c._base = best>=0? best : (home===0?1:0);
    c._built=true;
  }

  var cams=c._cams, NW=c._nw, fire=c._fire, ints=c._ints, EV=c._ev;
  var fx=PX(fire.lon), fy=PY(fire.lat), cross=c._cross;
  var t0=performance.now(), DUR=25000;
  var P={dots:0.06,ints:0.15,noise:0.25,smoke:0.33};
  var P_ALERT=cross, P_LAUNCH=cross+0.035, P_ARRIVE=P_LAUNCH+0.20, P_DONE=P_ARRIVE+0.05;

  loop(function(){
    var p=((performance.now()-t0)%DUR)/DUR;
    var now=performance.now()/1000;
    x.clearRect(0,0,W,H);
    x.lineJoin='round'; x.lineCap='round';

    /* ---------- state ---------- */
    var drawn=p<P.dots?Math.min(1,p/P.dots):1;
    if(drawn>=1){
      x.globalAlpha=.05; x.fillStyle=F; x.beginPath();
      CA.forEach(function(q,n){n?x.lineTo(PX(q[0]),PY(q[1])):x.moveTo(PX(q[0]),PY(q[1]));});
      x.closePath(); x.fill(); x.globalAlpha=1;
    }
    x.strokeStyle=F; x.globalAlpha=.5; x.lineWidth=1.3;
    var upto=Math.max(1,Math.floor((CA.length-1)*drawn));
    x.beginPath();
    for(var n1=0;n1<=upto;n1++){var q1=CA[n1];
      n1?x.lineTo(PX(q1[0]),PY(q1[1])):x.moveTo(PX(q1[0]),PY(q1[1]));}
    if(drawn>=1) x.closePath();
    x.stroke(); x.globalAlpha=1;

    /* ---------- integrator territories ---------- */
    if(p>=P.ints){
      var ia=Math.min(1,(p-P.ints)/(P.noise-P.ints));
      ints.forEach(function(m,idx){
        if(idx/ints.length>ia*1.2) return;
        var mx=PX(m.lon), my=PY(m.lat);
        var isHome=(idx===c._home), hot=isHome&&p>=P.smoke;
        var rr=sc*0.95;
        x.globalAlpha=hot?.10:.045; x.fillStyle=A;
        x.beginPath(); x.arc(mx,my,rr,0,7); x.fill();
        x.globalAlpha=hot?.5:.22; x.strokeStyle=A; x.lineWidth=1; x.setLineDash([3,4]);
        x.beginPath(); x.arc(mx,my,rr,0,7); x.stroke(); x.setLineDash([]); x.globalAlpha=1;
        /* the node itself: a square, so it never reads as a camera */
        var s3=hot?5:4;
        x.fillStyle=A; x.globalAlpha=hot?1:.8;
        x.fillRect(mx-s3,my-s3,s3*2,s3*2); x.globalAlpha=1;
        if(hot){
          var pl=(now*1.5)%1;
          x.globalAlpha=(1-pl)*.6; x.strokeStyle=A; x.lineWidth=1.4;
          x.strokeRect(mx-s3-pl*13,my-s3-pl*13,(s3+pl*13)*2,(s3+pl*13)*2);
          x.globalAlpha=1;
        }
      });
    }

    /* ---------- cameras ---------- */
    if(p>=P.dots){
      var appear=Math.min(1,(p-P.dots)/(P.ints-P.dots));
      cams.forEach(function(m,idx){
        if(idx/cams.length>appear*1.15) return;
        var mx=PX(m.lon), my=PY(m.lat);
        var col=D, rr2=1.5, al=.42;
        if(p>=P.noise && p<P.smoke){
          var ph=(now*0.85+m.ph)%6.28;
          if(ph<0.4 && ((idx*29)%11)===0){ col=Y; rr2=2.3; al=.3+.55*(1-ph/0.4); }
        }
        if(idx<NW && p>=P.smoke){
          var seen=false,flame=false,recent=0;
          for(var e2=0;e2<EV.length;e2++){
            if(EV[e2].w!==idx||EV[e2].t>p) continue;
            seen=true; if(EV[e2].fire) flame=true;
            recent=Math.max(recent,1-Math.min(1,(p-EV[e2].t)/0.02));
          }
          if(seen){ col=flame?R:Y; rr2=3+recent*1.6; al=1; }
        }
        x.globalAlpha=al; x.fillStyle=col;
        x.beginPath(); x.arc(mx,my,rr2,0,7); x.fill(); x.globalAlpha=1;
      });
    }

    /* ---------- sightlines, appearing as each report lands ---------- */
    if(p>=P.smoke){
      for(var e3=0;e3<EV.length;e3++){
        var ev=EV[e3]; if(ev.t>p) continue;
        var m3=cams[ev.w], mx3=PX(m3.lon), my3=PY(m3.lat);
        var age=(p-ev.t)/0.10, grow=Math.min(1,age/0.25);
        var fade=Math.max(.25,1-age*0.5);
        x.strokeStyle=ev.fire?R:Y; x.globalAlpha=.42*fade; x.lineWidth=1.1;
        x.setLineDash([4,4]);
        x.beginPath(); x.moveTo(mx3,my3);
        x.lineTo(mx3+(fx-mx3)*grow, my3+(fy-my3)*grow); x.stroke();
        x.setLineDash([]); x.globalAlpha=1;
      }
    }

    /* ---------- alert ---------- */
    if(p>=P_ALERT){
      var ap=(now*1.6)%1;
      x.globalAlpha=(1-ap)*.7; x.strokeStyle=R; x.lineWidth=2;
      x.beginPath(); x.arc(fx,fy,7+ap*28,0,7); x.stroke(); x.globalAlpha=1;
      x.fillStyle=R; x.beginPath(); x.arc(fx,fy,4.5,0,7); x.fill();
      x.strokeStyle=R; x.lineWidth=1.3; x.strokeRect(fx-12,fy-12,24,24);
    }

    /* ---------- drone ---------- */
    if(p>=P_LAUNCH){
      var bm=ints[c._base], bx=PX(bm.lon), by=PY(bm.lat);
      var dp=Math.min(1,(p-P_LAUNCH)/(P_ARRIVE-P_LAUNCH));
      var e4=1-Math.pow(1-dp,3);
      var dx=bx+(fx-bx)*e4, dy=by+(fy-by)*e4;
      x.strokeStyle=A; x.globalAlpha=.3; x.lineWidth=1; x.setLineDash([2,5]);
      x.beginPath(); x.moveTo(bx,by); x.lineTo(dx,dy); x.stroke();
      x.setLineDash([]); x.globalAlpha=1;
      if(dp>=1){ var o=now*2.4; dx=fx+Math.cos(o)*16; dy=fy+Math.sin(o)*9; }
      x.save(); x.translate(dx,dy); x.strokeStyle=A; x.lineWidth=1.5;
      x.beginPath(); x.moveTo(-5.5,-3.5); x.lineTo(5.5,3.5);
      x.moveTo(5.5,-3.5); x.lineTo(-5.5,3.5); x.stroke();
      var spin=(now*22)%6.28;
      [[-5.5,-3.5],[5.5,3.5],[5.5,-3.5],[-5.5,3.5]].forEach(function(r2){
        x.globalAlpha=.7; x.beginPath();
        x.ellipse(r2[0],r2[1],3.6,1.3,spin,0,6.28); x.stroke(); x.globalAlpha=1;});
      x.restore();
      if(dp>=1&&p>=P_DONE){
        x.fillStyle=A; x.font='bold 11px ui-monospace,monospace'; x.textAlign='left';
        x.fillText('confirmed',fx+20,fy-15);
      }
    }

    function panel(px,py,pw,ph,title,sub){
      x.globalAlpha=.94; x.fillStyle=CARD; x.beginPath();
      if(x.roundRect) x.roundRect(px,py,pw,ph,6); else x.rect(px,py,pw,ph);
      x.fill(); x.globalAlpha=1; x.strokeStyle=EDGE; x.lineWidth=1; x.stroke();
      x.fillStyle=D; x.font='9px ui-monospace,monospace'; x.textAlign='left';
      x.fillText(title,px+11,py+14);
      if(sub) x.fillText(sub,px+11,py+26);
    }

    /* ---------- membrane potential -- TOP RIGHT ---------- */
    if(p>=P.smoke-0.02){
      var iw=Math.min(310,W*0.40), ih=Math.min(140,H*0.31);
      var ix=W-iw-14, iy=14;
      panel(ix,iy,iw,ih,'MEMBRANE POTENTIAL',"the integrator's running evidence");

      var gl=ix+42, gr=ix+iw-12, gt=iy+40, gb=iy+ih-26;
      var t1=P.smoke-0.01, t2=Math.min(1,P_LAUNCH+0.05);
      function GX(t){return gl+(t-t1)/(t2-t1)*(gr-gl);}
      function GY(v){return gb-Math.min(v,1.05)/1.05*(gb-gt);}

      x.strokeStyle=R; x.setLineDash([3,3]); x.lineWidth=1;
      x.beginPath(); x.moveTo(gl,GY(V_TH)); x.lineTo(gr,GY(V_TH)); x.stroke(); x.setLineDash([]);
      x.fillStyle=R; x.textAlign='right'; x.font='8px ui-monospace,monospace';
      x.fillText('thresh',gl-4,GY(V_TH)+3);
      x.strokeStyle=D; x.globalAlpha=.3; x.lineWidth=1;
      x.beginPath(); x.moveTo(gl,gt-3); x.lineTo(gl,gb); x.lineTo(gr,gb); x.stroke();
      x.globalAlpha=1;

      var pnow=Math.min(p,t2), started=false;
      x.strokeStyle=A; x.lineWidth=1.8; x.beginPath();
      for(var s5=t1;s5<=pnow;s5+=(t2-t1)/260){
        var gx5=GX(s5), gy5=GY(c._vAt(s5));
        started?x.lineTo(gx5,gy5):(x.moveTo(gx5,gy5),started=true);
      }
      if(started){
        x.stroke();
        x.globalAlpha=.14; x.fillStyle=A; x.beginPath(); x.moveTo(GX(t1),gb);
        for(var s6=t1;s6<=pnow;s6+=(t2-t1)/260) x.lineTo(GX(s6),GY(c._vAt(s6)));
        x.lineTo(GX(pnow),gb); x.closePath(); x.fill(); x.globalAlpha=1;
      }
      EV.forEach(function(e7){
        if(e7.t>pnow) return;
        x.strokeStyle=e7.fire?R:Y; x.lineWidth=1.5;
        x.beginPath(); x.moveTo(GX(e7.t),gb+2); x.lineTo(GX(e7.t),gb+7); x.stroke();
      });
      x.fillStyle=D; x.font='8px ui-monospace,monospace'; x.textAlign='left';
      x.fillText('reports arriving',gl,gb+18);
      if(p>=P_ALERT){
        x.fillStyle=R; x.beginPath(); x.arc(GX(cross),GY(V_TH),3.5,0,7); x.fill();
        x.font='bold 9px ui-monospace,monospace'; x.textAlign='right';
        x.fillText('FIRES → DRONE',ix+iw-11,iy+14);
      }
    }

    /* ---------- legend -- over the ocean, left ---------- */
    if(W>620 && p>=P.dots){
      var lw=196, lh=150, lx=12, ly=Math.max(14,H*0.10);
      panel(lx,ly,lw,lh,'WHAT YOU ARE LOOKING AT','');
      var ex=lx+18, ey=ly+38, row=24;
      function item(icon,title,sub){
        icon(ex,ey);
        x.fillStyle=F; x.font='9px ui-monospace,monospace'; x.textAlign='left';
        x.fillText(title,ex+18,ey-1);
        x.fillStyle=D; x.font='7px ui-monospace,monospace';
        x.fillText(sub,ex+18,ey+8);
        ey+=row;
      }
      item(function(px,py){x.globalAlpha=.55;x.fillStyle=D;
        x.beginPath();x.arc(px,py-3,1.9,0,7);x.fill();x.globalAlpha=1;},
        'camera','336, each unreliable');
      item(function(px,py){x.strokeStyle=A;x.globalAlpha=.45;x.lineWidth=1;
        x.beginPath();x.arc(px,py-3,8,0,7);x.stroke();x.globalAlpha=1;
        x.fillStyle=A;x.fillRect(px-4,py-7,8,8);},
        'integrator + patch','15. no central brain');
      item(function(px,py){x.fillStyle=Y;x.beginPath();x.arc(px,py-3,3,0,7);x.fill();
        x.strokeStyle=Y;x.globalAlpha=.6;x.lineWidth=1.1;
        x.beginPath();x.moveTo(px+6,py-3);x.lineTo(px+13,py-3);x.stroke();x.globalAlpha=1;},
        'smoke reported','weak evidence');
      item(function(px,py){x.fillStyle=R;x.beginPath();x.arc(px,py-3,3,0,7);x.fill();
        x.strokeStyle=R;x.globalAlpha=.6;x.lineWidth=1.1;
        x.beginPath();x.moveTo(px+6,py-3);x.lineTo(px+13,py-3);x.stroke();x.globalAlpha=1;},
        'fire reported','strong evidence');
      item(function(px,py){x.strokeStyle=R;x.lineWidth=1.3;
        x.strokeRect(px-6,py-9,12,12);x.fillStyle=R;
        x.beginPath();x.arc(px,py-3,2.4,0,7);x.fill();},
        'threshold crossed','the integrator fires');
      item(function(px,py){x.strokeStyle=A;x.lineWidth=1.4;
        x.beginPath();x.moveTo(px-5,py-6);x.lineTo(px+5,py);x.moveTo(px+5,py-6);
        x.lineTo(px-5,py);x.stroke();},
        'drone dispatched','looks, then recalled');
    }

    /* ---------- incident close-up -- BOTTOM RIGHT ----------
       At state scale a 20 km triangulation is two pixels wide, so the whole
       point -- several cameras agreeing from different ANGLES -- is invisible.
       This inset is the only place the mechanism can be seen. */
    if(W>620 && p>=P.smoke-0.02){
      var zw=Math.min(300,W*0.38), zh=Math.min(150,H*0.32);
      var zx=W-zw-14, zy=H-zh-34;
      panel(zx,zy,zw,zh,'INCIDENT, CLOSE UP','90 km across');

      var KM_LON2=111*kx, KM_LAT2=111;
      var zl=zx+10, zr=zx+zw-10, zt=zy+34, zb=zy+zh-10;
      var zsc=(zr-zl)/90;
      function ZX(lon){return (zl+zr)/2 + (lon-fire.lon)*KM_LON2*zsc;}
      function ZY(lat){return (zt+zb)/2 - (lat-fire.lat)*KM_LAT2*zsc;}
      x.strokeStyle=D; x.globalAlpha=.5; x.lineWidth=1;
      x.beginPath(); x.moveTo(zl+6,zb-5); x.lineTo(zl+6+20*zsc,zb-5); x.stroke();
      x.fillStyle=D; x.font='7px ui-monospace,monospace'; x.textAlign='left';
      x.fillText('20 km',zl+6,zb-9); x.globalAlpha=1;

      var zfx=ZX(fire.lon), zfy=ZY(fire.lat);
      EV.forEach(function(e8){
        if(e8.t>p) return;
        var m8=cams[e8.w], mx8=ZX(m8.lon), my8=ZY(m8.lat);
        var age8=(p-e8.t)/0.10, grow8=Math.min(1,age8/0.25), fade8=Math.max(.3,1-age8*0.4);
        x.strokeStyle=e8.fire?R:Y; x.globalAlpha=.6*fade8; x.lineWidth=1;
        x.setLineDash([3,3]); x.beginPath(); x.moveTo(mx8,my8);
        x.lineTo(mx8+(zfx-mx8)*grow8, my8+(zfy-my8)*grow8); x.stroke();
        x.setLineDash([]); x.globalAlpha=1;
      });
      for(var w9=0;w9<NW;w9++){
        var m9=cams[w9], seen9=false, fl9=false;
        EV.forEach(function(e9){ if(e9.w===w9&&e9.t<=p){seen9=true; if(e9.fire) fl9=true;} });
        x.fillStyle = seen9?(fl9?R:Y):D; x.globalAlpha=seen9?1:.45;
        x.beginPath(); x.arc(ZX(m9.lon),ZY(m9.lat),seen9?3.2:2.2,0,7); x.fill();
        x.globalAlpha=1;
      }
      if(p>=P_ALERT){
        var za=(now*1.6)%1;
        x.globalAlpha=(1-za)*.7; x.strokeStyle=R; x.lineWidth=1.5;
        x.beginPath(); x.arc(zfx,zfy,5+za*16,0,7); x.stroke(); x.globalAlpha=1;
        x.strokeStyle=R; x.lineWidth=1.2; x.strokeRect(zfx-7,zfy-7,14,14);
        x.fillStyle=R; x.beginPath(); x.arc(zfx,zfy,2.5,0,7); x.fill();
        if(p>=P_LAUNCH){
          x.fillStyle=R; x.font='8px ui-monospace,monospace'; x.textAlign='left';
          x.fillText('one cell',zfx+11,zfy-9);
        }
      }
    }

    /* ---------- narration ---------- */
    var msg,col;
    if(p<P.dots){ msg='California.'; col=D; }
    else if(p<P.ints){ msg='Over a thousand cameras watching the ridgelines.'; col=D; }
    else if(p<P.noise){ msg='And many integrators — each owning a patch. No central brain to lose.'; col=A; }
    else if(p<P.smoke){ msg='Most of what the cameras see is nothing. None of it reaches a person.'; col=Y; }
    else if(p<P_ALERT){ msg='Reports trickle in — smoke, then fire — from different cameras, at their own pace.'; col=Y; }
    else if(p<P_LAUNCH){ msg='Evidence crosses the threshold. The integrator fires.'; col=R; }
    else if(p<P_DONE){ msg='A drone is dispatched to the cell to confirm.'; col=A; }
    else { msg='Confirmed. Total human attention spent: one look.'; col=A; }
    x.textAlign='left'; x.font='12px ui-monospace,monospace'; x.fillStyle=col;
    x.fillText(msg,14,H-11);
  });
};

/* ---------- boot ---------- */
window.addEventListener('resize',function(){clearTimeout(window._rz);window._rz=setTimeout(restart,180);});
go(0);
})();
"""
