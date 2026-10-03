from pydantic import BaseModel
from typing import Optional, List

class AssetSchema(BaseModel):
    symbol: str
    name: str
    amount: float
    price_usd: float
    change_24h: float
    value_usd: float
    allocation: float

class PortfolioResponse(BaseModel):
    total_balance: float
    pnl_today: float
    pnl_percent: float
    assets: List[AssetSchema]
    risk_insight: str
    is_demo: bool = True

class SettingsUpdate(BaseModel):
    language: Optional[str] = None
    alerts_enabled: Optional[bool] = None
    portfolio_threshold: Optional[float] = None
    btc_price_threshold: Optional[float] = None

class SettingsResponse(BaseModel):
    language: str
    alerts_enabled: bool
    portfolio_threshold: float
    btc_price_threshold: float
