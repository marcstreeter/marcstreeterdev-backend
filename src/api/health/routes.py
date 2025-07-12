import time
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from .schemas import LLMRequest, MultiTestResponse
from .models import run_llm_test


router = APIRouter()



# Cache for LLM results
_llm_cache = {
    "results": None,
    "last_updated": None,
    "cache_duration": 60  # 1 minute in seconds
}

def _is_cache_valid() -> bool:
    """Check if the cache is still valid (less than 1 minute old)"""
    if _llm_cache["results"] is None or _llm_cache["last_updated"] is None:
        return False
    return time.time() - _llm_cache["last_updated"] < _llm_cache["cache_duration"]

def _update_cache(results: MultiTestResponse):
    """Update the cache with new results"""
    _llm_cache["results"] = results
    _llm_cache["last_updated"] = time.time()

@router.get("/general")
async def health_check():
    """General health check endpoint for Kubernetes probes"""
    # This endpoint should always be fast and never block
    # It's used by Kubernetes readiness/liveness probes
    return {"status": "healthy", "timestamp": time.time()}

@router.get("/llm", response_model=MultiTestResponse)
async def get_llm_status(
    force_refresh: bool = Query(False, description="Force a fresh test instead of using cache"),
    prompt: Optional[str] = Query(None, description="Custom prompt to use for the LLM test")
):
    """Get LLM provider status from cache or run fresh test"""
    if force_refresh or not _is_cache_valid():
        # Run fresh test
        request = LLMRequest(prompt=prompt)
        results = await run_llm_test(request)
        _update_cache(results)
        return results
    else:
        # Return cached results
        return _llm_cache["results"]

@router.post("/llm", response_model=MultiTestResponse)
async def llm_multitest(req: LLMRequest, force_refresh: bool = Query(False, description="Force a fresh test instead of using cache")) -> MultiTestResponse:
    """Run LLM multi-provider test with optional caching"""
    if force_refresh or not _is_cache_valid():
        results = await run_llm_test(req)
        _update_cache(results)
        return results
    else:
        return _llm_cache["results"]
