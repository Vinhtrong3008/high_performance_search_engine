from slowapi import Limiter
from slowapi.util import get_remote_address

# Khởi tạo limiter dựa theo IP của client gọi request
limiter = Limiter(key_func=get_remote_address)