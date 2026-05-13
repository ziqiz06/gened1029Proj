"""
visuals.py
Voxel / block-game style HTML canvas for cosmic stages + SVG cross-section diagrams.
Drop-in replacement for the original visuals.py API.
"""
import json
import math
import random
from simulation import World


# ── Multi-planet system builder ───────────────────────────────────────────────

def _au_to_orbit_r(au: float) -> int:
    """Sqrt-compressed AU → canvas pixels so inner and outer planets both fit."""
    return min(280, max(55, int(60 + 82 * (au ** 0.38))))


def _system_planets(world: World) -> list[dict]:
    """Build a realistic multi-planet list for the solar_system canvas."""
    rng      = random.Random(42)   # deterministic so canvas is stable
    user_r   = _au_to_orbit_r(world.distance_au)
    planets  = []

    if world.journey == "star_system":
        # Show up to num_planets at realistic spacings
        distances = [0.35, 0.7, 1.0, 1.5, 2.2, 3.5, 5.2, 8.0]
        for i, d in enumerate(distances[: world.num_planets]):
            is_giant = d > 2.0
            planets.append({
                "name":     f"P{i+1}",
                "color":    "#c87040" if is_giant
                            else rng.choice(["#aa6644", "#886633", "#cc7733"]),
                "orbit_r":  _au_to_orbit_r(d),
                "size":     13 if is_giant else 6,
                "is_earth": False,
                "has_life": False,
            })
    else:
        # Add 2–3 background planets spread around the user's world
        used = {user_r}
        for d in [0.35, 0.7, 1.5, 2.5, 5.0]:
            r = _au_to_orbit_r(d)
            if any(abs(r - u) < 28 for u in used):
                continue
            used.add(r)
            is_giant = d > 2.0
            planets.append({
                "name":     "",
                "color":    "#c87040" if is_giant
                            else rng.choice(["#aa6644", "#886633", "#cc7733"]),
                "orbit_r":  r,
                "size":     14 if is_giant else 5,
                "is_earth": False,
                "has_life": False,
            })
            if len(planets) >= 3:
                break

        # Always show Earth as a reference unless this IS Earth
        earth_r = _au_to_orbit_r(1.0)
        if not world._is_earth and abs(earth_r - user_r) >= 22:
            planets.append({
                "name":     "Earth",
                "color":    "#2a6db5",
                "orbit_r":  earth_r,
                "size":     9,
                "is_earth": True,
                "has_life": True,
            })

    # User's planet last so it renders on top
    planets.append({
        "name":     world.display_name,
        "color":    world.color,
        "orbit_r":  user_r,
        "size":     11,
        "is_earth": world._is_earth,
        "has_life": world.hab_label in ("Life Confirmed", "Possible Life"),
    })

    planets.sort(key=lambda p: p["orbit_r"])
    return planets


# ── Stage canvas ──────────────────────────────────────────────────────────────

