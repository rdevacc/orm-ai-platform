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

from services.embedding_service import (
    find_embedding_match
)


router = APIRouter()


@router.post("/recognize-embedding")
async def recognize_embedding(

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

    max_width = 480

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
        # NORMALIZE EMBEDDING
        # =========================

        embedding = face.embedding

        embedding = embedding / np.linalg.norm(
            embedding
        )

        # =========================
        # FIND MATCH
        # =========================

        name, similarity = find_embedding_match(
            embedding
        )

        # =========================
        # UNKNOWN THRESHOLD
        # =========================

        if similarity < 0.40:

            name = "Unknown"

        # =========================
        # SCALE BACK TO ORIGINAL
        # =========================

        scaled_bbox = [

            int(x1 / resize_scale),

            int(y1 / resize_scale),

            int(x2 / resize_scale),

            int(y2 / resize_scale)
        ]

        results.append({

            "name": name,

            "similarity": float(similarity),

            "bbox": scaled_bbox
        })

    return {

        "success": True,

        "method": "embedding",

        "faces": results
    }