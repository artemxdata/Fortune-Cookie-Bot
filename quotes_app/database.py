import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Создаем папку data если её нет
os.makedirs('data', exist_ok=True)

DATABASE_URL = "sqlite:///data/quotes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()  # Новый синтаксис


def init_db():
    # Импортируем модели
    from models import Quote, User, UserInteraction  # без точки если файлы в корне
    # или from .models import Quote, User, UserInteraction  # если это пакет

    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы")
