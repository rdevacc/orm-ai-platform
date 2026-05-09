import pickle

from tensorflow.keras.models import load_model

from insightface.app import FaceAnalysis

from core.config import (
    EMBEDD_MODEL_PATH,
    CLASSIFIER_MODEL_PATH,
    CLASS_NAMES_PATH
)

with open(
    EMBEDD_MODEL_PATH,
    "rb"
) as f:

    known_embeddings = pickle.load(f)

classifier_model = load_model(
    CLASSIFIER_MODEL_PATH
)

with open(
    CLASS_NAMES_PATH,
    "rb"
) as f:

    CLASS_NAMES = pickle.load(f)

face_app = FaceAnalysis(
    name="buffalo_s"
)

face_app.prepare(
    ctx_id=-1,
    det_size=(320, 320)
)