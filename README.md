# 🍪 Fortune-Cookie-Bot

*Daily inspiration and challenges delivered through fortune cookies*

## 📖 Project Description

Fortune Cookie Bot is an interactive Telegram bot that provides daily inspiration through personalized fortune cookies. Users can choose from different categories of quotes or accept random challenges. The bot features a sophisticated daily limit system, image galleries for each category, and donation support.

## ✨ Features

### 🍪 **Core Functionality**
- **5 Quote Categories**: Love 💕, Self-Discovery 🧘‍♀️, Work 💼, Friendship 🤝, Memes 😂
- **Random Actions**: Daily challenges and activities
- **Daily Limits**: One quote per category + one random action per day
- **Smart Caching**: Prevents duplicate content within the same day

### 🎨 **Visual Experience**
- Unique images for each category
- Random welcome images
- Donation support images
- Professional inline keyboards

### 📊 **User Management**
- SQLite database for user tracking
- Usage statistics and analytics
- Daily notification system
- User interaction history

### 💰 **Monetization**
- Integrated donation system via CloudTips
- Support button with random images

## 🛠 Technology Stack

- **Language**: Python 3.9+
- **Framework**: aiogram 3.x
- **Database**: SQLite3
- **Environment**: python-dotenv
- **Scheduling**: schedule library
- **Async**: asyncio

## 📁 Project Structure

```
Fortune-Cookie-Bot/
├── main.py                 # Main bot application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── 
├── bot/                  # Bot logic (currently in main.py)
├── config/               # Configuration files
├── data/                 # Database and data files
│   └── bot_data.db      # SQLite database
├── 
├── quotes/              # Image galleries
│   ├── memes_images/    # Memes category images
│   ├── memes_loves/     # Love category images
│   ├── memes_work/      # Work category images
│   ├── memes_psy/       # Self-discovery images
│   ├── memes_friendship/ # Friendship images
│   ├── start_image/     # Welcome images
│   └── donate_picture/  # Donation images
└── 
└── quotes_app/          # Quote management system
    ├── __init__.py
    ├── database.py      # Database models
    ├── models.py        # SQLAlchemy models
    └── quotes_loader.py # Quote loading utilities
```

## 🎮 User Interface

### 📱 **Persistent Keyboard**
The bot features a permanent keyboard with quick access to main functions:

| Button | Function | Description |
|--------|----------|-------------|
| 🍪 **Выбрать категорию** | Category Selection | Choose from 5 themed categories |
| 🎲 **Случайная печенька** | Random Cookie | Get random fortune from all categories |
| 🎯 **Печенька или действие** | Challenge Mode | Receive daily action challenge |
| 💖 **Поддержать бота** | Support Bot | Donation and support information |

### 🎯 **Interactive Flow**
1. **Welcome Screen** - Random greeting image with "ПОЕХАЛИ" button
2. **Category Selection** - 5 themed categories with unique visuals
3. **Fortune Delivery** - Personalized quote with matching image
4. **Action Challenges** - Daily tasks and activities
5. **Progress Tracking** - Usage statistics and limits

### 🛡️ **Smart Limitations**
- **Daily Limits**: One quote per category + one random action per day
- **Content Rotation**: Prevents duplicate quotes/images within 24 hours
- **Reset Schedule**: Limits reset at midnight (server time)

### 🗺️ **User Journey Flow**

```
/start → Welcome Image + "ПОЕХАЛИ" 
   ↓
Main Menu (Persistent Keyboard)
   ├── 🍪 Choose Category → 5 Options → Fortune + Image
   ├── 🎲 Random Cookie → Random Fortune + Image  
   ├── 🎯 Challenge → Daily Action Task
   └── 💖 Support → Donation Info + Image

Daily Limits Applied:
✅ 1 quote per category
✅ 1 random quote  
✅ 1 challenge action
❌ Exceeded → "Come back tomorrow" message
```

### 🎨 **Visual Categories**

Each category has its own image collection and personality:

