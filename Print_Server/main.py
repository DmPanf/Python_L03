import asyncio
import logging
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

# --- Конфигурация ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Создаем папку для временного хранения файлов, если ее нет
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

# --- Инициализация ---
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
logging.basicConfig(level=logging.INFO)


# --- Обработчики сообщений ---

@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обработчик команды /start
    """
    await message.answer(
        "Привет! 👋\n"
        "Я бот-принтер для Raspberry Pi.\n"
        "Просто отправь мне документ, и я его распечатаю."
    )


@router.message(F.document)
async def handle_document(message: Message):
    """
    Обработчик входящих документов
    """
    document = message.document
    file_id = document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    
    # Формируем путь для сохранения файла
    file_name = document.file_name
    destination = DOWNLOAD_DIR / file_name
    
    await message.answer(f"📄 Получил файл: {file_name}\nСкачиваю и отправляю на печать...")

    try:
        # Скачиваем файл
        await bot.download_file(file_path, destination=str(destination))
        logging.info(f"Файл '{file_name}' успешно скачан в {destination}")

        # Отправляем файл на печать через системную команду lp
        # Используем `subprocess.run` для простоты и безопасности
        process = subprocess.run(
            ['lp', str(destination)],
            check=True,         # Вызовет исключение, если команда завершится с ошибкой
            capture_output=True, # Захватывает stdout и stderr
            text=True           # Декодирует вывод в текст
        )

        logging.info(f"Команда печати выполнена. STDOUT: {process.stdout}")
        await message.answer(f"✅ Файл '{file_name}' успешно отправлен на печать!")

    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при печати файла: {e.stderr}")
        await message.answer(f"❌ Ошибка при печати: {e.stderr}")
    except Exception as e:
        logging.error(f"Произошла непредвиденная ошибка: {e}")
        await message.answer("❌ Произошла неизвестная ошибка. Попробуйте еще раз.")
    finally:
        # Очищаем временный файл после печати (или ошибки)
        if os.path.exists(destination):
            os.remove(destination)
            logging.info(f"Временный файл '{file_name}' удален.")


@router.message()
async def handle_other_messages(message: Message):
    """
    Обработчик для всех остальных сообщений
    """
    await message.reply("Пожалуйста, отправьте мне документ для печати.")


# --- Основная функция для запуска бота ---

async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
