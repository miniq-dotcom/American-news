from datetime import datetime

from dns import update

from llm_client import LLMClient
import json
import os

if os.path.exists("prompt/summary.txt"):
    with open("prompt/summary.txt", 'r', encoding="utf-8") as f:
        SYSTEM_SUMMARY = f.read()

if os.path.exists("prompt/analysis.txt"):
    with open("prompt/analysis.txt", 'r', encoding="utf-8") as f:
        SYSTEM_ANALYSIS = f.read()

# 先确定json文件
'''
[
    {
    time:x,
    title:u,
    content:z,
    ai概括:m,
    ai_analysis:n,
    },
    {},
    ...
]
'''
# 如果前面三个有空的，就返回查询错误

# 如果后面两个是空的，调用llm_client进行回答，补全之后提交

# for json in jsons
# if json[time] is not None and json[title] is not None and json[content] is not None:
# 获取正常数据
# if json[ai概括] is '' or json[ai_analysis] is '':
# 调用LLMClient

# 返回有值之后就是：json[ai概括]=,json[ai_analysis]=

# 先进行json.load,写入之后json.dump

# ai 设定可以是新闻分析员，一个概括，一个分析，得到两个答案

client = LLMClient()
def get_ai_answer(system_content, user_content):
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]
    answer = client.chat(messages, model="deepseek-chat")
    return answer

def save_news(news_list):
    with open("../data/news.json", 'w', encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)

def main():
    with open("../data/news.json", 'r', encoding="utf-8") as f:
        news_list = json.load(f)
    for news in news_list:
        if not news.get("summary"):
            news['summary'] = get_ai_answer(system_content=SYSTEM_SUMMARY, user_content=news['content'])
            save_news(news_list)
        if not news.get("analysis"):
            news['analysis'] = get_ai_answer(system_content=SYSTEM_ANALYSIS, user_content=news['content'])
            save_news(news_list)


if __name__ == '__main__':
    main()
