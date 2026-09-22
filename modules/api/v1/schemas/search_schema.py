from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SearchRequest(BaseModel):
    keyword: str = Field(..., min_length=1, description="Từ khóa tìm kiếm")
    page: int = Field(1, ge=1, description="Trang số")
    size: int = Field(10, ge=1, le=50, description="Số lượng kết quả mỗi trang")

class SearchResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: str