- **💕 Love** (`memes_loves/`) - Romantic and relationship wisdom
- **🧘‍♀️ Self-Discovery** (`memes_psy/`) - Personal growth content  
- **💼 Work** (`memes_work/`) - Career and success motivation
- **🤝 Friendship** (`memes_friendship/`) - Social connection quotes
- **😂 Memes** (`memes_images/`) - Humorous and light content

## 🎮 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message with random image |
| `/categories` | Show category selection |
| `/quote` | Get random fortune cookie |
| `/todo` | Get random daily challenge |
| `/stats` | View personal statistics |
| `/support` | Show donation information |
| `/reload` | Reload built-in quotes |
| `/debug` | Show database statistics |

## 🚀 Installation & Setup

### 🖥️ **Production Deployment (Recommended)**

This bot is designed to run on a production server for 24/7 availability and scheduled notifications.

#### 1. Server Setup
```bash
# Clone repository on your server
git clone https://github.com/yourusername/Fortune-Cookie-Bot.git
cd Fortune-Cookie-Bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Environment Configuration
Create `.env` file with production settings:
```env
BOT_TOKEN=your_telegram_bot_token_here
```

#### 4. Setup Image Directories
Create and populate image directories on your server:
```bash
mkdir -p /root/bot/cookies/{memes_images,memes_loves,memes_work,memes_psy,memes_friendship,start_image,donate_picture}
```

Current production paths (update in `main.py` if needed):
- `/root/bot/cookies/memes_images/` - General meme images
- `/root/bot/cookies/memes_loves/` - Love category images  
- `/root/bot/cookies/memes_work/` - Work category images
- `/root/bot/cookies/memes_psy/` - Self-discovery images
- `/root/bot/cookies/memes_friendship/` - Friendship images
- `/root/bot/cookies/start_image/` - Welcome screen images
- `/root/bot/cookies/donate_picture/` - Donation support images

#### 5. Run Bot in Production
```bash
# Run with nohup for background execution
nohup python main.py > bot.log 2>&1 &

# Or use screen/tmux for session management
screen -S fortune_bot
python main.py

# Or setup as systemd service (recommended)
sudo systemctl enable fortune-cookie-bot
sudo systemctl start fortune-cookie-bot
```

### 🛠️ **Systemd Service Setup (Linux)**

Create `/etc/systemd/system/fortune-cookie-bot.service`:
```ini
[Unit]
Description=Fortune Cookie Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Fortune-Cookie-Bot
Environment=PATH=/root/Fortune-Cookie-Bot/venv/bin
ExecStart=/root/Fortune-Cookie-Bot/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=fortune-bot

[Install]
WantedBy=multi-user.target
```

Then activate:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fortune-cookie-bot
sudo systemctl start fortune-cookie-bot
```

### 💻 **Local Development**

For development and testing purposes:

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/Fortune-Cookie-Bot.git
cd Fortune-Cookie-Bot
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Setup Local Environment
Create `.env` file:
```env
BOT_TOKEN=your_test_bot_token_here
```

#### 4. Adjust Paths for Local Testing
Update image paths in `main.py` for local development:
```python
IMAGE_FOLDERS = {
    "memes": "quotes/memes_images",
    "love": "quotes/memes_loves", 
    # ... etc
}
```

#### 5. Run Locally
```bash
python main.py
```

## 🔧 Production Configuration

### Server Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended)
- **Python**: 3.9+
- **RAM**: 512MB minimum
- **Storage**: 2GB+ (for images and database)
- **Network**: Stable internet connection

### Environment Variables
```env
BOT_TOKEN=your_bot_token_here
# Optional configurations
DATABASE_PATH=/root/bot/data/bot_data.db
LOG_LEVEL=INFO
```

### Monitoring & Maintenance

#### Check Bot Status
```bash
# Check if bot is running
sudo systemctl status fortune-cookie-bot

# View recent logs
sudo journalctl -u fortune-cookie-bot -f

# Check bot process
ps aux | grep main.py
```

