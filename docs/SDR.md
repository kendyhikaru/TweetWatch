# Software Requirements Document
## Simple X (Twitter) Content Monitor with Telegram Notification

### 1. System Overview
A lightweight tool to automatically collect posts from X (Twitter), classify content using Anthropic API, and send notifications via Telegram for relevant topics.

### 2. Objectives
- Automatically fetch new posts from X via API
- Classify content using Anthropic API
- Send Telegram notifications for posts matching topics of interest

### 3. Functional Requirements

#### 3.1 Data Collection
- Connect to Twitter API to fetch new posts
- Store temporary cache in memory to avoid duplicates
- Run periodically every 5-10 minutes
- Handle API rate limits appropriately

#### 3.2 Content Classification
- Utilize Anthropic API for content analysis
- Simple configuration via YAML/JSON file:
  - List of topics of interest
  - Keywords per topic
  - Prompt templates for Anthropic API
- Classify posts based on content and keywords

#### 3.3 Telegram Notification
- Integrate simple Telegram Bot
- Send immediate notifications for relevant posts
- Format messages with post link and summary

### 4. Technical Architecture

```plaintext
[Twitter API] -> [Script Collector] -> [Anthropic API]
                                           |
                                           v
                                    [Telegram Bot]
```

### 5. Technology Stack
- Language: Python
- Configuration: YAML/JSON
- Key Libraries:
  - tweepy (Twitter API)
  - anthropic (Anthropic API)
  - python-telegram-bot
  - pyyaml/json

### 6. Code Structure

```python
# config.yaml
topics:
  tech:
    keywords: ["AI", "Python", "Programming"]
  finance:
    keywords: ["Bitcoin", "Stock", "Investment"]

# main.py
class SimpleNewsBot:
    def __init__(self):
        self.load_config()
        self.setup_apis()
        self.processed_tweets = set()  # Simple memory cache

    def process_tweets(self):
        tweets = self.get_new_tweets()
        for tweet in tweets:
            if tweet.id not in self.processed_tweets:
                classification = self.classify_tweet(tweet)
                if classification['relevant']:
                    self.send_telegram_notification(tweet)
                self.processed_tweets.add(tweet.id)
```

### 7. Deployment Options
- Run as a simple Python script
- Deployment platforms:
  - Local machine
  - Small VPS (DigitalOcean, Linode)
  - Heroku free tier

### 8. Error Handling & Logging
- Basic error handling for API failures
- Simple file logging
- Status updates via Telegram
- Retry mechanism for API calls

### 9. Limitations
- In-memory cache clears on restart
- Dependent on API availability
- Limited by API rate limits
- No persistent storage

### 10. Future Enhancements
- Add simple file-based storage
- Implement more sophisticated classification
- Add more notification channels
- Enhance error recovery

### 11. Configuration Requirements
Required API Keys and Tokens:
- Twitter API credentials
- Anthropic API key
- Telegram Bot token

### 12. Maintenance
- Regular monitoring of API limits
- Backup of configuration files
- Update of classification keywords
- Monitor system logs

### 13. Success Criteria
- Successfully fetch and process new posts
- Accurate classification of content
- Timely delivery of notifications
- System stability and reliability
