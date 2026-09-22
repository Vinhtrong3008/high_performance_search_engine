from abc import ABC, abstractmethod
from modules.crawler.domain.entities import RawArticle

class CrawlerRepository(ABC):
    @abstractmethod
    async def scrape(self, url: str) -> RawArticle:
        pass