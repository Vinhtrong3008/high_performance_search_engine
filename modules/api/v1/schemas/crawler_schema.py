from pydantic import BaseModel, HttpUrl
from typing import Optional

class CrawlRequest(BaseModel):
    url: str

class ArticleResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: str