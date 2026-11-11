import csv
import requests
from lxml import html
import re


# 常量
WEBSITE_URL1 = "https://www.whitehouse.gov/news/"
HTML_CONTENT = '//*[@id="wp--skip-link--target"]/div/p/text()'

# 获取HTML元素对象
def get_element(url):
    response = requests.get(url)
    document = html.fromstring(response.text)
    return document


# 获取新闻标题与新闻具体内容网站
def get_website_one(url,xpath):
    document = get_element(url)
    next_url = document.xpath(xpath+"/@href")[0]
    news_title = document.xpath(xpath+'[@target="_self"]/text()')[0]
    return news_title, next_url


# 获取新闻内容
def get_news_content(next_url,next_xpath):
    document = get_element(next_url)
    contents = document.xpath(next_xpath)
    return contents


# //*[@id="wp--skip-link--target"]/div/p[1]/text()
# //*[@id="wp--skip-link--target"]/div/p[2]/text()


if __name__ == "__main__":
    for i in range(1, 11):
        xpath = f'//*[@id="wp--skip-link--target"]/div[2]/ul/li[{i}]/div/div/h2/a'
        newstitle, next_url = get_website_one(WEBSITE_URL1,xpath)
        contents = get_news_content(next_url, HTML_CONTENT)
        print(contents)