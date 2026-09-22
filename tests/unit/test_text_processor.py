from modules.pipeline.infrastructure.processor import TextProcessor

def test_normalize_text():
    raw_text = "  Đà Nẵng   thành phố  đáng sống...   "
    normalized = TextProcessor.normalize_text(raw_text)
    assert normalized == "Đà Nẵng thành phố đáng sống..."

def test_extract_keywords():
    content = "Hệ thống tìm kiếm thông tin văn bản lớn, công nghệ tìm kiếm thông tin hiện đại."
    keywords = TextProcessor.extract_keywords(content, top_n=2)
    assert len(keywords) <= 2
    assert "thông" in keywords or "tin" in keywords or "kiếm" in keywords