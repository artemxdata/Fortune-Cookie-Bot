import asyncio
import sys
import os
import sqlite3
from datetime import datetime, date
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random
import hashlib
import schedule
from dotenv import load_dotenv

load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Пути к папкам с изображениями для категорий
IMAGE_FOLDERS = {
    "memes": "/root/bot/cookies/memes_images",
    "love": "/root/bot/cookies/memes_loves",
    "work": "/root/bot/cookies/memes_work",
    "self": "/root/bot/cookies/memes_psy",
    "friendship": "/root/bot/cookies/memes_friendship"
}

# Путь к папке с изображением для команды /start
START_IMAGE_FOLDER = "/root/bot/cookies/start_image"

# Путь к папке для случайной печеньки
RANDOM_QUOTE_IMAGE_FOLDER = "/root/bot/cookies/memes_images"

# Проверка существования папок
for folder in list(IMAGE_FOLDERS.values()) + [START_IMAGE_FOLDER, RANDOM_QUOTE_IMAGE_FOLDER]:
    if not os.path.exists(folder):
        print(f"⚠️ Папка не найдена: {folder}")

# Категории цитат
CATEGORIES = {
    "love": {"name": "💕 Любовь", "tags": ["любовь", "романтика", "чувства", "сердце"]},
    "self": {"name": "🧘‍♀️ Самопознание", "tags": ["самопознание", "психология", "духовность", "развитие"]},
    "work": {"name": "💼 Работа", "tags": ["работа", "карьера", "бизнес", "успех"]},
    "friendship": {"name": "🤝 Дружба", "tags": ["дружба", "друзья", "поддержка", "верность"]},
    "memes": {"name": "😂 Мемные", "tags": ["юмор", "смешное", "ирония", "веселье"]}
}

# Случайные действия для "печенька или действие"
RANDOM_ACTIONS = [
    "Погладь своего кота или собаку (а если их нет - воображаемого питомца) 🐱",
    "Скажи маме комплимент про ее сегодняшний внешний вид 👗",
    "Выпей стакан воды и почувствуй, как твой организм говорит 'спасибо' 💧",
    "Сделай 10 приседаний и почувствуй прилив энергии 💪",
    "Напиши благодарное сообщение другу, с которым давно не общался 📱",
    "Посмотри в окно и найди что-то красивое, чего раньше не замечал 🌸",
    "Обними себя за плечи и скажи: 'Я молодец!' 🤗",
    "Сделай глубокий вдох и медленный выдох 5 раз подряд 🌬",
    "Включи любимую песню и потанцуй хотя бы минуту 💃",
    "Напиши список из 3 вещей, за которые ты благодарен сегодня ✍️",
    "Улыбнись своему отражению в зеркале 😊",
    "Приберись на рабочем столе или в одном ящике 🗂",
    "Позвони бабушке или дедушке (или вспомни о них с теплотой) 👵",
    "Съешь что-то полезное - фрукт, орех или йогурт 🍎",
    "Выйди на балкон или к окну и подыши свежим воздухом 🌬",
    "Сделай комплимент первому встречному человеку (или члену семьи) 💖",
    "Потянись как кошка - руки вверх, спину прогни 🙆‍♀️",
    "Запиши одну идею или мысль, которая пришла в голову сегодня 💡",
    "Пошли смешную картинку другу в мессенджер 😄",
    "Поблагодари себя за что-то хорошее, что сделал на этой неделе 🌟",
    "Сделай фотографию чего-то красивого прямо сейчас 📸",
    "Почитай одну страницу любимой книги 📚",
    "Напиши короткое стихотворение из 4 строк ✍️",
    "Послушай звуки природы 5 минут (или включи их на телефоне) 🌿",
    "Сделай планку на 30 секунд 🏋️‍♀️",
    "Посмотри на старые фотографии и улыбнись воспоминаниям 📷",
    "Скажи 'спасибо' трем разным людям за что-то конкретное 🙏",
    "Сделай 5 глубоких приседаний и почувствуй силу в ногах 🦵",
    "Напиши анонимный комплимент и оставь его где-то для незнакомца 💌",
    "Помедитируй 3 минуты - просто сиди тихо и дыши ☯️",
    "Нарисуй что-то простое - солнце, облако, смайлик 🎨",
    "Выучи одно новое слово на иностранном языке 🌍",
    "Сделай доброе дело для соседа или коллеги 🤝",
    "Погуляй 10 минут на свежем воздухе 🚶‍♀️",
    "Посмотри мотивирующее видео на YouTube (не больше 5 минут) 🎬",
    "Организуй что-то маленькое: кошелек, сумку или полку 📦",
    "Позвони старому другу и скажи, что скучаешь 📞",
    "Сделай 20 прыжков на месте и почувствуй, как разгоняется кровь 🏃‍♀️",
    "Напиши письмо будущему себе (на 1 год вперед) 📝",
    "Покорми птиц или просто понаблюдай за ними 🐦"
]

