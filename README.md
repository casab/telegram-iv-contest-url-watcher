# Telegram IV Contest URL Watcher
A telegram bot that checks if your favorite URLs are added to the IV contest page and sends you a messasge if so.

## Getting Started
### Prerequisites
Python 2 or Python 3 and following libraries(which can be installed from requirements.txt);
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
- [html5lib](https://github.com/html5lib/html5lib-python)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [requests](https://github.com/requests/requests)

### Usage
```
git clone https://github.com/casab/telegram-iv-contest-url-watcher
cd telegram-iv-contest-url-watcher
pip install -r requirements.txt
```
Then open tracker.py and fill the TELEGRAM_API_TOKEN and select a proper CHECK_PERIOD.
```
python tracker.py
```
