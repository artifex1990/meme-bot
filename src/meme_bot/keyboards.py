from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# callback_data вернётся в поле CallbackQuery.data. Лимит Telegram: 64 байта.
choicestart = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мем из фотографии", callback_data="mem")],
    ]
)

cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
    ]
)

repeat = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Повторить ввод", callback_data="repeat")],
    ]
)
