from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from core.config.settings import settings
from core.logging.logger import setup_logging, get_logger
from core.database.elasticsearch import es_client
from core.middleware.rate_limiter import limiter
from modules.api.v1.endpoints.crawler import router as crawler_router
from modules.api.v1.endpoints.search import router as search_router

# Setup logging
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application infrastructure...")
    es_client.connect()
    yield
    logger.info("Shutting down application infrastructure...")
    await es_client.close()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)

# 1. Gắn Rate Limiter vào State của FastAPI app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 2. Cấu hình CORS bảo mật
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production thực tế, hãy thay bằng domain cụ thể (ví dụ: ["https://yourdomain.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Đăng ký Routers
app.include_router(crawler_router, prefix=settings.API_V1_STR)
app.include_router(search_router, prefix=settings.API_V1_STR)

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