def stage_canvas(mode: str, world: World | None = None) -> str:
    """
    Return a self-contained HTML page with an animated voxel-style canvas.
    In solar_system mode, renders a full multi-planet system.
    """
    planet_data = "[]"
    if world and mode == "solar_system":
        planet_data = json.dumps(_system_planets(world))

    return f"""<!DOCTYPE html>
<html>
<head><style>
html,body{{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#05070f;}}
canvas{{display:block;width:100%;height:100%;image-rendering:pixelated;background:#05070f;}}
</style></head>
<body>
<canvas id="c"></canvas>
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
// Fill the iframe completely — resolution matches actual rendered size
cv.width=cv.clientWidth||620;
cv.height=cv.clientHeight||440;
const W=cv.width,H=cv.height,CX=W/2,CY=H/2;
const MODE='{mode}';
const PLANETS={planet_data};
let t=0;

ctx.imageSmoothingEnabled=false;

const block=8;
const stars=Array.from({{length:150}},()=>({{
  x:Math.floor(Math.random()*W/block)*block,
  y:Math.floor(Math.random()*H/block)*block,
  s:[2,3,4,5][Math.floor(Math.random()*4)],
  a:.35+Math.random()*.65
}}));

function bg(){{
  ctx.fillStyle='#05070f';
  ctx.fillRect(0,0,W,H);
  // subtle pixel-grid sky
  ctx.globalAlpha=.09;
  ctx.strokeStyle='#20304a';
  for(let x=0;x<W;x+=block*3){{ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}}
  for(let y=0;y<H;y+=block*3){{ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}}
  ctx.globalAlpha=1;
}}

function rect(x,y,w,h,c,a=1){{
  ctx.globalAlpha=a;ctx.fillStyle=c;
  ctx.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h));
  ctx.globalAlpha=1;
}}

function blockCircle(cx,cy,r,c,step=8,a=1){{
  for(let y=-r;y<=r;y+=step) for(let x=-r;x<=r;x+=step){{
    if(x*x+y*y<=r*r) rect(cx+x,cy+y,step,step,c,a);
  }}
}}

function shadedBlockCircle(cx,cy,r,colors,step=8){{
  for(let y=-r;y<=r;y+=step) for(let x=-r;x<=r;x+=step){{
    if(x*x+y*y<=r*r){{
      const shade=(x-y+r*2)/(r*4);
      const idx=Math.max(0,Math.min(colors.length-1,Math.floor(shade*colors.length)));
      rect(cx+x,cy+y,step,step,colors[idx]);
    }}
  }}
  // chunky outline
  ctx.strokeStyle='rgba(0,0,0,.45)';ctx.lineWidth=3;
  ctx.strokeRect(cx-r,cy-r,r*2,r*2);
}}

function drawStars(){{
  stars.forEach((s,i)=>{{
    const blink=.6+.4*Math.sin(t*3+i);
    rect(s.x,s.y,s.s,s.s,'#e8f3ff',s.a*blink);
  }});
}}

function drawSun(){{
  const pulse=Math.sin(t*2)*4;
  blockCircle(CX,CY,64+pulse,'rgba(255,140,0,.16)',8,.85);
  blockCircle(CX,CY,48+pulse,'rgba(255,196,0,.22)',8,.95);
  shadedBlockCircle(CX,CY,34+pulse,['#ff7b22','#ff9d1c','#ffc72d','#fff2a6'],8);
}}

function drawOrbit(r){{
  ctx.strokeStyle='rgba(135,170,210,.18)';
  ctx.lineWidth=2;
  ctx.setLineDash([8,8]);
  ctx.beginPath();ctx.ellipse(CX,CY,r,r*.72,0,0,Math.PI*2);ctx.stroke();
  ctx.setLineDash([]);
}}

function drawPlanets(){{
  PLANETS.forEach((p,i)=>{{
    drawOrbit(p.orbit_r);
    const spd=.28/(p.orbit_r*.012), ang=t*spd+i*.78;
    const px=CX+Math.cos(ang)*p.orbit_r;
    const py=CY+Math.sin(ang)*p.orbit_r*.72;
    if(p.is_earth||p.has_life) blockCircle(px,py,p.size*2.3,p.is_earth?'rgba(80,180,255,.18)':'rgba(80,255,120,.16)',8,.9);
    shadedBlockCircle(px,py,p.size,[p.color,'#9bd6ff','#ffffff'],4);
    if(p.is_earth||p.has_life){{
      rect(px-4,py-2,5,5,'#4fbd55');
      rect(px+3,py+3,4,4,'#3da34a');
    }}
    ctx.fillStyle=p.is_earth?'#aee9ff':'#d0d0d0';
    ctx.font=p.is_earth?'bold 10px monospace':'9px monospace';
    ctx.fillText(p.name,px+p.size+8,py+4);
  }});
}}

// Uniform grid of particles — NOT centred on one point.
// Each particle stores a normalised position in [-1,1] space.
// All positions scale by the same factor → every point recedes from every other equally.
const bangGrid=Array.from({{length:63}},(_,i)=>{{
  const col=['#ffffff','#ffe8a0','#ffc870','#ff9040','#88c8ff','#a8b8ff'][(i*7+3)%6];
  return{{
    nx:((i%9)/8)*1.8-0.9,
    ny:(Math.floor(i/9)/6)*1.6-0.8,
    phase:(i*1.618)%(Math.PI*2),
    col
  }};
}});

function bigbang(){{
  const sec=t/.016;

  if(sec<2.5){{
    // Dense hot state: uniform glow everywhere — no single point
    const h=.5+.5*Math.sin(t*15);
    rect(0,0,W,H,'#ffffff',h*.35);
    rect(0,0,W,H,'#ffe0a0',h*.2);
    for(let i=0;i<18;i++){{
      rect(CX+(((i*73)%W)-W/2)*.9,CY+(((i*53)%H)-H/2)*.8,5,5,'#ffffff',.8);
    }}
    return;
  }}

  drawStars();
  const age=Math.min((sec-2.5)/8,1);
  // Particles start spread at 20% of canvas, expand to 47% — never cluster at one point
  const minSpread=0.20, maxSpread=0.47;
  const scale=minSpread+age*(maxSpread-minSpread);

  // Cooling colour: white-hot → orange → dim red
  const heat=1-age;
  const cr=255,cg=Math.floor(100+heat*140),cb=Math.floor(heat*70);
  const hotCol=`rgb(${{cr}},${{cg}},${{cb}})`;

  // Space-fabric grid — stretches as scale increases, always visible
  {{
    ctx.globalAlpha=.14*(1-age*.5);
    ctx.strokeStyle=hotCol; ctx.lineWidth=1;
    for(let i=0;i<=8;i++){{
      const x=CX+((i/8)*2-1)*W*.46*scale;
      if(x<-10||x>W+10)continue;
      ctx.beginPath();ctx.moveTo(x,CY-H*.44*scale);ctx.lineTo(x,CY+H*.44*scale);ctx.stroke();
    }}
    for(let j=0;j<=6;j++){{
      const y=CY+((j/6)*2-1)*H*.44*scale;
      if(y<-10||y>H+10)continue;
      ctx.beginPath();ctx.moveTo(CX-W*.46*scale,y);ctx.lineTo(CX+W*.46*scale,y);ctx.stroke();
    }}
    ctx.globalAlpha=1;
  }}

  // Uniformly distributed particles — spacing visibly increases each second
  bangGrid.forEach((p,i)=>{{
    const px=CX+p.nx*W*scale;
    const py=CY+p.ny*H*scale;
    if(px<-8||px>W+8||py<-8||py>H+8)return;
    const tw=.55+.45*Math.sin(t*2.5+p.phase);
    const sz=Math.max(3,5-scale*2);
    rect(px,py,sz,sz,p.col,tw);
    // Recession arrows on every 9th particle — shows direction of expansion
    if(scale>.35&&i%9===4){{
      const ax=p.nx*20*scale, ay=p.ny*14*scale;
      ctx.globalAlpha=.38*scale;
      ctx.strokeStyle=hotCol; ctx.lineWidth=1.5;
      ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(px+ax,py+ay);ctx.stroke();
      ctx.globalAlpha=1;
    }}
  }});

  // Temperature readout top-left
  {{
    const tLabels=['10²⁸ K','10²⁰ K','10¹² K','10⁹ K','10⁶ K','~3000 K'];
    const ti=Math.min(Math.floor(age*tLabels.length),tLabels.length-1);
    ctx.globalAlpha=.75; ctx.fillStyle=hotCol; ctx.font='11px monospace';
    ctx.fillText('T ≈ '+tLabels[ti],10,22);
    ctx.globalAlpha=1;
  }}

  // Main label — large, centred, pulsing
  if(age>.2){{
    const la=Math.min((age-.2)*2,.85);
    const pulse=.78+.22*Math.sin(t*1.8);
    ctx.globalAlpha=la*pulse;
    ctx.fillStyle=hotCol;
    ctx.font='bold 14px monospace'; ctx.textAlign='center';
    ctx.fillText('uniform expansion — no centre',CX,H-14);
    ctx.textAlign='left'; ctx.globalAlpha=1;
  }}
}}

// Nucleosynthesis: protons (red) + neutrons (blue) → H + He nuclei → freeze
const nucMoving=Array.from({{length:56}},(_,i)=>{{
  return{{
    x:((i*53+7)%560)-280, y:((i*41+13)%400)-200,
    type:i%3===0?'n':'p',
    phase:(i*1.3)%(Math.PI*2)
  }};
}});
const nucH=Array.from({{length:44}},(_,i)=>{{return{{x:((i*73+11)%520)-260,y:((i*37+23)%380)-190,phase:(i*2.1)%(Math.PI*2)}}}});
const nucHe=Array.from({{length:14}},(_,i)=>{{return{{x:((i*137+41)%480)-240,y:((i*89+17)%360)-180,phase:(i*1.7)%(Math.PI*2)}}}});

function plasma(){{
  drawStars();
  const sec=t/.016;

  if(sec<3){{
    // Hot quark-gluon plasma: bright chaotic flicker everywhere
    const h=.4+.6*Math.abs(Math.sin(t*11));
    const cols=['#ffffff','#ffe066','#ff9f1c','#ff5f3a','#7afcff'];
    for(let i=0;i<75;i++){{
      const px=CX+nucMoving[i%56].x+Math.sin(t*(i*.3+1))*25;
      const py=CY+nucMoving[i%56].y+Math.cos(t*(i*.2+.5))*18;
      rect(px,py,6,6,cols[i%5],h*.85);
    }}
    return;
  }}

  if(sec<7){{
    // Protons (red) + neutrons (blue) bouncing; some fuse into He (yellow)
    const frac=(sec-3)/4;
    const speed=1-frac*.65;
    nucMoving.slice(0,Math.floor((1-frac)*56)).forEach((n,i)=>{{
      const px=CX+n.x+Math.sin(t*(1.2+i*.04)+n.phase)*32*speed;
      const py=CY+n.y+Math.cos(t*(1.0+i*.03)+n.phase)*24*speed;
      rect(px,py,7,7,n.type==='p'?'#ff6060':'#5090ff',.75+.25*Math.sin(t*3+n.phase));
    }});
    nucHe.slice(0,Math.floor(frac*14)).forEach(h=>{{
      const px=CX+h.x+Math.sin(t*.8+h.phase)*8;
      const py=CY+h.y+Math.cos(t*.7+h.phase)*6;
      rect(px-5,py-5,14,14,'#ffd044',.88);
    }});
    return;
  }}

  // FREEZE — universe expanded too fast; fusion shut down
  const fa=Math.min((sec-7)/3,1);
  const tw=.2*(1-fa*.8);
  nucH.forEach(h=>{{
    rect(CX+h.x,CY+h.y,7,7,'#ff7070',.7+tw*Math.sin(t*1.5+h.phase));
  }});
  nucHe.forEach(h=>{{
    rect(CX+h.x-5,CY+h.y-5,14,14,'#ffd044',.75+tw*Math.sin(t*1.2+h.phase));
  }});
  ctx.globalAlpha=Math.min(fa*2,.8);
  ctx.fillStyle='#ff7070'; ctx.font='12px monospace';
  ctx.fillText('■ H  75%',CX-210,H-42);
  ctx.fillStyle='#ffd044';
  ctx.fillText('■ He 25%',CX-60,H-42);
  ctx.fillStyle='#88aacc'; ctx.font='10px monospace'; ctx.textAlign='center';
  ctx.fillText('fusion halted — expanded too fast — no carbon yet',CX,H-18);
  ctx.textAlign='left'; ctx.globalAlpha=1;
}}

function firstStars(){{
  drawStars();
  [[CX-120,CY-80],[CX+90,CY+60],[CX-40,CY+120],[CX+160,CY-50],[CX,CY-130]]
  .forEach(([bx,by],i)=>{{
    blockCircle(bx,by,28+Math.sin(t*2+i)*4,'rgba(130,200,255,.18)',8,.9);
    shadedBlockCircle(bx,by,14,['#9fd8ff','#ffffff','#fff6b0'],4);
  }});
}}

/* ── Supernova pre-generated data ── */
const snovaParts=Array.from({{length:200}},()=>{{
  const a=Math.random()*Math.PI*2;
  const r=30+Math.pow(Math.random(),.45)*245;
  return{{
    x:Math.cos(a)*r, y:Math.sin(a)*r*.72,
    size:[3,4,5,6][Math.floor(Math.random()*4)],
    col:['#ff6655','#ff9944','#ffee66','#88ddff','#dd88ff','#66ffbb','#ffaa44'][Math.floor(Math.random()*7)],
    al:.35+Math.random()*.65, tw:Math.random()*Math.PI*2
  }};
}});
const snovaFils=Array.from({{length:22}},(_,i)=>{{
  const colors=['#ff5533','#ff8844','#ffcc55','#8866ff','#44aaff','#ff4477'];
  return{{
    a:i*Math.PI*2/22+(Math.random()-.5)*.25,
    len:85+Math.random()*145,
    col:colors[i%colors.length],
    w:2+Math.floor(Math.random()*3)
  }};
}});

function supernova(){{
  drawStars();
  const sec=t/.016;

  // ── Phase 0 (0–3s): quiet pre-explosion star ──
  if(sec<3){{
    shadedBlockCircle(CX,CY,14,['#ffee99','#ffe066','#ffcc00'],4);
    return;
  }}

  const flashAge  = Math.min((sec-3)/2,1);           // 3–5s  : flash grows
  const expandAge = Math.min(Math.max((sec-5)/6,0),1); // 5–11s : wave expands
  const expandEase= 1-Math.pow(1-expandAge,3);
  const settled   = sec>11;
  const waveR     = expandEase*CX*1.18;

  // ── Initial brilliant flash (3–7s, fades as wave leaves) ──
  if(sec<8){{
    const fFade=Math.max(0,1-(sec-5)/2.5);
    blockCircle(CX,CY,10+flashAge*110,'rgba(255,210,90,.13)',8,fFade);
    blockCircle(CX,CY,10+flashAge*60,'rgba(255,245,160,.22)',8,fFade*.9);
  }}

  // ── Expanding shockwave ring (5–11s, fades as it spreads) ──
  if(sec>5&&!settled){{
    const rFade=Math.max(0,1-expandAge*.9);
    for(let i=0;i<80;i++){{
      const a=i*Math.PI*2/80;
      const wobble=Math.sin(i*7)*5;
      const rx=CX+Math.cos(a)*(waveR+wobble);
      const ry=CY+Math.sin(a)*(waveR+wobble)*.72;
      const col=i%4===0?'#ffffff':i%4===1?'#ffdd66':i%4===2?'#ff8844':'#ff5533';
      rect(rx,ry,6,6,col,rFade*(.5+.5*Math.sin(i*2)));
    }}
  }}

  // ── Glowing nebula shell — persists after ring passes ──
  if(sec>7){{
    const nAge=Math.min((sec-7)/4,1);
    const nR=70+expandEase*120;
    blockCircle(CX,CY,nR,'rgba(210,55,35,.11)',12,nAge);
    blockCircle(CX,CY,nR*.7,'rgba(50,110,230,.09)',12,nAge);
    blockCircle(CX,CY,nR*.42,'rgba(155,55,225,.07)',12,nAge);
  }}

  // ── Filaments — radiating streamers, like Crab Nebula ──
  if(sec>6){{
    const fAge=Math.min((sec-6)/5,1);
    const fEase=1-Math.pow(1-fAge,2);
    snovaFils.forEach(f=>{{
      const maxLen=f.len*Math.min(fEase*1.2,1);
      for(let s=0;s<9;s++){{
        const frac=s/8;
        const fx=CX+Math.cos(f.a)*maxLen*frac;
        const fy=CY+Math.sin(f.a)*maxLen*frac*.72;
        rect(fx,fy,f.w,f.w,f.col,(.15+.55*frac)*fAge);
      }}
    }});
  }}

  // ── Scattered element particles — spread and gently twinkle ──
  if(sec>6){{
    const pAge=Math.min((sec-6)/5,1);
    const pEase=1-Math.pow(1-pAge,3);
    snovaParts.forEach(p=>{{
      const px=CX+p.x*pEase, py=CY+p.y*pEase;
      const tw=settled?.5+.3*Math.sin(t*1.5+p.tw):.8;
      rect(px,py,p.size,p.size,p.col,p.al*tw);
    }});
  }}

  // ── Central neutron star — compact blue-white, subtle pulsation ──
  if(flashAge>0){{
    const nR=Math.max(4,16-expandAge*10);
    const glow=3+Math.sin(t*8)*1.5;
    blockCircle(CX,CY,nR+glow+4,'rgba(140,195,255,.18)',4,.85);
    shadedBlockCircle(CX,CY,nR+glow,['#99ccff','#cceeff','#ffffff'],4);
  }}
}}

const galPts=[];
for(let arm=0;arm<3;arm++) for(let i=0;i<105;i++){{
  const a=arm*Math.PI*2/3+i*.145,r=10+i*1.8;
  galPts.push({{x:Math.cos(a)*r,y:Math.sin(a)*r*.48,c:i%3===0?'#8ecaff':i%3===1?'#ffe28a':'#d6a4ff'}});
}}
function galaxy(){{
  drawStars();
  galPts.forEach((s,i)=>{{
    const rot=t*.035;
    const rx=CX+s.x*Math.cos(rot)-s.y*Math.sin(rot);
    const ry=CY+s.x*Math.sin(rot)+s.y*Math.cos(rot);
    rect(rx,ry,5,5,s.c,.75);
  }});
  shadedBlockCircle(CX,CY,20,['#fff0a0','#ffffff','#a9d8ff'],4);
}}

function nebula(){{
  drawStars();
  [['#3167ff',180,110],['#994cff',150,85],['#35e68a',120,70]].forEach(([col,rx,ry],li)=>{{
    for(let i=0;i<18;i++){{
      const a=t*.12+i*.75+li;
      rect(CX+Math.cos(a)*rx*.7,CY+Math.sin(a)*ry*.6,18,18,col,.13);
    }}
  }});
  drawSun();
}}

// Accretion: dust → runaway growth → heat → differentiation (Fe core)
const debrisPts=Array.from({{length:80}},(_,i)=>{{
  return{{
    r:62+(i%8)*26+((i*17)%22),
    size:3+(i%3)*2,
    col:i%4===0?'#9a6a3a':i%4===1?'#7d4c28':'#5a3520',
    speed:.42+(i%5)*.08,
    phase:(i*.73)%(Math.PI*2)
  }};
}});

function accretion(){{
  drawStars();
  const sec=t/.016;
  const age=Math.min(sec/14,1);
  const bodyR=Math.floor(10+age*62);
  const heat=Math.max(0,1-age*.55);

  // Debris spiraling inward — count drops as planet grows (runaway sweep-up)
  const debrisN=Math.floor(80*(1-age*.88));
  for(let i=0;i<debrisN;i++){{
    const d=debrisPts[i];
    const r=d.r*(1-age*.42);
    const a=t*d.speed+d.phase;
    const px=CX+Math.cos(a)*r, py=CY+Math.sin(a)*r*.72;
    rect(px,py,d.size,d.size,d.col,.8);
  }}

  // Growing planet body with differentiated layers
  if(age>.04){{
    // Impact-heat glow
    if(heat>.12)blockCircle(CX,CY,bodyR+18,`rgba(255,${{Math.floor(80+heat*110)}},0,${{heat*.17}})`,8,.9);

    // Crust — cools from lava-red to brown-grey
    const crustCol=heat>.65?'#d05028':heat>.3?'#8a4c30':'#5c3a22';
    shadedBlockCircle(CX,CY,bodyR,[crustCol,'#b87038','#d89050'],8);

    // Mantle
    const mR=Math.floor(bodyR*.70);
    if(mR>5){{
      const mCol=heat>.4?'#ff5822':'#a04020';
      shadedBlockCircle(CX,CY,mR,[mCol,'#cc4830','#e06040'],6);
    }}

    // Iron core — bright, shows differentiation starting
    const cR=Math.floor(bodyR*.35);
    if(cR>3)shadedBlockCircle(CX,CY,cR,['#ff3010','#ff8030','#ffee88'],4);

    // Label once core is visible
    if(age>.55){{
      ctx.globalAlpha=Math.min((age-.55)*3,.7);
      ctx.fillStyle='#ffcc88'; ctx.font='10px monospace'; ctx.textAlign='center';
      ctx.fillText('Fe sinks → core → magnetic dynamo → atmosphere shielded',CX,H-18);
      ctx.textAlign='left'; ctx.globalAlpha=1;
    }}
  }}
}}

function frame(){{
  bg();
  if(MODE==='bigbang')         bigbang();
  else if(MODE==='plasma')     plasma();
  else if(MODE==='first_stars')firstStars();
  else if(MODE==='supernova')  supernova();
  else if(MODE==='galaxy')     galaxy();
  else if(MODE==='nebula')     nebula();
  else if(MODE==='accretion')  accretion();
  else {{ drawStars();drawSun();drawPlanets(); }}
  t+=.016;requestAnimationFrame(frame);
}}
frame();
</script></body></html>"""


