from fastapi import APIRouter, Depends
from ..schemas import PortfolioResponse, AssetSchema
from ..telegram_auth import get_current_user

router = APIRouter()

@router.get("/", response_model=PortfolioResponse)
async def get_portfolio(user: dict = Depends(get_current_user)):
    """
    возвращает mock-данные портфеля.
    в будущем здесь будет запрос к бирже или бд.
    """
    assets = [
        AssetSchema(symbol="BTC", name="Bitcoin", amount=0.015, price_usd=64000, change_24h=2.1, value_usd=960.0, allocation=76.9),
        AssetSchema(symbol="ETH", name="Ethereum", amount=0.1, price_usd=2500, change_24h=-1.2, value_usd=250.0, allocation=20.0),
        AssetSchema(symbol="SOL", name="Solana", amount=2.5, price_usd=140, change_24h=5.4, value_usd=350.0, allocation=2.8), # ошибка в расчете аллокации для примера, исправим ниже
        AssetSchema(symbol="USDT", name="Tether", amount=12.8, price_usd=1.0, change_24h=0.01, value_usd=12.8, allocation=0.3)
    ]
    
    # пересчитаем аллокацию корректно для мока
    total = sum(a.value_usd for a in assets)
    for a in assets:
        a.allocation = round((a.value_usd / total) * 100, 1)
        
    # сортировка по стоимости
    assets.sort(key=lambda x: x.value_usd, reverse=True)

    return PortfolioResponse(
        total_balance=1247.80,
        pnl_today=32.14,
        pnl_percent=2.6,
        assets=assets,
        risk_insight="49.7% of portfolio is BTC",
        is_demo=True
    )
