from core.models import (
    classifier_model,
    CLASS_NAMES
)


def predict_classifier(face_crop):

    prediction = classifier_model.predict(
        face_crop,
        verbose=0
    )[0]

    class_index = prediction.argmax()

    confidence = float(
        prediction[class_index]
    )

    if class_index >= len(CLASS_NAMES):

        return None, 0

    name = CLASS_NAMES[class_index]

    return name, confidence