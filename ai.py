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

# Sentences that look like K2 meta-commentary — stripped from front AND back
_REASONING_SENT = re.compile(
    r'^(\[.*?\]\.?'                               # [Paragraph], [Note], etc.
    r"|i'll\s|i will\s|i can\s|i need\s"
    r'|will\s(?:do|respond|output|write|now|produce)'
    r'|ok\.?\s|okay\.?\s|sure[,.]'
    r'|good[,.]|then\s(?:paragraph|line|the\s)'
    r'|yes,?\s|thus\s|use\s(?:adjective|vivid|concrete)'
    r'|check[:\s]|double.?check\b|note:\s|step\s\d'
    r'|count:\s|that\'s\s(?:one|two|three|four|five|six)\.'
    r'|sentence\s\d+\s+ends|sentence\s\d+\s+should'
    r'|let\'s\s(?:write|examine|check|count|verify)'
    r'|line\s\d+[:\s]|formatting:|potential\sissue'
    r'|make sure\s|no extra\s|output must\s'
    r'|just output\s|just write\s|produce final\s'
    r'|now,?\s(?:let|i|we)\s|now\s+let\'s\s'
    r'|the (?:output|name|paragraph|lore|response|format)\s'
    r'|we (?:need|must|should|will|have)\s)',
    re.IGNORECASE
)

# Patterns that mark where K2 starts self-verification after writing the answer
_VERIFICATION_START = re.compile(
    r'\b(?:count:|that\'s\s(?:one|two|three|four|five)\.|'
    r'sentence\s*\d+\s+ends\s+after|sentence\s*\d+\s+should|'
    r'let\'s\s+(?:examine|check|count|verify)|now\s+let\'s\s+(?:examine|check)|'
    r'check\s+formatting:|check:\s+sentence|'
    r'(?:line|paragraph)\s+\d+\s+(?:is|should|ends|has))',
    re.IGNORECASE
)


def _strip_reasoning(text: str) -> str:
    """
    Remove leading AND trailing reasoning sentences.
    Also truncates at the point K2 starts self-verifying its own output.
    """
    # Hard truncate at verification comments ("Count:", "Sentence1 ends after...")
    vm = _VERIFICATION_START.search(text)
    if vm:
        text = text[:vm.start()].strip().rstrip('"').rstrip("'")

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    while sentences and _REASONING_SENT.match(sentences[0].strip()):
        sentences.pop(0)
    while sentences and _REASONING_SENT.match(sentences[-1].strip()):
        sentences.pop()
    return " ".join(sentences).strip()


def _complete_sentences(text: str, max_chars: int = 1500) -> str:
    """Return the longest complete-sentence prefix within max_chars.
    Never cuts mid-sentence — always ends at a period/!/? boundary."""
    if len(text) <= max_chars:
        return text
    # Find all sentence-end positions within (or just past) max_chars
    for m in reversed(list(re.finditer(r'(?<=[.!?])\s', text[:max_chars + 120]))):
        if m.start() <= max_chars:
            return text[:m.start()].strip()
    return text[:max_chars]  # last resort


def _extract(text: str) -> str:
    """
    Extract the final answer from K2-Think-v2 output.

    Strategy: prompts end with 'BEGIN:' so K2 writes its reasoning,
    then signals the start of the actual answer with BEGIN:.
    We take the text after the LAST occurrence of BEGIN:.
    Falls back to paragraph/sentence heuristics if BEGIN: is absent.
    """
    # Strip explicit <think> blocks if present
    text = re.sub(
        r"<(?:think|thinking|reasoning)[^>]*>.*?</(?:think|thinking|reasoning)>",
        "", text, flags=re.DOTALL | re.IGNORECASE,
    ).strip()

    # Strategy 1: BEGIN: marker — take text after the LAST occurrence
    if "BEGIN:" in text:
        after = text.rsplit("BEGIN:", 1)[-1].strip().lstrip('\n').strip()
        if len(after) > 30:
            return _complete_sentences(_strip_reasoning(after))

    # Strategy 2: last paragraph (K2 answers at the end)
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]
    if len(paragraphs) >= 2:
        last = paragraphs[-1]
        if len(last) < 60:
            last = paragraphs[-2] + " " + last
        return _complete_sentences(_strip_reasoning(last))

    # Strategy 3: last 5 sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    candidate = " ".join(sentences[-5:]).strip()
    return _complete_sentences(_strip_reasoning(candidate)) or text[:800]