# Кэш для использованных цитат и картинок
USED_CONTENT_CACHE = {}

# Встроенные цитаты по категориям
BUILTIN_QUOTES = {
    "love": [
        {"text": "Любовь — это не искать идеал, а видеть несовершенство и всё равно выбирать его.", "author": "Антуан де Сент-Экзюпери"},
        {"text": "Любить — значит видеть человека таким, каким его задумал Бог.", "author": "Фёдор Достоевский"},
        {"text": "В любви главное — не терять себя, отдавая другому.", "author": "Марина Цветаева"},
        {"text": "Любовь — это когда сердце поёт, даже если разум молчит.", "author": "Эрих Мария Ремарк"},
        {"text": "Настоящая любовь начинается там, где заканчиваются ожидания.", "author": "Ошо"},
        {"text": "Любовь — это свобода быть собой рядом с другим.", "author": "Джон Леннон"},
        {"text": "Любить — значит делить не только радость, но и боль.", "author": "Халиль Джебран"},
        {"text": "Любовь — это когда ты ставишь счастье другого выше своего.", "author": "Джейн Остин"},
        {"text": "В любви нет страха, но есть отвага быть уязвимым.", "author": "Брене Браун"},
        {"text": "Любовь — это искусство, где каждый день — новый штрих.", "author": "Лев Толстой"},
        {"text": "Любовь — это не слова, а поступки, которые говорят громче.", "author": "Одри Хепбёрн"},
        {"text": "Любить — значит находить в другом свой дом.", "author": "Рабиндранат Тагор"},
        {"text": "Любовь — это когда вы вместе растёте, а не растворяетесь.", "author": "Мадонна"},
        {"text": "В любви важно не то, что ты получаешь, а то, что отдаёшь.", "author": "Виктор Гюго"},
        {"text": "Любовь — это свет, который не гаснет даже в темноте.", "author": "Анна Ахматова"},
        {"text": "Любить — значит принимать человека целиком, с его светом и тенями.", "author": "Эльчин Сафарли"},
        {"text": "Любовь — это не сделка, а дар, который не требует возврата.", "author": "Тони Моррисон"},
        {"text": "Любовь — это когда два человека создают свою вселенную.", "author": "Иван Бунин"},
        {"text": "Любовь — это язык, который понимают сердца без слов.", "author": "Робин Уильямс"},
        {"text": "Любить — значит видеть чудо в обыденном.", "author": "Пауло Коэльо"}
    ],
    "self": [
        {"text": "Будь собой — мир подстроится под твою смелость.", "author": "Оскар Уайльд"},
        {"text": "Ты сильнее, чем твои страхи, и больше, чем твои сомнения.", "author": "Малала Юсафзай"},
        {"text": "Самопознание — это путешествие, где карта рисуется по пути.", "author": "Сократ"},
        {"text": "Твоя уникальность — это дар, а не недостаток.", "author": "Леди Гага"},
        {"text": "Не бойся своих ошибок — они твои лучшие учителя.", "author": "Опра Уинфри"},
        {"text": "Ты — не то, что с тобой случилось, а то, что ты выбираешь делать дальше.", "author": "Дж. К. Роулинг"},
        {"text": "Слушай своё сердце — оно знает путь, которого не знает разум.", "author": "Стив Джобс"},
        {"text": "Твои мечты — это компас, а не клетка.", "author": "Фрида Кало"},
        {"text": "Будь светом для себя, и другие последуют за тобой.", "author": "Будда"},
        {"text": "Ты — не черновик, а шедевр в процессе создания.", "author": "Винсент Ван Гог"},
        {"text": "Сила в том, чтобы вставать после каждого падения.", "author": "Нельсон Мандела"},
        {"text": "Твоя душа — это сад, где растут твои мечты.", "author": "Руми"},
        {"text": "Не сравнивай себя с другими — твоя история уникальна.", "author": "Эмили Дикинсон"},
        {"text": "Ты — автор своей судьбы, пиши смело.", "author": "Майя Анджелоу"},
        {"text": "Сомнения — это тени, а ты — свет.", "author": "Махатма Ганди"},
        {"text": "Твоя ценность не зависит от чужих лайков.", "author": "Бейонсе"},
        {"text": "Расти там, где ты посажен, и цвети.", "author": "Эрих Фромм"},
        {"text": "Ты — не проблема, а решение, которое ищет мир.", "author": "Альберт Эйнштейн"},
        {"text": "Твоя жизнь — это холст, рисуй ярко.", "author": "Марк Шагал"},
        {"text": "Будь верен себе — это твой главный успех.", "author": "Уильям Шекспир"}
    ],
    "work": [
        {"text": "Найди дело, которое зажигает тебя, и ты никогда не будешь работать.", "author": "Конфуций"},
        {"text": "Успех — это не финиш, а каждый шаг к цели.", "author": "Уинстон Черчилль"},
        {"text": "Твой труд — это твой след в мире.", "author": "Леонардо да Винчи"},
        {"text": "Мечты без действий — это просто фантазии.", "author": "Томас Эдисон"},
        {"text": "Каждая ошибка — это урок, а не провал.", "author": "Илон Маск"},
        {"text": "Работа — это не про деньги, а про смысл.", "author": "Стив Джобс"},
        {"text": "Твоя страсть — топливо для великих дел.", "author": "Майкл Джордан"},
        {"text": "Не бойся начинать с малого — великое растёт из мелочей.", "author": "Марк Цукерберг"},
        {"text": "Делай то, что любишь, и мир найдёт тебе место.", "author": "Коко Шанель"},
        {"text": "Успех — это когда ты не сдаёшься, даже если устал.", "author": "Серена Уильямс"},
        {"text": "Твой фокус определяет твою реальность.", "author": "Джордж Лукас"},
        {"text": "Работа — это твой шанс изменить мир.", "author": "Малкольм Гладуэлл"},
        {"text": "Не жди идеального момента — создавай его.", "author": "Шерил Сэндберг"},
        {"text": "Твой труд — это мост к твоим мечтам.", "author": "Мария Кюри"},
        {"text": "Каждый шаг вперёд — это победа над страхом.", "author": "Никола Тесла"},
        {"text": "Работа — это искусство, которое ты создаёшь каждый день.", "author": "Пабло Пикассо"},
        {"text": "Успех — это смелость начать и упорство продолжать.", "author": "Анна Винтур"},
        {"text": "Твои идеи — это искры, зажигающие будущее.", "author": "Элон Маск"},
        {"text": "Работай упорно, но не забывай мечтать.", "author": "Валентина Терешкова"},
        {"text": "Твой путь — это не гонка, а путешествие.", "author": "Ричард Брэнсон"}
    ],
    "friendship": [
        {"text": "Друзья — это те, кто видит тебя настоящего и остаётся рядом.", "author": "Марк Твен"},
        {"text": "Настоящий друг — это тот, с кем можно молчать и быть понятым.", "author": "Эрнест Хемингуэй"},
        {"text": "Дружба — это когда сердца бьются в одном ритме.", "author": "Чарльз Диккенс"},
        {"text": "Друзья — это семья, которую ты выбираешь сам.", "author": "Джессика Альба"},
        {"text": "Настоящая дружба — это свет, который не гаснет в бурю.", "author": "Халиль Джебран"},
        {"text": "Друг — это тот, кто знает твои слабости и всё равно тобой гордится.", "author": "Эльчин Сафарли"},
        {"text": "Дружба — это когда смех одного заражает другого.", "author": "Робин Уильямс"},
        {"text": "Друзья — это те, кто делает твой мир ярче.", "author": "Тейлор Свифт"},
        {"text": "Настоящий друг — это твой маяк в любой темноте.", "author": "Дж. Р. Р. Толкин"},
        {"text": "Дружба — это не про количество встреч, а про глубину связи.", "author": "Майя Анджелоу"},
        {"text": "Друзья — это те, кто верит в тебя, даже когда ты сам сомневаешься.", "author": "Опра Уинфри"},
        {"text": "Дружба — это когда вы вместе растёте, а не тянете друг друга назад.", "author": "К. С. Льюис"},
        {"text": "Настоящий друг — это тот, кто приходит, когда все уходят.", "author": "Уолтер Уинчелл"},
        {"text": "Дружба — это мост, который строят двое.", "author": "Антуан де Сент-Экзюпери"},
        {"text": "Друзья — это те, кто делает твой смех громче, а слёзы легче.", "author": "Мargeрита Пушкина"},
        {"text": "Дружба — это когда ты не боишься быть собой.", "author": "Эмили Дикинсон"},
        {"text": "Настоящий друг — это тот, кто видит твою боль за улыбкой.", "author": "Фрэнсис Бэкон"},
        {"text": "Дружба — это тёплое убежище в холодном мире.", "author": "Оскар Уайльд"},
        {"text": "Друзья — это звёзды, которые светят в твоей ночи.", "author": "Виктор Гюго"},
        {"text": "Дружба — это когда вы вместе создаёте воспоминания, которые греют годы.", "author": "Элизабет Тейлор"}
    ],
    "memes": [
        {"text": "Не то, чтобы понял, но понял", "author": "Классическая классика"},
        {"text": "Хорошо, что вы мне всё объяснили. Плохо, что я ничего не понял", "author": "Неизвестный автор"},
        {"text": "Трудные времена создают сильных котят", "author": "Мудрец интернета"},
        {"text": "Не терпила, а проработал принятие", "author": "Гений подъезда"},
        {"text": "С добрыми этими вашими утрами...", "author": "Философ чата"},
        {"text": "Держу баланс... но скоро не выдержу", "author": "Король твиттера"},
        {"text": "Посмотри до чево ты меня доводеш...", "author": "Мастер мемов"},
        {"text": "Тибе только хиханьки да хаханьки", "author": "Анонимный гений"},
        {"text": "Не позволяй никому испортить твой день. Это ТВОЙ день - испорть его сам!", "author": "Легенда форума"},
        {"text": "Снова эти как их там... мысли", "author": "Гуру соцсетей"},
        {"text": "Жизнь коротка. Обвини кого-то другого в своих ошибках и двигайся дальше", "author": "Классическая классика"},
        {"text": "Жизнь грустная, зато зарплата смешная", "author": "Неизвестный автор"},
        {"text": "Одна ошибка и ты ошибся ", "author": "Мудрец интернета"},
        {"text": "Абонент временно психует", "author": "Гений подъезда"},
        {"text": "Уже завтра сегодня станет вчера", "author": "Философ чата"},
        {"text": "Хорошо, я всё сделаю! (Я ничего не сделаю)", "author": "Король твиттера"},
        {"text": "Карты говорят, что ты умничка", "author": "Мастер мемов"},
        {"text": "Я бы только спал и спал. И спал и спал и спал и спал и спал и спал и спал и спал и спал и спал...", "author": "Анонимный гений"},
        {"text": "Штош... ладно, я уважаю твоё неправильное мнение", "author": "Как завещала Юля"},
        {"text": "Словами не описать, как я счастлив, но можно цифрами - 0/10", "author": "Гуру соцсетей"}
    ]
}

