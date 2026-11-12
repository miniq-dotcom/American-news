import requests
from lxml import etree,html


NEWS_XML = 'https://www.whitehouse.gov/news/feed/'
HTML_CONTENT = '//*[@id="wp--skip-link--target"]/div/p'


# 使用RSS查询新闻标题，新闻发布时间，新闻具体网站
def get_data(url):
    response = requests.get(NEWS_XML)
    document = etree.fromstring(response.content)
    titles = document.xpath('//title/text()')
    del titles[0]
    pubDates = document.xpath('//pubDate/text()')
    urls = document.xpath('//guid/text()')
    return titles, pubDates, urls


# 获取新闻内容
def get_news_content(urls:list,next_xpath):  # url,HTML_CONTENT
    for url in urls:
        response = requests.get(url)
        document = html.fromstring(response.content)
        paragraphs = document.xpath(next_xpath)
        content = ''

        for paragraph in paragraphs:
            paragraph = "".join(paragraph.xpath('.//text()'))
            content += paragraph
        yield content


def main():
    titles, pubDates, urls = get_data(NEWS_XML)
    i = 0
    for content in get_news_content(urls, HTML_CONTENT):
        i += 1
        yield titles[i], pubDates[i], content
        if i == len(urls)-1:
            break


if __name__ == '__main__':
    for title, pubDate, content in main():
        print(f"Title: {title}, PubDate: {pubDate}, Content: {content}")

