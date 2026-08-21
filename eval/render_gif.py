"""Render the statewide sequence to a GIF.

A faithful port of ANIM.statewide from the deck. Same polygon, same seeded
RNG, same event schedule, same membrane integration -- so the GIF and the live
slide tell the identical story.
"""
import math, pathlib
from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path(__file__).resolve().parent
SS = 3                      # supersample factor for smooth edges
W, H = 940, 664
FRAMES, FPS = 150, 11

# ---- Kernwerk light palette ----
BG   = (236,240,241); FRONT=(52,73,94); SELECT=(0,184,148)
RED  = (238,82,83);   YEL  =(255,168,1); CARD=(255,255,255)
DIM  = (52,73,94)

FONT = "/System/Library/Fonts/Menlo.ttc"
def f(sz): return ImageFont.truetype(FONT, sz*SS)

CA=[(-124.21,42.00),(-120.00,42.00),(-120.00,39.32),(-114.64,35.00),(-114.63,34.87),
(-114.47,34.71),(-114.14,34.30),(-114.44,34.08),(-114.53,33.55),(-114.72,33.40),
(-114.68,33.04),(-114.52,32.76),(-114.72,32.71),(-117.13,32.53),(-117.25,32.67),
(-117.32,33.10),(-117.60,33.39),(-118.09,33.74),(-118.41,33.74),(-118.52,34.02),
(-119.21,34.15),(-119.56,34.42),(-120.47,34.45),(-120.64,34.58),(-120.62,35.13),
(-120.90,35.42),(-121.28,35.67),(-121.90,36.31),(-121.89,36.58),(-121.79,36.80),
(-121.81,36.93),(-122.41,37.20),(-122.52,37.78),(-122.98,38.11),(-123.07,38.32),
(-123.73,38.95),(-123.83,39.77),(-124.11,40.10),(-124.41,40.44),(-124.15,41.05),
(-124.25,41.79),(-124.21,42.00)]

def in_poly(px,py,poly):
    c=False; b=len(poly)-1
    for a in range(len(poly)):
        xi,yi=poly[a]; xj,yj=poly[b]
        if (yi>py)!=(yj>py) and px < (xj-xi)*(py-yi)/(yj-yi)+xi: c=not c
        b=a
    return c

def mulberry(s):
    st=[s & 0xFFFFFFFF]
    def r():
        st[0]=(st[0]+0x6D2B79F5)&0xFFFFFFFF
        t=st[0]
        t=(t ^ (t>>15))*(1|t)&0xFFFFFFFF
        t=(t+((t ^ (t>>7))*(61|t)&0xFFFFFFFF))&0xFFFFFFFF ^ t
        return ((t ^ (t>>14))&0xFFFFFFFF)/4294967296
    return r

W_SMOKE,W_FIRE,V_TAU,V_TH = 0.085,0.20,0.085,0.80
EV=[(0.330,0,0),(0.352,2,0),(0.371,0,0),(0.389,1,0),(0.404,3,0),
    (0.421,0,1),(0.436,2,0),(0.452,1,1),(0.466,4,0),(0.481,2,1),
    (0.497,5,0),(0.510,0,1),(0.524,3,1),(0.538,1,1),(0.551,4,1)]

def v_at(p):
    v=0.0; last=EV[0][0]-0.001
    for t,w,fr in EV:
        if t>p: break
        v*=math.exp(-(t-last)/V_TAU); last=t
        v+= W_FIRE if fr else W_SMOKE
    if p>last: v*=math.exp(-(p-last)/V_TAU)
    return v

CROSS=0.58
for i in range(330,750):
    if v_at(i/1000)>=V_TH: CROSS=i/1000; break

# ---- projection ----
lo0=min(p[0] for p in CA); lo1=max(p[0] for p in CA)
la0=min(p[1] for p in CA); la1=max(p[1] for p in CA)
kx=math.cos((la0+la1)/2*math.pi/180)
MAPW = W-330                      # leave room for the right-hand panels
pad=18
availW, availH = MAPW-2*pad, H-2*pad-26
sc=min(availW/((lo1-lo0)*kx), availH/(la1-la0))
offX=pad+(availW-(lo1-lo0)*kx*sc)/2
offY=pad+(availH-(la1-la0)*sc)/2
PX=lambda lon:(offX+(lon-lo0)*kx*sc)
PY=lambda lat:(offY+(la1-lat)*sc)

