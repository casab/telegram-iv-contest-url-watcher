# Telegram IV Contest URL Watcher
A telegram bot that checks if your favorite URLs are added to the IV contest page and sends you a message if so.

## Getting Started
### Prerequisites
Python 2 or Python 3 and following libraries(which can be installed from requirements.txt);
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
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

By adding the telegram bot, you can give these commands;
```
To watch a specific website, type;
  /add url
To remove a url from the watchlist, type;
  /remove url
To get the list of all watched urls, type:
  /list
To start monitoring type:
  /monitor
To stop monitoring type:
  /stop
```
