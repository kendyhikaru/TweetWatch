# TweetWatch

A Python application that monitors Twitter accounts for security-related tweets, analyzes them using Claude AI, and sends alerts via Telegram.

## 📚 Documentation

- [How to Develop TweetWatch](docs/how_to_en.md) - Detailed development guide

## Overview

TweetWatch is a security monitoring tool that helps you stay updated with the latest security-related tweets. It automatically monitors specified Twitter accounts, analyzes tweets using Claude AI, and sends alerts via Telegram for important security findings.

## Features

- 🔍 Monitor multiple Twitter accounts using Nitter
- 🤖 Analyze tweets using Claude AI for security relevance
- 📢 Send alerts via Telegram for important security findings
- ⚙️ Configurable through YAML configuration
- 📝 Detailed logging system
- 🔒 Focus on cybersecurity and vulnerability information

## Requirements

- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver
- Anthropic API key
- Telegram Bot Token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kendyhikaru/TweetWatch.git
cd tweetwatch
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy and configure `config.yaml`:
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your settings
```

## Configuration

Edit `config.yaml` with your settings:

```yaml
anthropic:
  api_key: "your-anthropic-api-key"

telegram:
  token: "your-telegram-bot-token"
  chat_id: "your-chat-id"

nitter:
  base_url: "https://nitter.net"

system:
  users:
    - "Dinosn"
    - "other_security_accounts"
  topic: "cybersecurity"

logging:
  log_dir: "logs"
  log_level: "INFO"
```

## Usage

1. Start the application:
```bash
python main.py
```

2. TweetWatch will:
   - Monitor specified Twitter accounts
   - Analyze new tweets using Claude AI
   - Send alerts via Telegram for important security findings
   - Log all activities to the logs directory

## Project Structure

```
.
├── main.py              # Main application entry point
├── config.yaml          # Configuration file
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── libs/               # Library modules
    ├── logger.py       # Logging handler
    ├── nitter_selenium.py  # Nitter interaction
    ├── anthropic_handler.py  # Claude AI integration
    └── telegram_bot.py # Telegram bot handler
```

## Logging

Logs are stored in the `logs/` directory with the following format:
- `app.log`: Main application log
- Timestamp-based log files for each run

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Nitter](https://github.com/zedeus/nitter) - Twitter front-end
- [Anthropic](https://www.anthropic.com/) - Claude AI
- [Telegram Bot API](https://core.telegram.org/bots/api)

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 