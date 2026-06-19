FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Chạy bằng Uvicorn
CMD ["uvicorn", "app_ai:app", "--host", "0.0.0.0", "--port", "8000"]