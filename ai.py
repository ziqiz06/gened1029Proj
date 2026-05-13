"""
ai.py
K2-Think-v2 narrative + analysis generation with graceful fallback text.
"""
import os
import re

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(".env.local")

_client = OpenAI(
    api_key=os.getenv("K2_API_KEY", ""),
    base_url="https://api.k2think.ai/v1",
)
_MODEL         = os.getenv("K2_MODEL", "MBZUAI-IFM/K2-Think-v2")
_API_AVAILABLE = bool(os.getenv("K2_API_KEY"))

# ── Fallback text ─────────────────────────────────────────────────────────────

_STAGE_FALLBACK = {
    "bigbang":         "In the first instant, the entire universe was compressed into a point smaller than an atom, hotter than anything since. Space itself tore open, and the cosmos exploded into existence — not into emptiness, but as the very creation of space, time, and energy all at once.",
    "nucleosynthesis": "In the first three frantic minutes, the infant universe was a cosmic forge. Protons and neutrons collided and fused, building the first atomic nuclei — mostly hydrogen, a quarter helium, and a whisper of lithium. These three elements would be the only raw material available for the first billion years.",
    "first_stars":     "Darkness gave way to fire as the first stars ignited. Massive beyond imagination, these Population III giants lived only a few million years — but in that brief time they forged the universe's first carbon, oxygen, and nitrogen in their thermonuclear cores.",
    "supernova":       "The first stars died as supernovae, seeding the cosmos with carbon, silicon, iron, and phosphorus. Every heavy atom in your body was forged in a stellar furnace and scattered by one of these ancient explosions.",
    "galaxies":        "Over billions of years, gravity assembled stars into galaxies — vast islands of light separated by cosmic void. Each generation of stars left the universe richer in heavy elements, progressively assembling everything needed for planets and life.",
    "nebula":          "A dying star's shockwave compressed a nearby cloud of gas and dust. As the cloud collapsed and spun, a disk formed around a newborn star — a swirling nursery rich with every element needed to build worlds.",
    "accretion":       "Dust grains touched and stuck. Pebbles became boulders. Boulders swept up more material in a runaway process, growing into the planets taking shape within the disk right now.",
    "evolution":       "The young planet cooled from a molten ball into a world of rock, water, and air. Volcanoes outgassed primitive atmospheres. Over billions of years, the stage was set — for chemistry, complexity, and perhaps life.",
}

_QUESTION_FALLBACK = {
    "bigbang":         "If all the matter and energy in the universe was once compressed into a single point, what does that tell us about the nature of space itself?",
    "nucleosynthesis": "Why is it significant that the universe produced hydrogen and helium in a 3:1 ratio — and what would have been different if more heavy elements had formed?",
    "first_stars":     "Population III stars had no heavy elements at all. How does this make them fundamentally different from our Sun, and why does that matter for planet formation?",
    "supernova":       "Every carbon atom in your body was forged in a star that died before the Sun was born. What does this tell you about the relationship between life and cosmic history?",
    "galaxies":        "Galaxies recycle stellar material through successive generations of stars. How is this similar to — and different from — ecological recycling on Earth?",
    "nebula":          "The solar nebula had a frost line beyond which water ice could exist as a solid. How might the location of this frost line affect what kinds of worlds form?",
    "accretion":       "Why does a planet need to reach a certain mass to generate a magnetic field, and what would Earth look like today if it had formed with half its current mass?",
    "evolution":       "Earth is the only planet we know with active plate tectonics. What role does geology play in sustaining the conditions for life over billions of years?",
}

_HAB_ANALYSIS_FALLBACK = (
    "The combination of this world's properties creates a unique set of conditions. "
    "Whether life could emerge depends on whether liquid water can persist at the surface, "
    "whether the atmosphere can shield against radiation, and whether energy sources exist for biochemistry."
)
_CRITIQUE_FALLBACK = (
    "Every world faces trade-offs. The most promising worlds balance temperature, water, and "
    "protection from radiation — but each choice affects the others in ways that play out over billions of years."
)
_STUDY_GUIDE_FALLBACK = (
    "This planetary simulation demonstrates the key astrobiological principle that habitability "
    "is not a single factor but a convergence of conditions that must be sustained over geological timescales."
)


# ── Core helper ───────────────────────────────────────────────────────────────

# Sentences that look like K2 meta-commentary — strip from front of any output
_REASONING_SENT = re.compile(
    r'^(\[.*?\]\.?'                          # [Paragraph], [Note], etc.
    r"|i'll\s"                               # I'll output / I'll write
    r'|i will\s|i can\s|i need\s'
    r'|ok\.?\s|okay\.?\s|sure\.?\s'         # Ok, Okay, Sure
    r'|check:\s|note:\s|step\s\d'           # Check:, Note:, Step 1
    r'|make sure\s|print\s|no extra\s'
    r'|output must\s|just output\s|just write\s'
    r'|produce final\s|now,?\s(?:let|i|we)\s'
    r'|the (?:output|name|paragraph|lore|response|format)\s'
    r'|we (?:need|must|should|will|have)\s)',
    re.IGNORECASE
)


def _strip_reasoning(text: str) -> str:
    """Remove leading reasoning / meta-commentary sentences from a text block."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    while sentences and _REASONING_SENT.match(sentences[0].strip()):
        sentences.pop(0)
    return " ".join(sentences).strip()


def _extract(text: str) -> str:
    """
    Extract the final answer from K2-Think-v2 output.

    K2 reasons extensively then delivers the answer. Two observed patterns:
    1. K2 says "Now deliver:" / "Here is the answer:" → content follows on next line
    2. K2 writes reasoning paragraphs then a clean final paragraph = the answer

    We try both strategies in order and take the first that yields real content.
    All returned text is cleaned of leading reasoning sentences.
    """
    # Strip explicit <think> blocks if present
    text = re.sub(
        r"<(?:think|thinking|reasoning)[^>]*>.*?</(?:think|thinking|reasoning)>",
        "", text, flags=re.DOTALL | re.IGNORECASE,
    ).strip()

    # Strategy 1: find the LAST transition phrase K2 uses before delivering content
    transitions = list(re.finditer(
        r'(?:now\s+(?:deliver|write|here|provide|for\s+the)\b'
        r'|here\s+is\s+(?:the|my|a)\s+\w+'
        r'|final\s+(?:answer|response|narration|narrative|output)\s*[:.!-]'
        r'|(?:thus|therefore|so)[,\s]+(?:the\s+)?(?:answer|narration|response)\s*[:.!]'
        r'|(?:the|my)\s+(?:answer|response|narration|narrative|result)\s*[:.!]'
        r'|writing\s+(?:the|my)\s+(?:answer|narration|narrative))',
        text, re.IGNORECASE
    ))
    if transitions:
        last_t = transitions[-1]
        nl = text.find('\n', last_t.end())
        after = text[nl if nl != -1 else last_t.end():].strip()
        if len(after) > 40:
            return _strip_reasoning(after)[:800]

    # Strategy 2: last paragraph (answer comes last)
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]
    if len(paragraphs) >= 2:
        last = paragraphs[-1]
        if len(last) < 60:
            last = paragraphs[-2] + " " + last
        return _strip_reasoning(last)[:800]

    # Strategy 3: last 5 sentences with reasoning stripped
    sentences = re.split(r'(?<=[.!?])\s+', text)
    candidate = " ".join(sentences[-5:]).strip()
    return _strip_reasoning(candidate)[:700] or text[:500]


def _call(prompt: str, max_tokens: int = 4000) -> str:
    """
    Call K2 and extract the final answer.
    K2-Think-v2 always reasons before answering — high max_tokens gives it room
    to finish reasoning AND write the actual response.
    Instructions telling K2 'don't reason' are counterproductive: the model
    just reasons about the instruction and burns extra tokens doing so.
    """
    resp = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    raw = resp.choices[0].message.content or ""
    result = _extract(raw)
    # If the extracted text looks like mid-reasoning, signal failure so callers use fallback
    _reasoning_start = re.compile(
        r'^(so\b|well\b|but\b|the user\b|we must\b|we need\b|we should\b|'
        r'i need\b|i will\b|i think\b|i believe\b|let me\b|okay\b|alright\b|'
        r'now,\b|first,\b|to write\b|make sure\b|this asks\b|the prompt\b|'
        r'it says\b|the instruction\b|probably\b|maybe\b|perhaps\b|'
        r'looking at\b|considering\b|note that\b|also,\b|however,\b|'
        r'since\b|given\b|based on\b|according to\b|as per\b)',
        re.IGNORECASE
    )
    if _reasoning_start.match(result.strip()):
        return ""   # caller will use its own fallback
    return result


# ── 1. Stage narrative (personalised) ────────────────────────────────────────

@st.cache_data(show_spinner=False)
def stage_narrative(stage_key: str, stage_desc: str,
                    journey_context: str, choices_hint: str = "",
                    cannot_happen: tuple = ()) -> str:
    """2 vivid sentences about what is happening at this exact moment."""
    if not _API_AVAILABLE:
        return _STAGE_FALLBACK.get(stage_key, stage_desc[:200])
    try:
        # Ultra-minimal prompt — the fewer instructions, the less K2 reasons about format
        ctx = f" Context: {journey_context}" if journey_context else ""
        prompt = f"2 vivid sentences. Stage: {stage_key}.{ctx}\n\n{stage_desc[:180]}"
        result = _call(prompt, max_tokens=4000)
        return result or _STAGE_FALLBACK.get(stage_key, stage_desc[:200])
    except Exception:
        return _STAGE_FALLBACK.get(stage_key, stage_desc[:200])


# ── 2. Cosmic speculation (auto-generated what-if stories) ────────────────────

_SPECULATION_FALLBACK = {
    "rocky": (
        "On the third moon of your star's fourth planet, something unexpected is happening. "
        "Sheltered by a thick radiation belt and warmed by tidal flexing, a shallow ocean of "
        "brine has persisted for two billion years — long enough for chemistry to grow complicated. "
        "No one has looked yet, but the spectral signature of methane in that moon's thin haze "
        "does not have an obvious geological explanation."
    ),
    "gas_giant": (
        "Your gas giant's largest moon sits just inside the magnetic bubble that shields it from "
        "stellar radiation. Beneath its cracked ice shell, a salt ocean stretches 80 km deep — "
        "and near the hydrothermal vents on the seafloor, heat and minerals flow steadily upward. "
        "The chemical gradients there are eerily similar to the conditions where life first stirred on Earth."
    ),
    "icy_moon": (
        "Every 42 hours, your icy moon completes one orbit, flexing and cracking its frozen shell "
        "as it goes. The tidal stress carves fresh channels in the ice, and along those channels "
        "organic molecules — carried up from the subsurface ocean — are exposed to faint starlight. "
        "Whether any of those molecules have crossed the threshold into self-replication is a question "
        "a future probe might answer."
    ),
    "earth_like": (
        "A parallel history: if your world's early impactor had arrived ten million years later, "
        "the axial tilt would have been 42° instead of 23°. Seasonal swings of 80°C would have "
        "kept the tropics scorching and the poles frozen solid for half the year. Life might still "
        "have emerged in the deep ocean — but the land would have remained barren for far longer."
    ),
    "star_system": (
        "The fourth planet in your system sits just outside the habitable zone — cold, dry, and "
        "thin-aired. But three billion years ago it was warmer, and there are ancient river valleys "
        "preserved under the dust. Whether the microbes that may have thrived there survived "
        "underground, sheltered from radiation by a metre of rock, is still an open question."
    ),
}


@st.cache_data(show_spinner=False)
def cosmic_speculation(journey: str, world_summary: str, hab_label: str,
                       _seed: int = 0) -> str:
    """
    K2 invents one creative speculative scenario rooted in the world's actual properties.
    _seed is a cache-buster so clicking 'Generate Another' produces a fresh scenario.
    """
    if not _API_AVAILABLE:
        return _SPECULATION_FALLBACK.get(journey, _SPECULATION_FALLBACK["earth_like"])
    _seed_hints = [
        "focus on a hidden moon with unexpected chemistry",
        "explore an impact event that changed everything",
        "imagine how life might have started in an unlikely place",
        "describe how the star's evolution will reshape this world in 2 billion years",
        "invent a civilisation that might have risen and why it vanished",
        "trace one specific element — iron, phosphorus, or carbon — through cosmic history to here",
        "describe an orbital resonance or tidal effect that has surprising consequences",
        "speculate on what an alien probe would first detect from 10 light-years away",
    ]
    angle = _seed_hints[_seed % len(_seed_hints)]
    try:
        prompt = (
            f"Write exactly 3 vivid sentences: a speculative scenario for this world.\n"
            f"Angle: {angle}. Reference actual property values.\n\n"
            f"{world_summary}\nHabitability: {hab_label}"
        )
        result = _call(prompt, max_tokens=4000)
        return result or _SPECULATION_FALLBACK.get(journey, _SPECULATION_FALLBACK["earth_like"])
    except Exception:
        return _SPECULATION_FALLBACK.get(journey, _SPECULATION_FALLBACK["earth_like"])


# ── 3. Stage thought question ─────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def stage_question(stage_key: str, journey_context: str, choices_hint: str) -> str:
    """K2 generates one thought-provoking scientific question for this stage."""
    if not _API_AVAILABLE:
        return _QUESTION_FALLBACK.get(stage_key, "What surprised you most about this stage of cosmic history?")
    try:
        prompt = (
            f"Write exactly 1 causal question about '{stage_key}'.\n"
            f"Format: 'If [X] had been different, what would happen to [Y]?'\n"
            f"Connect to habitability or life. Output the question only.\n\n"
            f"World context: {journey_context}. Choices: {choices_hint or 'early stage'}"
        )
        result = _call(prompt, max_tokens=4000)
        return result or _QUESTION_FALLBACK.get(stage_key, "What surprised you most about this stage of cosmic history?")
    except Exception:
        return _QUESTION_FALLBACK.get(stage_key, "What surprised you most about this stage of cosmic history?")


# ── 4. Dynamic world identity (name + lore) ───────────────────────────────────

@st.cache_data(show_spinner=False)
def generate_world_identity(journey: str, world_summary: str, hab_label: str) -> tuple[str, str]:
    """Returns (planet_name, lore_paragraph) unique to this world's properties."""
    _defaults = {
        "rocky": ("Lithos-VII", _STAGE_FALLBACK["evolution"]),
        "gas_giant": ("Jovaris Prime", _STAGE_FALLBACK["evolution"]),
        "icy_moon": ("Glaceon-IV", _STAGE_FALLBACK["evolution"]),
        "earth_like": ("Nova Terra", _STAGE_FALLBACK["evolution"]),
        "star_system": ("Helio System Alpha", _STAGE_FALLBACK["evolution"]),
    }
    if not _API_AVAILABLE:
        return _defaults.get(journey, ("Unknown World", _STUDY_GUIDE_FALLBACK))
    try:
        prompt = (
            f"Write a name and origin paragraph for a {journey} world.\n"
            f"Line 1: planet name (1-3 words, scientific and evocative)\n"
            f"Line 2: one vivid paragraph describing how it formed and what it is like today.\n\n"
            f"{world_summary}\nHabitability: {hab_label}"
        )
        text = _call(prompt, max_tokens=3500)
        lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
        if len(lines) >= 2:
            name = lines[0]
            lore = " ".join(lines[1:])
            # Sanity: name should be short, lore should be substantial
            if 1 <= len(name.split()) <= 6 and len(lore) > 40:
                return name, lore
        # Fallback: use full text as lore with default name
        default_name = _defaults.get(journey, ("Unknown World",))[0]
        return default_name, text
    except Exception:
        return _defaults.get(journey, ("Unknown World", _STUDY_GUIDE_FALLBACK))


# ── 5. Scientific critique ────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def scientific_critique(world_summary: str, hab_label: str, journey: str) -> str:
    """K2 identifies specific scientific tensions in the world's configuration."""
    if not _API_AVAILABLE:
        return _CRITIQUE_FALLBACK
    try:
        prompt = (
            f"Write 4-5 sentences about this {journey} world.\n"
            f"Identify 2 scientific tensions. For each: state it, then trace consequences over geological time.\n"
            f"End with one astrobiological principle this world illustrates.\n\n"
            f"{world_summary}\nHabitability: {hab_label}"
        )
        result = _call(prompt, max_tokens=4000)
        return result or _CRITIQUE_FALLBACK
    except Exception:
        return _CRITIQUE_FALLBACK


# ── 6. Habitability analysis (replaces lookup-table explanation) ──────────────

@st.cache_data(show_spinner=False)
def habitability_analysis(world_summary: str, score: int,
                           hab_label: str, journey: str) -> str:
    """K2 reasons through WHY this world is or isn't habitable, step by step."""
    if not _API_AVAILABLE:
        return _HAB_ANALYSIS_FALLBACK
    try:
        prompt = (
            f"Write exactly 4 sentences about this {journey} world's habitability.\n"
            f"Sentences 1-3: explain why it is '{hab_label}' ({score}/100) using cause-and-effect (X → Y → Z).\n"
            f"Sentence 4: one factor that, if changed, would flip the verdict.\n\n"
            f"{world_summary}"
        )
        result = _call(prompt, max_tokens=4000)
        return result or _HAB_ANALYSIS_FALLBACK
    except Exception:
        return _HAB_ANALYSIS_FALLBACK


