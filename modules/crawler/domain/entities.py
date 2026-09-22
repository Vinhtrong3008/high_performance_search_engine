from dataclasses import dataclass
from typing import Optional

@dataclass
class RawArticle:
    url: str
    title: str
    content: str
    author: Optional[str] = None
    summary: Optional[str] = None