from fastapi import APIRouter, HTTPException, status
from modules.api.v1.schemas.crawler_schema import CrawlRequest, ArticleResponse
from modules.crawler.infrastructure.bs4_scraper import BS4CrawlerRepository
from modules.crawler.application.crawl_usecase import CrawlArticleUseCase

router = APIRouter(prefix="/crawler", tags=["Web Crawler"])

@router.post("/scrape", response_model=ArticleResponse)
async def scrape_article(payload: CrawlRequest):
    try:
        repository = BS4CrawlerRepository()
        use_case = CrawlArticleUseCase(repository)
        article = await use_case.execute(payload.url)
        
        return {
            "success": True,
            "data": {
                "url": article.url,
                "title": article.title,
                "summary": article.summary,
                "content_length": len(article.content)
            },
            "message": "Article scraped successfully."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )