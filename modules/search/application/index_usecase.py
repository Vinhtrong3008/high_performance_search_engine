from modules.pipeline.domain.entities import CleanedArticle
from modules.search.domain.entities import ArticleDocument
from modules.search.domain.repositories import SearchRepository

class IndexArticleUseCase:
    def __init__(self, search_repository: SearchRepository):
        self.search_repository = search_repository

    async def execute(self, cleaned: CleanedArticle) -> str:
        doc = ArticleDocument(
            url=cleaned.url,
            title=cleaned.title,
            content=cleaned.content,
            summary=cleaned.summary,
            author=cleaned.author,
            keywords=cleaned.keywords,
            word_count=cleaned.word_count
        )
        return await self.search_repository.index_document(doc)