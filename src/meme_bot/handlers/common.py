from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message

from meme_bot.keyboards import choicestart

router = Router(name="common")


@router.message(StateFilter(None), CommandStart())
async def send_welcome(message: Message) -> None:
    # StateFilter(None) пропускает сообщение, если шаг диалога ещё не задан.
    # CommandStart пропускает только команду /start.
    await message.answer(
        "Этот бот делает мем из фотографии.\n\nВыбери вариант:",
        reply_markup=choicestart,
    )
