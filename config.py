import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота (получите у @BotFather в Telegram)
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Путь к файлу с цитатами
QUOTES_CSV_PATH = os.getenv('QUOTES_CSV_PATH', 'quotes.csv')

# Количество цитат по умолчанию
DEFAULT_QUOTES_COUNT = int(os.getenv('DEFAULT_QUOTES_COUNT', '10'))

# Настройки базы данных (если будете использовать)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///quotes.db')
