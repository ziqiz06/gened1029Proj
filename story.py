"""
story.py
Journey definitions, cosmic stages, choice menus, and educational text.
"""

# ── Journeys ──────────────────────────────────────────────────────────────────

JOURNEYS = {
    "rocky": {
        "label": "Rocky Planet",
        "icon": "🪨",
        "desc": "Form a small, solid world like Mars or Venus. Distance, atmosphere, and geology decide its fate.",
        "example": "Mars · Venus · Mercury",
    },
    "gas_giant": {
        "label": "Gas Giant",
        "icon": "🌀",
        "desc": "Build a massive world of swirling hydrogen and helium like Jupiter. No solid surface — just scale.",
        "example": "Jupiter · Saturn",
    },
    "icy_moon": {
        "label": "Icy Moon",
        "icon": "🧊",
        "desc": "Form a frozen world orbiting a gas giant. Tidal heating could create a hidden ocean — and maybe life.",
        "example": "Europa · Enceladus",
    },
    "earth_like": {
        "label": "Earth-like World",
        "icon": "🌍",
        "desc": "Try to recreate all the conditions for life: liquid water, atmosphere, magnetic field, and plate tectonics.",
        "example": "Earth",
    },
    "star_system": {
        "label": "Star System",
        "icon": "⭐",
        "desc": "Shape the star itself and the system of planets that form around it.",
        "example": "The Solar System",
    },
}

# ── Cosmic Stages ─────────────────────────────────────────────────────────────

