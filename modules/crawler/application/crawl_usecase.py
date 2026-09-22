from modules.crawler.domain.entities import RawArticle
from modules.crawler.domain.repositories import CrawlerRepository

class CrawlArticleUseCase:
    def __init__(self, crawler_repository: CrawlerRepository):
        self.crawler_repository = crawler_repository

    async def execute(self, url: str) -> RawArticle:
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError("Invalid URL format provided.")
        return await self.crawler_repository.scrape(url)