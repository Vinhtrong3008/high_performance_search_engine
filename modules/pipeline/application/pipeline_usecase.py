from modules.crawler.domain.entities import RawArticle
from modules.pipeline.domain.entities import CleanedArticle
from modules.pipeline.infrastructure.processor import TextProcessor

class ProcessArticlePipelineUseCase:
    def __init__(self):
        self.processor = TextProcessor()

    def execute(self, raw_article: RawArticle) -> CleanedArticle:
        # 1. Làm sạch Title và Content
        cleaned_title = self.processor.normalize_text(raw_article.title)
        cleaned_content = self.processor.normalize_text(raw_article.content)
        cleaned_summary = self.processor.normalize_text(raw_article.summary or "")

        # 2. Tính toán số lượng từ và trích xuất từ khóa
        word_count = len(cleaned_content.split())
        keywords = self.processor.extract_keywords(cleaned_content, top_n=5)

        return CleanedArticle(
            url=raw_article.url,
            title=cleaned_title,
            content=cleaned_content,
            summary=cleaned_summary,
            author=raw_article.author,
            word_count=word_count,
            keywords=keywords
        )