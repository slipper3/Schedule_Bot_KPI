from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType, InlineKeyboardButton, InlineKeyboardMarkup

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/set_group'),
    KeyboardButton(text='/set_link'),
    KeyboardButton(text='/info')]
], resize_keyboard=True, one_time_keyboard=True, selective=True)

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📌 Встановити групу', callback_data='group'),
     InlineKeyboardButton(text='📎 Прикріпити силку', callback_data='link')],
    [InlineKeyboardButton(text='📚 Додатков інформація', callback_data='info')]
], resize_keyboard=True)

cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🚫 Відмінити', callback_data='cancel')]
], resize_keyboard=True, one_time_keyboard=True, selective=True)