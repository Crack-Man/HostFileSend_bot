import logging
import os
import urllib

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import Config

logging.basicConfig(level=logging.INFO)
TOKEN = Config.getInstance().getToken()
bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(content_types = ['document'])
async def upload(message: types.Message):
    global TOKEN
    filename = message.document.file_name
    id_doc = message.document.file_id
    file_info = await bot.get_file(id_doc)
    fi = file_info.file_path
    directory_files = os.path.join("files", filename)
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{fi}', f'./{directory_files}')
    await message.answer("Файл успешно отправлен")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)