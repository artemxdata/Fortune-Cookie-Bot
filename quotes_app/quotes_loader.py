import aiohttp
import asyncio
import random
import json
from typing import Dict, List, Optional


class RussianQuotesAPI:
    """Класс для работы с русскими цитатами"""

    def __init__(self):
        self.quotes_cache = []
        self.api_sources = [
            "https://api.quotable.io/quotes/random",  # Основной источник
            "https://quotegarden.com/api/v3/quotes/random",  # Альтернативный
        ]

        # Встроенная база русских цитат
        self.builtin_quotes = {
            "motivation": [
                {
                    "text": "Единственный способ делать великие дела — любить то, что вы делаете.",
                    "author": "Стив Джобс",
                    "category": "motivation"
                },
                {
                    "text": "Не бойтесь идти медленно, бойтесь остановиться.",
                    "author": "Китайская пословица",
                    "category": "motivation"
                },
                {
                    "text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.",
                    "author": "Уинстон Черчилль",
                    "category": "motivation"
                }
            ]
        }
