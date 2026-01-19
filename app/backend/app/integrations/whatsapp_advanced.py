"""
WhatsApp Advanced Features Module
Provides enhanced WhatsApp functionality for future use
"""

from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime


class ButtonType(Enum):
    """WhatsApp button types"""
    QUICK_REPLY = "quick_reply"
    URL = "url"
    PHONE = "phone_number"


class MediaType(Enum):
    """Supported media types for WhatsApp"""
    IMAGE = "image"
    PDF = "document"
    AUDIO = "audio"
    VIDEO = "video"


class WhatsAppButton:
    """Represents a WhatsApp interactive button"""
    
    def __init__(self, title: str, id: str, button_type: ButtonType = ButtonType.QUICK_REPLY):
        self.title = title
        self.id = id
        self.button_type = button_type
    
    def to_dict(self):
        return {
            "type": self.button_type.value,
            "title": self.title,
            "id": self.id
        }


class WhatsAppMediaMessage:
    """Represents a WhatsApp media message"""
    
    def __init__(self, media_type: MediaType, url: str, caption: Optional[str] = None):
        self.media_type = media_type
        self.url = url
        self.caption = caption
    
    def to_dict(self):
        return {
            "type": self.media_type.value,
            "url": self.url,
            "caption": self.caption
        }


class WhatsAppInteractiveMessage:
    """Build interactive WhatsApp messages with buttons"""
    
    def __init__(self, body: str, footer: Optional[str] = None):
        self.body = body
        self.footer = footer
        self.buttons: List[WhatsAppButton] = []
    
    def add_button(self, button: WhatsAppButton) -> 'WhatsAppInteractiveMessage':
        """Add button to message"""
        if len(self.buttons) < 3:  # WhatsApp limit
            self.buttons.append(button)
        return self
    
    def add_quick_reply(self, title: str, id: str) -> 'WhatsAppInteractiveMessage':
        """Add quick reply button"""
        self.add_button(WhatsAppButton(title, id, ButtonType.QUICK_REPLY))
        return self
    
    def to_dict(self):
        return {
            "type": "interactive",
            "body": {
                "text": self.body
            },
            "footer": {
                "text": self.footer
            } if self.footer else None,
            "action": {
                "buttons": [btn.to_dict() for btn in self.buttons]
            }
        }


class WhatsAppMessageTemplate:
    """WhatsApp message templates for common responses"""
    
    @staticmethod
    def main_menu_interactive() -> WhatsAppInteractiveMessage:
        """Interactive menu with buttons"""
        msg = WhatsAppInteractiveMessage(
            body="👋 Welcome to Barron Manufacturing!\n\nSelect an option:",
            footer="Reply with number or button"
        )
        msg.add_quick_reply("📝 Create Defect", "1")
        msg.add_quick_reply("📦 Order Status", "2")
        msg.add_quick_reply("🔧 Maintenance", "3")
        return msg
    
    @staticmethod
    def order_status_with_image(order_id: str, image_url: str) -> Dict:
        """Order status with Gantt chart image"""
        return {
            "type": "image",
            "image": {
                "url": image_url,
                "caption": f"Gantt Chart for Order {order_id}"
            }
        }
    
    @staticmethod
    def sla_alert(ticket_id: str, remaining_hours: float) -> str:
        """SLA breach alert message"""
        if remaining_hours < 1:
            emoji = "🔴"
            status = "CRITICAL"
        elif remaining_hours < 4:
            emoji = "🟠"
            status = "WARNING"
        else:
            emoji = "🟢"
            status = "OK"
        
        return f"""{emoji} SLA Alert: {ticket_id}

Time Remaining: {remaining_hours:.1f} hours
Status: {status}

⚠️ This ticket requires attention!"""
    
    @staticmethod
    def defect_report_pdf(order_id: str, pdf_url: str) -> Dict:
        """Send defect report as PDF"""
        return {
            "type": "document",
            "document": {
                "url": pdf_url,
                "caption": f"Defect Report for {order_id}"
            }
        }
    
    @staticmethod
    def multi_language_greeting(language: str = "en") -> str:
        """Multi-language greeting"""
        greetings = {
            "en": "👋 Welcome to Barron Manufacturing!\n\nType 'hi' for menu",
            "es": "👋 ¡Bienvenido a Barron Manufacturing!\n\nEscribe 'hola' para el menú",
            "fr": "👋 Bienvenue à Barron Manufacturing!\n\nTapez 'bonjour' pour le menu",
            "pt": "👋 Bem-vindo à Barron Manufacturing!\n\nDigite 'oi' para o menu",
            "ar": "👋 مرحبا بك في Barron Manufacturing!\n\nاكتب 'مرحبا' للقائمة",
        }
        return greetings.get(language, greetings["en"])