#### Log Management
```bash
# Bot logs location
tail -f /var/log/syslog | grep fortune-bot

# Or if using nohup
tail -f bot.log
```

#### Database Backup
```bash
# Backup database
cp /root/bot/data/bot_data.db /backup/bot_data_$(date +%Y%m%d).db

# Setup automatic backup (crontab)
0 2 * * * cp /root/bot/data/bot_data.db /backup/bot_data_$(date +\%Y\%m\%d).db
```

### Image Requirements
- **Format**: JPG, JPEG, PNG, GIF
- **Size**: Recommended 800x600px or higher
- **Content**: Family-friendly images matching category themes
- **Storage**: Organize in category-specific folders

## 🎯 Usage Examples

### Getting Started
1. Start the bot with `/start`
2. Choose a category or accept a random challenge
3. Receive your personalized fortune cookie with image
4. Come back tomorrow for fresh content!

### Category System
- **Love 💕**: Romantic quotes and relationship wisdom
- **Self-Discovery 🧘‍♀️**: Personal growth and mindfulness
- **Work 💼**: Career motivation and success quotes
- **Friendship 🤝**: Friendship and social connection wisdom
- **Memes 😂**: Humorous and light-hearted content

### Daily Challenges
Random actions include:
- Physical activities (exercises, walks)
- Social interactions (compliments, calls)
- Self-care activities (meditation, gratitude)
- Creative tasks (drawing, writing)

## 📊 Database Schema

### Users Table
- `user_id` - Telegram user ID
- `username` - Telegram username
- `first_name` - User's first name
- `last_name` - User's last name
- `registration_date` - Account creation date
- `quotes_received` - Total quotes received
- `favorite_category` - Most used category

### Quotes Table
- `id` - Unique quote identifier
- `text` - Quote content
- `author` - Quote author
- `category` - Quote category
- `source` - Data source

### Daily Usage Tracking
- `user_id` - User identifier
- `category` - Used category/action
- `date` - Usage date

## 💡 Technical Highlights

### 🎨 **Advanced UI/UX**
- **Persistent Keyboard**: Always-visible main menu using `ReplyKeyboardMarkup`
- **Inline Callbacks**: Category selection via `InlineKeyboardBuilder`
- **Rich Media**: Contextual images with every interaction
- **Smart Caching**: Daily content rotation system prevents repetition
- **Progress Feedback**: Real-time limit notifications and guidance

### 🔧 **Architecture Features**
- **Async Architecture**: Built with aiogram 3.x for high performance
- **Smart Caching**: Prevents content repetition within 24 hours using hashlib
- **Modular Design**: Separated concerns for maintainability
- **Error Handling**: Comprehensive exception handling with fallbacks
- **Database Integration**: SQLite with proper schema design and migrations
- **Scheduled Tasks**: Daily notifications and maintenance routines
- **Production Ready**: Systemd service configuration included

### 📊 **Content Management**
- **Built-in Database**: 100+ curated quotes across 5 categories
- **Dynamic Loading**: Automatic quote refresh and categorization
- **Image Galleries**: Category-specific visual content
- **Usage Analytics**: Track user engagement and preferences

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📈 Future Improvements

- [ ] Multi-language support
- [ ] Premium subscription features
- [ ] Advanced analytics dashboard
- [ ] Custom quote categories
- [ ] Social sharing features
- [ ] Web interface for administration

## 🐛 Known Issues

- Image loading requires proper directory structure
- Daily limits reset at midnight (server time)
- Large image files may cause slower response times

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💖 Support

If this bot brightens your day, consider supporting its development:
[☕ Buy me a coffee](https://pay.cloudtips.ru/p/93ad89fe)

## 📞 Contact

- **Telegram**: [@yourusername](https://t.me/yourusername)
- **Email**: your.email@example.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/Fortune-Cookie-Bot/issues)

---

*Made with ❤️ and lots of ☕*
