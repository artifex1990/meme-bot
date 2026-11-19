import io
from typing import Any

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError

from meme_bot.config import settings


def _load_font(size: int) -> Any:
    try:
        return ImageFont.truetype(settings.font_path, size=size)
    except OSError:
        return ImageFont.load_default()


def create_meme_sync(photo_bytes: bytes, text: str) -> bytes | None:
    try:
        # BytesIO даёт Pillow байты в виде файла. RGB нужен, потому что JPEG не хранит прозрачность.
        image = Image.open(io.BytesIO(photo_bytes)).convert("RGB")
    except UnidentifiedImageError:
        return None

    draw = ImageDraw.Draw(image)
    font_size = max(int(image.width / 10), 12)
    font = _load_font(font_size)
    stroke = max(font_size // 12, 2)

    # textbbox возвращает рамку самих букв. Её верх часто больше нуля, низ — ниже точки рисования.
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    text_width = bbox[2] - bbox[0]

    if text_width > image.width - 24 and text_width > 0:
        font_size = max(int(font_size * ((image.width - 24) / text_width)), 10)
        font = _load_font(font_size)
        stroke = max(font_size // 12, 2)
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        text_width = bbox[2] - bbox[0]

    margin = 20
    x = (image.width - text_width) // 2 - bbox[0]
    y = image.height - margin - bbox[3]
    if y + bbox[1] < margin:
        y = margin - bbox[1]

    draw.text(
        (x, y),
        text,
        font=font,
        fill="white",
        stroke_width=stroke,
        stroke_fill="black",
    )

    output = io.BytesIO()
    image.save(output, format="JPEG", quality=90)
    return output.getvalue()
