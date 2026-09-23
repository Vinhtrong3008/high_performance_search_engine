from fastapi import APIRouter, HTTPException, status, Request
from modules.api.v1.schemas.crawler_schema import CrawlRequest, ArticleResponse
from modules.crawler.infrastructure.bs4_scraper import BS4CrawlerRepository
from modules.crawler.application.crawl_usecase import CrawlArticleUseCase
from modules.pipeline.application.pipeline_usecase import ProcessArticlePipelineUseCase
from modules.search.infrastructure.es_repository import ElasticsearchSearchRepository
from modules.search.application.index_usecase import IndexArticleUseCase
from core.middleware.rate_limiter import limiter

router = APIRouter(prefix="/crawler", tags=["Web Crawler & Pipeline"])

@router.post("/scrape", response_model=ArticleResponse)
@limiter.limit("5/minute")  # Giới hạn tối đa 5 request cào dữ liệu mỗi phút từ 1 IP
async def scrape_article(request: Request, payload: CrawlRequest):
    try:
        # Bước 1: Cào dữ liệu thô (Raw Data) từ URL
        crawler_repo = BS4CrawlerRepository()
        crawl_use_case = CrawlArticleUseCase(crawler_repo)
        raw_article = await crawl_use_case.execute(payload.url)
        
        # Bước 2: Đưa dữ liệu thô qua Data Pipeline để làm sạch và chuẩn hóa
        pipeline_use_case = ProcessArticlePipelineUseCase()
        cleaned_article = pipeline_use_case.execute(raw_article)

        # Bước 3: Tự động Indexing dữ liệu sạch vào Elasticsearch
        search_repo = ElasticsearchSearchRepository()
        index_use_case = IndexArticleUseCase(search_repo)
        doc_id = await index_use_case.execute(cleaned_article)

        # Bước 4: Trả về kết quả JSON thống nhất qua API Response DTO
        return {
            "success": True,
            "data": {
                "document_id": doc_id,
                "url": cleaned_article.url,
                "title": cleaned_article.title,
                "summary": cleaned_article.summary,
                "word_count": cleaned_article.word_count,
                "keywords": cleaned_article.keywords,
                "content_preview": cleaned_article.content[:300] + "..."
            },
            "message": "Article successfully scraped, processed, and indexed into Elasticsearch."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )