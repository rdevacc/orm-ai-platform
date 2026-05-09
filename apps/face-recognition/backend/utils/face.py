def get_biggest_face(faces):

    return max(

        faces,

        key=lambda x:
        (x.bbox[2] - x.bbox[0]) *
        (x.bbox[3] - x.bbox[1])
    )


def get_safe_bbox(face, image):

    h, w = image.shape[:2]

    x1, y1, x2, y2 = map(
        int,
        face.bbox
    )

    x1 = max(0, x1)
    y1 = max(0, y1)

    x2 = min(w, x2)
    y2 = min(h, y2)

    return x1, y1, x2, y2