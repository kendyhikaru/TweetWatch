import requests
import logging
from typing import Dict, Optional

class TelegramBot:
    """Telegram bot handler for sending messages"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        """Initialize Telegram bot with configuration"""
        self.logger = logger
        self.token = config.get('bot_token')
        self.chat_id = config.get('chat_id')
        
        if not self.token or not self.chat_id:
            self.logger.error("Telegram configuration missing token or chat_id")
            raise ValueError("Telegram configuration missing token or chat_id")
            
    def send_message(self, message: str) -> bool:
        """Send message to Telegram channel"""
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, data=data)
            response.raise_for_status()
            
            self.logger.info("Message sent successfully to Telegram")
            return True
        except Exception as e:
            self.logger.error(f"Error sending message to Telegram: {str(e)}")
            return False 