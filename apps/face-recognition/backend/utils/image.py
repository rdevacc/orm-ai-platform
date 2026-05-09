import cv2
import tempfile

from pathlib import Path


def read_image(file_path):

    return cv2.imread(str(file_path))


async def save_temp_file(file):

    suffix = Path(file.filename).suffix

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    )

    contents = await file.read()

    temp.write(contents)

    temp.close()

    return temp.name