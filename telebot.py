import requests
import re, textwrap, feedparser
from dateutil import parser
import datetime
import sys
import time
import pytz

token = 'INSERT TOKEN'
CHAT_ID = 330551667
TELEGRAM_API_SEND_MSG = 'https://api.telegram.org/bot1253021225:AAEwW5Ajq8qvqc74CRZ7jFeLmQPgHmek-qw/sendMessage'

# timezone = pytz.timezone('Asia/Singapore')
today = datetime.date.today()
yesterday = today - datetime.timedelta(1)
# time_now = ((datetime.datetime.now()) + datetime.timedelta(hours = 8) - datetime.timedelta(minutes = 15)).strftime('%Y-%m-%d %I:%M')


def get_date(entries):  
 dop = entries['published'] # dop = "date of publishing"
 dop_to_date = parser.parse(dop, ignoretz = True)
 dop_date = dop_to_date.date()
 return dop_date

def main():
  urls = ['http://feeds.bbci.co.uk/news/rss.xml','https://www.jpost.com/rss/rssfeedsheadlines.aspx','https://www.aljazeera.com/xml/rss/all.xml', 'https://www.theguardian.com/world/rss', 'https://www.scmp.com/rss/2/feed', 'https://www.timesofisrael.com/feed/','http://www.israelnationalnews.com/Rss.aspx?act=.1']
  #,'https://www.jpost.com/rss/rssfeedsheadlines.aspx','https://www.aljazeera.com/xml/rss/all.xml', 'https://www.theguardian.com/world/rss', 'https://www.scmp.com/rss/2/feed', 'https://www.timesofisrael.com/feed/','http://www.israelnationalnews.com/Rss.aspx?act=.1'
  
  lst = []
  
  while True:
    for i in urls:
      parsed_url = feedparser.parse(i)
      entries = parsed_url.entries
      noe = len(entries)
      
      if noe > 0:
        dop_date = get_date(entries[0])
      
        if (dop_date == today or dop_date == yesterday):
          title = entries[0]['title']
          date = dop_date
          link = entries[0]['link']
          summary = re.sub('<[^<]+?>','',str(entries[0]['summary']).replace('\n',''))

          if title not in lst:
            lst.append(title)
            display_news(title, dop_date, summary,link)

def display_news(title, dop_date, summary, link):
  data = {
      'chat_id': CHAT_ID,
      'text': f'{title}\n{dop_date}\n{summary}\n{link}',
      'parse_mode': 'Markdown'
    }
  requests.post(TELEGRAM_API_SEND_MSG, data=data)
  
    

main()
