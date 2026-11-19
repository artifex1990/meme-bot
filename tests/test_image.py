import pytest

from meme_bot.services.image import create_meme_sync


def test_create_meme_returns_bytes(jpeg_bytes: bytes) -> None:
    result = create_meme_sync(jpeg_bytes, "Тест")
    assert isinstance(result, bytes)
    assert result is not None
    assert result[:2] == b"\xff\xd8"


@pytest.mark.parametrize("bad", [b"", b"not an image", b"\x00\x01"])
def test_create_meme_bad_bytes(bad: bytes) -> None:
    assert create_meme_sync(bad, "Тест") is None
