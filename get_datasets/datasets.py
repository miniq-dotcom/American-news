import csv
import requests
from lxml import html
import re

# 常量
WEBSITE_URL1 = "https://www.whitehouse.gov/news/"


# 获取新闻标题与新闻具体内容网站
def get_website_one(url,xpath):
    response = requests.get(url)
    document = html.fromstring(response.text)
    next_url = document.xpath(xpath+"/@href")[0]
    news_title = document.xpath(xpath+'[@target="_self"]/text()')[0]
    return news_title, next_url

if __name__ == "__main__":
    for i in range(1, 11):
        xpath = f'//*[@id="wp--skip-link--target"]/div[2]/ul/li[{i}]/div/div/h2/a'
        newstitle, next_url = get_website_one(WEBSITE_URL1,xpath)
        print(newstitle, next_url)