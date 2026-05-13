"""
app.py — Cosmic Origins Adventure
Page flow:  home  →  journey (stage by stage)  →  result
"""
import streamlit as st

from simulation import (
    EARTH, HABITABLE_ZONES, STAR_LABELS,
    build_world, calc_temp, in_hz,
)
import random

from story import (
    ACCRETION_CHOICES, DISTANCE_OPTIONS,
    EVOLUTION_CHOICES, GAS_GIANT_EVOLUTION,
    ICY_MOON_EVOLUTION, JOURNEY_DEFAULTS,
    JOURNEYS, STAGE_NARRATIVES, STAGES, STAR_SYSTEM_EVOLUTION,
)
from visuals import cross_section, stage_canvas
from ai import (
    cosmic_speculation,
    generate_world_identity,
    result_narrative,
)

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Cosmic Origins Adventure",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────

def _inject_css():
    st.html("""
<link href="https://fonts.googleapis.com/css2?family=VT323&family=Press+Start+2P&display=swap"
      rel="stylesheet">
<style>
header[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stDecoration"],.stDeployButton{display:none!important}
/* Hide the collapse/expand buttons — sidebar is always open */
[data-testid="stSidebarCollapseButton"]{display:none!important}
[data-testid="stSidebarCollapsedControl"]{display:none!important}

html,body,[class*="css"]{font-family:'VT323',monospace!important;font-size:14px!important;color:#f0f0f0!important}
.stApp{background-color:#1b1b1b!important}
.main .block-container{background-color:#1b1b1b!important;padding-top:.3rem!important;padding-bottom:.3rem!important}

p,li,span,div,label,td,th,caption,.stMarkdown,.stText,.stCaption{color:#eeeeee!important}
.stCaption,.stCaption p{color:#bbbbbb!important}

/* ── Journey cards — all cards reset to dark stone first ── */
.main [data-testid="stHorizontalBlock"]:first-of-type .stButton>button,
.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stBaseButton-secondary"]>button{
  height:230px!important;white-space:pre-line!important;text-align:center!important;
  font-family:'VT323',monospace!important;font-size:17px!important;line-height:1.55!important;
  padding:20px 14px!important;background-color:#1c1c1e!important;border:3px solid #3a3a3e!important;
  box-shadow:4px 4px 0 #000!important;color:#888899!important;opacity:.7!important;
  transition:none!important;overflow:hidden!important}
.main [data-testid="stHorizontalBlock"]:first-of-type .stButton>button:hover,
.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stBaseButton-secondary"]>button:hover{
  background-color:#242428!important;border-color:#5a5a66!important;color:#bbbbcc!important;
  opacity:.9!important;transform:translateY(-3px)!important;box-shadow:4px 7px 0 #000!important}
/* Selected card (primary) — green glow and pop-up */
.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stBaseButton-primary"]>button{
  background-color:#162416!important;border:3px solid #50a03c!important;
  box-shadow:0 0 0 2px #50a03c,0 0 22px #50a03c88,4px 10px 0 #0a1a08!important;
  color:#d4ffd4!important;opacity:1!important;transform:translateY(-8px)!important;
  height:230px!important;white-space:pre-line!important;text-align:center!important;
  font-family:'VT323',monospace!important;font-size:17px!important;line-height:1.55!important}

/* ── Sidebar ── */
section[data-testid="stSidebar"]>div:first-child{background-color:#222!important;border-right:4px solid #444!important}
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,section[data-testid="stSidebar"] li{font-family:'VT323',monospace!important;font-size:17px!important;color:#ddd!important}
section[data-testid="stSidebar"] h3,section[data-testid="stSidebar"] h2{font-family:'Press Start 2P',monospace!important;font-size:10px!important;line-height:1.8!important;color:#fff!important}

/* ── Headings ── */
h1{font-family:'Press Start 2P',monospace!important;font-size:22px!important;color:#fff!important;text-shadow:3px 3px 0 #1e4a15!important;line-height:1.6!important}
h2{font-family:'Press Start 2P',monospace!important;font-size:16px!important;color:#e8e8e8!important;line-height:1.6!important}
h3{font-family:'Press Start 2P',monospace!important;font-size:11px!important;color:#cccccc!important;line-height:1.8!important}
h4,h5,h6{font-family:'VT323',monospace!important;font-size:16px!important;color:#ccc!important}

/* ── Buttons ── */
.stButton>button{font-family:'Press Start 2P',monospace!important;font-size:9px!important;
  background-color:#3d7a2e!important;color:#fff!important;border:3px solid #1e4a15!important;
  border-radius:0!important;box-shadow:4px 4px 0 #0d220a!important;padding:10px 14px!important;
  transition:none!important;text-transform:uppercase!important;letter-spacing:1px!important;width:100%!important}
.stButton>button:hover{background-color:#50a03c!important;transform:translate(2px,2px)!important;box-shadow:2px 2px 0 #0d220a!important;color:#fff!important}
.stButton>button:active{transform:translate(4px,4px)!important;box-shadow:none!important}
[data-testid="stBaseButton-primary"]>button{background-color:#50a03c!important;border-color:#2d6020!important}

/* ── Alerts ── */
.stAlert{border-radius:0!important;border-width:3px!important}
.stAlert>div{font-family:'VT323',monospace!important;font-size:15px!important;border-radius:0!important}
div[class*="stInfo"]{background-color:#1a2e1a!important;border-color:#4a8f3a!important;border-radius:0!important}
div[class*="stSuccess"]{background-color:#0d1f0d!important;border-color:#50a03c!important;border-radius:0!important}
div[class*="stWarning"]{background-color:#2a1e00!important;border-color:#cc9900!important;border-radius:0!important}

/* ── Expanders ── */
[data-testid="stExpander"]{border:3px solid #444!important;border-radius:0!important;background-color:#252525!important;margin-bottom:8px!important}
[data-testid="stExpander"] summary{font-family:'Press Start 2P',monospace!important;font-size:8px!important;color:#ddd!important;background-color:#333!important;padding:10px 12px!important;border-radius:0!important;line-height:1.8!important}
[data-testid="stExpander"]>div:nth-child(2){background-color:#252525!important;padding:12px!important}

/* ── Progress bars ── */
[data-testid="stProgressBar"]{border-radius:0!important}
[data-testid="stProgressBar"]>div{background-color:#333!important;border:2px solid #555!important;border-radius:0!important;height:14px!important}
[data-testid="stProgressBar"]>div>div{background-color:#50a03c!important;border-radius:0!important}

/* ── Radio ── */
.stRadio>label{font-family:'Press Start 2P',monospace!important;font-size:9px!important;color:#ccc!important}
.stRadio>div{background-color:#252525!important;border:2px solid #444!important;padding:10px!important;border-radius:0!important}
.stRadio div[role="radiogroup"] label{font-family:'VT323',monospace!important;font-size:15px!important;color:#f0f0f0!important}

/* ── Misc ── */
.stCaption,.stCaption p{font-family:'VT323',monospace!important;font-size:13px!important;color:#888!important}
hr{border:none!important;border-top:2px solid #444!important;margin:10px 0!important}
.stSpinner>div{border-top-color:#50a03c!important}
table{border-collapse:collapse!important;background-color:#252525!important;border:3px solid #555!important;width:100%!important}
th{font-family:'Press Start 2P',monospace!important;font-size:7px!important;background-color:#333!important;border:2px solid #555!important;padding:7px 8px!important;color:#e0e0e0!important;line-height:1.8!important}
td{font-family:'VT323',monospace!important;font-size:14px!important;border:1px solid #444!important;padding:4px 8px!important;color:#ccc!important}
tr:nth-child(even) td{background-color:#2a2a2a!important}
::-webkit-scrollbar{width:10px;background:#1b1b1b}
::-webkit-scrollbar-thumb{background:#444;border:2px solid #1b1b1b}

/* ── Text input ── */
.stTextInput input{font-family:'VT323',monospace!important;font-size:18px!important;background:#252525!important;
  color:#eee!important;border:3px solid #444!important;border-radius:0!important;padding:8px!important}
.stTextInput input:focus{border-color:#50a03c!important;outline:none!important}
</style>
""")

