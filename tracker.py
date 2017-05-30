import requests, sys, logging, shelve
from telegram.ext import Updater, CommandHandler, Job
from bs4 import BeautifulSoup
from collections import defaultdict
from persist import PersistentDict
import os

if sys.version_info.major == 3:
    from urllib.parse import urlparse
elif sys.version_info.major == 2:
    from urlparse import urlparse

# Fill your API Token that you got from BotFather
TELEGRAM_API_TOKEN = ''

# Check every CHECK_PERIOD seconds to see if any url is added
CHECK_PERIOD = 60

URL_LIST_FILE = os.getcwd() + '\\url_list.json'
JOB_LIST_FILE = os.getcwd() + '\\job_list.json'
jobs = defaultdict(list)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(bot, update):
    update.message.reply_text(
    """
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
    """)

def get_url_list(chat_id):
    chat_id = str(chat_id)
    with PersistentDict(URL_LIST_FILE, 'c', format='json') as d:
        if chat_id in d.keys():
            url_list = d[chat_id]
        else:
            url_list = []
    return url_list

def add_to_url_list(url, chat_id):
    chat_id = str(chat_id)
    with PersistentDict(URL_LIST_FILE, 'c', format='json') as d:
        if chat_id not in d.keys():
            d[chat_id] = [url]
        else:
            temp = d[chat_id]
            temp.append(url)
            d[chat_id] = temp

def remove_from_url_list(url, chat_id):
    chat_id = str(chat_id)
    with PersistentDict(URL_LIST_FILE, 'c', format='json') as d:
        temp = d[chat_id]
        temp.remove(url)
        d[chat_id] = temp

def url_formatter(url):
    parsed = urlparse(url)
    if (parsed.path):
        if '.' not in parsed.path: return False
        if parsed.path.startswith('www.'): return parsed.path[4:]
        return parsed.path
    elif (parsed.netloc):
        if parsed.netloc.startswith('www.'): return parsed.netloc[4:]
        return parsed.netloc
    else: return False

def add(bot, update, args):
    url = url_formatter(args[0])
    if (not url):
        update.message.reply_text("Incorrect url")
    elif (url in get_url_list(update.message.chat_id)):
        update.message.reply_text("Already on watchlist")
    else:
        add_to_url_list(url, update.message.chat_id)

def remove(bot, update, args):
    url = url_formatter(args[0])
    if (not url):
        update.message.reply_text("Incorrect url")
    elif (url not in get_url_list(update.message.chat_id)):
        update.message.reply_text("That url is not on the watchlist")
    else:
        remove_from_url_list(url, update.message.chat_id)

def get_watchlist(bot, update):
    url_list = get_url_list(update.message.chat_id)
    update.message.reply_text("\n".join(url_list))

def check_urls(bot, job):
    r = requests.get('https://instantview.telegram.org/contest')
    page = BeautifulSoup(r.text, 'html5lib')
    url_list = get_url_list(job.context)
    for url in url_list:
        result = page.find('div', attrs={
            'data-domain': url
        })
        if(result):
            bot.send_message(
                chat_id=job.context,
                text="{} is added to contest page".format(url)
            )
            remove_from_url_list(url, job.context)

def cb_watch(bot, update, job_queue):
    if not jobs[update.message.chat_id]:
        job_watch = job_queue.run_repeating(
            check_urls,
            interval=CHECK_PERIOD,
            context=update.message.chat_id
        )
        jobs[update.message.chat_id].append(job_watch)
        update.message.reply_text("Started monitoring, type /stop to stop monitoring")
    else:
        update.message.reply_text("Already monitoring")

def stop_watch(bot, update):
    if jobs[update.message.chat_id]:
        jobs[update.message.chat_id][0].schedule_removal()
        del jobs[update.message.chat_id][0]
        update.message.reply_text("Stopped monitoring")

updater = Updater(TELEGRAM_API_TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', start))
updater.dispatcher.add_handler(CommandHandler('add', add, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('remove', remove, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('list', get_watchlist))
updater.dispatcher.add_handler(CommandHandler('monitor', cb_watch, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('stop', stop_watch))


updater.start_polling()
updater.idle()
