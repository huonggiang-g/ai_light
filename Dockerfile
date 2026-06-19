# Sử dụng base image Python
FROM python:3.9-slim

# Cài đặt các thư viện hệ thống cần thiết cho OpenCV (để tránh lỗi libxcb.so.1)
RUN apt-get update && apt-get install -y \
    libxcb1 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Lệnh khởi chạy ứng dụng (thay app_ai:app bằng tên file:tên biến FastAPI)
CMD ["uvicorn", "app_ai:app", "--host", "0.0.0.0", "--port", "8000"]
