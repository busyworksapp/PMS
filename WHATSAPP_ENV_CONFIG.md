# WhatsApp Integration Configuration
# Get these credentials from Meta WhatsApp Business Platform
# https://developers.facebook.com/docs/whatsapp/cloud-api

# Meta Business Account ID
# Found in: Meta Business Manager > WhatsApp > Settings > Account
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id_here

# WhatsApp Phone Number ID
# This is the unique identifier for your WhatsApp phone number
# Found in: Meta Business Manager > WhatsApp > Settings > Phone Numbers
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here

# WhatsApp Business API Token
# Generate a permanent token in: Meta App > Settings > Basic > App Passwords
# This token is used to authenticate API requests to Meta
WHATSAPP_API_TOKEN=your_api_token_here

# Webhook Verify Token
# Create any random string here
# This token is used to verify that webhooks are coming from Meta
# Must be at least 8 characters
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_webhook_verify_token_here

# Webhook URL
# The public URL where Meta will send webhook events
# Must be HTTPS and publicly accessible
# Should be: https://your-domain.com/api/whatsapp/webhook
WHATSAPP_WEBHOOK_URL=https://your-domain.com/api/whatsapp/webhook

# Optional: Enable WhatsApp debug logging
WHATSAPP_DEBUG=false
