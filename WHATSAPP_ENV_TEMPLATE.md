# WhatsApp Integration Configuration
# Add these to your .env file

# ==================== TWILIO WHATSAPP CONFIGURATION ====================

# Twilio Account Credentials
# Get these from: https://www.twilio.com/console
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here

# WhatsApp Number (Twilio Sandbox or Production)
# Sandbox: whatsapp:+14155238886
# Production: Your business number
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Optional: Meta WhatsApp Business API (for future migration)
# WHATSAPP_BUSINESS_PHONE_ID=your_phone_id
# WHATSAPP_BUSINESS_ACCESS_TOKEN=your_access_token

# ==================== WHATSAPP WEBHOOK CONFIGURATION ====================

# Webhook URL (where Twilio sends messages)
# Example: https://your-app.railway.app/api/whatsapp/webhook
WHATSAPP_WEBHOOK_URL=http://127.0.0.1:8000/api/whatsapp/webhook

# ==================== FEATURE FLAGS ====================

# Enable WhatsApp integration
ENABLE_WHATSAPP=true

# Enable WhatsApp notifications
WHATSAPP_NOTIFICATIONS_ENABLED=true

# Store sessions in Redis (production) or memory (development)
WHATSAPP_USE_REDIS=false
WHATSAPP_SESSION_TIMEOUT=3600  # 1 hour in seconds
