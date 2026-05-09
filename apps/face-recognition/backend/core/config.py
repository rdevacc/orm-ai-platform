from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

EMBEDD_MODEL_PATH = (
    BASE_DIR /
    "model" /
    "embedd" /
    "face_embeddings.pkl"
)

CLASSIFIER_MODEL_PATH = (
    BASE_DIR /
    "model" /
    "classifier" /
    "face_classifier.keras"
)

CLASS_NAMES_PATH = (
    BASE_DIR /
    "model" /
    "classifier" /
    "class_names.pkl"
)