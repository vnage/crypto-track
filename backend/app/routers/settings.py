from fastapi import APIRouter, Depends
from ..schemas import SettingsUpdate, SettingsResponse
from ..telegram_auth import get_current_user

router = APIRouter()

# mock storage for settings in memory for demo
_mock_settings = {
    "language": "en",
    "alerts_enabled": False,
    "portfolio_threshold": 5.0,
    "btc_price_threshold": 0.0
}

@router.get("/", response_model=SettingsResponse)
async def get_settings(user: dict = Depends(get_current_user)):
    return SettingsResponse(**_mock_settings)

@router.patch("/", response_model=SettingsResponse)
async def update_settings(settings: SettingsUpdate, user: dict = Depends(get_current_user)):
    if settings.language: _mock_settings["language"] = settings.language
    if settings.alerts_enabled is not None: _mock_settings["alerts_enabled"] = settings.alerts_enabled
    if settings.portfolio_threshold is not None: _mock_settings["portfolio_threshold"] = settings.portfolio_threshold
    if settings.btc_price_threshold is not None: _mock_settings["btc_price_threshold"] = settings.btc_price_threshold
    
    return SettingsResponse(**_mock_settings)
