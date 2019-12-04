
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
from datetime import datetime


chorus_dot_fm = "https://forum.chorus.fm/threads/"

class Thread:
    def __init__(self, thread_title):
        self.thread = thread_title
        self.url = f'{chorus_dot_fm}{thread_title}'
        self.first_page = BeautifulSoup(urllib.request.urlopen(f'{chorus_dot_fm}{thread_title}'), 'html.parser')
        self.current_page = self.first_page
        self.last_page_index = self.first_page.find_all('div',{'class': 'PageNav'})[0]['data-last']

    def pages(self, timestamp_one, timestamp_two):
        return_obj = []
        page_num = str(self.last_page_index)
        continue_search = True
        
        while (continue_search):
            self.navigate_to_page(page_num)
            posts_on_page = self.current_page.find_all('li', {'class': 'message'})
            posts_on_page.reverse()
            for post in posts_on_page:
                date_obj = post.find('abbr', {'class': 'DateTime'})
                if not date_obj:
                    date_epoch = post.find('span', {'class': 'DateTime'})['title']
                    date = datetime.strptime(date_epoch, '%b %d, %Y at %I:%M %p')
                else:
                    date_epoch = date_obj['data-time']
                    date = datetime.fromtimestamp(int(date_epoch))
                if date <= timestamp_one and date > timestamp_two:
                    return_obj += [post]

                else:
                    continue_search = False
            page_num = int(page_num) - 1
        
        return return_obj

    def navigate_to_page(self, index):
        self.current_page = BeautifulSoup(urllib.request.urlopen(f'{self.url}/page-{index}'), 'html.parser')

