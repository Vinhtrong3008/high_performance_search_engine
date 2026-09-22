import pytest
from unittest.mock import AsyncMock
from modules.crawler.domain.repositories import CrawlerRepository
from modules.crawler.application.crawl_usecase import CrawlArticleUseCase
from modules.crawler.domain.entities import RawArticle

@pytest.mark.asyncio
async def test_crawl_article_success(sample_raw_article):
    # 1. Khởi tạo Mock Repository
    mock_repo = AsyncMock(spec=CrawlerRepository)
    mock_repo.scrape.return_value = sample_raw_article

    # 2. Khởi tạo Use Case với Mock Repository
    use_case = CrawlArticleUseCase(mock_repo)

    # 3. Thực thi
    result = await use_case.execute("https://vnexpress.net/bai-viet-mau-123.html")

    # 4. Kiểm tra kết quả
    assert result.url == sample_raw_article.url
    assert result.title == sample_raw_article.title
    mock_repo.scrape.assert_awaited_once_with("https://vnexpress.net/bai-viet-mau-123.html")

@pytest.mark.asyncio
async def test_crawl_article_invalid_url():
    mock_repo = AsyncMock(spec=CrawlerRepository)
    use_case = CrawlArticleUseCase(mock_repo)

    # Kiểm tra xem truyền URL không hợp lệ có bắn ra ValueError không
    with pytest.raises(ValueError, match="Invalid URL format provided."):
        await use_case.execute("ftp://invalid-url.com")