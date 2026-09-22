from fastapi import APIRouter, HTTPException, status
from modules.api.v1.schemas.crawler_schema import CrawlRequest, ArticleResponse
from modules.crawler.infrastructure.bs4_scraper import BS4CrawlerRepository
from modules.crawler.application.crawl_usecase import CrawlArticleUseCase
from modules.pipeline.application.pipeline_usecase import ProcessArticlePipelineUseCase

router = APIRouter(prefix="/crawler", tags=["Web Crawler & Pipeline"])

@router.post("/scrape", response_model=ArticleResponse)
async def scrape_article(payload: CrawlRequest):
    try:
        # Bước 1: Cào dữ liệu thô (Raw Data) từ URL
        crawler_repo = BS4CrawlerRepository()
        crawl_use_case = CrawlArticleUseCase(crawler_repo)
        raw_article = await crawl_use_case.execute(payload.url)
        
        # Bước 2: Đưa dữ liệu thô qua Data Pipeline để làm sạch và chuẩn hóa
        pipeline_use_case = ProcessArticlePipelineUseCase()
        cleaned_article = pipeline_use_case.execute(raw_article)

        # Bước 3: Trả về kết quả JSON thống nhất qua API Response DTO
        return {
            "success": True,
            "data": {
                "url": cleaned_article.url,
                "title": cleaned_article.title,
                "summary": cleaned_article.summary,
                "word_count": cleaned_article.word_count,
                "keywords": cleaned_article.keywords,
                "content_preview": cleaned_article.content[:300] + "..."
            },
            "message": "Article successfully scraped and processed through pipeline."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )