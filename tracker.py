from telegram.ext import Updater, CommandHandler, Job
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import sys
import logging

if sys.version_info.major == 3:
    from urllib.parse import urlparse
elif sys.version_info.major == 2:
    from urlparse import urlparse

# Fill your API Token that you got from BotFather
TELEGRAM_API_TOKEN = ''

# Check every CHECK_PERIOD seconds to see if any url is added
CHECK_PERIOD = 60

url_list = defaultdict(list)
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
    elif (url in url_list[update.message.chat_id]):
        update.message.reply_text("Already on watchlist")
    else:
        url_list[update.message.chat_id].append(url)

def remove(bot, update, args):
    url = url_formatter(args[0])
    if (not url):
        update.message.reply_text("Incorrect url")
    else:
        url_list[update.message.chat_id].remove(url)

def get_watchlist(bot, update):
    update.message.reply_text("\n".join(url_list[update.message.chat_id]))

def check_urls(bot, job):
    r = requests.get('https://instantview.telegram.org/contest')
    page = BeautifulSoup(r.text, 'html5lib')
    for url in url_list[job.context]:
        result = page.find('div', attrs={
            'data-domain': url
        })
        if(result):
            bot.send_message(
                chat_id=job.context,
                text="{} is added to contest page".format(url)
            )
            url_list[job.context].remove(url)

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
