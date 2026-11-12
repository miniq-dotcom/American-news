from get_datasets import spider
from spider import main

# 数据问题
# 用了yield之后一次输出一条是没有问题的
# 但是有缺失，现在不想管，等以后看看有什么好方法
# 数据清理的话应该就只有\xa0需要替换成“”

dict = {}
for content,title in main():
    content = content.replace('\xa0', ' ')