STAGES = [
    {
        "key": "bigbang",
        "name": "The Big Bang",
        "time": "t = 0",
        "desc": (
            "Space itself tears open — not an explosion into existing emptiness, but the simultaneous "
            "creation of space, time, and energy. In the first trillionths of a second, the universe "
            "is so hot that matter and antimatter flash in and out of existence, annihilating each other "
            "almost perfectly. A tiny asymmetry — one extra matter particle per billion — is all that "
            "saves the material universe from complete cancellation. "
            "Temperature is the controlling variable: as the cosmos expands and cools, only the simplest "
            "particles (quarks and leptons) can survive. "
            "This cooling rate is the universe's first hard constraint — everything that comes later "
            "depends on how fast temperature drops."
        ),
        "critical_concept": "Space expands — it doesn't explode into existing space. Temperature controls what can exist. Cooling = increasing complexity.",
        "causal_chain": "Expansion rate → cooling rate → which particles survive → what chemistry becomes possible → all future structure.",
        "causal_summary": "How fast the universe cools determines the complexity of everything that can ever exist.",
        "cannot_happen": [
            "No atoms — quarks are not yet bound into nuclei",
            "No chemistry — no bonds, no molecules of any kind",
            "No structure — every point is equally hot and dense",
        ],
        "thought_prompt": "If matter and antimatter had been exactly equal, what would remain today?",
        "elements": ["Quarks", "Leptons", "Photons"],
        "canvas_mode": "bigbang",
        "choice": None,
        "journey_context": {
            "rocky":       "Every atom of iron, silicon, and carbon in your rocky world was pure energy — photons and quarks — in this instant.",
            "gas_giant":   "The hydrogen that will make up 90% of your gas giant does not yet exist as atoms. It is forming right now.",
            "icy_moon":    "The hydrogen and oxygen that will become your moon's ice both begin as pure energy. Water is still billions of years away.",
            "earth_like":  "Every ocean, every carbon molecule in every cell of life — it all begins right now as pure energy and elementary particles.",
            "star_system": "All the energy your star will ever radiate is unleashed in this moment. It is being set in motion right now.",
        },
    },
    {
        "key": "nucleosynthesis",
        "name": "Big Bang Nucleosynthesis",
        "time": "First 3 minutes",
        "desc": (
            "By three seconds in, the universe cools enough for quarks to bind into protons and neutrons. "
            "But here is the critical constraint: the expansion is happening so rapidly that by the time "
            "nuclei could fuse into carbon or oxygen, the temperature has already dropped too far. "
            "Nucleosynthesis shuts down after just three minutes, locking in a universe that is "
            "roughly 75% hydrogen and 25% helium by mass — permanently. "
            "No carbon, no oxygen, no nitrogen, no chemistry of life is yet possible. "
            "This 3:1 ratio is fixed by the physics of the early universe and matters enormously: "
            "the first stars will be made almost entirely of these two light elements, "
            "with none of the 'metals' needed for rocky planets or complex chemistry."
        ),
        "critical_concept": "The universe expands too fast for fusion to go past helium. This permanently limits early chemistry — all heavier elements must wait for stars.",
        "causal_chain": "Fast expansion → fusion shuts down at He → only H/He exist → first stars form from pure H/He → no metals, no rocky planets yet.",
        "causal_summary": "Because the universe expanded too fast, fusion stopped at helium — locking out all heavier chemistry until the first stars formed.",
        "cannot_happen": [
            "No carbon, oxygen, or nitrogen — fusion stops at helium",
            "No rocky planets — no silicon or iron exists yet",
            "No life chemistry — the carbon backbone doesn't exist anywhere",
        ],
        "thought_prompt": "If the universe had expanded twice as slowly, what heavier elements might have formed in these first three minutes?",
        "elements": ["H (75%)", "He (25%)", "trace Li"],
        "canvas_mode": "plasma",
        "choice": None,
        "journey_context": {
            "rocky":       "Silicon and iron — the stuff of rock and planetary cores — cannot form here. They must be built inside stars that don't yet exist.",
            "gas_giant":   "Your gas giant's bulk is being born right now: it will be 90% this primordial hydrogen and helium, unchanged since these three minutes.",
            "icy_moon":    "Water (H₂O) requires oxygen, which does not yet exist. That oxygen will only arrive from dying stars billions of years from now.",
            "earth_like":  "Because no heavy elements form here, life is impossible for the next billion years. All complexity waits for stellar chemistry.",
            "star_system": "Your star will be made almost entirely of this primordial hydrogen and helium. Its bulk composition is fixed right now.",
        },
    },
    {
        "key": "first_stars",
        "name": "First Stars (Population III)",
        "time": "100–500 million years",
        "desc": (
            "For over 100 million years, the universe is completely dark — hydrogen and helium gas, "
            "slowly cooling. Then gravity begins to win, pulling gas into clouds. "
            "But there are no heavy elements yet, so these clouds cannot cool efficiently: "
            "no carbon monoxide, no water vapor to radiate away heat. "
            "Gas that cannot cool cannot collapse into small, Sun-like stars — "
            "instead, entire massive clouds collapse at once, forming Population III stars "
            "hundreds of times more massive than the Sun. "
            "These giants live only a few million years, but their cores burn at extreme temperatures, "
            "fusing hydrogen all the way up to carbon, oxygen, nitrogen, and beyond — "
            "creating the first heavy elements anywhere in the universe. "
            "The universe has finally started building chemical complexity."
        ),
        "critical_concept": "No metals → gas cannot cool → cannot form small stars. The first stars must be enormous — short-lived factories that produce all heavy elements.",
        "causal_chain": "H/He only → inefficient cooling → massive stars required → short lifespan → cores fuse C, O, N → universe gains complexity.",
        "causal_summary": "Without heavy elements to cool the gas, only enormous short-lived stars could form — and their deaths produced all the complex chemistry that followed.",
        "cannot_happen": [
            "No small Sun-like stars — no metals means gas can't cool into compact cores",
            "No rocky planets yet — no silicon, iron, or magnesium in existence",
            "No liquid water anywhere — oxygen is only just being created",
        ],
        "thought_prompt": "Why could the first stars not be small, long-lived stars like our Sun — and why does that matter for planet formation?",
        "elements": ["H", "He", "C", "N", "O"],
        "canvas_mode": "first_stars",
        "choice": None,
        "journey_context": {
            "rocky":       "Carbon, silicon, and oxygen — the three most critical elements for building rock — are forged here for the very first time.",
            "gas_giant":   "Gas giants need a solid rocky core to trigger gas capture. That core's silicon and iron is first created in these stars.",
            "icy_moon":    "Oxygen is synthesized here for the first time. Now H₂O — water — can form anywhere in the universe for the first time ever.",
            "earth_like":  "Carbon, the backbone of all known biochemistry, exists for the first time. Life's chemical alphabet is just beginning to be written.",
            "star_system": "The heavy elements your star system needs — for rocky planets, atmospheres, and life — are just beginning to enter the universe.",
        },
    },
    {
        "key": "supernova",
        "name": "Supernovae & Heavy Elements",
        "time": "0.5–2 billion years",
        "desc": (
            "When a massive star exhausts its fuel, the iron core collapses in under a second — "
            "a gravitational implosion that releases more energy than the Sun will emit in its entire lifetime. "
            "This is physics necessity, not just drama: elements heavier than iron cannot form "
            "by ordinary fusion — they require more energy to build than they release. "
            "Only the catastrophic energy of a supernova shock can forge gold, uranium, phosphorus, "
            "and iodine in milliseconds. "
            "The explosion then disperses everything — carbon, oxygen, silicon, iron, phosphorus — "
            "across light-years of space, seeding future molecular clouds with planet-building material. "
            "Every atom in your world that is heavier than helium was either built inside a stellar "
            "core or forged in the final second of a supernova explosion."
        ),
        "critical_concept": "Elements heavier than iron require more energy to build than they release — only supernovae provide it. No explosions = no planets, no life.",
        "causal_chain": "Massive stars die → core collapses → explosion forges heavy elements → ejects into space → seeds future solar nebulae.",
        "causal_summary": "Every heavy atom in your world was forged inside a dying star and scattered across space by its explosion.",
        "cannot_happen": [
            "No planetary systems yet — material is just being scattered",
            "No gold or uranium from living stars — only supernovae provide enough energy",
            "No life — the building blocks are still dispersing through space",
        ],
        "thought_prompt": "Why can't gold or platinum form inside a living star — what makes supernovae the only factory for elements heavier than iron?",
        "elements": ["H", "He", "C", "N", "O", "Si", "S", "Fe", "Ni", "Ca", "P"],
        "canvas_mode": "supernova",
        "choice": {
            "key": "star_type",
            "question": "What type of star will your world orbit?",
            "explanation": (
                "The star's mass determines its luminosity, lifespan, habitable zone location, "
                "and the radiation environment. This is the single most important choice for your world."
            ),
            "options": [
                {
                    "value": "M",
                    "label": "M Dwarf — Red Dwarf",
                    "desc": "Very small and dim. Lives trillions of years. HZ: 0.1–0.4 AU. Prone to violent flares.",
                },
                {
                    "value": "K",
                    "label": "K Dwarf — Orange Dwarf",
                    "desc": "Slightly smaller than the Sun. Extremely stable, ~30 billion year lifespan. HZ: 0.4–0.8 AU.",
                },
                {
                    "value": "G",
                    "label": "G Dwarf — Sun-like ☀",
                    "desc": "Like our Sun. ~10 billion year lifespan. HZ: 0.7–1.5 AU. Earth orbits a G dwarf.",
                },
                {
                    "value": "F",
                    "label": "F Dwarf — Yellow-White",
                    "desc": "Hotter and brighter than the Sun. Only ~3–4 billion years. HZ: 1.2–2.5 AU. High UV.",
                },
            ],
        },
        "journey_context": {
            "rocky":       "Silicon, iron, and magnesium from supernovae will become your world's mantle, core, and crust. Without these explosions, rock is impossible.",
            "gas_giant":   "Your gas giant's rocky core — required to trigger gas capture — is made of silicon and iron first scattered by supernovae.",
            "icy_moon":    "Every water molecule on your moon contains oxygen forged in a stellar core and scattered by an explosion before your solar system existed.",
            "earth_like":  "Phosphorus — essential for DNA and ATP — is forged only in supernovae. Without stellar death, the chemistry of life cannot exist.",
            "star_system": "Your star forms from a cloud enriched by previous supernova generations. Its heavy element content sets what kinds of planets can form.",
        },
    },
    {
        "key": "galaxies",
        "name": "Galaxy Formation",
        "time": "2–8 billion years",
        "desc": (
            "Invisible dark matter — which interacts gravitationally but not electromagnetically — "
            "forms halos that act as gravitational scaffolding for the visible universe. "
            "Without dark matter, gas disperses uniformly and nothing clumps: "
            "no galaxies form, no stars, no planets, no life — ever. "
            "Where dark matter halos concentrate, gas flows in, collapsing into the first galaxies. "
            "Crucially, this is a multi-generational process: stars form, fuse heavy elements in their cores, "
            "die, and enrich the interstellar gas — which then forms the next generation of stars "
            "with even more heavy elements. "
            "By the time our solar system forms, the Milky Way has cycled through three or four stellar "
            "generations, building up the chemical richness that makes rocky planets and living chemistry possible."
        ),
        "critical_concept": "Dark matter is the invisible scaffolding — without it, no galaxies form. Galaxies enable multi-generational stellar recycling that builds heavy elements.",
        "causal_chain": "Dark matter halos → galaxy structure → successive stellar generations → progressive element enrichment → chemistry rich enough for life.",
        "causal_summary": "Without dark matter and multi-generational star cycles, the chemistry needed for planets and life could never have built up.",
        "cannot_happen": [
            "No solar systems yet — molecular clouds still assembling inside forming galaxies",
            "No Earth-like chemistry — heavy elements still building up over stellar generations",
            "No stable planetary systems — the galactic environment is still too turbulent",
        ],
        "thought_prompt": "Why does each generation of stars leave its successor's molecular cloud richer in heavy elements — and why does this matter for planet formation?",
        "elements": ["H", "He", "C", "N", "O", "Si", "S", "Fe", "Mg", "P", "Ca"],
        "canvas_mode": "galaxy",
        "choice": None,
        "journey_context": {
            "rocky":       "The molecular cloud your solar system will form from is only now accumulating enough silicon and iron for rocky planet-building.",
            "gas_giant":   "The gas-rich outer disk your giant forms from is being assembled inside a spiral arm, enriched by multiple stellar generations.",
            "icy_moon":    "Cold outer regions of forming solar systems — where icy moons live — are accumulating water-ice-rich material right now.",
            "earth_like":  "The galaxy is only now chemically mature enough to support water-bearing, potentially habitable rocky worlds.",
            "star_system": "Your star will be born in a stellar nursery inside a spiral arm, inheriting the element abundances of all previous stellar generations.",
        },
    },
    {
        "key": "nebula",
        "name": "Solar Nebula Forms",
        "time": "~9 billion years (4.6 Gya)",
        "desc": (
            "A nearby dying star's shockwave compresses a molecular cloud, triggering its gravitational collapse. "
            "As the cloud falls inward, conservation of angular momentum spins it faster — "
            "like a figure skater pulling in their arms — flattening it into a rotating disk. "
            "A protostar ignites at the center, heating the disk outward and creating a sharp temperature gradient. "
            "Inside the 'frost line' (~3 AU), only silicates and metals remain solid — the raw materials for rocky worlds. "
            "Beyond the frost line, water, ammonia, and methane freeze onto dust grains, "
            "more than doubling the solid material available and enabling both massive icy cores and frozen worlds. "
            "Your world's fundamental character — rocky or icy, solid or gaseous — is determined entirely "
            "by where in this disk it forms."
        ),
        "critical_concept": "Angular momentum conservation creates the disk. The frost line divides it into rocky inner and icy outer zones — determining what kinds of worlds form where.",
        "causal_chain": "Cloud collapse → spin-up → disk forms → temperature gradient → frost line → rocky worlds inside, icy worlds and gas giants outside.",
        "causal_summary": "The temperature at your orbit in the disk determined whether you became rocky, icy, or gaseous — before a single planet existed.",
        "cannot_happen": [
            "No planets yet — only the disk of gas and dust exists",
            "No atmospheres yet — no solid surfaces to outgas from",
            "No life — the building materials are just beginning to settle",
        ],
        "thought_prompt": "How does the frost line position determine whether a world will be rocky, icy, or gaseous — and what would change if the star were twice as bright?",
        "elements": ["H", "He", "C", "N", "O", "Si", "Fe", "Mg", "Ca", "P"],
        "canvas_mode": "nebula",
        "choice": {
            "key": "distance_au",
            "question": "Where in the protoplanetary disk does your world begin to form?",
            "explanation": (
                "Distance from the star determines surface temperature, whether water can be liquid or ice, "
                "and what materials are available. The 'frost line' at ~3 AU divides the rocky inner disk from the icy outer disk."
            ),
            "options": None,  # injected per journey in app.py
        },
        "journey_context": {
            "rocky":       "You form inside the frost line where only silicates and metals are solid. Water must arrive later via asteroids — or your world stays dry forever.",
            "gas_giant":   "You form beyond the frost line, where icy grains are abundant. That extra solid material is why your massive core can grow fast enough to capture gas.",
            "icy_moon":    "Your moon forms in the cold outer disk where water ice is stable and abundant — this is the direct origin of its icy composition.",
            "earth_like":  "Position is critical: too close and water boils into a runaway greenhouse; too far and it freezes permanently. The frost line is your boundary.",
            "star_system": "The disk's temperature gradient dictates which planets end up rocky (inner) and which are gas or ice giants (outer). The blueprint is being drawn now.",
        },
    },
    {
        "key": "accretion",
        "name": "Planet Accretion",
        "time": "9.3–9.8 billion years",
        "desc": (
            "Dust grains collide and stick — first by electrostatic attraction, then by gravity as objects grow. "
            "Once a body reaches tens of kilometers, a runaway feedback loop begins: "
            "larger mass → stronger gravity → sweeps up more material faster → grows even larger. "
            "This runaway accretion can build a planetary core in as little as a million years. "
            "The energy of all these collisions melts the young planet; "
            "in this molten state, heavy iron sinks to the center (the core) while lighter silicates rise "
            "to form the mantle and crust — a process called differentiation. "
            "This is not just geology: a large, convecting molten iron core generates the magnetic field "
            "that will shield any future atmosphere from being stripped by stellar wind. "
            "The chain is: mass → gravity → atmosphere retention → core size → magnetic field → long-term habitability."
        ),
        "critical_concept": "Runaway growth: bigger = faster. Melting causes differentiation. A large iron core directly determines whether a magnetic shield forms — and whether an atmosphere survives.",
        "causal_chain": "Runaway accretion → planet melts → Fe sinks to core → dynamo generates magnetic field → field shields atmosphere → habitability possible.",
        "causal_summary": "Mass determines everything downstream — gravity, differentiation, magnetic field, atmosphere, and ultimately whether life is conceivable.",
        "cannot_happen": [
            "No atmosphere yet — no solid surface to outgas from volcanoes",
            "No life — the surface is molten and bombarded by debris",
            "No stable oceans — no liquid water can exist on a magma ocean world",
        ],
        "thought_prompt": "Why must a planet reach a minimum mass before a magnetic field can form — and what happens to its atmosphere without one?",
        "elements": ["Si", "Fe", "Mg", "C", "O", "H", "He"],
        "canvas_mode": "accretion",
        "choice": {
            "key": None,
            "question": None,
            "explanation": None,
            "options": None,
        },
        "journey_context": {
            "rocky":       "Your world's mass determines everything downstream: too little and it cannot hold an atmosphere or generate a magnetic field.",
            "gas_giant":   "You need a rocky core of roughly 10 Earth masses to trigger runaway gas capture before the stellar wind disperses the disk.",
            "icy_moon":    "Your small moon forms from icy debris. Its limited mass means little internal heat — but tidal forces from the parent planet will compensate.",
            "earth_like":  "Mass is critical: too little → thin atmosphere, weak field; too much → hydrogen-dominated atmosphere and crushing surface gravity.",
            "star_system": "The disk's mass distribution determines how many planets form and how massive they get. Orbital resonances shape the final system architecture.",
        },
    },
    {
        "key": "evolution",
        "name": "Planetary Evolution",
        "time": "9.8–13.8 billion years (present)",
        "desc": (
            "Life, as we understand it, requires three independent conditions that must all be met simultaneously "
            "and sustained for billions of years: a liquid solvent (water has unique properties — "
            "maximum density at 4°C, so ice floats and insulates rather than sinking and freezing oceans solid; "
            "the highest heat capacity of any common liquid, stabilizing temperature), "
            "a flexible chemistry (carbon forms four bonds simultaneously, linking into chains, "
            "rings, and helices of almost unlimited complexity — no other element does this), "
            "and a sustained energy source (sunlight, chemical gradients, or tidal forces). "
            "Where plate tectonics is active, it closes a climate feedback loop: volcanism releases CO₂, "
            "weathering removes it, and this carbon-silicate cycle regulates temperature over billions of years. "
            "All three requirements must align — and stay aligned — for life to take hold. "
            "This is where 13.8 billion years of cosmic history either pays off or falls just short."
        ),
        "critical_concept": "Life needs three independent things simultaneously: liquid water, carbon chemistry, and a sustained energy source. All three must align for billions of years.",
        "causal_chain": "Magnetic field → atmosphere survives → water stays liquid → carbon chemistry operates → energy source available → life conceivable.",
        "causal_summary": "All three conditions for life must align simultaneously and stay aligned for billions of years — none of them are guaranteed.",
        "cannot_happen": [
            "No life without liquid water — the solvent for all known biochemistry",
            "No life without a carbon framework — no other element builds equivalent complexity",
            "No guaranteed life — even with all conditions met, the origin of life is not automatic",
        ],
        "thought_prompt": "If plate tectonics stopped on Earth tomorrow, how would the carbon-silicate cycle break down — and how long before the climate became uninhabitable?",
        "elements": ["all"],
        "canvas_mode": "solar_system",
        "choice": None,
        "journey_context": {
            "rocky":       "Without a magnetic field, stellar wind strips the atmosphere. Without atmosphere, water evaporates or freezes. Your choices converge here.",
            "gas_giant":   "Your gas giant itself is not habitable, but its moons may be — if tidal heating, magnetic shielding, and liquid water all align.",
            "icy_moon":    "Tidal forces flex your moon's interior, generating heat that sustains a liquid ocean beneath kilometers of ice — potentially for billions of years.",
            "earth_like":  "Every choice you made — distance, mass, atmosphere, water, field, geology — converges here. Does your world meet all three requirements for life?",
            "star_system": "Stability over geological time is the hidden requirement. Impacts, flares, and orbital chaos can sterilize a world that would otherwise be habitable.",
        },
    },
]

