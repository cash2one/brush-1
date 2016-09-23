#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import re
from zhihu import ZhihuClient

Cookies_File = 'cookies.json'
client = ZhihuClient(Cookies_File)

# url = 'http://www.zhihu.com/people/excited-vczh'
# author = client.author(url)
#
# print('用户名 %s' % author.name)
# print('用户简介 %s' % author.motto)
# print('用户关注人数 %d' % author.followee_num)
# print('取用户粉丝数 %d' % author.follower_num)
# print('用户得到赞同数 %d' % author.upvote_num)
# print('用户得到感谢数 %d' % author.thank_num)
# print('用户提问数 %d' % author.question_num)
# print('用户答题数 %d' % author.answer_num)
#
# print('用户专栏文章数 %d，名称分别为：' % author.post_num)
# for column in author.columns:
#   print(column.name)
# print('用户收藏夹数 %d，名称分别为：' % author.collection_num)
# for collection in author.collections:
#   print(collection.name)

# author = client.author('http://www.zhihu.com/people/excited-vczh')
# for act in author.activities:
#    if act.type == client.ActType.UPVOTE_ANSWER:
#        print('%s 在 %s 赞同了问题 %s 中 %s(motto: %s) 的回答, '
#              '此回答赞同数 %d' %
#              (author.name, act.time, act.answer.question.title,
#               act.answer.author.name, act.answer.author.motto,
#               act.answer.upvote_num))


url = 'http://www.zhihu.com/question/%s' % 31969621
question = client.question(url)

print(question.title)
# print(question.answer_num)
# print(question.follower_num)
# print(question.topics)

n = 0
with open("D:/brush/slave/scripts/doc/name2.txt", 'a', encoding='utf-8') as f:
    for answer in question.answers:
        n += 1
        if answer.author.name != "匿名用户" and answer.author.name != "[已重置]":
            print(answer.author.name)
            f.write(answer.author.name+'\n')
        time.sleep(0.01)
    print(n)
