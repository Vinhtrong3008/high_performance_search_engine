from abc import ABC, abstractmethod
from typing import List, Dict, Any
from modules.search.domain.entities import ArticleDocument, SearchQuery

class SearchRepository(ABC):
    @abstractmethod
    async def create_index_if_not_exists(self) -> None:
        pass

    @abstractmethod
    async def index_document(self, doc: ArticleDocument) -> str:
        pass

    @abstractmethod
    async def search(self, query: SearchQuery) -> Dict[str, Any]:
        pass