from fastapi import FastAPI, UploadFile, File, Query # Pastikan Query diimport
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import cv2
import numpy as np
import io
from PIL import Image

app = FastAPI(
    root_path="/orm/api",
    title="ORM AI Detection API"
)

# Izinkan Frontend Vue mengakses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models dalam dictionary
# Pastikan file .pt ada di direktori yang sama
models = {
    "fast": YOLO("yolov8n.pt"),
    "accurate": YOLO("yolov8m.pt"),
    "custom_model": YOLO("best_model.pt")
}

@app.post("/detect")
async def detect(
    file: UploadFile = File(...), 
    mode: str = Query("fast", enum=["fast", "accurate", "custom_model"])
):
    # 1. Baca file
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # 2. Konversi PIL ke format OpenCV (BGR)
    img_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 3. Ambil model dari dictionary
    selected_model = models.get(mode, models["fast"])

    # 4. Tentukan threshold berdasarkan mode
    if mode == "custom_model":
        conf_threshold = 0.5 
    elif mode == "accurate":
        conf_threshold = 0.4
    else:
        conf_threshold = 0.25

    # 5. Jalankan Prediksi (Cukup satu baris ini, tidak perlu if/else lagi)
    results = selected_model.predict(img_bgr, conf=conf_threshold)
    
    # 6. Ambil hasil deteksi
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": selected_model.names[int(box.cls)],
                "confidence": round(float(box.conf), 2),
                "bbox": box.xyxy[0].tolist()
            })
            
    return {"results": detections, "model_used": mode}