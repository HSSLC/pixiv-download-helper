import requests
import time
import threading
import re
import os
import bs4
import json
import os
import pyperclip as clip

def download(url):
    art_id = re.match('https://www\.pixiv\.net/artworks/(\\d+)', url).group(1)
    info_res = requests.get(url)
    bs = bs4.BeautifulSoup(info_res.text, features="html.parser")
    info = json.loads(bs.select("#meta-preload-data")[0].get('content'))['illust'][art_id]

    for page in range(info['pageCount']):
    
        height, width = info['height'], info['width']
        #add your filter in here
        if height < 1080 or width < 1920:
            print('size too small')
            return
        img_url = re.sub('p\d+', 'p%s' % page, info['urls']['original'])
        res = requests.get(img_url, headers={'referer': 'https://www.pixiv.net'})
        res.raise_for_status()
        with open(os.path.join('images', os.path.basename(img_url)), 'wb') as image_file:
            image_file.write(res.content)
    print('fin')

last_str = ''

while True:
    copy_content = clip.paste()
    #print(copy_content)
    if not copy_content == last_str:
        if re.match('https://(www\.)?pixiv\.net/artworks/(\\d+)', copy_content):
            print(copy_content)
            last_str = copy_content
            print('download %s' % copy_content)
            threading.Thread(target=download, args=[copy_content]).start()
    time.sleep(1)
