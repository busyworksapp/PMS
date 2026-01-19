import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App configuration from environment or .env file."""
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:fYJdZhXYpLzfiLFhgjvjkUWUzDKKCaYa@shortline.proxy.rlwy.net:19278/railway"
    
    # Redis
    REDIS_URL: str = "redis://default:maXFCPazHpxaASnHpDcszQQpTsfONXFE@caboose.proxy.rlwy.net:39766"
    
    # Auth
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Twilio WhatsApp Configuration
    TWILIO_ACCOUNT_SID: str = "AC21e03f1ff3792a2fe49435744505c53e"
    TWILIO_AUTH_TOKEN: str = "0d2692d716bc761af953a161492d2886"
    TWILIO_WHATSAPP_NUMBER: str = "whatsapp:+14155552671"  # Your Twilio WhatsApp sandbox number or production number
    TWILIO_WEBHOOK_VERIFY_TOKEN: str = "your-webhook-verify-token"
    
    # App
    APP_NAME: str = "Barron Production Management System"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
