import httpx
from bs4 import BeautifulSoup
from modules.crawler.domain.entities import RawArticle
from modules.crawler.domain.repositories import CrawlerRepository
from core.logging.logger import get_logger

logger = get_logger(__name__)

class BS4CrawlerRepository(CrawlerRepository):
    async def scrape(self, url: str) -> RawArticle:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        logger.info("Fetching URL content", url=url)
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")

        # Logic bóc tách chung (Có thể tối ưu hoặc override cho từng tờ báo cụ thể sau này)
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

        # Lấy các thẻ p làm nội dung chính
        paragraphs = soup.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

        logger.info("Successfully scraped article", url=url, title=title)
        
        return RawArticle(
            url=url,
            title=title,
            content=content,
            author=None,
            summary=content[:200] + "..." if len(content) > 200 else content
        )