import io

import pytest
from PIL import Image


@pytest.fixture
def jpeg_bytes() -> bytes:
    image = Image.new("RGB", (200, 200), color="blue")
    output = io.BytesIO()
    image.save(output, format="JPEG")
    return output.getvalue()