# ── Style constants ───────────────────────────────────────────────────────────

_NARR  = "background:#141e14;border:2px solid #3a7030;border-left:4px solid #3a7030;padding:8px 12px;font-family:'VT323',monospace;font-size:16px;color:#b8ddb8;line-height:1.45;"
_AMBER = "background:#1e1e10;border:2px solid #aa9900;border-left:5px solid #aa9900;padding:8px 12px;font-family:'VT323',monospace;font-size:15px;color:#f0e8a8;line-height:1.45;"


# ── Visual causal chain helper ────────────────────────────────────────────────

# Short emoji+label for each step concept, looked up by keyword
_CHAIN_ICONS = {
    "expansion": "📡 Expansion", "cooling": "🌡️ Cools", "particle": "⚛️ Particles",
    "quark": "⚛️ Quarks", "temperature": "🌡️ Temp", "chemistry": "⚗️ Chemistry",
    "fusion": "🔥 Fusion", "helium": "☁️ He Forms", "hydrogen": "💨 H Only",
    "metal": "🪨 No Metals", "rocky": "🪨 Rocky", "icy": "🧊 Icy",
    "massive": "⭐ Huge Stars", "star dies": "⭐ Star Dies", "star": "⭐ Stars",
    "lifespan": "💀 Short Life", "core": "💥 Core", "collapse": "💥 Collapse",
    "explosion": "💥 Explosion", "element": "⚗️ Elements", "eject": "🚀 Ejected",
    "nebula": "🪐 Seeds Nebula", "seed": "🪐 Seeds", "dark matter": "🕳️ Dark Matter",
    "galaxy": "🌌 Galaxies", "generat": "🔄 Generations", "enrich": "✨ Enrichment",
    "cloud": "☁️ Cloud", "disk": "🌀 Disk", "frost": "❄️ Frost Line",
    "spin": "🌀 Spins", "planet melts": "🔥 Melts", "melt": "🔥 Melts",
    "fe sink": "⬇️ Fe Sinks", "iron": "⬇️ Fe Sinks", "dynamo": "🔄 Dynamo",
    "magnetic": "🧲 Mag Field", "field shields": "🛡️ Shields", "shield": "🛡️ Shields",
    "atmosphere": "🌫️ Atmosphere", "water": "💧 Water", "carbon": "🧬 Carbon",
    "energy": "⚡ Energy", "life": "🌱 Life", "habitable": "🌍 Habitable",
    "accretion": "🌀 Accretion", "runaway": "📈 Runaway", "complexity": "🧠 Complexity",
    "structure": "🏗️ Structure", "possible": "✅ Possible",
}


