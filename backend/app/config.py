import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEB_APP_URL = os.getenv("WEB_APP_URL", "http://localhost:8080")
DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"
API_PREFIX = "/api/v1"

# безопасность: в dev режиме мы можем отключать строгие проверки
# в продакшене DEV_MODE должен быть false
if not DEV_MODE and not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required when DEV_MODE is false")
