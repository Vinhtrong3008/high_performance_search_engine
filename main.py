from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.config.settings import settings
from core.logging.logger import setup_logging, get_logger
from core.database.elasticsearch import es_client

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

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.main(["main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])