def _chain_label(step: str) -> str:
    """Map a causal chain step phrase to a short emoji+label."""
    s = step.lower().strip().rstrip(".")
    for keyword, label in _CHAIN_ICONS.items():
        if keyword in s:
            return label
    # Fallback: capitalise and truncate to ~12 chars
    words = s.split()[:3]
    return "🔗 " + " ".join(w.capitalize() for w in words)


def _render_causal_chain(chain_text: str, summary: str = "") -> str:
    """Return HTML for a visual block-based causal flow."""
    steps = [s.strip().rstrip(".") for s in chain_text.split("→") if s.strip()]
    tile = (
        "background:#1a1608;border:2px solid #7a6200;padding:5px 10px;"
        "font-family:'VT323',monospace;font-size:15px;color:#e8c040;white-space:nowrap"
    )
    arrow = "<span style='color:#886600;font-size:15px;flex-shrink:0'>→</span>"
    tiles = f" {arrow} ".join(
        f"<div style='{tile}'>{_chain_label(s)}</div>" for s in steps
    )
    caption = (
        f"<div style='font-family:VT323,monospace;font-size:14px;color:#666;"
        f"margin:3px 0 6px 4px'>{summary}</div>"
        if summary else ""
    )
    return (
        f"<div style='display:flex;align-items:center;gap:5px;flex-wrap:wrap;"
        f"padding:10px 12px;background:#100e00;border:2px solid #554400;"
        f"border-left:5px solid #998800;margin:6px 0'>{tiles}</div>{caption}"
    )

# ── Session state ─────────────────────────────────────────────────────────────

def _init():
    for k, v in {
        "page": "home", "journey": None, "stage": 0,
        "choices": {}, "selected_journey": None,
        "speculation_seed": 0,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()
_inject_css()

# ── Navigation ────────────────────────────────────────────────────────────────

def _start(key: str):
    st.session_state.update(page="journey", journey=key, stage=0,
                             choices=dict(JOURNEY_DEFAULTS[key]),
                             speculation_seed=0)
    st.rerun()

def _goto(page: str):
    st.session_state.page = page
    st.rerun()

def _next():
    if st.session_state.stage < len(STAGES) - 1:
        st.session_state.stage += 1
    else:
        st.session_state.page = "result"
    st.rerun()

def _prev():
    if st.session_state.stage > 0:
        st.session_state.stage -= 1
    st.rerun()

# ── Choice widget ─────────────────────────────────────────────────────────────

def _radio(label, opts, state_key, *, widget_key):
    values = [o["value"] for o in opts]
    labels = [o["label"] for o in opts]
    try:
        idx = values.index(st.session_state.choices.get(state_key))
    except ValueError:
        idx = 0
    sel = st.radio(label, range(len(opts)), index=idx,
                   format_func=lambda i: labels[i], key=widget_key)
    st.caption(opts[sel]["desc"])
    st.session_state.choices[state_key] = values[sel]



# ═══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def show_home():
    st.markdown("# 🌌 Cosmic Origins Adventure")
    st.markdown(
        "#### Build a World from the Big Bang\n"
        "Travel through 13.8 billion years of cosmic history and make choices "
        "that shape your world — from the type of star it orbits to whether life ever emerges."
    )
    st.divider()
    st.markdown("### Choose your journey")

    sel  = st.session_state.selected_journey
    cols = st.columns(len(JOURNEYS))
    for col, (key, info) in zip(cols, JOURNEYS.items()):
        label = f"{info['icon']}\n\n{info['label']}\n\n{info['desc']}\n\n— {info['example']} —"
        with col:
            if st.button(label, key=f"card_{key}", use_container_width=True,
                         type="primary" if sel == key else "secondary"):
                st.session_state.selected_journey = key
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if sel:
        jinfo = JOURNEYS[sel]
        if st.button(f"▶  Start Adventure — {jinfo['label']} {jinfo['icon']}",
                     use_container_width=True, type="primary"):
            _start(sel)
    else:
        st.markdown(
            "<div style='text-align:center;color:#555;font-family:VT323,monospace;"
            "font-size:20px;padding:10px'>← Select a journey above to begin →</div>",
            unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🌍 Earth — Reference Case")
    ec1, ec2, ec3 = st.columns([1, 1, 2])
    with ec1:
        st.components.v1.html(
            "<html><body style='margin:0;padding:0;background:#07101f'>"
            + cross_section(EARTH) + "</body></html>", height=290)
    with ec2:
        for line in EARTH.summary_lines:
            st.write(line)
    with ec3:
        st.markdown(
            f"**Habitability: {EARTH.hab_label}**&nbsp;"
            f"<span style='color:{EARTH.hab_color}'>●</span>",
            unsafe_allow_html=True)
        st.progress(EARTH.habitability_score / 100,
                    text=f"Score: {EARTH.habitability_score}/100")
        st.info(
            "Earth is our only confirmed example of life. It sits comfortably in "
            "the Sun's habitable zone, has abundant liquid water, a thick N₂/O₂ atmosphere, "
            "a strong magnetic field, and active plate tectonics — all factors that emerged "
            "across billions of years of cosmic and geological history."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# JOURNEY PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def show_journey():
    journey   = st.session_state.journey
    stage_idx = st.session_state.stage
    choices   = st.session_state.choices
    stage     = STAGES[stage_idx]
    jinfo     = JOURNEYS[journey]
    ctx       = stage["journey_context"].get(journey, "")

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"### {jinfo['icon']} {jinfo['label']}")
        st.progress(stage_idx / (len(STAGES) - 1),
                    text=f"Stage {stage_idx + 1} of {len(STAGES)}")
        st.divider()
        for i, s in enumerate(STAGES):
            if i < stage_idx:
                st.markdown(f"✅ {s['name']}")
            elif i == stage_idx:
                st.markdown(f"**▶ {s['name']}**")
            else:
                st.markdown(f"<span style='color:#555;font-family:VT323,monospace'>○ {s['name']}</span>",
                            unsafe_allow_html=True)
        st.divider()
        if st.button("🏠 Home", use_container_width=True):
            _goto("home")

    # ── Stage header ──────────────────────────────────────────────────────────
    st.markdown(f"## {stage['name']}")
    st.caption(f"⏱ {stage['time']}  ·  Stage {stage_idx + 1} of {len(STAGES)}")

    left, right = st.columns([1, 1.4], gap="large")

    # ── Shared section-label renderer ────────────────────────────────────────
    def _sec(label: str, color: str) -> None:
        st.markdown(
            f"<div style='font-family:\"Press Start 2P\",monospace;font-size:11px;"
            f"color:{color};letter-spacing:1px;margin:12px 0 6px 0'>{label}</div>",
            unsafe_allow_html=True)

    def _tags(elements) -> str:
        return " ".join(
            f"<span style='background:#1c1c28;border:1px solid #444;padding:2px 6px;"
            f"font-family:VT323,monospace;font-size:13px;color:#aaaacc;margin:1px;"
            f"display:inline-block'>{e}</span>"
            for e in elements
        )

    # ── ROW 1: Description (left) + Animation (right) ─────────────────────────
    with left:
        _sec("📋 What Is Happening", "#666666")
        st.markdown(
            f"<div style='font-family:VT323,monospace;font-size:15px;color:#ddd;"
            f"line-height:1.45;margin-bottom:6px'>{stage['desc']}</div>",
            unsafe_allow_html=True)
        st.markdown(
            f"<div style='margin:4px 0'>"
            f"<span style='font-family:VT323,monospace;font-size:13px;color:#555'>elements: </span>"
            f"{_tags(stage['elements'])}</div>",
            unsafe_allow_html=True)

    with right:
        world_preview = build_world(journey, choices) if stage["canvas_mode"] == "solar_system" else None
        st.components.v1.html(
            stage_canvas(stage["canvas_mode"], world_preview), height=350)

    # ── ROW 2: Key Insight (left) + Cause Chain (right) ───────────────────────
    ins_col, chain_col = st.columns([1, 1.4], gap="medium")
    with ins_col:
        if stage.get("critical_concept"):
            _sec("⚡ Key Insight", "#4488ff")
            st.markdown(
                f"<div style='background:#0d1a2e;border:2px solid #3366cc;"
                f"border-left:5px solid #4488ff;padding:8px 12px;"
                f"font-family:VT323,monospace;font-size:15px;color:#aac8ff;line-height:1.45'>"
                f"{stage['critical_concept']}</div>",
                unsafe_allow_html=True)

    with chain_col:
        if stage.get("causal_chain"):
            _sec("🔗 Cause Chain — how this stage shapes what comes next", "#998800")
            st.markdown(
                _render_causal_chain(stage["causal_chain"], stage.get("causal_summary", "")),
                unsafe_allow_html=True)

    st.divider()

    # ── ROW 3: Your Story (full width, journey context merged in) ─────────────
    _sec("📖 Your Story", "#3a7030")
    narr_variants = STAGE_NARRATIVES.get((stage["key"], journey), [])
    narr = random.choice(narr_variants) if narr_variants else stage["desc"][:300]
    journey_append = (
        f"<div style='margin-top:8px;padding-top:8px;border-top:1px solid #2a4a2a;"
        f"font-size:14px;color:#88aa88'>{ctx}</div>"
        if ctx else ""
    )
    st.markdown(f"<div style='{_NARR}'>{narr}{journey_append}</div>",
                unsafe_allow_html=True)

    _render_choice(stage, journey, choices)

    st.divider()
    nav_l, nav_r = st.columns(2)
    with nav_l:
        if stage_idx > 0:
            if st.button("← Previous", use_container_width=True):
                _prev()
    with nav_r:
        is_last = stage_idx == len(STAGES) - 1
        if st.button("See My World →" if is_last else "Next Stage →",
                     use_container_width=True, type="primary"):
            _next()


def _render_choice(stage, journey, choices) -> bool:
    key = stage["key"]

    if key == "supernova" and stage["choice"]:
        c = stage["choice"]
        st.divider()
        st.markdown(f"### 🔭 Your Choice: {c['question']}")
        st.caption(c["explanation"])
        _radio("", c["options"], "star_type", widget_key="radio_star_type")
        hz = HABITABLE_ZONES.get(choices.get("star_type", "G"), (0.7, 1.5))
        st.caption(f"Habitable zone for your star: **{hz[0]}–{hz[1]} AU**")
        return True

    if key == "nebula" and stage["choice"]:
        opts = DISTANCE_OPTIONS.get(journey, DISTANCE_OPTIONS["earth_like"])
        st.divider()
        st.markdown(f"### 🌀 Your Choice: {stage['choice']['question']}")
        st.caption(stage["choice"]["explanation"])
        _radio("", opts, "distance_au", widget_key="radio_distance")

        dist = choices.get("distance_au", 1.0)
        star = choices.get("star_type", "G")
        hz   = HABITABLE_ZONES.get(star, (0.7, 1.5))
        # Feature 9: real-time temperature at chosen distance
        temp_baseline = calc_temp(star, dist, "none")
        if journey == "icy_moon":
            # Icy moons SHOULD be outside the HZ — tidal heating is their energy source
            st.info(
                f"🧊 At {dist} AU, stellar surface temperature: **{temp_baseline}°C**. "
                f"Icy moons form far beyond the habitable zone — tidal heating from the "
                f"parent planet, not sunlight, will be the primary energy source.")
        elif in_hz(star, dist):
            st.success(
                f"✅ {dist} AU is in the habitable zone of your {STAR_LABELS[star]}. "
                f"Baseline temperature (no atmosphere): **{temp_baseline}°C**")
        else:
            st.warning(
                f"⚠️ {dist} AU is outside the habitable zone ({hz[0]}–{hz[1]} AU). "
                f"Baseline temperature (no atmosphere): **{temp_baseline}°C**")
        return True

    if key == "accretion":
        ac = ACCRETION_CHOICES.get(journey)
        if not ac:
            return False
        st.divider()
        st.markdown(f"### 🪐 Your Choice: {ac['question']}")
        st.caption(ac["explanation"])
        _radio("", ac["options"], ac["key"], widget_key="radio_accretion")
        return True

    if key == "evolution":
        st.divider()
        st.markdown("### ⚙️ Configure Your World")

        evo_map = {
            "gas_giant":   GAS_GIANT_EVOLUTION,
            "star_system": STAR_SYSTEM_EVOLUTION,
            "icy_moon":    ICY_MOON_EVOLUTION,
        }
        evo_list = evo_map.get(journey, EVOLUTION_CHOICES)

        col_a, col_b = st.columns(2)
        for i, evo in enumerate(evo_list):
            with col_a if i % 2 == 0 else col_b:
                with st.expander(f"{evo['icon']} {evo['question']}", expanded=True):
                    st.caption(evo["explanation"])
                    _radio("", evo["options"], evo["key"],
                           widget_key=f"radio_evo_{evo['key']}")

        # Features 9: live temperature + habitability preview
        st.divider()
        preview = build_world(journey, choices)
        bar_col = preview.hab_color
        st.markdown(
            f"<div style='font-family:\"Press Start 2P\",monospace;font-size:9px;"
            f"color:{bar_col};margin-bottom:4px'>Estimate: {preview.hab_label}</div>",
            unsafe_allow_html=True)
        st.progress(preview.habitability_score / 100,
                    text=f"Habitability: {preview.habitability_score}/100")
        if journey not in ("gas_giant", "star_system"):
            st.caption(
                f"Surface temperature with current choices: **{preview.surface_temp_c}°C** "
                f"({'in' if preview.in_habitable_zone else 'outside'} habitable zone)")
        return True

    return False


# ═══════════════════════════════════════════════════════════════════════════════
# RESULT PAGE
# ═══════════════════════════════════════════════════════════════════════════════


def show_result():
    journey = st.session_state.journey
    choices = st.session_state.choices
    world   = build_world(journey, choices)
    jinfo   = JOURNEYS[journey]
    summary = "\n".join(world.summary_lines)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"### {jinfo['icon']} {jinfo['label']}")
        st.markdown("**All stages complete!**")
        st.divider()
        for s in STAGES:
            st.markdown(f"✅ {s['name']}")
        st.divider()
        if st.button("🔁 Restart", use_container_width=True):
            _goto("home")
        if st.button("🏠 Home", use_container_width=True):
            _goto("home")

    # ── Feature 4: K2-generated world name + lore ──────────────────────────
    with st.spinner("Naming your world…"):
        world_name, world_lore = generate_world_identity(journey, summary, world.hab_label)

    st.markdown(f"# 🌍 {world_name}")
    st.markdown(
        f"<h3 style='color:{world.hab_color};font-family:\"Press Start 2P\",monospace;"
        f"font-size:11px;line-height:1.8'>{world.hab_label}</h3>",
        unsafe_allow_html=True)
    st.markdown(f"<div style='{_NARR}'>{world_lore}</div>", unsafe_allow_html=True)
    st.progress(world.habitability_score / 100,
                text=f"Habitability Score: {world.habitability_score}/100")
    st.divider()

    # ── Cross-Section | Properties | Description ──────────────────────────────
    col_svg, col_props, col_narr = st.columns([1, 1, 1.2])
    with col_svg:
        st.markdown("**Cross-Section**")
        # Wrap SVG in a full HTML doc so st.components renders it correctly
        svg_html = (
            "<html><body style='margin:0;padding:0;background:#07101f'>"
            + cross_section(world)
            + "</body></html>"
        )
        st.components.v1.html(svg_html, height=290)
    with col_props:
        st.markdown("**Properties**")
        for line in world.summary_lines:
            st.write(line)
    with col_narr:
        st.markdown("**Description**")
        with st.spinner("Generating description…"):
            narr = result_narrative(journey, summary, world.hab_label)
        st.markdown(f"<div style='{_NARR}'>{narr}</div>", unsafe_allow_html=True)

    # ── Factor Breakdown ──────────────────────────────────────────────────────
    st.divider()
    st.markdown("### Factor Breakdown")
    rows_html = ""
    for label, pts, max_pts in world.score_explanation:
        pct     = int(pts / max_pts * 100) if max_pts else 0
        bar_col = "#4ecf58" if pts > 0 else ("#d84a32" if pts < 0 else "#555")
        rows_html += (
            f"<tr><td style='padding:5px 10px;color:#ddd;font-family:VT323,monospace;font-size:13px'>{label}</td>"
            f"<td style='padding:5px 10px;width:140px'><div style='background:#111;border:2px solid #333;height:13px'>"
            f"<div style='background:{bar_col};width:{max(0,pct)}%;height:13px'></div></div></td>"
            f"<td style='padding:5px 10px;color:#aaa;font-family:VT323,monospace;font-size:12px'>{pts:+d}/{max_pts}</td></tr>"
        )
    st.markdown(
        f"<table style='border-collapse:collapse;width:100%;background:#111;border:2px solid #333'>"
        f"{rows_html}</table>", unsafe_allow_html=True)

    # ── Cosmic Story ──────────────────────────────────────────────────────────
    st.divider()
    st.markdown("### 🌌 Cosmic Story")
    st.caption("K2 tells a story about your world.")
    with st.spinner("K2 is imagining…"):
        story = cosmic_speculation(journey, summary, world.hab_label,
                                   st.session_state.speculation_seed)
    st.markdown(f"<div style='{_AMBER}'>{story}</div>", unsafe_allow_html=True)
    if st.button("Generate Another Story →", key="spec_btn"):
        st.session_state.speculation_seed += 1
        st.rerun()

    st.divider()
    if st.button("🔁 Start a New Adventure", type="primary"):
        _goto("home")


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════════

if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "journey":
    show_journey()
elif st.session_state.page == "result":
    show_result()
