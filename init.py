from forumscrapper import Thread
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import urllib.request
import json


def parse_bandcamp(source):
    return_obj = {}
    album_emb = BeautifulSoup(urllib.request.urlopen(f'https:{source}'), 'html.parser')
    a_tags = album_emb.find_all('a')
    for all in a_tags:
        if(all['href']):
            if(all['href'].startswith("https")):
                album = BeautifulSoup(urllib.request.urlopen(all['href']), 'html.parser')
                return(album.find('title').text.split('|'))
                



# Takes List of HTML pages and returns list of DICT, with each dict being an album info
def extract_artists(posts):
    releases = {}
    for post in posts:
        bandcamp = post.find_all('span', {'data-s9e-mediaembed': 'bandcamp'})
        if bandcamp:
            for album in bandcamp:
                bc_src = album.find('iframe')['src']
            band_info = parse_bandcamp(bc_src)
            releases[band_info[1].strip()] = band_info[0].strip()
    return releases


today = datetime.today()
two_week = today - timedelta(days=14)
emoThread = Thread("the-emo-thread.43651")
last_two_weeks = emoThread.pages(today, two_week)
all_artists = extract_artists(last_two_weeks)

print(all_artists)