# ── Distance options (injected into the nebula stage per journey) ─────────────

DISTANCE_OPTIONS = {
    "rocky": [
        {"value": 0.3,  "label": "0.3 AU — Scorched inner zone",    "desc": "Extreme heat. No liquid water possible. Like Mercury."},
        {"value": 0.5,  "label": "0.5 AU — Hot inner zone",         "desc": "Very hot. Possible runaway greenhouse if atmosphere builds up."},
        {"value": 0.7,  "label": "0.7 AU — Inner habitable edge",   "desc": "Warm. Like a hotter Venus or a cooler Earth."},
        {"value": 1.5,  "label": "1.5 AU — Outer rocky zone",       "desc": "Cool. Like Mars' orbit. Thin atmosphere, likely frozen surface."},
    ],
    "gas_giant": [
        {"value": 2.0,  "label": "2.0 AU — Inner giant zone",       "desc": "Just beyond the frost line. Rocky core forms quickly."},
        {"value": 5.2,  "label": "5.2 AU — Jupiter distance",       "desc": "Classic gas giant orbit. Like Jupiter in our solar system."},
        {"value": 9.5,  "label": "9.5 AU — Saturn distance",        "desc": "Cold outer zone. Like Saturn — rings likely."},
        {"value": 19.0, "label": "19 AU — Uranus distance",         "desc": "Very cold. Ice giant territory. Slow formation."},
    ],
    "icy_moon": [
        {"value": 3.0,  "label": "3.0 AU — Inner ice belt",         "desc": "Parent planet near inner ice belt. Some solar heating reaches the moon."},
        {"value": 5.2,  "label": "5.2 AU — Jupiter analog",         "desc": "Like Europa or Ganymede orbiting a Jupiter-like planet."},
        {"value": 9.5,  "label": "9.5 AU — Saturn analog",          "desc": "Like Enceladus orbiting a Saturn-like planet."},
        {"value": 19.0, "label": "19 AU — Cold outer system",       "desc": "Very cold outer system. Tidal heating must provide all energy."},
    ],
    "earth_like": [
        {"value": 0.7,  "label": "0.7 AU — Warm inner habitable zone",  "desc": "Warm. Risk of runaway greenhouse if CO₂ builds up."},
        {"value": 1.0,  "label": "1.0 AU — Earth's orbit ✓",            "desc": "Like Earth. Comfortably in the habitable zone of a G star."},
        {"value": 1.2,  "label": "1.2 AU — Mid habitable zone",         "desc": "Slightly cooler. Still habitable with the right greenhouse effect."},
        {"value": 1.5,  "label": "1.5 AU — Cool outer habitable zone",  "desc": "Cool edge. Needs a moderate greenhouse to stay above freezing."},
    ],
    "star_system": [
        {"value": 0.5,  "label": "0.5 AU — Inner system",   "desc": "Rocky inner planets dominate. Habitable zone depends on star type."},
        {"value": 1.0,  "label": "1.0 AU — Earth-like orbit", "desc": "Focus on the habitable zone of the system."},
        {"value": 5.0,  "label": "5.0 AU — Outer system",   "desc": "Gas giants in the outer system."},
        {"value": 2.0,  "label": "2.0 AU — Mixed system",   "desc": "Both rocky and icy worlds spread across the disk."},
    ],
}

