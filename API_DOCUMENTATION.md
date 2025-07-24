# 🔧 API Documentation

## Core Functions

### Database Operations

#### `class Database`
Main database handler for all bot operations.

```python
db = Database("bot_data.db")

# User management
db.add_user(user_id, username, first_name, last_name)
db.get_user_stats(user_id)
db.update_user_stats(user_id)

# Quote management  
db.add_quote(text, author, category, source)
db.get_random_quote(category=None, user_id=None)
db.get_quotes_by_category(category)

# Usage tracking
db.check_category_usage(user_id, category)
db.mark_category_used(user_id, category)
```

### Content Management

#### Image Selection
```python
# Get random category image
get_random_image(category, user_id=None)

# Get random quote image
get_random_quote_image(user_id=None)

# Get start screen image
get_random_start_image()

# Get donation image
get_random_donate_image()
```

#### Content Caching
```python
# Global cache for daily content rotation
USED_CONTENT_CACHE = {
    "user_123_love_2024-01-15": {"image1.jpg", "quote_hash_1"},
    "user_123_random_quote_2024-01-15": {"image2.jpg", "quote_hash_2"}
}
```

### Interface Components

#### Keyboard Builders
```python
# Main persistent keyboard
create_main_keyboard()

# Category selection
create_categories_keyboard()

# Limit reached options
create_limit_reached_keyboard()
```

#### Message Formatters
```python
# Format quote for display
format_quote(quote_data)
# Returns: "💭 *Quote text*\n\n— _Author_"
```

## Handler Functions

### Command Handlers
```python
async def cmd_start(message: types.Message)
async def cmd_categories(message: types.Message)  
async def cmd_quote(message: types.Message)
async def cmd_todo(message: types.Message)
async def cmd_stats(message: types.Message)
async def cmd_support(message: types.Message)
```

### Callback Handlers
```python
async def handle_category_callback(callback: types.CallbackQuery)
async def handle_random_action_callback(callback: types.CallbackQuery)
async def handle_show_categories_callback(callback: types.CallbackQuery)
```

### Keyboard Message Handler
```python
async def handle_keyboard_buttons(message: types.Message)
# Handles: "🍪 Выбрать категорию", "🎲 Случайная печенька", etc.
```

## Configuration Constants

### Categories Structure
```python
CATEGORIES = {
    "love": {"name": "💕 Любовь", "tags": ["любовь", "романтика"]},
    "self": {"name": "🧘‍♀️ Самопознание", "tags": ["психология"]},
    "work": {"name": "💼 Работа", "tags": ["карьера", "успех"]},
    "friendship": {"name": "🤝 Дружба", "tags": ["друзья"]},
    "memes": {"name": "😂 Мемные", "tags": ["юмор", "смешное"]}
}
```

### Image Paths
```python
IMAGE_FOLDERS = {
    "memes": "/root/bot/cookies/memes_images",
    "love": "/root/bot/cookies/memes_loves",
    "work": "/root/bot/cookies/memes_work", 
    "self": "/root/bot/cookies/memes_psy",
    "friendship": "/root/bot/cookies/memes_friendship"
}
```

### Random Actions
```python
RANDOM_ACTIONS = [
    "Погладь своего кота или собаку 🐱",
    "Скажи маме комплимент 👗",
    "Выпей стакан воды 💧",
    # ... 40+ actions
]
```

## Database Schema

### Tables Structure

#### Users Table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quotes_received INTEGER DEFAULT 0,
    favorite_category TEXT
);
```

#### Quotes Table  
```sql
CREATE TABLE quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    author TEXT,
    category TEXT,
    source TEXT
);
```

#### Daily Usage Tracking
```sql
CREATE TABLE daily_category_usage (
    user_id INTEGER,
    category TEXT,
    date TEXT,
    PRIMARY KEY (user_id, category, date)
);
```

## Scheduled Tasks

### Notification System
```python
# Daily notifications at 8:00 AM
schedule.every().day.at("08:00").do(send_daily_notification)

# Weekly notifications on Wednesday at 2:00 PM  
schedule.every().wednesday.at("14:00").do(send_weekly_notification)
```

### Background Task Runner
```python
async def schedule_tasks(bot):
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)  # Check every minute
```

## Error Handling

### Image Loading Fallbacks
```python
if not image_path:
    await message.answer("😔 Изображение не найдено, но вот твоя печенька!")
    await message.answer(format_quote(quote), parse_mode="Markdown")
    return
```

### Database Connection Safety
```python
try:
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    # ... operations
finally:
    conn.close()
```

### Service Availability
```python
async def send_daily_notification(bot):
    users = db.get_all_users()
    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Ошибка отправки пользователю {user_id}: {e}")
```

## Extending the Bot

### Adding New Categories
1. Update `CATEGORIES` dictionary
2. Add new image folder path to `IMAGE_FOLDERS`
3. Create physical directory structure
4. Add quotes to `BUILTIN_QUOTES`
5. Update keyboard layout if needed

### Adding New Commands
1. Create handler function: `async def cmd_newcommand(message: types.Message)`
2. Register handler: `dp.message.register(cmd_newcommand, Command("newcommand"))`
3. Add to help text and documentation

### Custom Quote Sources
1. Extend `Database.add_quote()` method
2. Create loading function in `quotes_loader.py`
3. Call during bot initialization
