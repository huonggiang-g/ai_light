import os
import gc
import base64
import numpy as np
import cv2
from fastapi import FastAPI, Request
from deepface import DeepFace
import tensorflow as tf

# Tối ưu TensorFlow để không chiếm dụng quá nhiều RAM ngay lúc khởi động
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
try:
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
except:
    pass

app = FastAPI()

# NẠP MODEL VGG-FACE (NHẸ HƠN FACENET512 RẤT NHIỀU)
print("Đang nạp model VGG-Face nhẹ hơn...")
try:
    # Nạp sẵn model vào RAM
    model = DeepFace.build_model("VGG-Face")
    print("Model VGG-Face đã sẵn sàng!")
except Exception as e:
    print(f"Lỗi nạp model: {e}")

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
        
        # Trích xuất vector với VGG-Face
        # detector_backend="skip" vì smart-safe đã xử lý crop ảnh rồi
        res = DeepFace.represent(
            img_path=face_img, 
            model_name="VGG-Face", 
            detector_backend="skip", 
            enforce_detection=False
        )
        
        embedding = res[0]["embedding"]
        
        # Giải phóng bộ nhớ thủ công sau mỗi request
        gc.collect()
        
        return {"embedding": embedding}
    except Exception as e:
        gc.collect()
        return {"error": str(e)}
