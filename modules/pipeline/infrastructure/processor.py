import re
import unicodedata
from modules.pipeline.domain.cleaning_rules import CleaningRules

class TextProcessor:
    @staticmethod
    def normalize_text(text: str) -> str:
        if not text:
            return ""
        # Chuẩn hóa Unicode NFC
        text = unicodedata.normalize("NFC", text)
        # Áp dụng các rules từ Domain
        text = CleaningRules.clean_whitespace(text)
        text = CleaningRules.remove_unwanted_characters(text)
        return text

    @staticmethod
    def extract_keywords(content: str, top_n: int = 5) -> list[str]:
        words = re.findall(r'\b\w+\b', content.lower())
        filtered_words = [w for w in words if len(w) > 3]
        from collections import Counter
        common_words = Counter(filtered_words).most_common(top_n)
        return [word for word, freq in common_words]