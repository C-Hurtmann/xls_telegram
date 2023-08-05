from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from core.config import API_TOKEN
from core.google_sheet_api import GoogleSheetAPI

google_sheet = GoogleSheetAPI()

bot = Bot(API_TOKEN)
dispatcher = Dispatcher(bot)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('/country'))
keyboard.add(KeyboardButton('/book'))
keyboard.add(KeyboardButton('/movie'))

@dispatcher.message_handler(commands=['start'])
async def startup(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.full_name
    await bot.send_message(
        chat_id=user_id,
        text=f'Welcome {username}!',
        reply_markup=keyboard
    )

@dispatcher.message_handler(commands=['country', 'book', 'movie'])
async def get_random_item(message: types.Message):
    group = message.text[1:]
    random_item = google_sheet.get_random_value_from_sheet(group)
    await message.answer(
        text=f'Your random {group} is {random_item}!',
        reply_markup=keyboard
        )

if __name__ == '__main__':
    executor.start_polling(dispatcher)