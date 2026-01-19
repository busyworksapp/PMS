import os
from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """App configuration from environment or .env file."""
    
    # Database - Get from environment or use default
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:fYJdZhXYpLzfiLFhgjvjkUWUzDKKCaYa@shortline.proxy.rlwy.net:19278/railway"
    )
    
    # Redis - Get from environment or use default
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://default:maXFCPazHpxaASnHpDcszQQpTsfONXFE@caboose.proxy.rlwy.net:39766"
    )
    
    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Twilio WhatsApp Configuration
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "AC21e03f1ff3792a2fe49435744505c53e")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "0d2692d716bc761af953a161492d2886")
    TWILIO_WHATSAPP_NUMBER: str = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155552671")
    TWILIO_WEBHOOK_VERIFY_TOKEN: str = os.getenv("TWILIO_WEBHOOK_VERIFY_TOKEN", "your-webhook-verify-token")
    
    # App
    APP_NAME: str = "Barron Production Management System"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Log config (without exposing secrets)
logger.info(f"App: {settings.APP_NAME}")
logger.info(f"Debug: {settings.DEBUG}")
logger.info(f"Database host configured: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'N/A'}")
