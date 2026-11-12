from spider import main
import json
import os


# 数据问题
# 用了yield之后一次输出一条是没有问题的
# 但是有缺失，现在不想管，等以后看看有什么好方法
# 数据清理的话应该就只有\xa0需要替换成“”

if not os.path.isdir("data"):
    os.mkdir("data")


news_list = []
for content,title in main():
    dict = {}
    content = content.replace('\xa0', ' ')
    dict['title'] = title
    dict['content'] = content
    news_list.append(dict)

with open("data/news.json", 'w', encoding="utf-8") as f:
    json.dump(news_list, f, ensure_ascii=False, indent=4)


# 现在需要封装数据，把数据保存起来，可以调用
"""
1.日期，通过Rss推送
2.标题
3.原文

"""




