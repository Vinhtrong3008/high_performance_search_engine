import re

class CleaningRules:
    @staticmethod
    def remove_unwanted_characters(text: str) -> str:
        # Loại bỏ các ký tự điều khiển hoặc rác HTML còn sót lại nếu cần
        if not text:
            return ""
        return text.strip()

    @staticmethod
    def clean_whitespace(text: str) -> str:
        # Thay thế nhiều khoảng trắng hoặc xuống dòng liên tiếp bằng 1 khoảng trắng
        return re.sub(r'\s+', ' ', text)