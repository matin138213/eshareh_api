from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def create_picture():
    size = (800, 600)
    storage = BytesIO()
    img = Image.new("RGB", size)
    img.save(storage, "JPEG")
    storage.seek(0)
    file = SimpleUploadedFile(
        name="test_image.jpg", content=storage.getvalue(), content_type="image/jpeg"
    )
    return file
