Конечно\! Вот элегантное решение для создания Telegram-бота на Aiogram 3.x, который будет принимать документы и отправлять их на печать на USB-принтер, подключенный к вашему Raspberry Pi 4.

Это решение можно разделить на два основных этапа:

1.  **Настройка Raspberry Pi и принтера**: Установка и настройка службы печати CUPS.
2.  **Создание Telegram-бота**: Написание асинхронного бота на Aiogram 3.x, который будет обрабатывать файлы.

-----

### \#\# 🖨️ Этап 1: Настройка принтера на Raspberry Pi с помощью CUPS

**CUPS (Common Unix Printing System)** — это стандартная система печати для Linux, которая позволит вашему Raspberry Pi работать с принтером.

1.  **Обновите вашу систему**:

    ```bash
    sudo apt update && sudo apt upgrade
    ```

2.  **Установите CUPS**:

    ```bash
    sudo apt install cups
    ```

3.  **Добавьте вашего пользователя в группу администраторов печати**: По умолчанию это пользователь `pi`.

    ```bash
    sudo usermod -a -G lpadmin pi
    ```

4.  **Разрешите удаленное управление CUPS** (чтобы вы могли настраивать его с другого компьютера в вашей сети):

    ```bash
    sudo cupsctl --remote-any
    sudo systemctl restart cups
    ```

5.  **Подключите ваш USB-принтер** к Raspberry Pi и включите его.

6.  **Добавьте принтер через веб-интерфейс CUPS**:

      * Откройте браузер на компьютере в той же сети, что и ваш Raspberry Pi, и перейдите по адресу: `https://<IP-адрес_вашего_RPi>:631`. Например: `https://192.168.1.10:631`.
      * Браузер может выдать предупреждение о безопасности, просто проигнорируйте его.
      * Перейдите в раздел **"Administration"** и нажмите **"Add Printer"**.
      * CUPS должен автоматически обнаружить ваш подключенный принтер. Выберите его и следуйте инструкциям на экране, чтобы добавить его в систему. Обычно CUPS сам подбирает нужный драйвер.

7.  **Проверьте печать из командной строки**: После добавления принтера, вы можете проверить его работу, распечатав тестовый файл:

    ```bash
    # Создаем тестовый файл
    echo "Привет, мир!" > test.txt
    # Отправляем на печать
    lp test.txt
    ```

    Если принтер распечатал "Привет, мир\!", значит, вы все настроили правильно\!

-----

### \#\# 🤖 Этап 2: Элегантный код для Telegram-бота на Aiogram 3.x

Теперь создадим бота, который будет принимать файлы и использовать команду `lp` для их печати.

#### **Структура проекта**

Рекомендую создать отдельную папку для вашего проекта:

```
print_bot/
├── main.py
└── .env
```

  * **`main.py`**: Основной файл с кодом бота.
  * **`.env`**: Файл для хранения вашего токена бота (для безопасности).

#### **Содержимое `.env`**

```
BOT_TOKEN=ВАШ_ТЕЛЕГРАМ_БОТ_ТОКЕН
```

#### **Установка необходимых библиотек**

```bash
pip install aiogram python-dotenv
```

#### **Код бота (`main.py`)**

Этот код элегантен, потому что он:

  * **Асинхронный**: Использует все преимущества `asyncio` и `aiogram`.
  * **Безопасный**: Хранит токен в отдельном файле.
  * **Информативный**: Отправляет пользователю сообщения о статусе печати.
  * **Чистый**: Использует современные возможности Aiogram 3.x, такие как роутеры и фильтры.

<!-- end list -->

```python
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
```

-----

### \#\# 🚀 Запуск и использование

1.  **Сохраните код** в файл `main.py` и токен в `.env`.
2.  **Запустите бота** на вашем Raspberry Pi из терминала:
    ```bash
    python main.py
    ```
3.  **Отправьте любой документ** (PDF, TXT, изображение и т.д., поддерживаемый вашим принтером) вашему боту в Telegram.
4.  Бот скачает файл, отправит его на печать и сообщит вам о результате\!

Это решение является надежным и расширяемым. Вы можете легко добавить авторизацию пользователей, очередь печати или другие функции по мере необходимости.

This video provides a great visual guide on setting up CUPS, which is the first crucial step of the process.
[A helpful guide to setting up your Raspberry Pi print server](https://www.youtube.com/watch?v=8CG1nrrsY2w)
http://googleusercontent.com/youtube_content/0
