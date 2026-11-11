import requests
from lxml import html


# 常量
WEBSITE_URL1 = "https://www.whitehouse.gov/news/"
HTML_TITLE = '//*[@id="wp--skip-link--target"]/div[2]/ul/li/div/div/h2/a'
HTML_CONTENT = '//*[@id="wp--skip-link--target"]/div/p/text()'

# 获取HTML元素对象
def get_element(url):
    response = requests.get(url)
    document = html.fromstring(response.text)
    return document



# 获取新闻标题与新闻具体内容网站
def get_website_one(url,xpath):
    document = get_element(url)
    nodes = document.xpath(xpath)
    for node in nodes:
        website = node.get('href')
        title = node.xpath('.//text()')[0]
        yield website, title


# 获取新闻内容
def get_news_content(next_url,next_xpath):
    document = get_element(next_url)
    contents = document.xpath(next_xpath)
    return contents


# //*[@id="wp--skip-link--target"]/div/p[1]/text()
# //*[@id="wp--skip-link--target"]/div/p[2]/text()

# 主程序
def main():
    for a, b in get_website_one(WEBSITE_URL1, HTML_TITLE):
        content = get_news_content(a, HTML_CONTENT)
        yield content

if __name__ == "__main__":
    for content in main():
        print(content)