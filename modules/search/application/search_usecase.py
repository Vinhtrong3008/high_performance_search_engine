from typing import Dict, Any
from modules.search.domain.entities import SearchQuery
from modules.search.domain.repositories import SearchRepository

class SearchArticlesUseCase:
    def __init__(self, search_repository: SearchRepository):
        self.search_repository = search_repository

    async def execute(self, keyword: str, page: int = 1, size: int = 10) -> Dict[str, Any]:
        query = SearchQuery(keyword=keyword, page=page, size=size)
        return await self.search_repository.search(query)