def _call(prompt: str, max_tokens: int = 4000) -> str:
    """
    Call K2 and extract the final answer.
    K2-Think-v2 always reasons before answering.  We append a BEGIN: instruction
    so K2 signals exactly where its final answer starts — we crop everything before it.
    """
    marked = prompt + "\n\nWhen finished thinking, write BEGIN: on its own line, then write only the final answer."
    resp = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": marked}],
        max_tokens=max_tokens,
    )
    raw = resp.choices[0].message.content or ""
    result = _extract(raw)
    # If the extracted text looks like mid-reasoning, signal failure so callers use fallback
    _reasoning_start = re.compile(
        r'^(so\b|well\b|but\b|yes\b|good\b|sure\b|'
        r'will do\b|will respond\b|will write\b|will output\b|'
        r'the user\b|we must\b|we need\b|we should\b|'
        r'i need\b|i will\b|i\'ll\b|i think\b|i believe\b|let me\b|'
        r'okay\b|alright\b|now,\b|first,\b|to write\b|make sure\b|'
        r'this asks\b|the prompt\b|it says\b|the instruction\b|'
        r'probably\b|maybe\b|perhaps\b|looking at\b|considering\b|'
        r'note that\b|also,\b|however,\b|since\b|given\b|'
        r'based on\b|according to\b|as per\b|check:\b|double.?check\b)',
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
        "The wind never stops on this world. It moves in slow, patient circles across cracked orange rock, "
        "carrying dust that has been carried before, ten thousand times. At the edge of a canyon so wide "
        "you cannot see the other side, something dark stains the stone — a streak of wet minerals "
        "that appears every morning and vanishes by noon, as if the cliff itself is breathing. "
        "Nothing lives here. But something keeps leaving marks."
    ),
    "gas_giant": (
        "Far below the highest cloud bands, where no sunlight has ever reached, the pressure is "
        "so immense that hydrogen stops being a gas and starts being something else entirely — "
        "a liquid metal that conducts electricity like copper and glows faintly from within. "
        "The storms that rage at the top of the atmosphere are old. The largest one has been "
        "spinning for longer than life has existed on Earth. No one knows what lives at the bottom "
        "of this world. No probe could survive the descent to find out."
    ),
    "icy_moon": (
        "Every few hours, a crack opens in the ice near the equator, and a plume of warm water "
        "shoots into space — rising fifty kilometres before freezing into crystals and drifting "
        "back down as snow. Inside the plume, if you could hover there, you would smell something "
        "faintly chemical, like rust and ocean mixed together. Scientists argue about what it means. "
        "The plume keeps erupting, patient and regular, like a heartbeat."
    ),
    "earth_like": (
        "On the night side, just before the terminator sweeps back into day, the temperature drops "
        "fast enough to freeze dew on every surface within an hour. In those quiet minutes, the "
        "world is still. Then the star crests the horizon and everything thaws at once — water "
        "running in thin films over rock, pooling in footprint-shaped hollows, evaporating before "
        "noon. If you stood there long enough, you would start to feel like the world was breathing."
    ),
    "star_system": (
        "The second planet is too hot. The fourth is too cold. But the third has had liquid water "
        "on its surface for six hundred million years, and in that time the ocean has learned "
        "a few tricks. From orbit it looks blue and white, ordinary, unremarkable. "
        "Up close, at the shoreline where the waves drag and release, "
        "something in the foam catches the light differently than water should. "
        "The third planet is still deciding what it wants to become."
    ),
}


@st.cache_data(show_spinner=False)
def cosmic_speculation(journey: str, world_summary: str, hab_label: str,
                       _seed: int = 0) -> str:
    """
    K2 writes a short creative story about the world — what it feels like to be there.
    _seed is a cache-buster so clicking 'Generate Another' produces a fresh story.
    """
    if not _API_AVAILABLE:
        return _SPECULATION_FALLBACK.get(journey, _SPECULATION_FALLBACK["earth_like"])
    _story_angles = [
        "describe what a single day feels like on this world — the light, the air, the sounds",
        "tell the story of one small thing that happens on this world: a wave, a storm, a crack in the ice",
        "write from the perspective of the first visitor to set foot here — what they see and smell and hear",
        "describe what this world looks like from its own sky at night",
        "tell what happens to this world in the far future — in a billion years",
        "describe the strangest thing about this world that a visitor would notice first",
        "write about this world as if it were alive — patient, ancient, and indifferent to visitors",
        "tell the story of one object — a rock, a wave, a cloud — and trace where it has been",
    ]
    angle = _story_angles[_seed % len(_story_angles)]
    try:
        prompt = (
            f"Write a short creative story (3–5 sentences) set on this world.\n"
            f"Angle: {angle}.\n"
            f"Write like a novelist, not a scientist. No numbers, no scientific terms. "
            f"Make it vivid, atmospheric, and surprising. Use the world's real properties to inspire the mood and details.\n\n"
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
            f"Invent a name (1-3 evocative scientific words) and one vivid origin paragraph "
            f"for this {journey} world based on its properties.\n\n"
            f"{world_summary}\nHabitability: {hab_label}\n\n"
            f"Reply with the name on the first line and the paragraph on the next line."
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