# ── Accretion choices (injected into the accretion stage per journey) ─────────

ACCRETION_CHOICES = {
    "rocky": {
        "key": "mass_earth",
        "question": "How much material does your world accumulate?",
        "explanation": "Mass determines gravity, atmospheric retention, geological longevity, and whether a magnetic field can form.",
        "options": [
            {"value": 0.1,  "label": "0.1× Earth — Tiny world",       "desc": "Gravity too weak to hold an atmosphere. Like a large asteroid."},
            {"value": 0.3,  "label": "0.3× Earth — Small rocky world", "desc": "Like Mars. Loses most atmosphere over billions of years."},
            {"value": 1.0,  "label": "1.0× Earth — Earth-sized",      "desc": "Strong enough gravity for a long-lived N₂/O₂ atmosphere."},
            {"value": 3.0,  "label": "3.0× Earth — Super-Earth",      "desc": "Heavier than Earth. Thick atmosphere, powerful geology."},
        ],
    },
    "gas_giant": {
        "key": "mass_earth",
        "question": "How massive does your gas giant grow?",
        "explanation": "Gas giants need a ~10 Earth-mass rocky core to trigger runaway gas accretion. Final size depends on disk material.",
        "options": [
            {"value": 30.0,  "label": "30× Earth — Mini-Neptune",  "desc": "A smaller gas-rich world with a thick H/He envelope."},
            {"value": 95.0,  "label": "95× Earth — Saturn-like",   "desc": "A massive, ringed gas giant. Mostly hydrogen and helium."},
            {"value": 318.0, "label": "318× Earth — Jupiter-like", "desc": "The most stable gas giant size. Powerful magnetic field and many moons."},
            {"value": 900.0, "label": "900× Earth — Super-Jupiter","desc": "Approaching brown-dwarf territory. Extreme gravity and radiation."},
        ],
    },
    "icy_moon": {
        "key": "mass_earth",
        "question": "How large is your icy moon?",
        "explanation": "Moon mass determines internal heat retention, atmospheric potential, and how strongly tidal forces act on it.",
        "options": [
            {"value": 0.005, "label": "0.005× Earth — Tiny icy moon",   "desc": "Like Enceladus. Small but possibly active from tidal heating."},
            {"value": 0.015, "label": "0.015× Earth — Small moon",      "desc": "Enough mass for moderate tidal activity and some internal heat."},
            {"value": 0.07,  "label": "0.07× Earth — Moon-sized",       "desc": "Like our Moon but icy. Sufficient mass for a subsurface ocean."},
            {"value": 0.25,  "label": "0.25× Earth — Large ocean moon", "desc": "Like a massive Europa. Thick ice shell over a deep ocean."},
        ],
    },
    "earth_like": {
        "key": "mass_earth",
        "question": "How much material does your world gather?",
        "explanation": "For an Earth-like world, mass is crucial — too small and the atmosphere escapes; too large and gravity dominates.",
        "options": [
            {"value": 0.5,  "label": "0.5× Earth — Small world",  "desc": "Weaker gravity. Thin atmosphere likely. Cooler interior."},
            {"value": 1.0,  "label": "1.0× Earth — Earth-sized ✓","desc": "Ideal. Strong enough for a thick atmosphere and active core."},
            {"value": 2.0,  "label": "2.0× Earth — Large world",  "desc": "More massive. Stronger gravity and likely thicker atmosphere."},
            {"value": 5.0,  "label": "5.0× Earth — Super-Earth",  "desc": "Very heavy. May develop a hydrogen-dominated atmosphere."},
        ],
    },
    "star_system": {
        "key": "num_planets",
        "question": "How many planets form around your star?",
        "explanation": "The number of planets depends on how much material is in the disk and how gravitational resonances shape orbits.",
        "options": [
            {"value": 2,  "label": "2 planets — Sparse system",      "desc": "Minimal system. Most disk material ends up as asteroids."},
            {"value": 4,  "label": "4 planets — Compact system",     "desc": "Like our inner solar system."},
            {"value": 8,  "label": "8 planets — Solar System-like ✓","desc": "Our solar system has 8 planets."},
            {"value": 12, "label": "12 planets — Crowded system",    "desc": "Many orbital resonances and interactions."},
        ],
    },
}

# ── Planetary evolution choices ───────────────────────────────────────────────

