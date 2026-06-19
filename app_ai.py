from fastapi import FastAPI, Request
import numpy as np
import cv2
import base64
from deepface import DeepFace

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/embed")
async def get_embedding(request: Request):
    data = await request.json()
    # Decode ảnh từ base64
    img_data = base64.b64decode(data["image"])
    nparr = np.frombuffer(img_data, np.uint8)
    face_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Trích xuất vector với Facenet512
    # detector_backend="skip" vì khuôn mặt đã được cắt bởi smart-safe rồi
    res = DeepFace.represent(img_path=face_img, model_name="Facenet512", detector_backend="skip", enforce_detection=False)
    embedding = res[0]["embedding"]
    
    return {"embedding": embedding}