# ---- build the world (same seed / rules as the JS) ----
rnd=mulberry(20260906); cams=[]; guard=0
while len(cams)<330 and guard<60000:
    guard+=1
    lon=lo0+rnd()*(lo1-lo0); lat=la0+rnd()*(la1-la0)
    if not in_poly(lon,lat,CA): continue
    if lon>-116.5 and lat<35.5 and rnd()<0.6: continue
    cams.append({'lon':lon,'lat':lat,'ph':rnd()*6.28})
FIRE={'lon':-120.72,'lat':39.30}
KM_LAT,KM_LON=111,111*kx
for n,(a_deg,d) in enumerate([(210,15),(330,14),(95,17),(265,23),(30,26),(150,19)]):
    a=a_deg*math.pi/180
    cams.insert(0,{'lon':FIRE['lon']+math.sin(a)*d/KM_LON,
                   'lat':FIRE['lat']+math.cos(a)*d/KM_LAT,'ph':n*2.1})
NW=6
ints=[]; ig=0
while len(ints)<15 and ig<40000:
    ig+=1
    ilon=lo0+rnd()*(lo1-lo0); ilat=la0+rnd()*(la1-la0)
    if not in_poly(ilon,ilat,CA): continue
    if any(math.hypot((q['lon']-ilon)*kx,(q['lat']-ilat))<1.35 for q in ints): continue
    ints.append({'lon':ilon,'lat':ilat})
HOME=min(range(len(ints)),key=lambda i:math.hypot((ints[i]['lon']-FIRE['lon'])*kx,
                                                  (ints[i]['lat']-FIRE['lat'])))
cand=[(math.hypot((m['lon']-FIRE['lon'])*KM_LON,(m['lat']-FIRE['lat'])*KM_LAT),i)
      for i,m in enumerate(ints)]
BASE=min([c for c in cand if c[0]>35])[1]

P={'dots':0.06,'ints':0.15,'noise':0.25,'smoke':0.33}
P_ALERT=CROSS; P_LAUNCH=CROSS+0.035; P_ARRIVE=P_LAUNCH+0.20; P_DONE=P_ARRIVE+0.05
FX,FY=PX(FIRE['lon']),PY(FIRE['lat'])

def S(v): return int(round(v*SS))

