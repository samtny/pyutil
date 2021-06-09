import time
import praw
import telegram
import logging
import sys
import credentials

### Original code by voron Discord user So I says to the guy

### DO NOT USE THIS TO AUTOMATE POSTING YOUR REQUEST!!!!!!
### ONLY USE IT TO NOTIFY YOU WHEN IT'S TIME TO POST

next_serial=496  # the next v0 serial that will be assigned (look at the sub and figure this out)
wanted_serial=496 # the serial you want
chat_id=0  # telegram chat id to send messages to

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logging.info('Starting bot')

bot = telegram.Bot(credentials.telegramSecret)

reddit = praw.Reddit(
    client_id=credentials.redditClientId, 
    client_secret=credentials.redditSecret, 
    user_agent='voronsnipebot')

seen = set()

def explode():
    while True:
        bot.send_message(chat_id=chat_id, text='{} is READY!!!!'.format(wanted_serial))
        time.sleep(20)

def initialize_seen():
    for post in reddit.subreddit('voroncorexy').new(limit=20):
        logging.info('Seen post {}'.format(post.id))
        if post.id in seen:
            continue
        seen.add(post.id)

initialize_seen()

def is_v0(t):
    t = t.lower()
    return 'v0' in t or 'v 0' in t or 'zero' in t

def update():
    global next_serial
    for post in reddit.subreddit('voroncorexy').new(limit=20):
        if post.id in seen:
            continue
        seen.add(post.id)
        if 'serial request' in post.title.lower() and is_v0(post.title):
            next_serial += 1
            if next_serial == wanted_serial:
                explode()

if __name__ == '__main__':
    while True:
        time.sleep(20)
        update()
