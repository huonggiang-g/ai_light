from fastapi import FastAPI, Request
import numpy as np
import cv2
import base64
from deepface import DeepFace

app = FastAPI()

# --- NẠP MODEL MỘT LẦN DUY NHẤT KHI KHỞI ĐỘNG ---
print("Đang khởi tạo model Facenet512, vui lòng đợi...")
# Gọi hàm để build model trước, điều này sẽ lưu vào RAM/Cache
# Chúng ta chỉ thực hiện bước này 1 lần duy nhất lúc server chạy
try:
    model = DeepFace.build_model("Facenet512")
    print("Model đã sẵn sàng!")
except Exception as e:
    print(f"Lỗi khởi tạo model: {e}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/embed")
async def get_embedding(request: Request):
    try:
        data = await request.json()
        img_data = base64.b64decode(data["image"])
        nparr = np.frombuffer(img_data, np.uint8)
        face_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # SỬ DỤNG LẠI MODEL ĐÃ NẠP SẴN
        # Lưu ý: Vì model đã được build, DeepFace sẽ sử dụng nó cực nhanh
        res = DeepFace.represent(
            img_path=face_img, 
            model_name="Facenet512", 
            detector_backend="skip", 
            enforce_detection=False
        )
        
        embedding = res[0]["embedding"]
        return {"embedding": embedding}
        
    except Exception as e:
        return {"error": str(e)}
