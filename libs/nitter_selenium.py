from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from typing import Dict, List, Optional
import time
import json
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class NitterSeleniumHandler:
    """Handler for interacting with Nitter using Selenium"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        """Initialize Nitter handler with configuration"""
        self.logger = logger
        self.base_url = config.get('base_url', 'https://nitter.net')
        self.driver = None
        self.processed_tweets = set()
        self.config = config
        # Tải danh sách tweets đã xử lý
        self._load_processed_tweets()
        
    def _load_processed_tweets(self):
        """Load processed tweets from file"""
        try:
            if os.path.exists('processed_tweets.json'):
                with open('processed_tweets.json', 'r') as f:
                    self.processed_tweets = set(json.load(f))
        except Exception as e:
            self.logger.error(f"Lỗi khi tải processed_tweets.json: {str(e)}")
            
    def _save_processed_tweets(self):
        """Save processed tweets to file"""
        try:
            with open('processed_tweets.json', 'w') as f:
                json.dump(list(self.processed_tweets), f)
        except Exception as e:
            self.logger.error(f"Lỗi khi lưu processed_tweets.json: {str(e)}")
            
    def start(self) -> bool:
        """Start the Selenium WebDriver"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            # Add options to bypass Cloudflare
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Add real user agent
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
            
            # Cấu hình đường dẫn binary của Chromium
            if 'binary_location' in self.config:
                options.binary_location = self.config['binary_location']
        
            
            self.driver = webdriver.Chrome(options=options, service=Service())
            
            # Add JavaScript to hide automation signs
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("WebDriver started successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error starting WebDriver: {str(e)}")
            return False
            
    def stop(self):
        """Stop the Selenium WebDriver"""
        if self.driver:
            self.driver.quit()
            
    def get_new_tweets(self, username: str) -> List[Dict]:
        """Get new tweets from a user"""
        if not self.driver:
            self.logger.error("WebDriver not started")
            return []
            
        try:
            # Navigate to user's page
            url = f"{self.base_url}/{username}"
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.timeline-item"))
            )
            
            # Wait for document to be ready
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Get tweet elements
            tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.timeline-item")
            tweets = []
            
            for tweet_element in tweet_elements:
                try:
                    # Get tweet ID
                    tweet_link = tweet_element.find_element(By.CSS_SELECTOR, "a.tweet-link").get_attribute("href")
                    tweet_id = tweet_link.split("/")[-1]
                    
                    # Get tweet time
                    time_element = tweet_element.find_element(By.CSS_SELECTOR, "span.tweet-date a")
                    time_text = time_element.text.strip()
                    # Check tweet time 
                    if time_text.endswith('m') :
                        # Get tweet content
                        content_element = tweet_element.find_element(By.CSS_SELECTOR, "div.tweet-content")
                        tweet_content = content_element.get_attribute("outerHTML")
                        
                        tweets.append({
                            'id': tweet_id,
                            'time': time_text,
                            'content': tweet_content,
                            'link': tweet_link
                        })
                except NoSuchElementException as e:
                    self.logger.error(f"Error extracting tweet data: {str(e)}")
                    continue
                    
            return tweets
        except TimeoutException:
            self.logger.error("Timeout waiting for tweets to load")
            return []
        except Exception as e:
            self.logger.error(f"Error getting tweets: {str(e)}")
            return []
            
    def get_tweet_content(self, tweet_id: str) -> Optional[str]:
        """Get full content of a specific tweet"""
        if not self.driver:
            self.logger.error("WebDriver not started")
            return None
            
        try:
            # Navigate to tweet page
            url = f"{self.base_url}/i/status/{tweet_id}"
            self.driver.get(url)
            
            # Wait for tweet content to load
            content_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.tweet-content"))
            )
            
            return content_element.text
        except TimeoutException:
            self.logger.error(f"Timeout waiting for tweet {tweet_id} to load")
            return None
        except Exception as e:
            self.logger.error(f"Error getting tweet content: {str(e)}")
            return None
            
    def is_tweet_processed(self, tweet_id: str) -> bool:
        """Kiểm tra tweet đã được xử lý chưa"""
        return tweet_id in self.processed_tweets
        
    def mark_tweet_processed(self, tweet_id: str):
        """Đánh dấu tweet đã được xử lý"""
        self.processed_tweets.add(tweet_id)
        self._save_processed_tweets()
        
    def get_tweet_metrics(self, tweet_id: str) -> Optional[Dict]:
        """Lấy các chỉ số của tweet (likes, retweets, replies)"""
        try:
            if not self.driver:
                if not self.start():
                    return None
                    
            # Truy cập trang tweet
            tweet_url = f"{self.base_url}/i/status/{tweet_id}"
            self.driver.get(tweet_url)
            
            # Đợi các chỉ số load
            try:
                self.driver.find_element(By.CSS_SELECTOR, "div.tweet-stats")
                
                metrics = {
                    'likes': self.driver.find_element(By.CSS_SELECTOR, "div.tweet-stat:nth-child(1)").text,
                    'retweets': self.driver.find_element(By.CSS_SELECTOR, "div.tweet-stat:nth-child(2)").text,
                    'replies': self.driver.find_element(By.CSS_SELECTOR, "div.tweet-stat:nth-child(3)").text
                }
                return metrics
            except TimeoutException:
                self.logger.error(f"Timeout khi đợi chỉ số tweet {tweet_id}")
                return None
                
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy chỉ số tweet {tweet_id}: {str(e)}")
            return None 