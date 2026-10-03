from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True) # строка, т.к. может быть большой
    language = Column(String, default="en")
    alerts_enabled = Column(Boolean, default=False)
    portfolio_threshold = Column(Float, default=5.0) # процент
    btc_price_threshold = Column(Float, default=0.0) # цена
