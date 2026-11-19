from unittest.mock import AsyncMock

import pytest
from aiogram.fsm.context import FSMContext

from meme_bot.handlers.common import send_welcome
from meme_bot.handlers.meme import Form, wait_for_mem_text


@pytest.mark.asyncio
async def test_send_welcome() -> None:
    message = AsyncMock()
    await send_welcome(message)
    message.answer.assert_awaited_once()
    kwargs = message.answer.await_args
    assert kwargs is not None
    assert "мем" in kwargs.args[0].lower()


@pytest.mark.asyncio
async def test_wait_for_mem_text_saves_state() -> None:
    message = AsyncMock()
    message.text = "Привет мем"
    state = AsyncMock(spec=FSMContext)
    await wait_for_mem_text(message, state)
    state.update_data.assert_awaited_once_with(text="Привет мем")
    state.set_state.assert_awaited_once_with(Form.waiting_memphoto)
