from fastapi import Header, HTTPException, Depends
from .config import DEV_MODE, BOT_TOKEN
from .security import verify_telegram_init_data

async def get_current_user(x_telegram_init_data: str = Header(None)):
    """
    извлекает и проверяет пользователя.
    """
    if DEV_MODE:
        # заглушка для разработки
        return {"id": "123456789", "first_name": "Dev User"}
    
    if not x_telegram_init_data:
        raise HTTPException(status_code=401, detail="Missing Telegram Init Data")
    
    if not verify_telegram_init_data(x_telegram_init_data, BOT_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid Telegram Init Data")
    
    # парсинг user data из строки (упрощенно)
    # в реальном проекте лучше использовать библиотеку типа python-telegram-bot или ручный парсинг JSON из user поля
    return {"id": "verified_user", "first_name": "Telegram User"}