EVOLUTION_CHOICES = [
    {
        "key": "atmosphere",
        "question": "What atmosphere does your world develop?",
        "icon": "🌫️",
        "explanation": "Atmospheres form from volcanic outgassing. Their thickness determines surface temperature, UV shielding, and whether liquid water can exist.",
        "options": [
            {"value": "none",       "label": "No atmosphere",           "desc": "Like the Moon. Extreme temperature swings. No liquid water."},
            {"value": "thin",       "label": "Thin atmosphere",         "desc": "Like Mars. Some protection, but too thin for liquid water on most worlds."},
            {"value": "thick",      "label": "Thick N₂/O₂ atmosphere ✓","desc": "Like Earth. Moderate greenhouse, UV shielding, stable liquid water."},
            {"value": "greenhouse", "label": "Dense CO₂ greenhouse",    "desc": "Like Venus. Runaway greenhouse — surface temperature above 400°C."},
        ],
    },
    {
        "key": "water",
        "question": "How does your world acquire water?",
        "icon": "💧",
        "explanation": "Water is essential for life as we know it. It can arrive via asteroids and comets, or be present from the start in water-rich rocks.",
        "options": [
            {"value": "none",     "label": "No water",                  "desc": "Completely dry. Life as we know it is impossible."},
            {"value": "ice",      "label": "Polar ice caps only",       "desc": "Water exists only as ice. No liquid surface water."},
            {"value": "liquid",   "label": "Partial liquid water",      "desc": "Oceans or lakes cover part of the surface. Life may be possible."},
            {"value": "abundant", "label": "Abundant liquid water ✓",   "desc": "Like Earth — 70% ocean. Excellent for life and climate stability."},
        ],
    },
    {
        "key": "magnetic_field",
        "question": "Does your world generate a magnetic field?",
        "icon": "🧲",
        "explanation": "A magnetic field is generated by a molten convecting iron core. It shields the atmosphere from solar wind stripping — critical for long-term habitability.",
        "options": [
            {"value": "absent", "label": "No magnetic field",   "desc": "Like Mars. Solar wind gradually strips the atmosphere over billions of years."},
            {"value": "weak",   "label": "Weak field",          "desc": "Partial protection. Better than nothing, but atmosphere may still erode."},
            {"value": "strong", "label": "Strong field ✓",      "desc": "Like Earth. Full protection. Essential for atmospheric longevity."},
        ],
    },
    {
        "key": "geology",
        "question": "How geologically active is your world?",
        "icon": "🌋",
        "explanation": "Plate tectonics recycles carbon, replenishes nutrients, and regulates long-term climate through the carbon-silicate cycle.",
        "options": [
            {"value": "dead",     "label": "Geologically dead",         "desc": "Like Mars today. No volcanism or plate movement. Nutrients locked in the crust."},
            {"value": "moderate", "label": "Moderate volcanism",        "desc": "Like Venus. Outgassing occurs, but no plate tectonics."},
            {"value": "active",   "label": "Active plate tectonics ✓",  "desc": "Like Earth. Nutrient cycling, climate regulation, rich geology."},
        ],
    },
]

ICY_MOON_EVOLUTION = [
    {
        "key": "tidal_heating",
        "question": "How strong is tidal heating from the parent planet?",
        "icon": "🔥",
        "explanation": "Tidal forces squeeze and stretch the moon as it orbits, generating internal heat through friction. This can melt ice and drive geological activity beneath the surface.",
        "options": [
            {"value": "none",     "label": "No tidal heating",        "desc": "The moon is frozen solid with no internal heat source."},
            {"value": "moderate", "label": "Moderate heating ✓",      "desc": "Like Europa. Enough heat to maintain a liquid subsurface ocean."},
            {"value": "strong",   "label": "Extreme tidal heating",   "desc": "Like Io. Intense volcanism across the surface — possibly too harsh for life."},
        ],
    },
    {
        "key": "subsurface_ocean",
        "question": "Does your moon have a subsurface liquid ocean?",
        "icon": "🌊",
        "explanation": "A liquid ocean beneath an ice shell is one of the most promising environments for life in the solar system.",
        "options": [
            {"value": False, "label": "No — completely frozen",      "desc": "No liquid water anywhere on or inside the moon."},
            {"value": True,  "label": "Yes — subsurface ocean ✓",   "desc": "A liquid water ocean exists beneath the ice. Life is conceivable."},
        ],
    },
    {
        "key": "magnetic_field",
        "question": "Is your moon shielded from radiation?",
        "icon": "🧲",
        "explanation": "Moons orbiting gas giants face intense radiation from the planet's magnetosphere. Shielding is critical.",
        "options": [
            {"value": "absent", "label": "No shielding",             "desc": "Directly exposed to intense radiation from the parent planet."},
            {"value": "weak",   "label": "Partial shielding",        "desc": "Parent planet's field offers some protection."},
            {"value": "strong", "label": "Well shielded ✓",          "desc": "Moon sits within a protective region of the planet's magnetosphere."},
        ],
    },
]

GAS_GIANT_EVOLUTION = [
    {
        "key": "magnetic_field",
        "question": "How strong is your gas giant's magnetic field?",
        "icon": "🧲",
        "explanation": (
            "Gas giants generate powerful magnetic fields from metallic hydrogen cores. "
            "A strong field creates a magnetosphere that shields orbiting moons from deadly stellar radiation."
        ),
        "options": [
            {"value": "absent", "label": "Weak field",       "desc": "Moons are exposed to full stellar radiation. Life on any moon is extremely unlikely."},
            {"value": "weak",   "label": "Moderate field",   "desc": "Some protection for the innermost moons. Marginal conditions possible."},
            {"value": "strong", "label": "Strong field ✓",   "desc": "Like Jupiter. Moons well-shielded. Europa-style subsurface ocean habitability is conceivable."},
        ],
    },
    {
        "key": "moon",
        "question": "How many large moons orbit your gas giant?",
        "icon": "🌕",
        "explanation": (
            "Large moons like Europa and Enceladus are among the most promising places for life. "
            "Tidal heating can sustain liquid water oceans beneath their ice shells for billions of years."
        ),
        "options": [
            {"value": "none",  "label": "No large moons",          "desc": "Only small captured asteroids. No moon habitability possible."},
            {"value": "small", "label": "A few small moons",       "desc": "Limited potential. Tidal heating unlikely to sustain liquid water."},
            {"value": "large", "label": "Multiple large moons ✓",  "desc": "Like Jupiter's Galilean moons — prime candidates for subsurface oceans."},
        ],
    },
]

STAR_SYSTEM_EVOLUTION = [
    {
        "key": "moon",
        "question": "Does your system have an outer gas giant to act as a shield?",
        "icon": "🌀",
        "explanation": (
            "Jupiter acts as Earth's gravitational bodyguard — its massive gravity "
            "captures or deflects many comets and asteroids that would otherwise strike the inner solar system."
        ),
        "options": [
            {"value": "none",  "label": "No outer giant",        "desc": "Inner rocky planets are unshielded. High bombardment rate makes life difficult to establish."},
            {"value": "small", "label": "Small outer giant",     "desc": "Partial shielding. Better than nothing but inner worlds still take frequent hits."},
            {"value": "large", "label": "Jupiter-like shield ✓", "desc": "Like our solar system. Powerful gravitational shield allows long stable periods for life to evolve."},
        ],
    },
    {
        "key": "impact_history",
        "question": "How stable has the planetary system been over time?",
        "icon": "☄️",
        "explanation": (
            "Stability matters enormously for life. A moderate bombardment delivers water and organics "
            "to inner planets, as happened in Earth's Late Heavy Bombardment."
        ),
        "options": [
            {"value": "heavy",    "label": "Heavy bombardment",  "desc": "Constant impacts sterilize inner planets repeatedly. Life never gets a foothold."},
            {"value": "moderate", "label": "Moderate impacts ✓", "desc": "Like early Earth. Delivers water and organics without constant extinction-level events."},
            {"value": "calm",     "label": "Very stable system", "desc": "Minimal impacts. Long uninterrupted periods for life to evolve — but possibly less water delivered."},
        ],
    },
]

JOURNEY_DEFAULTS = {
    "rocky": {
        "star_type": "G", "distance_au": 0.7, "mass_earth": 0.3,
        "atmosphere": "thin", "water": "none",
        "magnetic_field": "weak", "geology": "dead",
        "impact_history": "moderate", "moon": "none",
        "tidal_heating": "none", "subsurface_ocean": False,
    },
    "gas_giant": {
        "star_type": "G", "distance_au": 5.2, "mass_earth": 318.0,
        "atmosphere": "thick", "water": "ice",
        "magnetic_field": "strong", "geology": "dead",
        "impact_history": "moderate", "moon": "large",
        "tidal_heating": "none", "subsurface_ocean": False,
    },
    "icy_moon": {
        "star_type": "G", "distance_au": 5.2, "mass_earth": 0.015,
        "atmosphere": "none", "water": "ice",
        "magnetic_field": "weak", "geology": "moderate",
        "impact_history": "calm", "moon": "none",
        "tidal_heating": "moderate", "subsurface_ocean": True,
    },
    "earth_like": {
        "star_type": "G", "distance_au": 1.0, "mass_earth": 1.0,
        "atmosphere": "thick", "water": "abundant",
        "magnetic_field": "strong", "geology": "active",
        "impact_history": "moderate", "moon": "large",
        "tidal_heating": "none", "subsurface_ocean": False,
    },
    "star_system": {
        "star_type": "G", "distance_au": 1.0, "mass_earth": 1.0,
        "num_planets": 8, "atmosphere": "thick", "water": "liquid",
        "magnetic_field": "strong", "geology": "active",
        "impact_history": "moderate", "moon": "large",
        "tidal_heating": "none", "subsurface_ocean": False,
    },
}

