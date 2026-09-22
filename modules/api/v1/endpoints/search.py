from fastapi import APIRouter, HTTPException, status, Query
from modules.api.v1.schemas.search_schema import SearchResponse
from modules.search.infrastructure.es_repository import ElasticsearchSearchRepository
from modules.search.application.search_usecase import SearchArticlesUseCase

router = APIRouter(prefix="/search", tags=["Search Engine"])

@router.get("", response_model=SearchResponse)
async def search_articles(
    keyword: str = Query(..., min_length=1, description="Từ khóa cần tìm kiếm"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50)
):
    try:
        repo = ElasticsearchSearchRepository()
        use_case = SearchArticlesUseCase(repo)
        result = await use_case.execute(keyword=keyword, page=page, size=size)

        return {
            "success": True,
            "data": result,
            "message": "Search executed successfully."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )