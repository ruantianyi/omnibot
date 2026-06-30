import re

with open('7.0.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Reduce hook injection chance
c = c.replace(
    'if (allowHooks && rand < 0.45) {',
    'if (allowHooks && rand < 0.10) { // Reduced hook chance based on statistical predictability'
)

# 2. Reverse MEGA_SYNONYMS to SIMPLIFY_SYNONYMS
old_synonyms = '''                        const MEGA_SYNONYMS = {
                            "important": ["paramount", "critical", "indispensable", "vital", "consequential"],
                            "complex": ["labyrinthine", "multifaceted", "intricate", "Byzantine"],
                            "good": ["exceptional", "stellar", "optimal", "superb"],
                            "bad": ["suboptimal", "detrimental", "adverse", "deleterious"],
                            "show": ["elucidate", "illustrate", "demonstrate", "reveal"],
                            "use": ["leverage", "employ", "utilize", "harness"],
                            "make": ["fabricate", "generate", "construct", "formulate"],
                            "think": ["postulate", "hypothesize", "reason", "contemplate"],
                            "help": ["facilitate", "assist", "expedite", "bolster"],
                            "change": ["transform", "metamorphose", "shift", "recalibrate"],
                            "idea": ["paradigm", "concept", "framework", "notion"],
                            "problem": ["dilemma", "predicament", "challenge", "quagmire"],
                            "result": ["outcome", "ramification", "consequence", "corollary"],
                            "system": ["infrastructure", "ecosystem", "architecture", "framework"]
                        };

                        let words = trimmed.split(/\\b/);
                        let wordHumanized = words.map(w => {
                            if (!w.trim() || !/^[A-Za-z]+$/.test(w)) return w;
                            let lowerW = w.toLowerCase();
                            if (MEGA_SYNONYMS[lowerW] && Math.random() < 0.85) {
                                let options = MEGA_SYNONYMS[lowerW];
                                let syn = options[Math.floor(Math.random() * options.length)];'''

new_synonyms = '''                        const SIMPLIFY_SYNONYMS = {
                            "paramount": ["important", "key", "main"],
                            "critical": ["important", "key", "main"],
                            "indispensable": ["important", "needed"],
                            "vital": ["important", "key"],
                            "consequential": ["important", "big"],
                            "labyrinthine": ["complex", "hard"],
                            "multifaceted": ["complex", "layered"],
                            "intricate": ["complex", "detailed"],
                            "byzantine": ["complex", "confusing"],
                            "exceptional": ["good", "great"],
                            "stellar": ["good", "great"],
                            "optimal": ["best", "good"],
                            "superb": ["good", "great"],
                            "suboptimal": ["bad", "poor"],
                            "detrimental": ["bad", "harmful"],
                            "adverse": ["bad", "negative"],
                            "deleterious": ["bad", "harmful"],
                            "elucidate": ["show", "explain", "clear up"],
                            "illustrate": ["show", "draw", "explain"],
                            "demonstrate": ["show", "prove"],
                            "reveal": ["show", "tell"],
                            "leverage": ["use", "apply"],
                            "employ": ["use", "hire"],
                            "utilize": ["use"],
                            "harness": ["use", "control"],
                            "fabricate": ["make", "build"],
                            "generate": ["make", "create"],
                            "construct": ["make", "build"],
                            "formulate": ["make", "plan"],
                            "postulate": ["think", "say"],
                            "hypothesize": ["think", "guess"],
                            "contemplate": ["think", "consider"],
                            "facilitate": ["help", "ease"],
                            "assist": ["help"],
                            "expedite": ["help", "speed up"],
                            "bolster": ["help", "boost"],
                            "transform": ["change", "turn"],
                            "metamorphose": ["change"],
                            "recalibrate": ["change", "adjust"],
                            "paradigm": ["idea", "model"],
                            "concept": ["idea", "thought"],
                            "framework": ["idea", "plan", "system"],
                            "notion": ["idea", "belief"],
                            "dilemma": ["problem", "issue"],
                            "predicament": ["problem", "mess"],
                            "quagmire": ["problem", "trap"],
                            "outcome": ["result", "end"],
                            "ramification": ["result", "effect"],
                            "consequence": ["result", "effect"],
                            "corollary": ["result", "link"],
                            "infrastructure": ["system", "base"],
                            "ecosystem": ["system", "world"],
                            "architecture": ["system", "design"],
                            "delve": ["look", "dig"],
                            "testament": ["sign", "proof"],
                            "tapestry": ["mix", "blend"],
                            "robust": ["strong", "solid"],
                            "meticulous": ["careful", "detailed"],
                            "foster": ["help", "grow"]
                        };

                        let words = trimmed.split(/\\b/);
                        let wordHumanized = words.map(w => {
                            if (!w.trim() || !/^[A-Za-z]+$/.test(w)) return w;
                            let lowerW = w.toLowerCase();
                            if (SIMPLIFY_SYNONYMS[lowerW] && Math.random() < 0.95) {
                                let options = SIMPLIFY_SYNONYMS[lowerW];
                                let syn = options[Math.floor(Math.random() * options.length)];'''

c = c.replace(old_synonyms, new_synonyms)

# 3. Reduce sentence swapping
c = c.replace(
    'if (Math.random() < 0.3) {',
    'if (Math.random() < 0.05) { // Dramatically reduced swapping to preserve human paragraph flow'
)

with open('7.0.html', 'w', encoding='utf-8') as f:
    f.write(c)
