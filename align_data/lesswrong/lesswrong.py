import gdown
import json
import os
from bs4 import BeautifulSoup
import requests
import time


class Lesswrong:
    def __init__(self, gdrive_address):
        self.name = 'lesswrong'
        self.gdrive_address = gdrive_address
        self.local_path = 'data/lesswrong/'
        self.local_htmls = self.local_path + 'lesswrong_htmls/'
        self.local_out = self.local_path + 'lesswrong_json/'

    def fetch_entries(self):
        os.makedirs(self.local_path) if not os.path.exists(self.local_path) else ''
        os.makedirs(self.local_out) if not os.path.exists(self.local_out) else ''
        # check if there are any files in local htmls, if not create folder, pull the html files
        if not os.path.isdir(self.local_htmls):
            os.makedirs(self.local_htmls)
        if not len(os.listdir(self.local_htmls)):
            self.scrape_html_files()

    def scrape_html_files(self):
        self.pull_drom_gdrive()
        # unzip the downloaded folder
        print('Unzipping...')
        os.system('unzip -o ' + self.local_path + 'lesswrong.zip -d ' + self.local_path)
        with open(self.local_path+'lesswrong.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
            posts = soup.find_all('div', {'class':
                                        'PostsItem2-postsItem PostsItem2-withGrayHover PostsItem2-withRelevanceVoting'})
            titles = []
            links = []
            authors = []
            for post in posts:
                title_span = post.find('span', {'class': 'PostsItem2-title'})
                titles.append(title_span.text)
                links.append(title_span.select_one("a")['href'])
                author_span = post.find_all('span', {'class': 'PostsUserAndCoauthors-lengthLimited'})
                authors.append([x.text for x in author_span])
            for link, title, author in zip(links, titles, authors):
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, '
                                         'like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                r = requests.get(link)
                with open(self.local_htmls+title+'.json', 'wb') as output_json:
                    json.dump({'title': title, 'link': link, 'authors': author}, output_json)
                time.sleep(1)

    def pull_drom_gdrive(self):
        gdown.download(url=self.gdrive_address, output=self.local_path + 'lesswrong.zip', quiet=False)
