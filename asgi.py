"""Vercel-compatible ASGI entrypoint for the existing Streamlit dashboard."""

from pathlib import Path
import os

# External ASGI hosts may start outside the repository. Streamlit discovers
# project configuration from the working directory, including the light theme.
ROOT_DIR = Path(__file__).resolve().parent
os.chdir(ROOT_DIR)

from fastapi import FastAPI
import streamlit as st


streamlit_app = st.App(ROOT_DIR / "app" / "main.py")
app = FastAPI(
    title="OpsPilot AI",
    lifespan=streamlit_app.lifespan(),
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


@app.get("/api/health")
async def health():
    """Report server readiness separately from model and UI validation."""
    return {"status": "ok", "application": "OpsPilot AI"}


# Mount last so the health endpoint takes precedence over the dashboard routes.
app.mount("/", streamlit_app)
