from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ArticleDocument:
    url: str
    title: str
    content: str
    summary: str
    author: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    word_count: int = 0

@dataclass
class SearchQuery:
    keyword: str
    page: int = 1
    size: int = 10