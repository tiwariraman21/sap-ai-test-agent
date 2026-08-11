"""
main.py

FastAPI application entrypoint.

Run with:
    uvicorn main:app --reload --port 8000

Then open http://localhost:8000 in your browser.

Author: Raman Tiwari
Project: SAP AI Test Agent
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import abap, inventory, report, rules

app = FastAPI(title="SAP AI Test Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report.router)
app.include_router(abap.router)
app.include_router(rules.router)
app.include_router(inventory.router)


@app.middleware("http")
async def no_cache_for_frontend(request, call_next):
    """
    Without this, browsers can cache index.html/style.css/app.js
    aggressively even without an explicit Cache-Control header (Chrome's
    heuristic caching in particular). That silently serves a stale UI
    after every frontend update unless the person remembers to hard-
    refresh. This forces the browser to always revalidate with the
    server (cheap - a 304 if nothing changed) instead of trusting a
    local copy blindly. Only applies to static frontend files, not the
    /api/* routes, which shouldn't be cached differently than normal.
    """
    response = await call_next(request)
    if not request.url.path.startswith("/api"):
        response.headers["Cache-Control"] = "no-cache"
    return response


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
