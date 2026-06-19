# Sử dụng base image Python 3.9 bản gọn nhẹ
FROM python:3.9-slim

# Cài đặt các thư viện hệ thống cần thiết để OpenCV và DeepFace hoạt động
# Chúng ta cài libgl1 (chứa libGL.so.1) và libglib2.0-0
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code từ máy bạn vào thư mục /app trong container
COPY . .

# Lệnh chạy ứng dụng FastAPI của bạn
# Đảm bảo app_ai:app khớp với tên file và tên biến FastAPI của bạn
CMD ["uvicorn", "app_ai:app", "--host", "0.0.0.0", "--port", "8000"]
