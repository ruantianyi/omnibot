const OMNI_KB = [
  {
    keywords: ["periapsis", "apoapsis", "perigee", "apogee", "close", "far"],
    topic: "Orbital Extremes",
    text: "Periapsis ($r_p$) is the closest point in an orbit to the central body, while apoapsis ($r_a$) is the farthest. At periapsis, the satellite moves fastest. At apoapsis, it moves slowest. This is a direct consequence of the conservation of angular momentum."
  },
  {
    keywords: ["velocity", "speed", "vis-viva", "vis viva", "fast", "slow", "ratio"],
    topic: "Vis-Viva Equation & Velocity",
    text: "The Vis-Viva equation describes the velocity of an orbiting body: $v = \\sqrt{\\mu(\\frac{2}{r} - \\frac{1}{a})}$. Because angular momentum is conserved ($r_p v_p = r_a v_a$), the ratio of velocities between any two points is inversely proportional to their radii."
  },
  {
    keywords: ["eccentricity", "circle", "ellipse", "parabola", "hyperbola", "shape", "e"],
    topic: "Orbital Eccentricity",
    text: "Eccentricity ($e$) defines the shape of an orbit. If $e = 0$, it's a perfect circle (so radius $r = p$ everywhere). If $0 < e < 1$, it's an ellipse. If $e = 1$, it's a parabola (escape trajectory), and if $e > 1$, it's a hyperbola."
  },
  {
    keywords: ["energy", "specific energy", "epsilon", "positive", "negative", "bound", "escape", "return"],
    topic: "Specific Orbital Energy",
    text: "Specific orbital energy ($\\epsilon = \\frac{v^2}{2} - \\frac{\\mu}{r}$) remains constant. If $\\epsilon < 0$, the orbit is bound (elliptical/circular) and the body will return to periapsis. If $\\epsilon \\ge 0$, it has positive or zero energy and will escape the gravity well, never to return."
  },
  {
    keywords: ["momentum", "angular momentum", "h", "constant", "spin", "torque", "dot product", "vector"],
    topic: "Angular Momentum & Forces",
    text: "Gravity is a central force, meaning it always pulls directly toward the center of mass. Because there is no lateral force, the torque in an unperturbed orbital system is exactly zero. At periapsis and apoapsis, the velocity vector is perfectly perpendicular to the gravity vector, so their dot product is 0."
  },
  {
    keywords: ["period", "time", "kepler", "third law", "law"],
    topic: "Kepler's Third Law",
    text: "Kepler's Third Law states that the square of the orbital period is proportional to the cube of the semi-major axis: $T^2 \\propto a^3$. This means larger orbits take significantly longer to complete."
  },
  {
    keywords: ["hohmann", "transfer", "maneuver", "burn", "delta-v", "tangent"],
    topic: "Hohmann Transfer",
    text: "A Hohmann transfer is an energy-efficient maneuver that uses exactly two tangent burns to move between circular orbits. It relies on an elliptical transfer orbit that touches both the initial and target orbits."
  },
  {
    keywords: ["inclination", "plane", "equatorial", "reference"],
    topic: "Orbital Inclination",
    text: "Inclination ($i$) measures the tilt of an orbit relative to a reference plane. If an orbit has an inclination of 0 degrees, it perfectly aligns with the equatorial plane (or reference plane)."
  },
  {
    keywords: ["runge-lenz", "eccentricity vector", "point"],
    topic: "Eccentricity / Runge-Lenz Vector",
    text: "The Runge-Lenz vector (or eccentricity vector) is a constant of motion that points precisely from the central body toward the periapsis point of the orbit. Its magnitude is equal to the orbit's eccentricity."
  }
];

function queryAI(prompt) {
  const lowerPrompt = prompt.toLowerCase();
  
  // Find the best matching topic based on keyword hits
  let bestMatch = null;
  let maxHits = 0;
  
  for (const entry of OMNI_KB) {
    let hits = 0;
    for (const kw of entry.keywords) {
      if (lowerPrompt.includes(kw)) {
        hits++;
      }
    }
    if (hits > maxHits) {
      maxHits = hits;
      bestMatch = entry;
    }
  }
  
  if (bestMatch) {
    return `<div class="bg-indigo-50 border border-indigo-200 text-indigo-900 p-4 rounded-xl shadow-sm text-sm my-3"><div class="flex items-center gap-2 font-bold mb-1"><i class="fa-solid fa-robot text-indigo-500"></i> AI Tutor: ${bestMatch.topic}</div><div>${bestMatch.text}</div></div>`;
  } else {
    return `<div class="bg-slate-50 border border-slate-200 text-slate-700 p-4 rounded-xl shadow-sm text-sm my-3"><div class="flex items-center gap-2 font-bold mb-1"><i class="fa-solid fa-robot text-slate-500"></i> AI Tutor</div><div>I'm not quite sure about that specific orbital concept. Try asking about eccentricity, vis-viva, energy, or Kepler's laws!</div></div>`;
  }
}

window.queryAI = queryAI;
