from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import cv2
import numpy as np

from core.models import face_app

from utils.image import (
    save_temp_file,
    read_image
)

from utils.face import (
    get_safe_bbox
)

from services.classifier_service import (
    predict_classifier
)


router = APIRouter()


@router.post("/recognize-classifier")
async def recognize_classifier(

    file: UploadFile = File(...)
):

    temp_path = await save_temp_file(file)

    image = read_image(temp_path)

    if image is None:

        return {
            "success": False,
            "message": "Invalid image"
        }

    # =========================
    # RESIZE IMAGE
    # =========================

    max_width = 640

    original_h, original_w = image.shape[:2]

    resize_scale = 1.0

    if original_w > max_width:

        resize_scale = max_width / original_w

        image = cv2.resize(

            image,

            (
                int(original_w * resize_scale),
                int(original_h * resize_scale)
            )
        )

    # =========================
    # FACE DETECTION
    # =========================

    faces = face_app.get(image)

    if len(faces) == 0:

        return {
            "success": False,
            "message": "No face detected"
        }

    # =========================
    # PROCESS ALL FACES
    # =========================

    results = []

    for face in faces:

        x1, y1, x2, y2 = get_safe_bbox(
            face,
            image
        )

        # =========================
        # SAVE RESIZED BBOX
        # =========================

        resized_bbox = [
            x1,
            y1,
            x2,
            y2
        ]

        # =========================
        # FACE CROP
        # =========================

        face_crop = image[
            resized_bbox[1]:resized_bbox[3],
            resized_bbox[0]:resized_bbox[2]
        ]

        if face_crop.size == 0:

            continue

        # =========================
        # PREPARE CLASSIFIER INPUT
        # =========================

        face_crop = cv2.resize(
            face_crop,
            (224, 224)
        )

        face_crop = face_crop.astype(
            "float32"
        ) / 255.0

        face_crop = np.expand_dims(
            face_crop,
            axis=0
        )

        # =========================
        # PREDICT
        # =========================

        name, confidence = predict_classifier(
            face_crop
        )

        print(
            f"[CLASSIFIER] "
            f"{name} "
            f"{confidence}"
        )

        # =========================
        # UNKNOWN THRESHOLD
        # =========================

        if confidence < 0.75:

            name = "Unknown"

        # =========================
        # SCALE BBOX TO ORIGINAL
        # =========================

        scaled_bbox = [

            int(resized_bbox[0] / resize_scale),

            int(resized_bbox[1] / resize_scale),

            int(resized_bbox[2] / resize_scale),

            int(resized_bbox[3] / resize_scale)
        ]

        results.append({

            "name": name,

            "confidence": float(confidence),

            "bbox": scaled_bbox
        })

    return {

        "success": True,

        "method": "classifier",

        "faces": results
    }