from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api import upload, recovery, artifacts, reports

app = FastAPI(
    title="AI-RecoverX",
    description="AI-assisted digital data recovery and investigation platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(recovery.router, prefix="/api")
app.include_router(artifacts.router, prefix="/api")
app.include_router(reports.router, prefix="/api")

BACKEND_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BACKEND_DIR / "frontend"
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = BACKEND_DIR / "fronted" / "dist"
FRONTEND_INDEX = FRONTEND_DIR / "index.html"


@app.get("/")
def root():
    if FRONTEND_INDEX.exists():
        return FileResponse(FRONTEND_INDEX)
    return {
        "project": "AI-RecoverX",
        "message": "AI-RecoverX API is running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "project": "AI-RecoverX",
        "version": "1.0.0"
    }


@app.get("/{path:path}")
def frontend_routes(path: str):
    """Serve the React SPA from the same origin in production builds."""
    if path.startswith("api/") or not FRONTEND_INDEX.exists():
        return {"detail": "Not found"}

    try:
        requested = (FRONTEND_DIR / path).resolve()
        requested.relative_to(FRONTEND_DIR.resolve())
    except ValueError:
        return {"detail": "Not found"}
    if requested.is_file():
        return FileResponse(requested)
    return FileResponse(FRONTEND_INDEX)