# ── Creative 2nd-person stage narratives ─────────────────────────────────────
# Each entry is a list of 2-3 variants. One is chosen randomly on page load.
# Narratives follow the player's matter through cosmic history, personalized
# to the journey type they chose.

STAGE_NARRATIVES = {

    # ── BIG BANG ──────────────────────────────────────────────────────────────
    ("bigbang", "icy_moon"): [
        "You do not exist yet — only the energy that will one day condense into the oxygen and hydrogen atoms that form your moon's ice. Space is tearing open everywhere at once, no centre, no edge, just a trillion-degree ocean of quarks and photons setting the first rule of existence: temperature decides everything.",
        "You are a quark in a plasma hotter than any star will ever be, and in a fraction of a second you will become a proton — one step closer to the hydrogen and oxygen that will freeze on your moon's surface billions of years from now. The universe is being born not from a point, but everywhere simultaneously.",
        "Right now you are pure energy, indistinguishable from the rest of the newborn cosmos. The asymmetry that saved matter from antimatter — one extra particle per billion — is the only reason you will one day exist as water on a frozen moon.",
    ],
    ("bigbang", "rocky"): [
        "You are energy — not yet silicon, not yet iron, not yet the bedrock of any world. In the first trillionths of a second, the universe is too hot for matter to last: quarks flicker into existence and annihilate again, and only a razor-thin surplus of matter over antimatter saves the material universe.",
        "The quarks that will one day become your rocky planet's iron core exist right now only as sparks in a trillion-degree plasma. Space is expanding everywhere at once, cooling fast, and the rate of that cooling is the most important fact about your world's future.",
    ],
    ("bigbang", "gas_giant"): [
        "You are energy that will become hydrogen — mostly hydrogen, almost entirely hydrogen, hydrogen forever. In the first microseconds, quarks are flickering into and out of existence, and the expanding universe is already writing your recipe: three parts hydrogen to one part helium, nothing heavier.",
        "The protons that will make up 90% of your gas giant do not yet exist as particles — only as quarks in a trillion-degree plasma. By a margin of one in a billion, matter wins over antimatter, and you survive to become the largest world in your solar system.",
    ],
    ("bigbang", "earth_like"): [
        "You are every element that will ever exist on your world — but right now you are nothing but energy. Space is being created around you, and the first hard rule is being written: the faster the universe cools, the simpler the particles that survive; the slower it cools, the more complex the chemistry that becomes possible.",
        "The carbon that will anchor every living molecule on your future planet does not exist yet — only the energy that will eventually become it. You are in the first instant of a 13.8 billion year journey toward a world that might harbour life.",
    ],
    ("bigbang", "star_system"): [
        "The energy being released right now is all the fuel your star will ever have. In the first fractions of a second, the cosmos is a trillion-degree plasma with no atoms, no chemistry, no structure — only the rate of cooling determines what complex things will ever be possible.",
        "Every photon your star will ever emit begins right here as pure energy, indistinguishable from the rest of the universe. The Big Bang is not an explosion into space — it is the creation of space itself, expanding everywhere at once, and you are in all of it simultaneously.",
    ],

    # ── NUCLEOSYNTHESIS ───────────────────────────────────────────────────────
    ("nucleosynthesis", "icy_moon"): [
        "You are a proton bouncing through the universe's first forge, and in the next three minutes the expansion will decide your fate: fuse into helium, or stay hydrogen forever. Either way, the oxygen you need to become water does not exist yet — that will take a billion years and a dying star.",
        "The universe is a cosmic furnace, but it shuts down after three minutes — the expansion is simply too fast for fusion to reach carbon or oxygen. You are hydrogen, and the molecule of water you will one day become is still impossibly far away.",
    ],
    ("nucleosynthesis", "rocky"): [
        "Three frantic minutes of fusion, then silence. The universe produced hydrogen and helium, and nothing else — the expansion was too fast for the silicon and iron of your future rocky world to form here. You will have to wait for stars.",
        "You are a proton that may or may not fuse into helium in the next three minutes, depending on the exact temperature and timing. Either way, the silicon, iron, and magnesium of your rocky planet cannot form in this primordial forge — the universe cools too fast.",
    ],
    ("nucleosynthesis", "gas_giant"): [
        "In three minutes, the universe pre-loads your gas giant's recipe: 75% hydrogen, 25% helium, locked in by the physics of expansion before anything more complex had a chance to form. You are this mixture, and you always will be.",
        "The cosmic forge runs for exactly three minutes and shuts down. What it produces — hydrogen and helium in a 3:1 ratio — is almost exactly what a gas giant needs. Your world's composition was determined before a single star existed.",
    ],
    ("nucleosynthesis", "earth_like"): [
        "The universe's first forge produces hydrogen and helium and shuts down — the expansion is too fast for any heavier chemistry. Every element your living planet will need is still locked behind a door that only dying stars can open, billions of years from now.",
        "Three minutes, two elements, and then nothing. The carbon, nitrogen, oxygen, and phosphorus that life on your future planet requires cannot form here — the universe is simply expanding too fast. You will have to wait for stars that don't yet exist.",
    ],
    ("nucleosynthesis", "star_system"): [
        "In three minutes, the universe mixes your star's fuel: roughly three parts hydrogen to one part helium, the feedstock for billions of years of nuclear burning. This ratio is not an accident — it is determined precisely by how fast the universe expanded.",
        "The cosmic forge shuts down after three minutes, having produced hydrogen and helium and barely a whisper of lithium. The heavier elements that will build your star system's planets must wait for generations of stars to manufacture them.",
    ],

    # ── FIRST STARS ───────────────────────────────────────────────────────────
    ("first_stars", "icy_moon"): [
        "A hundred million years of darkness, then fire: the first star ignites above you in a cloud of hydrogen gas, and in its core, oxygen is being forged for the first time in cosmic history. That oxygen will eventually bond with hydrogen to form the water that freezes on your moon — but first it has to survive a supernova.",
        "You have been drifting in darkness as a wisp of hydrogen gas for a hundred million years. Now the first stars blaze to life, and in their thermonuclear cores, the oxygen that will one day become your moon's ice is being created for the first time anywhere in the universe.",
    ],
    ("first_stars", "rocky"): [
        "The darkness ends with a star — enormous, short-lived, and blazing at millions of degrees. In its core, silicon and iron are being forged for the first time: the future building blocks of your rocky world, though they will need billions more years and several more stellar deaths to reach you.",
        "The first Population III stars ignite in the darkness, hundreds of times more massive than our sun, and in their cores they forge silicon, magnesium, and iron from scratch. Your rocky planet's ingredients are being produced right now in the universe's first stellar furnaces.",
    ],
    ("first_stars", "gas_giant"): [
        "The first stars burn brilliantly and briefly — they have no heavy elements to help gas clouds cool, so they form enormous, and they live only a few million years. When they die, they scatter the small amounts of silicon and iron that your gas giant's hidden rocky core will eventually need.",
        "Population III stars light up the universe for the first time, and in their brief lives they produce the first heavy elements. You need almost none of them — your gas giant will be mostly primordial hydrogen — but the tiny rocky seed at your centre will be built from their legacy.",
    ],
    ("first_stars", "earth_like"): [
        "The universe's first lights appear — not small, stable stars like your future sun, but enormous, short-lived giants that burn their fuel in a few million years. In their cores, carbon is being created for the first time in cosmic history: the atom that will one day anchor every living molecule on your planet.",
        "A hundred million years of darkness, and then the first fires. These Population III stars live brilliantly and die violently, seeding the cosmos with carbon, nitrogen, and oxygen for the first time — the chemical foundations of the life that might one day emerge on your world.",
    ],
    ("first_stars", "star_system"): [
        "The first generation of stars lives and dies, each one scattering heavy elements into the cosmos and enriching the next molecular cloud a little more. Your star system is many generations away from forming — but every death happening now is making it slightly more possible.",
        "Population III stars ignite, burn through their hydrogen in a few million years, and die — and each death leaves the cosmos a little richer in carbon, oxygen, and silicon. Your future star system requires several of these cycles before the molecular cloud it forms from will be rich enough.",
    ],

    # ── SUPERNOVA ─────────────────────────────────────────────────────────────
    ("supernova", "icy_moon"): [
        "A massive star collapses in under a second and detonates — and in the shockwave, oxygen is forged and blasted across light-years of space. That oxygen is on its way to you: it will drift through the interstellar medium for millions of years before bonding with hydrogen and freezing on your moon's surface.",
        "In the final millisecond of a dying star's life, every heavy element that ordinary fusion can't produce is forged at once — including the oxygen that will one day become your moon's water. Every molecule of ice on your surface will have passed through a death like this one.",
        "The core collapses, the shockwave propagates, and in the explosion, oxygen and silicon and iron are scattered across light-years. Your moon's ice didn't form in space — it was forged inside a star and blasted outward by its death.",
    ],
    ("supernova", "rocky"): [
        "A star explodes, and silicon, magnesium, and iron are scattered across the void. These atoms will drift for millions of years before being swept up into the collapsing cloud that will form your star — carrying the building blocks of your rocky planet inside them.",
        "Iron core collapse, millisecond implosion, titanic explosion: in that one detonation, every heavy element that requires more energy to build than it releases is forged at once. The silicon and iron of your future planet's mantle and core are being scattered into space right now.",
    ],
    ("supernova", "gas_giant"): [
        "A massive star explodes, and mostly what it contains is hydrogen and helium — your future body. The small fraction of silicon and iron in the shockwave will eventually form the rocky core that triggers your gas giant's runaway hydrogen capture, but your bulk has been prepared since the Big Bang.",
        "The supernova scatters its contents across light-years of space, seeding the next molecular cloud with silicon and iron. Your gas giant will need just enough of these heavy elements to build a rocky core — the rest of you will be the primordial hydrogen that has been waiting since the first three minutes.",
    ],
    ("supernova", "earth_like"): [
        "A star explodes, and in that one catastrophic second, phosphorus — the element that anchors the backbone of DNA — is created and scattered into space. Without this death, and many others like it, the chemistry of life on your planet would be impossible.",
        "The supernova flings carbon, oxygen, silicon, phosphorus, and iron across light-years of space. These atoms will drift for millions of years before being swept into the cloud that births your star — carrying every ingredient your living world will need.",
    ],
    ("supernova", "star_system"): [
        "Supernova after supernova enriches the galaxy, and each explosion makes the next molecular cloud a little richer in heavy elements. Your star system is being prepared, one stellar death at a time — it will take dozens of these explosions before the cloud is ready.",
        "A nearby star detonates, and the shockwave compresses the molecular cloud that will eventually collapse into your star system. The explosion is not just destructive — it is the trigger that will, in a few million years, set everything in motion.",
    ],

    # ── GALAXY FORMATION ──────────────────────────────────────────────────────
    ("galaxies", "icy_moon"): [
        "You are drifting through the forming Milky Way — a wisp of oxygen and hydrogen that will one day bond into water on an icy moon. Dark matter halos are pulling the galaxy together around you, and inside its spiral arms, stellar nurseries are building up the heavy-element reserves your moon's birthplace will need.",
        "Generations of stars have lived and died in the galaxy around you, each one leaving the cosmos a little richer in oxygen. The galaxy is slowly assembling the chemistry needed for water-bearing worlds — and you are one of the oxygen atoms that will end up frozen on one of them.",
    ],
    ("galaxies", "rocky"): [
        "You are drifting through the forming spiral arms of the Milky Way, an atom of silicon that has already passed through one stellar core and one supernova. Around you, more stars are being born, living, and dying — each cycle enriching the galaxy a little more with the elements your rocky world will need.",
        "The Milky Way is assembling itself, and inside it, each stellar generation leaves behind a richer interstellar medium. Your rocky planet's ingredients are accumulating slowly — silicon, iron, magnesium — atom by atom, supernova by supernova.",
    ],
    ("galaxies", "gas_giant"): [
        "The galaxy is forming, and out in its cold, hydrogen-rich outer reaches — where gas giants live — molecular clouds are accumulating the small amounts of heavy elements needed to build a rocky core. Your gas giant is mostly primordial hydrogen, but without these trace elements, it could never form.",
        "Dark matter halos pull the Milky Way together, and inside its spiral arms, multiple generations of stars are cycling through — each one making the next cloud slightly richer in silicon and iron. You need only a little of both to build your gas giant's core, but even that required billions of years of stellar recycling.",
    ],
    ("galaxies", "earth_like"): [
        "Four or five stellar generations have already lived and died in the galaxy around you. Each death enriched the cosmos a little more, adding the carbon, oxygen, and phosphorus that a habitable world requires. The galaxy is only now becoming chemically mature enough to produce a planet like yours.",
        "You are drifting through a galaxy that is still assembling itself — a carbon atom that has already been inside two stars and scattered by one supernova. The Milky Way's spiral arms are becoming richer with every passing generation, and the molecular cloud that will birth your star is still accumulating mass.",
    ],
    ("galaxies", "star_system"): [
        "The Milky Way takes shape around you — spiral arms, stellar nurseries, dark matter halos — and inside it, the multi-generational process of heavy element enrichment is steadily continuing. Your star system is generations away from forming, but every death happening now is making it possible.",
        "Stellar generation after stellar generation enriches the interstellar medium, and the molecular cloud that will one day collapse into your star system is slowly accumulating. Dark matter provides the gravitational scaffolding; dying stars provide the chemistry.",
    ],

    # ── NEBULA ────────────────────────────────────────────────────────────────
    ("nebula", "icy_moon"): [
        "A shockwave from a dying star compresses your molecular cloud, and as it collapses and spins into a disk, the temperature drops sharply with distance from the newborn star. Out where you are forming — beyond the frost line — water ice is condensing onto dust grains for the first time in this solar system.",
        "The cloud collapses, angular momentum spins it flat, and a protostar ignites at the center. Beyond three AU, where you are gathering, the temperature is cold enough for water ice to be solid — and grain by grain, your future moon's body is beginning to assemble from the frozen debris of a billion years of stellar chemistry.",
        "A dying star's final gift is this shockwave that collapses the cloud into your future solar system. Out in the cold outer disk, far from the new star's heat, ices are condensing onto every dust grain — and you are accumulating from these icy fragments, growing slowly toward the frozen world you will become.",
    ],
    ("nebula", "rocky"): [
        "The collapsing cloud spins into a disk, and inside the frost line — where the young star's heat keeps ice from forming — only silicates and iron dust survive. You are forming here, in the hot inner zone, sweeping up rock-forming minerals that will become your mantle, your crust, your core.",
        "A protostar ignites at the center of the spinning disk, and its heat draws a line: inside the frost line, only rock; outside, ice and gas. You are in the rocky inner zone, assembling from silicate and iron grains that will differentiate into layers when the heat of accretion melts you.",
    ],
    ("nebula", "gas_giant"): [
        "The cloud collapses into a disk, and beyond the frost line — your territory — water ice condenses onto dust grains, more than doubling the solid material available for planet building. This is the moment your gas giant becomes possible: without the frost line, there wouldn't be enough solid material to build the massive core you need to capture gas.",
        "Beyond three AU, where you are forming, icy grains are abundant and solid material is plentiful. You are assembling a rocky core fast, racing against the clock — if the stellar wind disperses the disk before your core reaches critical mass, you will never capture the hydrogen envelope that makes you a gas giant.",
    ],
    ("nebula", "earth_like"): [
        "The nebula collapses and the new star ignites, casting its heat outward across the disk. You are forming at one AU — close enough to be warm, far enough to keep water from boiling away. The habitable zone where you are assembling is narrow, and your position in it is the most important fact about your future.",
        "The disk forms around the young star, and temperature dictates everything: inside your orbit it's too hot for water ice, outside it's too cold for liquid water. You are in the sweet spot — the Goldilocks zone — but whether you stay there for long enough depends on every choice that follows.",
    ],
    ("nebula", "star_system"): [
        "The collapsing cloud spins into a disk spanning billions of kilometers, and the young star's heat draws the frost line at roughly three AU. Rocky planets will form inside that line, icy worlds and gas giants outside it — the entire architecture of your star system is being decided right now by temperature alone.",
        "A molecular cloud collapses inward, spinning faster and faster until it flattens into a disk. The protostar igniting at the center is already sorting the disk by temperature: silicates and iron fall close in, ice and hydrogen pool further out. Your star system's blueprint is being written.",
    ],

    # ── ACCRETION ─────────────────────────────────────────────────────────────
    ("accretion", "icy_moon"): [
        "Icy dust grains are colliding and sticking in the cold outer disk — pebbles, then boulders, then a growing moon. The gas giant you orbit is already pulling at you gravitationally, and that same tidal kneading that shapes your orbit will one day heat your interior enough to keep an ocean liquid beneath your ice.",
        "You are accumulating — collision by collision, grain by grain — from the icy debris of the outer disk. Your mass is small, but your orbit is close enough to a growing gas giant that tidal forces are already flexing you, generating the heat that will persist for billions of years inside your frozen shell.",
        "Your moon is growing from the debris of the outer solar system, sweeping up ice and rock in a runaway accretion that takes only a million years. The gas giant you orbit is a gravitational anchor and a heat source both — and the ocean it will eventually warm inside you is already being prepared.",
    ],
    ("accretion", "rocky"): [
        "Dust becomes pebbles, pebbles become boulders, and boulders sweep up everything around them in a runaway cascade. The energy of the collisions melts you — iron sinks to your core, silicates rise to your mantle — and in that liquid iron core, your future magnetic field is beginning to stir.",
        "You are growing at your orbital distance, sweeping up planetesimals and melting from the heat of constant collision. Differentiation is happening inside you right now: iron falling inward to form a core, lighter silicates rising — and whether your world generates a magnetic field depends on how large that iron core grows.",
    ],
    ("accretion", "gas_giant"): [
        "Your rocky core has just crossed ten Earth masses — and now runaway gas accretion begins. Hydrogen and helium pour inward from the disk faster than the disk can replenish, and in less than a million years you will grow from a rocky seed into a world three hundred times the mass of Earth.",
        "The rocky core threshold is crossed and gas floods in — you are becoming a gas giant in geological fast-forward. The disk's hydrogen and helium rush toward your growing gravity well, and the runaway process that is happening right now will make you the dominant gravitational force in your entire solar system.",
    ],
    ("accretion", "earth_like"): [
        "You are sweeping up silicate and iron-rich debris in a runaway feedback loop — each collision melts you a little more, iron differentiates downward into your core, and in that liquid iron heart, a magnetic dynamo is beginning to form. Whether that dynamo survives will determine whether your atmosphere survives.",
        "Collision after collision remelts you and reshapes you: iron falling to your core, lighter silicates rising to your mantle, differentiation carving you into layers. The molten iron at your centre is the most important thing about you right now — it will generate the magnetic field that may one day protect everything living on your surface.",
    ],
    ("accretion", "star_system"): [
        "Planets are forming simultaneously across the disk — rocky worlds in the inner zone, gas giants racing to capture hydrogen in the outer zone before the stellar wind disperses the disk. The architecture of your star system is being locked in right now, in a few million chaotic years of runaway growth and giant impacts.",
        "The disk is a construction site: multiple worlds assembling at once, sweeping up material, colliding and merging. The final orbital configuration that emerges from this chaos will determine whether any of these worlds ends up in a stable position — and stability, over geological time, is the hidden prerequisite for life.",
    ],

    # ── EVOLUTION ────────────────────────────────────────────────────────────
    ("evolution", "icy_moon"): [
        "You orbit your gas giant in an endless tidal embrace — every orbit squeezes and stretches your interior, generating heat through friction deep in your rock and ice. Beneath kilometers of frozen shell, a saltwater ocean has been liquid for a billion years, and near its hydrothermal vents, the chemistry of life is being tested against geological time.",
        "The tidal kneading never stops — your gas giant's gravity flexes you with every orbit, converting orbital energy into interior heat, keeping your ocean from freezing solid. In that dark, warm water beneath your ice shell, mineral-rich hydrothermal vents are producing the same chemical gradients that Earth's early ocean once did.",
        "Your ice shell is cracking and reforming on geological timescales as tidal forces churn your interior. Beneath it, a global ocean has persisted for over a billion years — warmed from below by tidal friction, shielded from radiation by your gas giant's magnetic field. Whether life has stirred in that ocean is the question.",
    ],
    ("evolution", "rocky"): [
        "Your magma ocean has cooled to basalt, and now volcanoes are building your first atmosphere from outgassed carbon dioxide and water vapor. Whether that atmosphere survives the next billion years depends on one thing: whether your liquid iron core generates a magnetic field strong enough to hold back the stellar wind.",
        "The surface has cooled, a crust has formed, and your primitive atmosphere is growing from volcanic outgassing. You sit at the edge of habitability — warm enough for water to be liquid if your atmosphere is thick enough, but the stellar wind is always pushing back, and only your magnetic field stands between you and a barren future like Mars.",
    ],
    ("evolution", "gas_giant"): [
        "You are a swirling colossus of hydrogen and helium, generating more heat from gravitational contraction than you receive from your star. Your magnetic field stretches across millions of kilometres, shielding your moons from radiation — and in the tidal forces you exert on those moons, at least one of them may be hosting a warm hidden ocean right now.",
        "You will never have a solid surface, never have liquid water, never be a candidate for life yourself. But your gravity is reshaping everything around you — deflecting comets from the inner planets, heating your moons from the inside out, setting orbital resonances that will persist for billions of years. The story of your system's habitability runs through you.",
    ],
    ("evolution", "earth_like"): [
        "Plate tectonics has begun, and with it a feedback loop that will regulate your climate for billions of years: volcanism releases carbon dioxide, weathering removes it, and the ocean absorbs the rest. Your magnetic field holds back the stellar wind, liquid water covers most of your surface, and active geology keeps the carbon cycle running. All three conditions are aligned — and that alignment took 13.8 billion years to achieve.",
        "Your world has everything a habitable planet needs — but none of it was guaranteed. The liquid water, the magnetic shield, the thick atmosphere, the plate tectonics: each one depended on choices made billions of years ago, from the supernova that seeded your system to the mass you accumulated during accretion. You are the improbable result of all of them working together.",
    ],
    ("evolution", "star_system"): [
        "The planets have settled into stable orbits, the late heavy bombardment has tapered off, and in your system's habitable zone, at least one world has liquid water on its surface. Whether that world can sustain those conditions for the billions of years life requires is the question your star system is now quietly answering.",
        "Your star system has reached a kind of equilibrium — rocky worlds in the inner zone, gas giants in the outer zone, a moderate impact rate delivering water and organics to the habitable worlds. Whether any of these worlds will remain stable long enough for life to take hold is the ultimate test of everything that happened in the previous 9 billion years.",
    ],
}