def frame(p):
    im=Image.new("RGB",(W*SS,H*SS),BG)
    ov=Image.new("RGBA",(W*SS,H*SS),(0,0,0,0))
    d=ImageDraw.Draw(ov)
    now=p*(FRAMES/FPS)

    # ---- state ----
    drawn=min(1.0,p/P['dots']) if p<P['dots'] else 1.0
    pts=[(S(PX(q[0])),S(PY(q[1]))) for q in CA]
    if drawn>=1: d.polygon(pts,fill=FRONT+(10,))

    # ---- integrator territories ----
    if p>=P['ints']:
        ia=min(1.0,(p-P['ints'])/(P['noise']-P['ints']))
        for idx,m in enumerate(ints):
            if idx/len(ints)>ia*1.2: continue
            mx,my=S(PX(m['lon'])),S(PY(m['lat'])); rr=S(sc*0.55)
            hot = (idx==HOME and p>=P['smoke'])
            d.ellipse([mx-rr,my-rr,mx+rr,my+rr],
                      fill=SELECT+(20 if hot else 7,),
                      outline=SELECT+(120 if hot else 38,),width=S(1))
            s3=S(5 if hot else 4)
            d.rectangle([mx-s3,my-s3,mx+s3,my+s3],fill=SELECT+(255 if hot else 204,))
            if hot:
                pl=(now*1.5)%1; g=S(pl*13)
                d.rectangle([mx-s3-g,my-s3-g,mx+s3+g,my+s3+g],
                            outline=SELECT+(int((1-pl)*150),),width=S(1.4))

    # state outline last, over the territories, so California stays readable
    upto=max(1,int((len(CA)-1)*drawn))
    d.line(pts[:upto+1],fill=FRONT+(150,),width=S(1.3),joint="curve")

    # ---- cameras ----
    if p>=P['dots']:
        ap=min(1.0,(p-P['dots'])/(P['ints']-P['dots']))
        for idx,m in enumerate(cams):
            if idx/len(cams)>ap*1.15: continue
            mx,my=S(PX(m['lon'])),S(PY(m['lat']))
            col,rr2,al=DIM,1.7,135
            if P['noise']<=p<P['smoke']:
                ph=(now*0.85+m['ph'])%6.28
                if ph<0.4 and (idx*29)%11==0:
                    col,rr2,al=YEL,2.3,int((0.3+0.55*(1-ph/0.4))*255)
            if idx<NW and p>=P['smoke']:
                seen=flame=False; recent=0
                for t,w,fr in EV:
                    if w!=idx or t>p: continue
                    seen=True; flame=flame or bool(fr)
                    recent=max(recent,1-min(1,(p-t)/0.02))
                if seen: col,rr2,al=(RED if flame else YEL),3+recent*1.6,255
            r=S(rr2)
            d.ellipse([mx-r,my-r,mx+r,my+r],fill=col+(al,))

    # ---- sightlines ----
    if p>=P['smoke']:
        for t,w,fr in EV:
            if t>p: continue
            m=cams[w]; mx,my=PX(m['lon']),PY(m['lat'])
            age=(p-t)/0.10; grow=min(1,age/0.25); fade=max(.25,1-age*0.5)
            ex,ey=mx+(FX-mx)*grow,my+(FY-my)*grow
            # dashed
            n=int(math.hypot(ex-mx,ey-my)/6)+1
            for k in range(0,n,2):
                a1,a2=k/n,min(1,(k+1)/n)
                d.line([S(mx+(ex-mx)*a1),S(my+(ey-my)*a1),
                        S(mx+(ex-mx)*a2),S(my+(ey-my)*a2)],
                       fill=(RED if fr else YEL)+(int(107*fade),),width=S(1.1))

    # ---- alert ----
    if p>=P_ALERT:
        a=(now*1.6)%1; r=S(7+a*28)
        d.ellipse([S(FX)-r,S(FY)-r,S(FX)+r,S(FY)+r],outline=RED+(int((1-a)*180),),width=S(2))
        r2=S(4.5); d.ellipse([S(FX)-r2,S(FY)-r2,S(FX)+r2,S(FY)+r2],fill=RED+(255,))
        b=S(12); d.rectangle([S(FX)-b,S(FY)-b,S(FX)+b,S(FY)+b],outline=RED+(255,),width=S(1.3))

    # ---- drone ----
    if p>=P_LAUNCH:
        bm=ints[BASE]; bx,by=PX(bm['lon']),PY(bm['lat'])
        dp=min(1.0,(p-P_LAUNCH)/(P_ARRIVE-P_LAUNCH)); e=1-(1-dp)**3
        dx,dy=bx+(FX-bx)*e,by+(FY-by)*e
        n=int(math.hypot(dx-bx,dy-by)/8)+1
        for k in range(0,n,2):
            a1,a2=k/n,min(1,(k+1)/n)
            d.line([S(bx+(dx-bx)*a1),S(by+(dy-by)*a1),
                    S(bx+(dx-bx)*a2),S(by+(dy-by)*a2)],fill=SELECT+(77,),width=S(1))
        if dp>=1:
            o=now*2.4; dx,dy=FX+math.cos(o)*16,FY+math.sin(o)*9
        d.line([S(dx-5.5),S(dy-3.5),S(dx+5.5),S(dy+3.5)],fill=SELECT+(255,),width=S(1.5))
        d.line([S(dx+5.5),S(dy-3.5),S(dx-5.5),S(dy+3.5)],fill=SELECT+(255,),width=S(1.5))
        for rx,ry in [(-5.5,-3.5),(5.5,3.5),(5.5,-3.5),(-5.5,3.5)]:
            d.ellipse([S(dx+rx-3.6),S(dy+ry-1.3),S(dx+rx+3.6),S(dy+ry+1.3)],
                      outline=SELECT+(180,),width=S(1.2))
        if dp>=1 and p>=P_DONE:
            d.text((S(FX+20),S(FY-22)),"confirmed",font=f(11),fill=SELECT+(255,))
    return im,ov,d,now


