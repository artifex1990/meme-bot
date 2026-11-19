import asyncio
import io

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from meme_bot.config import settings
from meme_bot.keyboards import cancel, choicestart, repeat
from meme_bot.services.image import create_meme_sync

router = Router(name="meme")


class Form(StatesGroup):
    waiting_text_for_mem = State()
    waiting_memphoto = State()


@router.callback_query(F.data == "mem")
async def process_mem_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.waiting_text_for_mem)
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            "Вы выбрали: Мем из фотографии\nВведите текст.",
            reply_markup=cancel,
        )
    await callback.answer()


@router.callback_query(F.data == "cancel")
async def process_cancel_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            "Выбери вариант:",
            reply_markup=choicestart,
        )
    await callback.answer()


@router.callback_query(F.data == "repeat")
async def process_repeat_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.waiting_text_for_mem)
    if isinstance(callback.message, Message):
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("Введите текст.", reply_markup=cancel)
    await callback.answer()


@router.message(Form.waiting_text_for_mem, F.text)
async def wait_for_mem_text(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text or "")
    await state.set_state(Form.waiting_memphoto)
    await message.answer("Теперь отправьте фото.")


@router.message(Form.waiting_text_for_mem)
async def wait_for_mem_text_wrong(message: Message) -> None:
    await message.answer("Пожалуйста, введите именно текст.")


@router.message(Form.waiting_memphoto, F.photo)
async def wait_for_mem_photo(message: Message, state: FSMContext) -> None:
    if message.photo is None or message.bot is None:
        await message.answer("Нужна именно фотография.")
        return

    photo = message.photo[-1]  # самый большой размер
    if photo.file_size is not None and photo.file_size > settings.max_photo_size:
        await message.answer("Фото слишком большое.")
        return

    downloaded = await message.bot.download(photo)
    if downloaded is None:
        await message.answer("Не удалось скачать фото.")
        return

    photo_bytes = downloaded.getvalue() if isinstance(downloaded, io.BytesIO) else downloaded.read()
    data = await state.get_data()
    meme = await asyncio.to_thread(
        create_meme_sync,
        photo_bytes,
        str(data.get("text", "")),
    )
    if meme is None:
        await message.answer("Не получилось обработать фото.")
        return

    await message.answer_photo(
        BufferedInputFile(meme, filename="meme.jpg"),
        caption="Мем готов!",
        reply_markup=repeat,
    )
    await state.clear()


@router.message(Form.waiting_memphoto)
async def wait_for_mem_photo_wrong(message: Message) -> None:
    await message.answer("Нужна именно фотография.")
