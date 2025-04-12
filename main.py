import yaml
import os
import sys
import time
from typing import Dict, Optional
from libs.logger import Logger
from libs.nitter_selenium import NitterSeleniumHandler
from libs.anthropic_handler import AnthropicHandler
from libs.gemini_handler import GeminiHandler
from libs.telegram_bot import TelegramBot

def load_config() -> Optional[Dict]:
    """Load configuration from config.yaml file"""
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            if not config:
                print("Error: config.yaml file is empty")
                return None
            return config
    except FileNotFoundError:
        print("Error: config.yaml file not found")
        return None
    except yaml.YAMLError as e:
        print(f"Error reading config.yaml: {str(e)}")
        return None
    except Exception as e:
        print(f"Unknown error when reading config: {str(e)}")
        return None

def setup_logging(config: Dict) -> Optional[Logger]:
    """Setup logging system"""
    try:
        # Ensure log directory exists
        log_dir = config.get('logging', {}).get('log_dir', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Initialize logger
        logger = Logger(config.get('logging', {}))
        return logger
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        return None

def process_tweets(nitter_handler: NitterSeleniumHandler, 
                  ai_handler,
                  username: str,
                  logger: Logger,
                  telegram_bot: TelegramBot) -> bool:
    """Process tweets from a user"""
    try:
        logger.info(f"Processing tweets from @{username}")
        
        # Get new tweets
        tweets = nitter_handler.get_new_tweets(username)
        if not tweets:
            logger.info(f"No new tweets from @{username}")
            return True
            
        # Process each tweet
        for tweet in tweets:
            try:
                # Get full tweet content
                tweet_content = tweet['content']
                if not tweet_content:
                    logger.error(f"Could not get content for tweet {tweet['id']}")
                    continue
                
                # Analyze tweet with Claude
                analysis = ai_handler.analyze_tweet(tweet_content)
                
                if analysis:
                    logger.info(f"Analyzed tweet {tweet['id']}: {analysis}")
                else:
                    logger.error(f"Could not analyze tweet {tweet['id']}")

                # Check analysis result and send warning if needed
                if analysis and analysis.get('is_warning'):
                    # Create warning message
                    warning_msg = f"""⚠️ <b>Security Warning</b>
                    
🔍 <b>{analysis.get('title')}</b>

📌 Information:
- Topic: {analysis.get('topic')}
- Info Type: {analysis.get('info_type')}
- Target: {analysis.get('target')}
- Product: {analysis.get('product_name')}
- Company: {analysis.get('company_name')}
- Vulnerability Type: {analysis.get('exploit_type')}
- Summary: {analysis.get('summary')}

🔗 Tweet Link: {tweet.get('link')}"""

                    # Send warning via Telegram
                    if not telegram_bot.send_message(warning_msg):
                        logger.error(f"Could not send warning for tweet {tweet['id']}")
            except Exception as e:
                logger.error(f"Error processing tweet {tweet['id']}: {str(e)}")
                continue
            time.sleep(10)  # Wait 10 seconds before processing next tweet
        return True
    except Exception as e:
        logger.error(f"Error processing user @{username}: {str(e)}")
        return False

def main() -> int:
    """Main program function"""
    # Load configuration
    config = load_config()
    if not config:
        return 1
        
    # Setup logging
    logger = setup_logging(config)
    if not logger:
        return 1
        
    try:
        # Initialize Telegram bot
        telegram_bot = TelegramBot(config.get('telegram', {}), logger)
        
        # Initialize handlers
        nitter_handler = NitterSeleniumHandler(config.get('nitter', {}), logger)
        # anthropic_handler = AnthropicHandler(config.get('anthropic', {}), logger)
        gemini_handler = GeminiHandler(config.get('gemini', {}), logger)
        # Start Nitter handler
        if not nitter_handler.start():
            logger.error("Failed to start Nitter handler")
            return 1
        
        # Get users list and topic from config
        users = config.get('system', {}).get('users', [])
        if not users:
            logger.error("No users found in configuration")
            return 1
                    
        # Process tweets from each user
        success = True
        for username in users:
            if not process_tweets(nitter_handler, gemini_handler, username, logger, telegram_bot):
                success = False
                
        # Stop Nitter handler
        nitter_handler.stop()
                
        return 0 if success else 1
        
    except Exception as e:
        logger.error(f"Program error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 