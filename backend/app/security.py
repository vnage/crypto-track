import hashlib
import hmac

def verify_telegram_init_data(init_data: str, bot_token: str) -> bool:
    """
    проверяет подпись initData от telegram.
    в v1 используется только если DEV_MODE=false.
    """
    if not bot_token:
        return False
    
    try:
        parsed_data = dict(x.split('=', 1) for x in init_data.split('&'))
        hash_check = parsed_data.pop('hash', '')
        
        data_check_string = '\n'.join(
            f"{k}={v}" for k, v in sorted(parsed_data.items())
        )
        
        secret_key = hmac.new(
            bot_token.encode(), 
            b"WebAppData", 
            hashlib.sha256
        ).digest()
        
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(calculated_hash, hash_check)
    except Exception:
        return False
