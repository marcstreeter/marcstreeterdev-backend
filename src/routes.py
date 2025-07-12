"""
Route organization and configuration.

This module imports and configures all API routers with their prefixes.
"""

from fastapi import APIRouter
from api.health.routes import router as health_router

# Create the main API router
api_router = APIRouter()

# Include all feature routers with their prefixes
api_router.include_router(health_router, prefix="/health", tags=["health"])

# Add more routers here as needed:
# api_router.include_router(users_router, prefix="/users", tags=["users"])
# api_router.include_router(auth_router, prefix="/auth", tags=["auth"]) 