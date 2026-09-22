from dataclasses import dataclass
from typing import Optional, List

@dataclass
class CleanedArticle:
    url: str
    title: str
    content: str
    summary: str
    author: Optional[str] = None
    word_count: int = 0
    keywords: List[str] = None