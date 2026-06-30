import re

# Large phrase generation
base_complexities = [
    "of immense gravity", "a crux of the matter", "the fulcrum upon which this rests", "paramount to the foundational structure",
    "harness the latent potential of", "deploy the mechanics of", "wield the inherent capabilities of", "instrumentalize",
    "unveil the underlying architecture of", "cast light upon the intricacies of", "expose the foundational paradigm of",
    "forge the structural underpinnings of", "synthesize the elements into", "orchestrate the assembly of",
    "philosophically extrapolate", "deduce from the abstract principles", "ruminate upon the metaphysical implications of",
    "serve as a catalyst for", "act as a force multiplier for", "pave an unencumbered pathway toward",
    "instigate a paradigm shift in", "catalyze a fundamental metamorphosis within", "re-architect the foundational state of",
    "structurally impeccable", "of unparalleled efficacy", "exceedingly optimal in its configuration",
    "fundamentally compromised", "plagued by systemic inefficiencies", "inherently detrimental to the overarching goal",
    "a complex theoretical entanglement", "an architectural conundrum", "a multifaceted logistical bottleneck",
    "the inevitable culmination of these vectors", "the cascading consequence of the initial state", "the downstream manifestation of these variables",
    "embark upon a granular analysis of", "plunge into the theoretical depths of", "undertake a rigorous excavation of",
    "a profound validation of", "an incontrovertible manifestation of", "a robust empirical proof of",
    "fortified against systemic perturbations", "exhibiting unparalleled resilience", "structurally uncompromising",
    "exhibiting a fractal level of complexity", "comprising an intricate web of interdependencies",
    "an interwoven lattice of conceptual threads", "a complex matrix of interacting variables",
    "operating beyond conventional paradigms", "transcending established boundaries", "navigating uncharted conceptual territory",
    "synthesizing disparate data streams", "orchestrating a symphony of variables", "curating an esoteric collection of insights",
    "unearthing subliminal connections", "illuminating the penumbra of understanding", "deciphering the cryptic lexicon of",
    "navigating the labyrinthine corridors of", "charting the multidimensional topology of", "exploring the theoretical hinterlands of"
]

import random
random.seed(42) # Deterministic

huge_dict = {}
buzzwords = [
    "important", "use", "show", "make", "think", "help", "change", "good", "bad", "problem", "result", 
    "delve", "testament", "robust", "multifaceted", "tapestry", "foster", "meticulous", "utilize", "leverage",
    "crucial", "vital", "essential", "demonstrate", "illustrate", "innovative", "comprehensive", "seamless",
    "dynamic", "empower", "enhance", "optimize", "streamline", "synergy", "navigate", "landscape"
]

for word in buzzwords:
    huge_dict[word] = random.sample(base_complexities, min(10, len(base_complexities)))
    # Add a few highly specific esoteric ones
    huge_dict[word].append(f"transmuting the quintessential nature of {word}")
    huge_dict[word].append(f"operating within a structurally hyper-complex formulation of {word}")

# Format dict to string
out = []
for k, v in huge_dict.items():
    v_str = ', '.join([f'"{x}"' for x in v])
    out.append(f'                            "{k}": [{v_str}]')
huge_dict_str = '{\n' + ',\n'.join(out) + '\n}'

with open('7.0.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update populateModelSelectors
old_pop = '''                    downloadedKeys.forEach(k => {
                        if (window.isPlannerMode && !k.includes('planner')) return; 
                        if (!window.isPlannerMode && k.includes('planner')) return; '''

new_pop = '''                    downloadedKeys.forEach(k => {
                        if (k.includes('planner')) return; '''

c = c.replace(old_pop, new_pop)

# 2. Update planner execution logic
old_exec = '''                            if (window.isPlannerMode && useLocalModel) {
                                const plannerKey = localModelSelector.value;
                                const engine = window.modelManager?.activeEngines?.[plannerKey];'''

new_exec = '''                            if (window.isPlannerMode && useLocalModel) {
                                let plannerKey = localModelSelector.value;
                                if (plannerKey.includes('-text') || plannerKey.includes('-coder')) {
                                    plannerKey = plannerKey.replace(/-text|-coder/, '-planner');
                                }
                                const engine = window.modelManager?.activeEngines?.[plannerKey];'''

c = c.replace(old_exec, new_exec)

# 3. Disable dropdown auto-switch in togglePlannerMode
old_toggle_logic = '''                if (window.isPlannerMode) {
                    const select = document.getElementById('chat-local-model');
                    if (select.value === 'none' || select.value === 'cloud' || !select.value.includes('planner')) {
                        const firstPlanner = Array.from(select.options).find(o => o.value.includes('planner'));
                        if (firstPlanner) {
                            select.value = firstPlanner.value;
                            handleLocalModelChange(select);
                        }
                    }
                }'''

c = c.replace(old_toggle_logic, '')

# 4. Humanizer: Restore shuffling
c = c.replace(
    'if (Math.random() < 0.05) { // Dramatically reduced swapping to preserve human paragraph flow',
    'if (Math.random() < 0.10) { // Restored swapping'
)

# 5. Replace SIMPLIFY_SYNONYMS with COMPLEXIFY_PHRASES
import re
c = re.sub(r'const SIMPLIFY_SYNONYMS = \{.*?\};\n\n                        let words = trimmed\.split\(\/\\b\/\);\n                        let wordHumanized = words\.map\(w => \{\n                            if \(\!w\.trim\(\) \|\| \!\/\^\[A-Za-z\]\+\$\/\.test\(w\)\) return w;\n                            let lowerW = w\.toLowerCase\(\);\n                            if \(SIMPLIFY_SYNONYMS\[lowerW\] && Math\.random\(\) < 0\.95\) \{\n                                let options = SIMPLIFY_SYNONYMS\[lowerW\];', 
f'''const COMPLEXIFY_PHRASES = {huge_dict_str};

                        let words = trimmed.split(/\\b/);
                        let wordHumanized = words.map(w => {{
                            if (!w.trim() || !/^[A-Za-z]+$/.test(w)) return w;
                            let lowerW = w.toLowerCase();
                            if (COMPLEXIFY_PHRASES[lowerW] && Math.random() < 0.95) {{
                                let options = COMPLEXIFY_PHRASES[lowerW];''', c, flags=re.DOTALL)

with open('7.0.html', 'w', encoding='utf-8') as f:
    f.write(c)