# ── SVG helpers ───────────────────────────────────────────────────────────────

def _svg_header() -> str:
    return """<defs>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="4" dy="5" stdDeviation="0" flood-color="#000" flood-opacity="0.45"/>
  </filter>
  <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
    <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#1d2941" stroke-width="1" opacity="0.5"/>
  </pattern>
</defs>
<rect width="280" height="280" fill="#07101f"/>
<rect width="280" height="280" fill="url(#grid)" opacity="0.45"/>"""


def _iso_block(x: float, y: float, size: float, color: str, opacity: float = 1.0) -> str:
    """Tiny square block, used to add pixel/voxel texture."""
    return f'<rect x="{x:.0f}" y="{y:.0f}" width="{size:.0f}" height="{size:.0f}" fill="{color}" opacity="{opacity}"/>'


def _voxel_ring(cx: int, cy: int, r: int, color: str, step: int = 10, opacity: float = 1.0) -> str:
    bits = []
    for yy in range(-r, r + 1, step):
        for xx in range(-r, r + 1, step):
            if xx * xx + yy * yy <= r * r:
                bits.append(_iso_block(cx + xx, cy + yy, step, color, opacity))
    return "".join(bits)


# ── Cross-section SVGs ────────────────────────────────────────────────────────

def cross_section(world: World) -> str:
    """Dispatch to the correct SVG builder based on journey type."""
    if world.journey == "gas_giant":
        return _gas_giant_svg(world)
    if world.journey == "icy_moon":
        return _icy_moon_svg(world)
    if world.journey == "star_system":
        return _star_system_svg(world)
    return _rocky_planet_svg(world)