def panels(im,ov,d,p,now):
    """Membrane panel TOP RIGHT, legend under it, narration bottom left."""
    PANX, PANW = W-318, 302

    # ================= membrane potential (top right) =================
    py,ph = 16,152
    d.rounded_rectangle([S(PANX),S(py),S(PANX+PANW),S(py+ph)],radius=S(6),
                        fill=CARD+(242,),outline=FRONT+(28,),width=S(1))
    d.text((S(PANX+12),S(py+10)),"MEMBRANE POTENTIAL",font=f(9),fill=DIM+(150,))
    d.text((S(PANX+12),S(py+23)),"the integrator's running evidence",font=f(9),fill=DIM+(120,))

    gl,gr = PANX+46, PANX+PANW-14
    gt,gb = py+44, py+ph-30
    t1,t2 = P['smoke']-0.01, min(1.0,P_LAUNCH+0.05)
    GX=lambda t: gl+(t-t1)/(t2-t1)*(gr-gl)
    GY=lambda v: gb-min(v,1.05)/1.05*(gb-gt)

    d.line([S(gl),S(GY(V_TH)),S(gr),S(GY(V_TH))],fill=RED+(140,),width=S(1))
    d.text((S(gl-42),S(GY(V_TH)-5)),"thresh",font=f(8),fill=RED+(200,))
    d.line([S(gl),S(gt-4),S(gl),S(gb),S(gr),S(gb)],fill=DIM+(70,),width=S(1))

    if p>=t1:
        pn=min(p,t2); steps=240
        pts=[]; xs=[]
        for k in range(steps+1):
            t=t1+(pn-t1)*k/steps
            pts.append((S(GX(t)),S(GY(v_at(t))))); xs.append(GX(t))
        if len(pts)>1:
            d.polygon([(S(gl),S(gb))]+pts+[(S(xs[-1]),S(gb))],fill=SELECT+(36,))
            d.line(pts,fill=SELECT+(255,),width=S(1.8),joint="curve")
        for t,w,fr in EV:
            if t>pn: continue
            d.line([S(GX(t)),S(gb+2),S(GX(t)),S(gb+7)],
                   fill=(RED if fr else YEL)+(255,),width=S(1.6))
        d.text((S(gl),S(gb+11)),"reports arriving",font=f(8),fill=DIM+(120,))
        if p>=P_ALERT:
            r=S(3.5); d.ellipse([S(GX(CROSS))-r,S(GY(V_TH))-r,S(GX(CROSS))+r,S(GY(V_TH))+r],
                                fill=RED+(255,))
            d.text((S(PANX+PANW-96),S(py+10)),"FIRES → DRONE",font=f(9),fill=RED+(255,))

    # ================= legend =================
    ly,lh = py+ph+14, 228
    d.rounded_rectangle([S(PANX),S(ly),S(PANX+PANW),S(ly+lh)],radius=S(6),
                        fill=CARD+(242,),outline=FRONT+(28,),width=S(1))
    d.text((S(PANX+12),S(ly+10)),"WHAT YOU ARE LOOKING AT",font=f(9),fill=DIM+(150,))
    gx,gy = PANX+22, ly+32
    row=32

    def lbl(yy,title,sub):
        d.text((S(gx+26),S(yy-6)),title,font=f(10),fill=FRONT+(255,))
        d.text((S(gx+26),S(yy+6)),sub,font=f(8),fill=DIM+(140,))

    # camera
    r=S(1.9); d.ellipse([S(gx)-r,S(gy)-r,S(gx)+r,S(gy)+r],fill=DIM+(120,))
    lbl(gy,"camera","336 of them, each unreliable")
    # integrator
    gy+=row; s3=S(4.5)
    d.ellipse([S(gx-11),S(gy-11),S(gx+11),S(gy+11)],outline=SELECT+(90,),width=S(1))
    d.rectangle([S(gx)-s3,S(gy)-s3,S(gx)+s3,S(gy)+s3],fill=SELECT+(255,))
    lbl(gy,"integrator + territory","15 of them. no central brain")
    # smoke
    gy+=row; r=S(3)
    d.ellipse([S(gx)-r,S(gy)-r,S(gx)+r,S(gy)+r],fill=YEL+(255,))
    d.line([S(gx+7),S(gy),S(gx+15),S(gy)],fill=YEL+(160,),width=S(1.2))
    lbl(gy,"smoke reported","weak evidence, one direction")
    # fire
    gy+=row; r=S(3)
    d.ellipse([S(gx)-r,S(gy)-r,S(gx)+r,S(gy)+r],fill=RED+(255,))
    d.line([S(gx+7),S(gy),S(gx+15),S(gy)],fill=RED+(160,),width=S(1.2))
    lbl(gy,"fire reported","strong evidence")
    # alert
    gy+=row; b=S(6)
    d.rectangle([S(gx)-b,S(gy)-b,S(gx)+b,S(gy)+b],outline=RED+(255,),width=S(1.4))
    r=S(2.5); d.ellipse([S(gx)-r,S(gy)-r,S(gx)+r,S(gy)+r],fill=RED+(255,))
    lbl(gy,"threshold crossed","the integrator fires")
    # drone
    gy+=row
    d.line([S(gx-5),S(gy-3),S(gx+5),S(gy+3)],fill=SELECT+(255,),width=S(1.5))
    d.line([S(gx+5),S(gy-3),S(gx-5),S(gy+3)],fill=SELECT+(255,),width=S(1.5))
    for rx,ry in [(-5,-3),(5,3),(5,-3),(-5,3)]:
        d.ellipse([S(gx+rx-3.2),S(gy+ry-1.2),S(gx+rx+3.2),S(gy+ry+1.2)],
                  outline=SELECT+(190,),width=S(1))
    lbl(gy,"drone dispatched","goes and looks. then recalled")

    # ================= incident, close up =================
    # At state scale a 20 km triangulation is two pixels wide, so the whole
    # point -- three cameras agreeing from different angles -- is invisible.
    # This inset is the only place the mechanism can actually be seen.
    zy,zh = ly+lh+14, 172
    d.rounded_rectangle([S(PANX),S(zy),S(PANX+PANW),S(zy+zh)],radius=S(6),
                        fill=CARD+(242,),outline=FRONT+(28,),width=S(1))
    d.text((S(PANX+12),S(zy+10)),"INCIDENT, CLOSE UP",font=f(9),fill=DIM+(150,))
    d.text((S(PANX+12),S(zy+23)),"90 km across",font=f(9),fill=DIM+(120,))

    zl,zr,zt,zb = PANX+10, PANX+PANW-10, zy+36, zy+zh-10
    KM_W=90.0; zscale=(zr-zl)/KM_W
    ZX=lambda lon:(zl+zr)/2 + (lon-FIRE['lon'])*KM_LON*zscale
    ZY=lambda lat:(zt+zb)/2 - (lat-FIRE['lat'])*KM_LAT*zscale

    # scale bar
    d.line([S(zl+8),S(zb-6),S(zl+8+20*zscale),S(zb-6)],fill=DIM+(120,),width=S(1))
    d.text((S(zl+8),S(zb-18)),"20 km",font=f(8),fill=DIM+(120,))

    zfx,zfy = ZX(FIRE['lon']),ZY(FIRE['lat'])
    if p>=P['smoke']:
        for t,w,fr in EV:
            if t>p: continue
            m=cams[w]; mx,my=ZX(m['lon']),ZY(m['lat'])
            grow=min(1,((p-t)/0.10)/0.25); fade=max(.3,1-((p-t)/0.10)*0.4)
            ex,ey=mx+(zfx-mx)*grow,my+(zfy-my)*grow
            n=int(math.hypot(ex-mx,ey-my)/5)+1
            for k in range(0,n,2):
                a1,a2=k/n,min(1,(k+1)/n)
                d.line([S(mx+(ex-mx)*a1),S(my+(ey-my)*a1),
                        S(mx+(ex-mx)*a2),S(my+(ey-my)*a2)],
                       fill=(RED if fr else YEL)+(int(150*fade),),width=S(1))
    for idx in range(NW):
        m=cams[idx]; mx,my=ZX(m['lon']),ZY(m['lat'])
        seen=flame=False
        if p>=P['smoke']:
            for t,w,fr in EV:
                if w==idx and t<=p:
                    seen=True; flame=flame or bool(fr)
        col=(RED if flame else YEL) if seen else DIM
        r=S(3.2 if seen else 2.2)
        d.ellipse([S(mx)-r,S(my)-r,S(mx)+r,S(my)+r],fill=col+(255 if seen else 120,))
    if p>=P_ALERT:
        a=(now*1.6)%1; r=S(5+a*16)
        d.ellipse([S(zfx)-r,S(zfy)-r,S(zfx)+r,S(zfy)+r],
                  outline=RED+(int((1-a)*170),),width=S(1.5))
        b=S(7); d.rectangle([S(zfx)-b,S(zfy)-b,S(zfx)+b,S(zfy)+b],outline=RED+(255,),width=S(1.2))
        r2=S(2.5); d.ellipse([S(zfx)-r2,S(zfy)-r2,S(zfx)+r2,S(zfy)+r2],fill=RED+(255,))
        if p>=P_LAUNCH:
            d.text((S(zfx+12),S(zfy-20)),"one cell",font=f(8),fill=RED+(220,))

    # ================= narration =================
    if p<P['dots']: msg,col="California.",DIM
    elif p<P['ints']: msg,col="Over a thousand cameras watching the ridgelines.",DIM
    elif p<P['noise']: msg,col="And many integrators — each owning a patch. No central brain to lose.",SELECT
    elif p<P['smoke']: msg,col="Most of what they see is nothing. None of it reaches a person.",YEL
    elif p<P_ALERT: msg,col="Reports trickle in — smoke, then fire — from different cameras, at their own pace.",YEL
    elif p<P_LAUNCH: msg,col="Evidence crosses the threshold. The integrator fires.",RED
    elif p<P_DONE: msg,col="A drone is dispatched to the cell to confirm.",SELECT
    else: msg,col="Confirmed. Total human attention spent: one look.",SELECT
    d.text((S(16),S(H-26)),msg,font=f(11),fill=col+(255,))
    d.text((S(16),S(H-13)),"KERNWERK  ·  wildfire integrator",font=f(9),fill=DIM+(110,))



