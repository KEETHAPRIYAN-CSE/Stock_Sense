from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.init_db import init_db
from app.api.v1.auth import router as auth_router
from app.api.v1.master_data import router as master_router
from app.api.v1.operations import router as operations_router
from app.api.v1.stock import router as stock_router
from app.api.v1.dashboard import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables and baseline demo users/data on application startup
    try:
        init_db()
    except Exception as e:
        print(f"Warning: Database initialization error: {e}")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(master_router, prefix=settings.API_V1_STR)
app.include_router(operations_router, prefix=settings.API_V1_STR)
app.include_router(stock_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["System"])
def health_check():
    """Application health check endpoint returning system status."""
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/", tags=["System"])
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": "/docs",
        "health": "/health",
    }