def _rocky_planet_svg(w: World) -> str:
    """Voxel-style cross-section for rocky / earth_like worlds."""
    if w.water in ("liquid", "abundant"):
        surf = "#2468c9"
        surf_hi = "#57a6ff"
    elif w.water == "ice":
        surf = "#bfd8e8"
        surf_hi = "#eefaff"
    elif w.surface_temp_c > 400:
        surf = "#b8341d"
        surf_hi = "#ff6b32"
    else:
        surf = "#8a5b35"
        surf_hi = "#c18a54"

    atm_fill = {
        "thick":      "#4ea1ff",
        "thin":       "#78caff",
        "greenhouse": "#b6ff5c",
        "none":       "#000000",
    }.get(w.atmosphere, "#000000")
    atm_opacity = 0.18 if w.atmosphere != "none" else 0

    core_col = "#ff6b22" if w.geology != "dead" else "#654331"

    life_svg = ""
    if w.hab_label in ("Life Confirmed", "Possible Life"):
        for i in range(7):
            rad = math.radians(i * 51 + 18)
            lx = 140 + math.cos(rad) * 78
            ly = 140 + math.sin(rad) * 78
            life_svg += _iso_block(lx, ly, 10, "#4ecf58", 0.9)

    earth_svg = ""
    if w._is_earth:
        earth_svg = (
            '<rect x="112" y="124" width="28" height="18" fill="#4ecf58" opacity="0.88"/>'
            '<rect x="157" y="146" width="22" height="14" fill="#4ecf58" opacity="0.88"/>'
            '<rect x="136" y="166" width="28" height="10" fill="#3eb34d" opacity="0.84"/>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="280" height="280"
     style="background:#07101f;border-radius:10px;display:block;margin:auto;image-rendering:pixelated;">
  {_svg_header()}
  <g filter="url(#shadow)">
    <circle cx="140" cy="140" r="128" fill="{atm_fill}" opacity="{atm_opacity}"/>
    <circle cx="140" cy="140" r="114" fill="{surf}"/>
    <circle cx="112" cy="108" r="18" fill="{surf_hi}" opacity="0.35"/>
    {life_svg}{earth_svg}
    <circle cx="140" cy="140" r="88" fill="#8f6039" opacity="0.95"/>
    <circle cx="140" cy="140" r="62" fill="#c85b2b"/>
    <circle cx="140" cy="140" r="36" fill="{core_col}"/>
    <rect x="128" y="128" width="18" height="18" fill="#ffd166" opacity="0.55"/>
  </g>
  <text x="140" y="18" text-anchor="middle" fill="#b9c7d8" font-size="9" font-family="monospace">ATMOSPHERE</text>
  <text x="140" y="38" text-anchor="middle" fill="#b9c7d8" font-size="9" font-family="monospace">SURFACE BLOCKS</text>
  <text x="140" y="62" text-anchor="middle" fill="#d6b28a" font-size="9" font-family="monospace">MANTLE</text>
  <text x="140" y="145" text-anchor="middle" fill="#fff0c2" font-size="9" font-family="monospace">CORE</text>
  <text x="140" y="273" text-anchor="middle" fill="#8190a6" font-size="9" font-family="monospace">{w.display_name}</text>
</svg>"""


def _gas_giant_svg(w: World) -> str:
    """Blocky bands for a gas giant."""
    bands = ["#f0b46a", "#d98d4e", "#b9663b", "#e6a466", "#c57743", "#f0c083", "#a95b38"]
    band_svgs = ""
    for i, col in enumerate(bands):
        y = 28 + i * 28
        band_svgs += (
            f'<rect x="30" y="{y}" width="220" height="24" fill="{col}" clip-path="url(#planetClip)"/>'
            f'<rect x="{46 + (i % 3) * 25}" y="{y + 7}" width="46" height="8" fill="#fff0c2" opacity="0.18" clip-path="url(#planetClip)"/>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="280" height="280"
     style="background:#07101f;border-radius:10px;display:block;margin:auto;image-rendering:pixelated;">
  {_svg_header()}
  <defs><clipPath id="planetClip"><circle cx="140" cy="140" r="120"/></clipPath></defs>
  <g filter="url(#shadow)">
    <circle cx="140" cy="140" r="120" fill="#c87040"/>
    {band_svgs}
    <circle cx="140" cy="140" r="68" fill="#9d5036" opacity="0.65"/>
    <circle cx="140" cy="140" r="30" fill="#6f5534"/>
    <rect x="128" y="128" width="24" height="24" fill="#9b7847" opacity="0.8"/>
  </g>
  <text x="140" y="18" text-anchor="middle" fill="#b9c7d8" font-size="9" font-family="monospace">CLOUD BANDS</text>
  <text x="140" y="85" text-anchor="middle" fill="#ffd9a0" font-size="9" font-family="monospace">METALLIC H</text>
  <text x="140" y="145" text-anchor="middle" fill="#ffe2b6" font-size="9" font-family="monospace">CORE</text>
  <text x="140" y="273" text-anchor="middle" fill="#8190a6" font-size="9" font-family="monospace">{w.display_name}</text>
</svg>"""


def _icy_moon_svg(w: World) -> str:
    """Ice shell, subsurface ocean, rocky mantle, warm core."""
    ocean_fill = "#2266c9" if w.subsurface_ocean else "#7e9baa"
    core_col = "#ff7430" if w.tidal_heating in ("moderate", "strong") else "#5f4545"
    crack_svg = ""
    if w.tidal_heating != "none":
        for i in range(5):
            rad = math.radians(i * 72 + 22)
            x1 = 140 + math.cos(rad) * 96
            y1 = 140 + math.sin(rad) * 96
            x2 = 140 + math.cos(rad) * 120
            y2 = 140 + math.sin(rad) * 120
            crack_svg += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#ffffff" stroke-width="3" opacity="0.75"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="280" height="280"
     style="background:#07101f;border-radius:10px;display:block;margin:auto;image-rendering:pixelated;">
  {_svg_header()}
  <g filter="url(#shadow)">
    <circle cx="140" cy="140" r="120" fill="#cfe8f4"/>
    <circle cx="100" cy="96" r="16" fill="#ffffff" opacity="0.35"/>
    {crack_svg}
    <circle cx="140" cy="140" r="96" fill="{ocean_fill}"/>
    <circle cx="140" cy="140" r="68" fill="#7d5c49"/>
    <circle cx="140" cy="140" r="38" fill="{core_col}"/>
    <rect x="130" y="130" width="20" height="20" fill="#ffd166" opacity="0.35"/>
  </g>
  <text x="140" y="18" text-anchor="middle" fill="#dcefff" font-size="9" font-family="monospace">ICE SHELL</text>
  <text x="140" y="52" text-anchor="middle" fill="#9bd1ff" font-size="9" font-family="monospace">{"SUBSURFACE OCEAN" if w.subsurface_ocean else "FROZEN INTERIOR"}</text>
  <text x="140" y="84" text-anchor="middle" fill="#d6b28a" font-size="9" font-family="monospace">ROCKY MANTLE</text>
  <text x="140" y="143" text-anchor="middle" fill="#fff0c2" font-size="9" font-family="monospace">{"WARM CORE" if w.tidal_heating != "none" else "COLD CORE"}</text>
  <text x="140" y="273" text-anchor="middle" fill="#8190a6" font-size="9" font-family="monospace">{w.display_name}</text>
</svg>"""


def _star_system_svg(w: World) -> str:
    """Centered orbital diagram — star in the middle, all planets fit within SVG."""
    from simulation import HABITABLE_ZONES
    hz_in, hz_out = HABITABLE_ZONES.get(w.star_type, (0.7, 1.5))

    star_colors  = {"M": "#ff7755", "K": "#ffaa55", "G": "#ffdd55", "F": "#ffffee"}
    star_col     = star_colors.get(w.star_type, "#ffdd55")
    star_radii   = {"M": 10, "K": 13, "G": 16, "F": 19}
    star_r       = star_radii.get(w.star_type, 16)

    def au_to_px(au: float) -> int:
        # sqrt-compressed: ~0.3 AU→28px, 8 AU→122px — all fit inside 280px SVG
        return max(28, min(122, int(28 + 94 * ((max(au, 0.3) - 0.3) / 7.7) ** 0.5)))

    hz_in_px  = au_to_px(hz_in)
    hz_out_px = au_to_px(hz_out)

    orbits_au = [0.4, 0.7, 1.0, 1.5, 2.2, 3.5, 5.2, 8.0]
    orbit_svg = ""
    planet_svg = ""
    for i, au in enumerate(orbits_au[: w.num_planets]):
        r         = au_to_px(au)
        in_hz     = hz_in <= au <= hz_out
        is_giant  = au > 2.0
        dot_col   = "#4fa3ff" if in_hz else ("#c87040" if is_giant else "#aa7a4a")
        dot_r     = 6 if is_giant else 4
        # stagger planet positions around orbits so they're all visible
        angle     = math.radians(22 + i * 51)
        px        = 140 + math.cos(angle) * r
        py        = 140 + math.sin(angle) * r
        orbit_svg  += (
            f'<circle cx="140" cy="140" r="{r}" fill="none" '
            f'stroke="rgba(185,210,240,0.20)" stroke-width="1.5" stroke-dasharray="4 6"/>'
        )
        planet_svg += (
            f'<rect x="{px - dot_r:.0f}" y="{py - dot_r:.0f}" '
            f'width="{dot_r * 2}" height="{dot_r * 2}" fill="{dot_col}"/>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="280" height="280"
     style="background:#07101f;border-radius:10px;display:block;margin:auto;image-rendering:pixelated;">
  {_svg_header()}
  <!-- habitable zone annulus -->
  <circle cx="140" cy="140" r="{hz_out_px}" fill="#4ecf58" opacity="0.14"/>
  <circle cx="140" cy="140" r="{hz_in_px}"  fill="#07101f"/>
  <!-- orbit rings -->
  {orbit_svg}
  <!-- planets -->
  {planet_svg}
  <!-- star -->
  <g filter="url(#shadow)">
    <circle cx="140" cy="140" r="{star_r + 10}" fill="{star_col}" opacity="0.22"/>
    <circle cx="140" cy="140" r="{star_r + 5}"  fill="{star_col}" opacity="0.30"/>
    <rect x="{140 - star_r}" y="{140 - star_r}" width="{star_r * 2}" height="{star_r * 2}" fill="{star_col}"/>
    <rect x="{140 - star_r // 2}" y="{140 - star_r // 2}" width="{star_r}" height="{star_r}" fill="#ffffff" opacity="0.30"/>
  </g>
  <text x="140" y="14" text-anchor="middle" fill="#9ce89c" font-size="8" font-family="monospace">GREEN RING = HABITABLE ZONE</text>
  <text x="140" y="273" text-anchor="middle" fill="#8190a6" font-size="8" font-family="monospace">{w.display_name} · {w.num_planets} PLANETS</text>
</svg>"""


# ── Habitability factors breakdown ────────────────────────────────────────────

def factors_html(world: World) -> str:
    """
    Return a voxel-style HTML table showing which factors helped or hurt habitability.
    Used on the result page.
    """
    from simulation import (
        WATER_SCORE, ATM_SCORE, MAG_SCORE, GEO_SCORE, IMPACT_MOD,
    )

    if world.journey in ("gas_giant", "star_system"):
        return "<p style='color:#93a1b8;font-family:monospace'>No surface habitability for this world type.</p>"

    if world.journey == "icy_moon":
        rows = [
            ("Subsurface ocean", 35 if world.subsurface_ocean else 0, 35),
            ("Tidal heating",    {"none": 5, "moderate": 30, "strong": 15}[world.tidal_heating], 30),
            ("Magnetic shielding", MAG_SCORE.get(world.magnetic_field, 0) // 2, 7),
            ("Geological activity", GEO_SCORE.get(world.geology, 0), 15),
        ]
    else:
        temp_pts = 30 if -20 <= world.surface_temp_c <= 65 else (10 if -60 <= world.surface_temp_c <= 100 else 0)
        rows = [
            ("Temperature range",    temp_pts, 30),
            ("Water presence",       WATER_SCORE.get(world.water, 0), 25),
            ("Atmosphere",           ATM_SCORE.get(world.atmosphere, 0), 20),
            ("Magnetic field",       MAG_SCORE.get(world.magnetic_field, 0), 15),
            ("Geological activity",  GEO_SCORE.get(world.geology, 0), 15),
            ("Impact history",       IMPACT_MOD.get(world.impact_history, 0), 5),
        ]

    cells = ""
    for label, pts, max_pts in rows:
        pct = int(pts / max_pts * 100) if max_pts else 0
        bar_col = "#4ecf58" if pts > 0 else ("#d84a32" if pts < 0 else "#586375")
        cells += (
            "<tr>"
            f"<td style='padding:5px 8px;color:#d9e2f1;font-size:12px;font-family:monospace;text-shadow:1px 1px #000'>{label}</td>"
            "<td style='padding:5px 8px;width:130px'>"
            "<div style='background:#101828;border:2px solid #26354f;height:13px;box-shadow:3px 3px 0 #000'>"
            f"<div style='background:{bar_col};width:{max(0, pct)}%;height:13px'></div>"
            "</div></td>"
            f"<td style='padding:5px 8px;color:#aebbd0;font-size:11px;font-family:monospace'>{pts:+d}/{max_pts}</td>"
            "</tr>"
        )

    return (
        "<table style='border-collapse:collapse;width:100%;background:#07101f;border:2px solid #26354f;box-shadow:4px 4px 0 #000'>"
        f"{cells}"
        "</table>"
    )