def build_palette():
    """A designed palette, not a statistical one.

    Median cut spends its slots where the PIXELS are -- background and greys --
    and quietly discards the colours that carry MEANING. At 96 colours it put
    amber 126 units away from itself, collapsing "smoke" onto "fire" and
    destroying the legend. Every pixel here is an alpha blend of five known
    brand colours over one of two grounds, so the exact set can be enumerated
    instead of guessed.
    """
    def blend(base, c, a):
        return tuple(int(round(base[i]*(1-a) + c[i]*a)) for i in range(3))
    fg = [FRONT, SELECT, RED, YEL, (255,255,255), (0,0,0)]
    alphas = [0.025,0.05,0.08,0.11,0.15,0.19,0.24,0.30,0.37,0.45,
              0.54,0.63,0.72,0.81,0.90,1.0]
    cols, seen = [], set()
    for base in (BG, CARD):
        for c in fg:
            for a in alphas:
                v = blend(base, c, a)
                if v not in seen:
                    seen.add(v); cols.append(v)
    for g in range(0, 256, 16):                 # neutral safety ramp
        v = (g, g, g)
        if v not in seen: seen.add(v); cols.append(v)
    cols = cols[:256]
    flat = [ch for c in cols for ch in c] + [0]*(768 - len(cols)*3)
    pim = Image.new("P", (1, 1)); pim.putpalette(flat)
    return pim

