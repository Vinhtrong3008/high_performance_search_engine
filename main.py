from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config.settings import settings
from core.logging.logger import setup_logging, get_logger
from core.database.elasticsearch import es_client
from modules.api.v1.endpoints.crawler import router as crawler_router
from modules.api.v1.endpoints.search import router as search_router

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Starting up application infrastructure...")

    es_client.connect()

    yield

    # Shutdown actions
    logger.info("Shutting down application infrastructure...")

    await es_client.close()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)


# Register routers
app.include_router(
    crawler_router,
    prefix=settings.API_V1_STR
)
app.include_router(
    search_router, 
    prefix=settings.API_V1_STR
)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )