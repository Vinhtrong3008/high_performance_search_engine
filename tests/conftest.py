import pytest
from modules.crawler.domain.entities import RawArticle

@pytest.fixture
def sample_raw_article():
    return RawArticle(
        url="https://vnexpress.net/bai-viet-mau-123.html",
        title="  Tiêu đề bài báo mẫu kiểm thử  ",
        content="Đây là nội dung bài báo mẫu dùng để kiểm thử hệ thống web crawler và data pipeline trong môi trường unit test. Nội dung cần đủ dài để test bộ đếm từ và trích xuất từ khóa.",
        author="Nguyễn Văn A",
        summary="Tóm tắt ngắn gọn bài báo mẫu."
    )