# База данных для хранения цитат и пользователей
class Database:
    def __init__(self, db_path="bot_data.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Таблица цитат
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT,
                category TEXT,
                source TEXT
            )
        ''')

        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                quotes_received INTEGER DEFAULT 0,
                favorite_category TEXT
            )
        ''')

        # Таблица статистики
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id INTEGER,
                date TEXT,
                quotes_count INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        # Таблица для отслеживания использованных категорий и действий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_category_usage (
                user_id INTEGER,
                category TEXT,
                date TEXT,
                PRIMARY KEY (user_id, category, date),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_user(self, user_id, username, first_name, last_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        conn.commit()
        conn.close()

    def get_all_users(self):
        """Получает всех пользователей из базы"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users')
        users = cursor.fetchall()
        conn.close()
        return [user[0] for user in users]

    def get_user_stats(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def update_user_stats(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET quotes_received = quotes_received + 1 
            WHERE user_id = ?
        ''', (user_id,))

        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT OR REPLACE INTO user_stats (user_id, date, quotes_count)
            VALUES (?, ?, COALESCE((SELECT quotes_count FROM user_stats WHERE user_id = ? AND date = ?), 0) + 1)
        ''', (user_id, today, user_id, today))

        conn.commit()
        conn.close()

    def check_category_usage(self, user_id, category):
        """Проверяет, использовал ли пользователь категорию или действие сегодня"""
        today = date.today().strftime('%Y-%m-%d')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1 FROM daily_category_usage 
            WHERE user_id = ? AND category = ? AND date = ?
        ''', (user_id, category, today))
        result = cursor.fetchone()
        conn.close()
        return bool(result)

    def mark_category_used(self, user_id, category):
        """Отмечает категорию или действие как использованное сегодня"""
        today = date.today().strftime('%Y-%m-%d')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO daily_category_usage (user_id, category, date)
            VALUES (?, ?, ?)
        ''', (user_id, category, today))
        conn.commit()
        conn.close()

    def add_quote(self, text, author, category, source="Russian Quotes API"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO quotes (text, author, category, source)
            VALUES (?, ?, ?, ?)
        ''', (text, author, category, source))
        conn.commit()
        conn.close()

    def get_quotes_by_category(self, category):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM quotes WHERE category = ?', (category,))
        quotes = cursor.fetchall()
        conn.close()
        return quotes

    def get_random_quote(self, category=None, user_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Создаем уникальный ключ для кэша
        cache_key = f"{user_id}_{category}_{date.today()}" if user_id and category else f"general_{date.today()}"
        used_quotes = USED_CONTENT_CACHE.get(cache_key, set())

        if category:
            cursor.execute('SELECT * FROM quotes WHERE category = ?', (category,))
        else:
            cursor.execute('SELECT * FROM quotes')

        quotes = cursor.fetchall()

        # Фильтруем неиспользованные цитаты
        available_quotes = [q for q in quotes if hashlib.md5(str(q).encode()).hexdigest() not in used_quotes]

        if not available_quotes:
            # Сбрасываем кэш, если все цитаты использованы
            USED_CONTENT_CACHE[cache_key] = set()
            available_quotes = quotes

        if not available_quotes:
            conn.close()
            return None

        # Выбираем случайную цитату
        quote = random.choice(available_quotes)

        # Добавляем в кэш использованных
        USED_CONTENT_CACHE.setdefault(cache_key, set()).add(hashlib.md5(str(quote).encode()).hexdigest())

        conn.close()
        return quote

    def get_quotes_count(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM quotes')
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def clear_quotes(self):
        """Очистить все цитаты из базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM quotes')
        conn.commit()
        conn.close()

# Инициализация базы данных
db = Database()

def get_random_image(category, user_id=None):
    """Возвращает случайное изображение из папки категории"""
    folder = IMAGE_FOLDERS.get(category)
    if not folder or not os.path.exists(folder):
        return None

    images = [f for f in os.listdir(folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    if not images:
        return None

    # Создаем уникальный ключ для пользователя и категории
    cache_key = f"{user_id}_{category}_{date.today()}"

    # Получаем список уже использованных изображений
    used_images = USED_CONTENT_CACHE.get(cache_key, set())

    # Фильтруем доступные изображения
    available_images = [img for img in images if img not in used_images]

    if not available_images:
        # Сбрасываем кэш, если все изображения использованы
        USED_CONTENT_CACHE[cache_key] = set()
        available_images = images

    # Выбираем случайное изображение
    selected_image = random.choice(available_images)

    # Добавляем в кэш использованных
    USED_CONTENT_CACHE.setdefault(cache_key, set()).add(selected_image)

    return os.path.join(folder, selected_image)

def get_random_quote_image(user_id=None):
    """Возвращает случайное изображение из папки для случайной печеньки"""
    folder = RANDOM_QUOTE_IMAGE_FOLDER
    if not os.path.exists(folder):
        return None

    images = [f for f in os.listdir(folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    if not images:
        return None

    # Создаем уникальный ключ для пользователя и категории
    cache_key = f"{user_id}_random_quote_{date.today()}"

    # Получаем список уже использованных изображений
    used_images = USED_CONTENT_CACHE.get(cache_key, set())

    # Фильтруем доступные изображения
    available_images = [img for img in images if img not in used_images]

    if not available_images:
        # Сбрасываем кэш, если все изображения использованы
        USED_CONTENT_CACHE[cache_key] = set()
        available_images = images

    # Выбираем случайное изображение
    selected_image = random.choice(available_images)

    # Добавляем в кэш использованных
    USED_CONTENT_CACHE.setdefault(cache_key, set()).add(selected_image)

    return os.path.join(folder, selected_image)

def get_random_start_image():
    """Возвращает случайное изображение из папки для команды /start"""
    if not os.path.exists(START_IMAGE_FOLDER):
        return None
    images = [f for f in os.listdir(START_IMAGE_FOLDER) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    if not images:
        return None
    return os.path.join(START_IMAGE_FOLDER, random.choice(images))

async def load_builtin_quotes():
    """Загружает встроенные цитаты в базу данных"""
    try:
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM quotes WHERE source = ?', ("Встроенная база",))
        conn.commit()
        conn.close()

        loaded_count = 0
        for category, quotes in BUILTIN_QUOTES.items():
            for quote_data in quotes:
                author = quote_data.get("author", None)
                db.add_quote(quote_data["text"], author, category, "Встроенная база")
                loaded_count += 1

        print(f"✅ Загружено {loaded_count} встроенных цитат")
        for category in BUILTIN_QUOTES.keys():
            count = len(db.get_quotes_by_category(category))
            print(f"📂 Категория '{category}': {count} цитат")
    except Exception as e:
        print(f"❌ Ошибка при загрузке цитат: {e}")

def create_categories_keyboard():
    """Создает клавиатуру с категориями"""
    builder = InlineKeyboardBuilder()
    for key in ["love", "self", "work", "friendship", "memes"]:
        builder.button(
            text=CATEGORIES[key]["name"],
            callback_data=f"category_{key}",
        )
    builder.adjust(2)
    builder.button(text="🎯 Печенька или действие!", callback_data="random_action")
    builder.adjust(1)
    return builder.as_markup()

def create_limit_reached_keyboard():
    """Создает клавиатуру для случая превышения лимита"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🍪 Выбрать категорию", callback_data="show_categories")
    builder.button(text="🎯 Печенька или действие!", callback_data="random_action")
    builder.adjust(1)
    return builder.as_markup()

def create_main_keyboard():
    """Создает постоянную клавиатуру с основными действиями"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍪 Выбрать категорию")],
            [KeyboardButton(text="🎲 Случайная печенька")],
            [KeyboardButton(text="🎯 Печенька или действие")],
            [KeyboardButton(text="💖 Поддержать бота")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def format_quote(quote_data):
    """Форматирует цитату для вывода"""
    if isinstance(quote_data, tuple):
        _, text, author, category, _ = quote_data
    else:
        text = quote_data.get('text', '')
        author = quote_data.get('author', 'Неизвестный автор')
        category = quote_data.get('category', '')

    emoji = "💭"
    if category in CATEGORIES:
        emoji = CATEGORIES[category]["name"].split()[0]

    formatted = f"{emoji} *{text}*\n\n"
    if author:
        formatted += f"— _{author}_"

    return formatted

async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    user = message.from_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)

    start_image_path = get_random_start_image()
    if not start_image_path:
        await message.answer(
            "😔 Изображение для приветствия не найдено. Но не переживай, печеньки всё равно ждут тебя!",
            reply_markup=create_main_keyboard()
        )
        return

    start_keyboard = InlineKeyboardBuilder()
    start_keyboard.button(text="🚀 ПОЕХАЛИ", callback_data="start_next_step")
    start_keyboard.adjust(1)

    welcome_text = (
        "🍪 *Добро пожаловать в Cookie Lucky Bot!* 🍪\n\n"
        "Мы уже начинаем месить тесто, чтобы тебе досталась твоя печенька с предсказанием. "
        "Не переживай, хватит на все твои запросы!"
    )
    photo = FSInputFile(start_image_path)
    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption=welcome_text,
        reply_markup=start_keyboard.as_markup(),
        parse_mode="Markdown"
    )
    # Добавляем основную клавиатуру после фото
    await message.answer(
        "Выбери действие:",
        reply_markup=create_main_keyboard()
    )

async def handle_start_next_step_callback(callback: types.CallbackQuery):
    """Обработчик нажатия кнопки 'ПОЕХАЛИ'"""
    second_keyboard = InlineKeyboardBuilder()
    second_keyboard.button(text="🍪 Выбрать категорию", callback_data="show_categories")
    second_keyboard.button(text="🎯 Принять вызов", callback_data="random_action")
    second_keyboard.adjust(2)

    second_text = (
        "🚀 *Начни с выбора категории или прими вызов!*"
    )
    await callback.message.answer(
        second_text,
        reply_markup=second_keyboard.as_markup(),
        parse_mode="Markdown"
    )
    await callback.answer()

async def cmd_categories(message: types.Message):
    """Обработчик команды /categories"""
    await message.answer(
        "*Выбери категорию печеньки с предсказанием на сегодняшний день* 🍪",
        reply_markup=create_categories_keyboard(),
        parse_mode="Markdown"
    )

async def cmd_quote(message: types.Message):
    """Обработчик команды /quote"""
    user_id = message.from_user.id
    if db.check_category_usage(user_id, "random_quote"):
        await message.answer(
            "😔 *Ты уже съел случайную печеньку. Попробуй выбрать категорию или приходи завтра за новой печенькой!*",
            reply_markup=create_limit_reached_keyboard(),
            parse_mode="Markdown"
        )
        return

    quote = db.get_random_quote(user_id=user_id)
    if not quote:
        await message.answer(
            "😔 Цитаты пока не загружены. Попробуй команду /reload",
            reply_markup=create_main_keyboard()
        )
        return

    # Получаем случайное изображение из папки memes_images
    image_path = get_random_quote_image(user_id)
    if not image_path:
        await message.answer(
            "😔 Изображение не найдено, но вот твоя печенька!",
            reply_markup=create_main_keyboard()
        )
        await message.answer(
            format_quote(quote),
            parse_mode="Markdown"
        )
        return

    db.update_user_stats(user_id)
    db.mark_category_used(user_id, "random_quote")
    caption = format_quote(quote)
    photo = FSInputFile(image_path)
    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption=caption,
        parse_mode="Markdown"
    )

    # Добавляем кнопки
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🍪 Выбрать категорию", callback_data="show_categories")
    keyboard.button(text="🎯 Печенька или действие!", callback_data="random_action")
    keyboard.adjust(2)

    await message.answer(
        "Выбери еще что-нибудь:",
        reply_markup=keyboard.as_markup()
    )

async def cmd_todo(message: types.Message):
    """Обработчик команды /todo - случайное действие"""
    user_id = message.from_user.id
    if db.check_category_usage(user_id, "random_action"):
        await message.answer(
            "😔 *Вы уже приняли вызов сегодня!*\n"
            "Попробуйте выбрать категорию или приходите завтра за новым действием!",
            reply_markup=create_limit_reached_keyboard(),
            parse_mode="Markdown"
        )
        return

    action = random.choice(RANDOM_ACTIONS)
    db.mark_category_used(user_id, "random_action")

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🍪 Лучше печеньку", callback_data="show_categories")
    keyboard.adjust(1)

    formatted = f"🎯 *Твой вызов дня:*\n\n{action}\n\n_Готов принять вызов?_ 💪"
    await message.answer(
        formatted,
        reply_markup=keyboard.as_markup(),
        parse_mode="Markdown"
    )

async def cmd_stats(message: types.Message):
    """Обработчик команды /stats"""
    user_stats = db.get_user_stats(message.from_user.id)
    if not user_stats:
        await message.answer(
            "📊 Статистика не найдена. Начните с команды /start",
            reply_markup=create_main_keyboard()
        )
        return

    total_quotes = db.get_quotes_count()
    stats_text = (
        f"📊 *Ваша статистика:*\n\n"
        f"🍪 Получено печенек: {user_stats[5]}\n"
        f"📅 Дата регистрации: {user_stats[4][:10]}\n"
        f"📚 Всего печенек в базе: {total_quotes}\n"
        f"⭐ Любимая категория: {user_stats[6] or 'Не выбрана'}"
    )

    await message.answer(
        stats_text,
        parse_mode="Markdown",
        reply_markup=create_main_keyboard()
    )

async def cmd_reload(message: types.Message):
    """Обработчик команды /reload"""
    await load_builtin_quotes()
    count = db.get_quotes_count()
    await message.answer(
        f"🔄 База печенек обновлена!\n🍪 Загружено {count} печенек",
        reply_markup=create_main_keyboard()
    )

async def cmd_debug(message: types.Message):
    """Обработчик команды /debug - для отладки категорий"""
    debug_text = "*🔧 Отладочная информация:*\n\n"

    for category in BUILTIN_QUOTES.keys():
        quotes_count = len(db.get_quotes_by_category(category))
        debug_text += f"📂 {CATEGORIES[category]['name']}: {quotes_count} цитат\n"

    total_count = db.get_quotes_count()
    debug_text += f"\n📚 Всего цитат в базе: {total_count}"

    await message.answer(
        debug_text,
        parse_mode="Markdown",
        reply_markup=create_main_keyboard()
    )

def get_random_donate_image():
    """Возвращает случайное изображение из папки для поддержки"""
    donate_folder = "/root/bot/cookies/donate_picture"
    if not os.path.exists(donate_folder):
        print(f"⚠️ Папка не найдена: {donate_folder}")
        return None
    images = [f for f in os.listdir(donate_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    if not images:
        print(f"⚠️ Изображения в папке {donate_folder} не найдены")
        return None
    return os.path.join(donate_folder, random.choice(images))

async def cmd_support(message: types.Message):
    """Обработчик команды /support"""
    support_text = (
        "💖 *Если этот бот делает твой день чуть теплее - можешь поддержать его работу, "
        "закинув любую сумму на тесто, сахар и красоту!* "
        "[Поддержать](https://pay.cloudtips.ru/p/93ad89fe)"
    )
    donate_image_path = get_random_donate_image()
    if donate_image_path:
        photo = FSInputFile(donate_image_path)
        await message.answer_photo(
            photo=photo,
            caption=support_text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=create_main_keyboard()
        )
    else:
        await message.answer(
            support_text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=create_main_keyboard()
        )

async def handle_keyboard_buttons(message: types.Message):
    """Обработчик текстовых сообщений для кнопок основной клавиатуры"""
    text = message.text

    if text == "🍪 Выбрать категорию":
        await cmd_categories(message)
    elif text == "🎲 Случайная печенька":
        await cmd_quote(message)
    elif text == "🎯 Печенька или действие":
        await cmd_todo(message)
    elif text == "💖 Поддержать бота":
        await cmd_support(message)
    else:
        await message.answer(
            "😔 Пожалуйста, используй кнопки для выбора действия!",
            reply_markup=create_main_keyboard()
        )

async def handle_category_callback(callback: types.CallbackQuery):
    """Обработчик выбора категории"""
    category = callback.data.replace("category_", "")
    user_id = callback.from_user.id

    # Проверяем лимит на категорию
    if db.check_category_usage(user_id, category):
        await callback.message.answer(
            "😔 *Извините, но вы уже съели печеньку этой категории.*\n"
            "Попробуйте другую или приходите завтра за свежей выпечкой!",
            reply_markup=create_limit_reached_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    # Получаем случайное изображение для категории
    image_path = get_random_image(category, user_id)
    if not image_path:
        await callback.answer(
            f"😔 Изображения для категории '{CATEGORIES[category]['name']}' не найдены",
            show_alert=True
        )
        return

    # Получаем случайную цитату
    quote = db.get_random_quote(category, user_id)
    if not quote:
        await callback.answer(
            f"😔 Печенек в категории '{CATEGORIES[category]['name']}' не найдено"
        )
        return

    # Отмечаем категорию как использованную
    db.mark_category_used(user_id, category)
    db.update_user_stats(user_id)

    # Формируем ответ
    caption = format_quote(quote)
    photo = FSInputFile(image_path)
    await callback.bot.send_photo(
        chat_id=callback.message.chat.id,
        photo=photo,
        caption=caption,
        parse_mode="Markdown"
    )

    # Добавляем кнопки
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🍪 Выбрать категорию", callback_data="show_categories")
    keyboard.button(text="🎯 Печенька или действие!", callback_data="random_action")
    keyboard.adjust(2)

    await callback.message.answer(
        "Выбери еще что-нибудь:",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()

async def handle_random_action_callback(callback: types.CallbackQuery):
    """Обработчик случайного действия"""
    user_id = callback.from_user.id
    if db.check_category_usage(user_id, "random_action"):
        await callback.message.answer(
            "😔 *Вы уже приняли вызов сегодня!*\n"
            "Попробуйте выбрать категорию или приходите завтра за новым действием!",
            reply_markup=create_limit_reached_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    action = random.choice(RANDOM_ACTIONS)
    db.mark_category_used(user_id, "random_action")

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🍪 Лучше печеньку", callback_data="show_categories")
    keyboard.adjust(1)

    formatted = f"🎯 *Твой вызов дня:*\n\n{action}\n\n_Готов принять вызов?_ 💪"
    await callback.message.answer(
        formatted,
        reply_markup=keyboard.as_markup(),
        parse_mode="Markdown"
    )
    await callback.answer()

async def handle_show_categories_callback(callback: types.CallbackQuery):
    """Показать категории"""
    await callback.message.answer(
        "*Выбери категорию печеньки с предсказанием на сегодняшний день* 🍪",
        reply_markup=create_categories_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

async def send_daily_notification(bot):
    """Отправляет ежедневное уведомление всем пользователям"""
    users = db.get_all_users()
    daily_message = (
        "🍪 *Привет от твоей Печеньки с предсказаниями!* ✨\n\n"
        "Каждый день — новая порция вдохновения! Выбери свою печеньку или прими вызов!\n\n"
        "🍪 Выбрать категорию\n"
        "🎯 Печенька или действие!"
    )
    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=daily_message, parse_mode="Markdown")
        except Exception as e:
            print(f"Ошибка отправки уведомления пользователю {user_id}: {e}")

async def schedule_tasks(bot):
    """Запускает задачи по расписанию"""
    schedule.every().day.at("08:00").do(lambda: asyncio.create_task(send_daily_notification(bot)))
    schedule.every().wednesday.at("14:00").do(lambda: asyncio.create_task(send_weekly_notification(bot)))

    while True:
        schedule.run_pending()
        await asyncio.sleep(60)  # Проверка каждую минуту

async def main():
    """Основная функция бота"""
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Удаляем вебхук перед запуском
    await bot.delete_webhook()

    # Загружаем встроенные цитаты при каждом запуске
    await load_builtin_quotes()

    # Регистрируем обработчики команд
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_categories, Command("categories"))
    dp.message.register(cmd_quote, Command("quote"))
    dp.message.register(cmd_todo, Command("todo"))
    dp.message.register(cmd_stats, Command("stats"))
    dp.message.register(cmd_reload, Command("reload"))
    dp.message.register(cmd_debug, Command("debug"))
    dp.message.register(cmd_support, Command("support"))

    # Регистрируем обработчик текстовых сообщений для кнопок
    dp.message.register(handle_keyboard_buttons)

    # Регистрируем обработчики callback-запросов
    dp.callback_query.register(handle_category_callback, F.data.startswith("category_"))
    dp.callback_query.register(handle_random_action_callback, F.data == "random_action")
    dp.callback_query.register(handle_show_categories_callback, F.data == "show_categories")
    dp.callback_query.register(handle_start_next_step_callback, F.data == "start_next_step")

    print("🚀 Cookie Lucky Bot запущен!")
    print(f"🍪 Загружено {db.get_quotes_count()} печенек")
    print("🎯 Cookie Lucky Bot готов к работе!")

    # Запускаем задачи по расписанию в фоновом режиме
    asyncio.create_task(schedule_tasks(bot))

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("👋 Бот остановлен!")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    # Устанавливаем библиотеку schedule
    try:
        import schedule
    except ImportError:
        print("⚠️ Библиотека 'schedule' не найдена. Установите её с помощью 'pip install schedule'")
        sys.exit(1)
    asyncio.run(main())