def render(scale=1.0, nframes=210, frame_ms=80, dither=False):
    """Render, then squeeze.

    A GIF of this is mostly static furniture -- panels, legend, the state
    outline -- with a little motion in three places. So: one global palette
    for the whole sequence (no per-frame palette drift, which is what makes
    naive GIFs enormous), disposal=1 so the encoder can delta-encode the
    unchanged regions, and a modest colour count since the palette is small
    by design.
    """
    # GIF stores frame delay in HUNDREDTHS of a second, so any duration that
    # is not a multiple of 10 ms is silently rounded down -- 1000/12 = 83 ms
    # became 80 ms and the whole loop ran 4% fast. Specify the delay directly
    # in a legal unit instead of deriving it from a frame rate.
    assert frame_ms % 10 == 0, "frame_ms must be a multiple of 10"
    ow,oh = int(W*scale), int(H*scale)
    frames=[]
    for k in range(nframes):
        p=k/nframes
        im,ov,d,now=frame(p)
        panels(im,ov,d,p,now)
        im=Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB")
        frames.append(im.resize((ow,oh),Image.LANCZOS))

    master=build_palette()
    dm = Image.FLOYDSTEINBERG if dither else Image.NONE
    pal=[fr.quantize(palette=master,dither=dm) for fr in frames]

    out=OUT/"wildfire-integrator.gif"
    pal[0].save(out,save_all=True,append_images=pal[1:],
                duration=frame_ms,loop=0,optimize=True,disposal=1)
    mb=out.stat().st_size/1024/1024
    print(f"wrote {out.name}  {ow}x{oh}  {len(pal)} frames  "
          f"{nframes*frame_ms/1000:.2f}s @ {1000/frame_ms:.1f}fps  {mb:.2f} MB")

    for tag,pp in [("a_network",0.22),("b_noise",0.29),("c_reports",0.45),
                   ("d_fires",0.60),("e_drone",0.72),("f_done",0.90)]:
        im,ov,d,now=frame(pp); panels(im,ov,d,pp,now)
        Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB")\
             .resize((ow,oh),Image.LANCZOS).save(OUT/f"still_{tag}.png")
    return mb

if __name__=="__main__":
    print(f"threshold crosses at p={CROSS:.3f}  cameras={len(cams)}  integrators={len(ints)}")
    render()
