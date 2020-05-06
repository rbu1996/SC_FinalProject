from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import datetime
import json

class Crawler_CNN():
    def __init__(self):
        self.driver=webdriver.Chrome()
        
    def get_url(self):
        date = str(datetime.date.today()).split('-')
        url = 'https://www.cnn.com/world/live-news/coronavirus-pandemic-' + date[1] + '-' + date[2] + "-20-intl/index.html"
        return url

    # Mouse swipe down
    def execute_times(self, times):
        for i in range(times + 1):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
    
    def replace(self, text):
        return text.replace(u"\u2019", "'").replace(u"\u00a0", "'")

    def get_article(self, filename):
        # self.driver=webdriver.Chrome()
        url = self.get_url()
        self.driver.get(url)     # open the cnn website
        self.execute_times(10)       # swipe down 10 times

        html=self.driver.page_source
        bf=BeautifulSoup(html,'lxml')
        output_file = open(filename, 'w', encoding='utf-8')

        articles = bf.find_all('article', class_="sc-cJSrbW poststyles__PostBox-sc-1egoi1-0 tzojb")
        for article in articles:
            title = article.find('h2', class_="post-headlinestyles__Headline-sc-2ts3cz-1 gzgZOi")
            time = article.find('span')
            author = article.find('p', class_="post-headlinestyles__Byline-sc-2ts3cz-2 goqrhH")
            try:
                title = self.replace(title.text)
            except:
                title = "Unknown"
            try:
                time = self.replace(time.text)
            except:
                time = "Unknown"
            try:
                author = self.replace(author.text)
            except:
                author = "Unknown"
            main_text = article.find_all('p', class_="Text-sc-1amvtpj-0-p render-stellar-contentstyles__Paragraph-sc-9v7nwy-2 fAchMW")
            content = ""
            for mt in main_text:
                content += self.replace(mt.text)

            res = {
                'title':title,
                'time': time,
                'author':author,
                'link':url,
                'content':content,
	                    }
            
            json.dump(res, output_file)
            output_file.write("\n")

        output_file.close()


if __name__ == '__main__':
    cc = Crawler_CNN()
    cc.get_article("CNN_output_1.json")