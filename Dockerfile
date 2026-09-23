# Sử dụng Python 3.12 slim image chính thức làm nền tảng
FROM python:3.12-slim

# Đặt thư mục làm việc bên trong container
WORKDIR /app

# Cài đặt các gói hệ thống cần thiết (nếu có)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Cập nhật pip
RUN pip install --no-cache-dir --upgrade pip

# Sao chép file dependencies vào container trước để tận dụng Docker layer caching
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn dự án vào container
COPY . .

# Mở cổng 8000 cho FastAPI
EXPOSE 8000

# Lệnh chạy ứng dụng khi container khởi động
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]