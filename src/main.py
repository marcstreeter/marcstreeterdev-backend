from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.settings import settings
from routes import api_router

app = FastAPI(
    title="MarcStreeterDev Backend",
    description="Backend service for MarcStreeterDev",
    version="0.1.0",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_urls_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

def setup_debugpy():
    """Setup debugpy with non-blocking configuration"""
    if (not settings.debugpy_enabled) or (settings.is_production):
        return
    
    try:
        import debugpy
        
        if not debugpy.is_client_connected():  # Check if debugpy is already listening
            debugpy.listen(('0.0.0.0', settings.debugpy_port))
            print(f"Debugpy listening on port {settings.debugpy_port}")
        
        if settings.debugpy_wait:
            print("Waiting for debugger to attach...")
            debugpy.wait_for_client()
            print("Debugger attached!")
            
    except Exception as e:
        print(f"Failed to setup debugpy: {e}")

setup_debugpy()  # Setting up debugpy before FastAPI initialization
