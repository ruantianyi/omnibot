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
  },
  {
    keywords: ["lagrange", "libration", "point", "l1", "l2", "l3", "l4", "l5", "stability", "stable"],
    topic: "Lagrange Points",
    text: "Lagrange points ($L_1$ to $L_5$) are positions in space where the gravitational forces of a two-body system produce enhanced regions of attraction and repulsion. $L_1$, $L_2$, and $L_3$ are unstable, while $L_4$ and $L_5$ are stable."
  },
  {
    keywords: ["keplerian", "elements", "classical", "anomaly", "mean", "true", "eccentric", "ascending node", "periapsis argument"],
    topic: "Keplerian Orbital Elements",
    text: "Classical orbital elements define an orbit uniquely via six parameters: semi-major axis ($a$), eccentricity ($e$), inclination ($i$), longitude of ascending node ($\\Omega$), argument of periapsis ($\\omega$), and true anomaly ($\\nu$)."
  },
  {
    keywords: ["slingshot", "gravity assist", "flyby", "momentum transfer", "speedup"],
    topic: "Gravity Assist Maneuvers",
    text: "A gravity assist or slingshot maneuver uses the relative movement and gravity of a planet or other celestial body to alter the path and speed of a spacecraft, saving propellant by exchanging orbital momentum."
  },
  {
    keywords: ["escape velocity", "escape speed", "gravitational pull", "infinity"],
    topic: "Escape Velocity Mechanics",
    text: "Escape velocity is the minimum speed needed for a free, non-propelled object to escape from the gravitational influence of a primary body: $v_e = \\sqrt{\\frac{2\\mu}{r}}$. It is exactly $\\sqrt{2}$ times the circular orbit speed."
  },
  {
    keywords: ["geostationary", "geosynchronous", "geo", "synchronous", "stationary"],
    topic: "Geosynchronous & Geostationary Orbits",
    text: "A geostationary orbit (GEO) is a circular orbit 35,786 km above Earth's equator with an eccentricity of 0 and an inclination of 0. Objects in GEO appear stationary in the sky to ground observers."
  },
  {
    keywords: ["roche limit", "tidal", "disruption", "shatter", "ring", "moon"],
    topic: "Roche Limit Disruption",
    text: "The Roche limit is the minimum distance to which a celestial body, held together only by its own gravity, can approach a second body without being torn apart by tidal forces exceeding its self-gravitational attraction."
  },
  {
    keywords: ["perturbation", "j2", "oblateness", "drag", "decay", "atmospheric"],
    topic: "Orbital Perturbations",
    text: "Real orbits deviate from Keplerian ellipses due to perturbations like Earth's equatorial bulge ($J_2$ effect, causing nodal precession), atmospheric drag (causing orbit decay), solar radiation pressure, and third-body gravity."
  },
  {
    keywords: ["soi", "sphere of influence", "patched conic", "conic", "boundary"],
    topic: "Sphere of Influence (SOI)",
    text: "The Sphere of Influence (SOI) is the oblate-spheroid-shaped region around a celestial body where its gravitational influence is the primary force on orbiting objects, critical for patched-conic approximation."
  },
  {
    keywords: ["bi-elliptic", "transfer", "bielliptic", "three burns", "efficient"],
    topic: "Bi-elliptic Transfer",
    text: "A bi-elliptic transfer is an orbital maneuver that moves a spacecraft between two circular orbits and can be more energy-efficient than a Hohmann transfer if the ratio of the final to initial semi-major axis is greater than 11.94."
  },
  {
    keywords: ["semi-latus rectum", "rectum", "p", "parameter"],
    topic: "Semi-Latus Rectum",
    text: "The semi-latus rectum ($p$) is the chord through a focus parallel to the conic section directrix. For an ellipse, $p = a(1-e^2)$. It is a fundamental scaling parameter in general conic trajectory equations: $r = \\frac{p}{1 + e \\cos \\nu}$."
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
