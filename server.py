import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

app = FastAPI(
    title="Anthocyan AI Web Service",
    description="A Python FastAPI backend serving Anthocyan AI static files and API integrations.",
    version="7.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standard API Endpoints
@app.get("/api/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "service": "Anthocyan AI Web Service"}

@app.get("/api/info")
async def get_info():
    """Returns basic workspace metadata."""
    html_files = [f for f in os.listdir(".") if f.endswith(".html")]
    return {
        "workspace": "Anthocyan AI",
        "html_pages_available": sorted(html_files),
        "active_version": "7.0"
    }

# Mock API for querying local orbital mechanics rules (based on knowledge_base.js)
@app.get("/api/query")
async def query_knowledge_base(q: str):
    """Mock search query backend for orbital concepts."""
    q_lower = q.lower()
    # Simple search rules
    if "eccentricity" in q_lower:
        return {
            "topic": "Orbital Eccentricity",
            "explanation": "Eccentricity (e) defines the shape of an orbit. e = 0 is a circle, 0 < e < 1 is an ellipse, e = 1 is a parabola, and e > 1 is a hyperbola."
        }
    elif "energy" in q_lower or "escape" in q_lower:
        return {
            "topic": "Specific Orbital Energy",
            "explanation": "If specific energy (epsilon) is less than 0, the orbit is bound. If epsilon >= 0, the body will escape the gravity well."
        }
    elif "velocity" in q_lower or "speed" in q_lower:
        return {
            "topic": "Vis-Viva Equation",
            "explanation": "Velocity is given by v = sqrt(mu * (2/r - 1/a)). The body moves fastest at periapsis and slowest at apoapsis."
        }
    return {
        "topic": "General Query",
        "explanation": f"Query '{q}' received. Try querying 'eccentricity', 'energy', or 'velocity' for specific orbital mechanics details."
    }

# Root redirect to help start-up
@app.get("/")
async def root():
    """Redirect to the main landing page or serve about.html/7.0.html if available."""
    if os.path.exists("7.0.html"):
        return FileResponse("7.0.html")
    elif os.path.exists("about.html"):
        return FileResponse("about.html")
    return {"message": "Welcome to Anthocyan AI. No entry pages found."}

# Mount static files to serve 7.0.html, 6.4.html, assets, sw.js, manifest.json, etc.
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    # Run the server locally on port 8000
    print("Starting Anthocyan AI Web Service on http://127.0.0.1:8000")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
