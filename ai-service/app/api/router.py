"""Aggregates all routers. Health sits at root; CV/review under /api/v1."""
from fastapi import APIRouter

from app.api.v1.routes import cv, health, review

# Root-level (no prefix): GET /health
root_router = APIRouter()
root_router.include_router(health.router)

# Versioned API: /api/v1/*
api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(cv.router)
api_v1_router.include_router(review.router)
