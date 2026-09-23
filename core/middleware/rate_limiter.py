from slowapi import Limiter
from slowapi.util import get_remote_address

# Khởi tạo đối tượng Limiter dựa trên địa chỉ IP của client
limiter = Limiter(key_func=get_remote_address)