# ── 9. Result narrative (used on result page) ─────────────────────────────────

@st.cache_data(show_spinner=False)
def result_narrative(journey: str, world_summary: str, hab_label: str) -> str:
    """3–4 sentence description of the final world's conditions."""
    _fallback = (
        "This world has been shaped by 13.8 billion years of cosmic history. "
        "Every choice echoes decisions made by nature on countless worlds across the universe."
    )
    if not _API_AVAILABLE:
        return _fallback
    try:
        earth_note = " Life is confirmed here." if hab_label == "Life Confirmed" else ""
        prompt = (
            f"Write exactly 2 vivid sentences describing the surface of this {journey} world right now.\n"
            f"Be specific about the listed properties.{earth_note}\n\n"
            f"{world_summary}\nHabitability: {hab_label}"
        )
        return _call(prompt)
    except Exception:
        return _fallback


# ── 10. Study guide ───────────────────────────────────────────────────────────

def study_guide_text(journey: str, world_summary: str,
                     hab_label: str, score: int) -> str:
    """
    K2 writes a 3-paragraph academic study guide.
    Not @cached — called only when the user clicks the button,
    stored in st.session_state by the caller.
    """
    if not _API_AVAILABLE:
        return _STUDY_GUIDE_FALLBACK
    try:
        prompt = (
            "Write a 3-paragraph academic reflection about this planetary simulation, "
            "suitable for a general education science course.\n\n"
            "Paragraph 1: Describe how this world's key properties emerged from "
            "cosmic history — Big Bang nucleosynthesis, stellar evolution, supernovae, "
            "and planetary accretion.\n"
            "Paragraph 2: Explain why this world does or does not meet the conditions "
            "for life, referencing specific astrobiological criteria such as the "
            "habitable zone, liquid water, atmospheric shielding, and magnetic protection.\n"
            "Paragraph 3: Connect to the broader themes of the course — entropy and life "
            "as local organisation, the origin of life from simple molecules, and what "
            "Earth's example teaches us about the rarity or commonness of habitable worlds.\n\n"
            "Write in academic prose. No bullet points. No headers.\n\n"
            f"World properties:\n{world_summary}\n"
            f"Journey: {journey}\nHabitability: {hab_label} ({score}/100)"
        )
        return _call(prompt, max_tokens=4000)
    except Exception:
        return _STUDY_GUIDE_FALLBACK
