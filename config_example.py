import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# ВНИМАНИЕ: Никогда не публикуйте реальные токены в GitHub!
# Создайте файл .env и добавьте туда:
# BOT_TOKEN=your_real_bot_token_here

# Токен бота (получите у @BotFather в Telegram)
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Пути к папкам с изображениями (настройте под свою структуру)
IMAGE_FOLDERS = {
    "memes": "quotes/memes_images",
    "love": "quotes/memes_loves", 
    "work": "quotes/memes_work",
    "self": "quotes/memes_psy",
    "friendship": "quotes/memes_friendship"
}

# Путь к папке с изображением для команды /start
START_IMAGE_FOLDER = "quotes/start_image"

# Путь к папке для случайной печеньки
RANDOM_QUOTE_IMAGE_FOLDER = "quotes/memes_images"

# Путь к папке для поддержки
DONATE_IMAGE_FOLDER = "quotes/donate_picture"

# Путь к файлу базы данных
DATABASE_PATH = "data/bot_data.db"

# Настройки уведомлений
DAILY_NOTIFICATION_TIME = "08:00"
WEEKLY_NOTIFICATION_DAY = "wednesday"
WEEKLY_NOTIFICATION_TIME = "14:00"

# Ссылка для доната
DONATE_URL = "https://pay.cloudtips.ru/p/93ad89fe"

# Количество цитат по умолчанию
DEFAULT_QUOTES_COUNT = int(os.getenv('DEFAULT_QUOTES_COUNT', '10'))

# Настройки базы данных (если будете использовать)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/quotes.db')