class WhatsAppNotificationService:
    """Send WhatsApp notifications for important events"""
    
    @staticmethod
    def sla_breach_notification(ticket_id: str, machine_id: str, hours_remaining: float) -> str:
        """Notify when SLA is about to breach"""
        return f"""🚨 SLA Breach Warning!

Ticket: {ticket_id}
Machine: {machine_id}
Time Remaining: {hours_remaining:.1f}h

Immediate action required!
Visit dashboard for details."""
    
    @staticmethod
    def order_completed_notification(order_id: str, completion_date: str) -> str:
        """Notify when order is completed"""
        return f"""✅ Order Complete!

Order: {order_id}
Completion Date: {completion_date}

Quality Check: PASSED
Ready for Shipment

Thank you for using Barron Manufacturing!"""
    
    @staticmethod
    def shift_notification(shift_info: Dict) -> str:
        """Notify about upcoming shift"""
        return f"""📢 Shift Notification

Shift: {shift_info.get('shift_name')}
Start Time: {shift_info.get('start_time')}
Machine: {shift_info.get('machine')}
Operator: {shift_info.get('operator')}

Please report on time!"""
    
    @staticmethod
    def quality_alert_notification(defect_info: Dict) -> str:
        """Notify about quality issue"""
        return f"""⚠️ Quality Alert

Order: {defect_info.get('order')}
Defect Type: {defect_info.get('defect_type')}
Severity: {defect_info.get('severity')}
Impact: Order ON HOLD

Investigation Required!"""


class WhatsAppAnalytics:
    """Track WhatsApp interaction analytics"""
    
    def __init__(self):
        self.messages_received = 0
        self.messages_sent = 0
        self.workflows_completed = 0
        self.errors_occurred = 0
        self.active_users = set()
        self.session_durations: List[float] = []
    
    def record_incoming_message(self, phone_number: str):
        """Record incoming message"""
        self.messages_received += 1
        self.active_users.add(phone_number)
    
    def record_outgoing_message(self):
        """Record outgoing message"""
        self.messages_sent += 1
    
    def record_workflow_completion(self, duration: float):
        """Record completed workflow"""
        self.workflows_completed += 1
        self.session_durations.append(duration)
    
    def record_error(self):
        """Record error"""
        self.errors_occurred += 1
    
    def get_stats(self) -> Dict:
        """Get analytics statistics"""
        avg_duration = sum(self.session_durations) / len(self.session_durations) if self.session_durations else 0
        
        return {
            "messages_received": self.messages_received,
            "messages_sent": self.messages_sent,
            "workflows_completed": self.workflows_completed,
            "errors_occurred": self.errors_occurred,
            "active_users": len(self.active_users),
            "average_session_duration": avg_duration,
            "message_ratio": self.messages_sent / max(self.messages_received, 1)
        }


class WhatsAppRateLimiter:
    """Rate limiting for WhatsApp messages"""
    
    def __init__(self, max_messages_per_minute: int = 10):
        self.max_messages = max_messages_per_minute
        self.user_message_times: Dict[str, List[datetime]] = {}
    
    def is_allowed(self, phone_number: str) -> bool:
        """Check if user can send message"""
        now = datetime.utcnow()
        
        if phone_number not in self.user_message_times:
            self.user_message_times[phone_number] = []
        
        # Remove old messages (> 1 minute)
        self.user_message_times[phone_number] = [
            msg_time for msg_time in self.user_message_times[phone_number]
            if (now - msg_time).seconds < 60
        ]
        
        # Check limit
        if len(self.user_message_times[phone_number]) >= self.max_messages:
            return False
        
        # Record message
        self.user_message_times[phone_number].append(now)
        return True
    
    def get_remaining(self, phone_number: str) -> int:
        """Get remaining messages for user"""
        now = datetime.utcnow()
        
        if phone_number not in self.user_message_times:
            return self.max_messages
        
        # Remove old messages
        self.user_message_times[phone_number] = [
            msg_time for msg_time in self.user_message_times[phone_number]
            if (now - msg_time).seconds < 60
        ]
        
        return self.max_messages - len(self.user_message_times[phone_number])


# Example usage in future enhancements:
"""
# Interactive menu with buttons
menu = WhatsAppMessageTemplate.main_menu_interactive()
response = send_whatsapp_message(phone, menu.to_dict())

# Notifications
notification = WhatsAppNotificationService.sla_breach_notification(...)
send_whatsapp_message(phone, notification)

# Analytics
analytics = WhatsAppAnalytics()
analytics.record_incoming_message(phone)
stats = analytics.get_stats()

# Rate limiting
limiter = WhatsAppRateLimiter()
if limiter.is_allowed(phone):
    send_whatsapp_message(phone, "message")
"""
